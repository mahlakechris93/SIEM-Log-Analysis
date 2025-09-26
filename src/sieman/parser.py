"""Log parsing module for SIEM log analyzer.

Provides parsing capabilities for various log formats and
extracts structured data from unstructured logs.
"""

import re
import logging
from typing import Dict, Any, Optional, List, Pattern
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class LogParser:
    """Base class for log parsing functionality."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.patterns = self._load_patterns()
    
    def parse(self, log_entry: Dict[str, Any]) -> Dict[str, Any]:
        """Parse a log entry and extract structured data.
        
        Args:
            log_entry: Raw log entry dictionary
            
        Returns:
            Parsed and structured log entry
        """
        parsed_entry = log_entry.copy()
        
        # Extract timestamp if not already present
        if 'timestamp' not in parsed_entry:
            parsed_entry['timestamp'] = self._extract_timestamp(log_entry.get('message', ''))
        
        # Extract IP addresses
        parsed_entry['ip_addresses'] = self._extract_ip_addresses(log_entry.get('message', ''))
        
        # Extract user information
        parsed_entry['users'] = self._extract_users(log_entry.get('message', ''))
        
        # Classify log level
        parsed_entry['log_level'] = self._classify_log_level(log_entry.get('message', ''))
        
        return parsed_entry
    
    def _load_patterns(self) -> Dict[str, Pattern]:
        """Load regex patterns for parsing."""
        return {
            'ip_v4': re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'),
            'ip_v6': re.compile(r'\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b'),
            'timestamp_iso': re.compile(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}'),
            'timestamp_common': re.compile(r'\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}'),
            'user_pattern': re.compile(r'user[:\s]+([a-zA-Z0-9_\-\.@]+)', re.IGNORECASE),
            'error_patterns': re.compile(r'\b(error|fail|exception|critical)\b', re.IGNORECASE),
            'warning_patterns': re.compile(r'\b(warn|warning|alert)\b', re.IGNORECASE)
        }
    
    def _extract_timestamp(self, message: str) -> Optional[str]:
        """Extract timestamp from log message."""
        # Try ISO format first
        match = self.patterns['timestamp_iso'].search(message)
        if match:
            return match.group(0)
        
        # Try common syslog format
        match = self.patterns['timestamp_common'].search(message)
        if match:
            # Convert to ISO format (simplified)
            return datetime.now().isoformat()
        
        return None
    
    def _extract_ip_addresses(self, message: str) -> List[str]:
        """Extract IP addresses from log message."""
        ips = []
        
        # IPv4 addresses
        ips.extend(self.patterns['ip_v4'].findall(message))
        
        # IPv6 addresses
        ips.extend(self.patterns['ip_v6'].findall(message))
        
        return list(set(ips))  # Remove duplicates
    
    def _extract_users(self, message: str) -> List[str]:
        """Extract user information from log message."""
        matches = self.patterns['user_pattern'].findall(message)
        return list(set(matches))  # Remove duplicates
    
    def _classify_log_level(self, message: str) -> str:
        """Classify the log level based on message content."""
        message_lower = message.lower()
        
        if self.patterns['error_patterns'].search(message):
            return 'ERROR'
        elif self.patterns['warning_patterns'].search(message):
            return 'WARNING'
        elif any(word in message_lower for word in ['info', 'information']):
            return 'INFO'
        elif 'debug' in message_lower:
            return 'DEBUG'
        else:
            return 'INFO'  # Default


class SyslogParser(LogParser):
    """Specialized parser for syslog format."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.syslog_pattern = re.compile(
            r'<(\d+)>([A-Za-z]{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+(\S+)\s+([^\s:]+)(?::|\s)(.*)'
        )
    
    def parse(self, log_entry: Dict[str, Any]) -> Dict[str, Any]:
        """Parse syslog format specifically."""
        parsed_entry = super().parse(log_entry)
        
        message = log_entry.get('message', '')
        match = self.syslog_pattern.match(message)
        
        if match:
            priority, timestamp, hostname, program, msg = match.groups()
            
            # Calculate facility and severity
            priority_int = int(priority)
            facility = priority_int // 8
            severity = priority_int % 8
            
            parsed_entry.update({
                'syslog_facility': facility,
                'syslog_severity': severity,
                'hostname': hostname,
                'program': program,
                'parsed_message': msg.strip()
            })
        
        return parsed_entry


class WebLogParser(LogParser):
    """Parser for web server logs (Common/Combined Log Format)."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        # Common Log Format pattern
        self.common_log_pattern = re.compile(
            r'(\S+) \S+ \S+ \[([^\]]+)\] "(\S+) (\S+) (\S+)" (\d+) (\S+)'
        )
    
    def parse(self, log_entry: Dict[str, Any]) -> Dict[str, Any]:
        """Parse web server log format."""
        parsed_entry = super().parse(log_entry)
        
        message = log_entry.get('message', '')
        match = self.common_log_pattern.match(message)
        
        if match:
            ip, timestamp, method, url, protocol, status, size = match.groups()
            
            parsed_entry.update({
                'client_ip': ip,
                'http_method': method,
                'url': url,
                'http_protocol': protocol,
                'status_code': int(status),
                'response_size': size if size != '-' else 0
            })
        
        return parsed_entry


def create_parser(parser_type: str = 'generic', **kwargs) -> LogParser:
    """Factory function to create appropriate parser.
    
    Args:
        parser_type: Type of parser to create
        **kwargs: Additional configuration
        
    Returns:
        LogParser instance
    """
    parsers = {
        'generic': LogParser,
        'syslog': SyslogParser,
        'web': WebLogParser
    }
    
    parser_class = parsers.get(parser_type, LogParser)
    return parser_class(kwargs)
