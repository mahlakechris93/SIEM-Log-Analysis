"""Log ingestion module for SIEM log analyzer.

Handles reading and preprocessing of various log formats
including syslog, Windows Event Log, and custom formats.
"""

import logging
import os
from pathlib import Path
from typing import Iterator, Dict, Any, Optional, List
from datetime import datetime
import json
import csv

logger = logging.getLogger(__name__)


class LogIngestor:
    """Base class for log ingestion."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.supported_formats = ['json', 'csv', 'syslog', 'txt']
    
    def ingest_file(self, file_path: str) -> Iterator[Dict[str, Any]]:
        """Ingest logs from a file.
        
        Args:
            file_path: Path to the log file
            
        Yields:
            Dict containing log entry data
        """
        path = Path(file_path)
        if not path.exists():
            logger.error(f"File not found: {file_path}")
            return
        
        file_ext = path.suffix.lower()
        
        if file_ext == '.json':
            yield from self._ingest_json(path)
        elif file_ext == '.csv':
            yield from self._ingest_csv(path)
        else:
            yield from self._ingest_text(path)
    
    def ingest_directory(self, directory_path: str) -> Iterator[Dict[str, Any]]:
        """Ingest all log files from a directory.
        
        Args:
            directory_path: Path to directory containing log files
            
        Yields:
            Dict containing log entry data
        """
        path = Path(directory_path)
        if not path.is_dir():
            logger.error(f"Directory not found: {directory_path}")
            return
        
        for file_path in path.rglob("*.log"):
            logger.info(f"Processing file: {file_path}")
            yield from self.ingest_file(str(file_path))
    
    def _ingest_json(self, file_path: Path) -> Iterator[Dict[str, Any]]:
        """Ingest JSON formatted logs."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    if not line.strip():
                        continue
                    try:
                        entry = json.loads(line)
                        entry['_file_source'] = str(file_path)
                        entry['_line_number'] = line_num
                        yield entry
                    except json.JSONDecodeError as e:
                        logger.warning(f"Invalid JSON at {file_path}:{line_num}: {e}")
        except Exception as e:
            logger.error(f"Error reading {file_path}: {e}")
    
    def _ingest_csv(self, file_path: Path) -> Iterator[Dict[str, Any]]:
        """Ingest CSV formatted logs."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for line_num, row in enumerate(reader, 1):
                    row['_file_source'] = str(file_path)
                    row['_line_number'] = line_num
                    yield row
        except Exception as e:
            logger.error(f"Error reading {file_path}: {e}")
    
    def _ingest_text(self, file_path: Path) -> Iterator[Dict[str, Any]]:
        """Ingest plain text logs."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    if not line.strip():
                        continue
                    yield {
                        'message': line.strip(),
                        'timestamp': datetime.now().isoformat(),
                        '_file_source': str(file_path),
                        '_line_number': line_num
                    }
        except Exception as e:
            logger.error(f"Error reading {file_path}: {e}")


class SyslogIngestor(LogIngestor):
    """Specialized ingestor for syslog format."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.facility_names = {
            0: 'kernel', 1: 'user', 2: 'mail', 3: 'daemon',
            4: 'auth', 5: 'syslog', 6: 'lpr', 7: 'news'
        }
        self.severity_names = {
            0: 'emergency', 1: 'alert', 2: 'critical', 3: 'error',
            4: 'warning', 5: 'notice', 6: 'info', 7: 'debug'
        }


class WindowsEventLogIngestor(LogIngestor):
    """Specialized ingestor for Windows Event Logs."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        # Placeholder for Windows-specific logic
        pass


def create_ingestor(log_type: str = 'generic', **kwargs) -> LogIngestor:
    """Factory function to create appropriate ingestor.
    
    Args:
        log_type: Type of log ingestor to create
        **kwargs: Additional configuration
        
    Returns:
        LogIngestor instance
    """
    ingestors = {
        'generic': LogIngestor,
        'syslog': SyslogIngestor,
        'windows': WindowsEventLogIngestor
    }
    
    ingestor_class = ingestors.get(log_type, LogIngestor)
    return ingestor_class(kwargs)
