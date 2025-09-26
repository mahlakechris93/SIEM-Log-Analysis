# SIEM Log Analyzer

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A modern, modular Python framework for SIEM (Security Information and Event Management) log analysis and security monitoring. Built for cybersecurity professionals, blue teams, and security researchers.

## 🚀 Features

- **Multi-format Log Ingestion**: Support for JSON, CSV, syslog, Windows Event Logs, and custom formats
- **Intelligent Parsing**: Extract structured data from unstructured logs with regex patterns
- **Real-time Analysis**: Detect security threats and anomalies as they happen  
- **Customizable Alerts**: Configure rules for different attack patterns and security events
- **Rich Reporting**: Generate comprehensive security reports in multiple formats
- **Modular Architecture**: Easy to extend and customize for specific use cases
- **CLI Interface**: Command-line tools for automation and integration

## 🏗️ Architecture

```
src/sieman/
├── ingest.py     # Log ingestion from multiple sources
├── parser.py     # Log parsing and data extraction
├── alerts.py     # Alert generation and rule engine
├── report.py     # Report generation and output
├── models.py     # Data models and schemas
├── cli.py        # Command-line interface
└── __init__.py   # Package initialization
```

## 📦 Installation

### From PyPI (Recommended)

```bash
pip install sieman
```

## 🚀 Quick Start

### Command Line Usage

```bash
# Analyze a single log file
sieman analyze /path/to/logfile.log

# Process multiple files with specific parser
sieman analyze /var/log/syslog --parser syslog --output report.json

# Real-time monitoring
sieman monitor /var/log/ --alerts-only

# Generate security report
sieman report --input /path/to/logs/ --format html --output security_report.html
```

### Python API Usage

```python
from sieman import create_ingestor, create_parser, AlertEngine

# Basic log analysis
ingestor = create_ingestor('generic')
parser = create_parser('syslog')
alert_engine = AlertEngine()

# Process logs
for log_entry in ingestor.ingest_file('/var/log/syslog'):
    parsed_entry = parser.parse(log_entry)
    alerts = alert_engine.evaluate(parsed_entry)
    
    if alerts:
        print(f"🚨 Alert: {alerts}")
```

### Configuration Example

```python
from sieman.models import Config

config = Config(
    ingest={
        'formats': ['json', 'syslog', 'csv'],
        'watch_directories': ['/var/log', '/opt/app/logs']
    },
    alerts={
        'rules_file': 'rules/security_rules.yml',
        'severity_threshold': 'medium'
    },
    output={
        'format': 'json',
        'destination': '/opt/siem/reports/'
    }
)
```

## 📖 Use Cases

- **Security Operations Centers (SOC)**: Centralized log analysis and threat detection
- **Incident Response**: Quick analysis of security events and attack patterns
- **Compliance Monitoring**: Automated compliance reporting for various standards
- **Threat Hunting**: Proactive search for indicators of compromise
- **Forensic Analysis**: Post-incident investigation and evidence collection
- **Security Research**: Analysis of attack patterns and malware behavior

## 🛡️ Security Features

### Built-in Detection Rules

- Failed authentication attempts
- Brute force attacks
- Privilege escalation
- Suspicious file access
- Network anomalies
- Malware indicators
- Data exfiltration patterns

### Alert Types

- **Real-time alerts**: Immediate notification of critical events
- **Batch alerts**: Summary of events over time periods
- **Threshold alerts**: Triggered when event counts exceed limits
- **Correlation alerts**: Multi-event pattern matching

## 📊 Supported Log Formats

| Format | Description | Example Use Case |
|--------|-------------|-----------------|
| Syslog | Standard Unix/Linux system logs | Server monitoring, network devices |
| JSON | Structured JSON logs | Modern applications, APIs |
| CSV | Comma-separated values | Database exports, spreadsheets |
| Windows Event Log | Windows system events | Windows server monitoring |
| Common Log Format | Web server access logs | Apache, Nginx analysis |
| Custom | User-defined patterns | Proprietary applications |

## 🔧 Configuration

Create a configuration file `config.yml`:

```yaml
ingest:
  sources:
    - type: file
      path: /var/log/syslog
      format: syslog
    - type: directory
      path: /opt/app/logs
      format: json
      recursive: true

alerts:
  rules:
    - name: "Failed SSH Login"
      pattern: "Failed password for .* from"
      severity: medium
      threshold: 5
      window: 300  # 5 minutes
    
    - name: "Root Login"
      pattern: "Accepted .* for root from"
      severity: high
      action: immediate

output:
  reports:
    - format: json
      file: /var/log/siem/alerts.json
    - format: html
      file: /var/www/siem/dashboard.html
      template: security_dashboard
```


### Development Setup

```bash
# Clone the repository
git clone https://github.com/mahlakechris93/SIEM-Log-Analysis.git
cd siem-log-analyzer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
black src/ tests/
mypy src/
```

## ⚖️ Legal Disclaimer

**IMPORTANT: This tool is intended for authorized security testing and monitoring only.**

- ✅ **Authorized Use**: Use this tool only on systems you own or have explicit permission to test
- ✅ **Educational Purpose**: Designed for learning cybersecurity concepts and techniques
- ✅ **Professional Use**: Suitable for security professionals, SOC analysts, and blue teams
- ❌ **Prohibited**: Do not use for unauthorized access, malicious activities, or illegal purposes

### Terms of Use

1. **Legal Compliance**: Users must comply with all applicable laws and regulations
2. **Authorization Required**: Only use on systems with proper authorization
3. **No Warranty**: This software is provided "as is" without warranty of any kind
4. **Responsibility**: Users are solely responsible for their use of this software
5. **Reporting**: Discovered vulnerabilities should be reported responsibly

By using this software, you agree to use it ethically and legally. The developers are not responsible for any misuse or damage caused by this tool.

## 🆘 Support

- 📧 **Email**: [security@example.com](mailto:security@example.com)
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/mahlakechris93/SIEM-Log-Analysis/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/mahlakechris93/SIEM-Log-Analysis/discussions)
- 📖 **Documentation**: [Wiki](https://github.com/mahlakechris93/SIEM-Log-Analysis/wiki)


**Made with ❤️ for the cybersecurity community**
