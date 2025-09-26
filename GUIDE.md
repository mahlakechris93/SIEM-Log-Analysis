# SIEM Log Analyzer - Setup and Usage Guide

A step-by-step guide to get you started with the SIEM Log Analyzer project.

## Prerequisites

- Python 3.8 or higher
- Git (for cloning the repository)
- Basic understanding of command line operations

## Step 1: Setting up Virtual Environment and Installation

### 1.1 Clone the Repository

```bash
git clone https://github.com/Akhilkrishna1/siem-log-analyzer.git
cd siem-log-analyzer
```

### 1.2 Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 1.3 Install the Package

```bash
# Install in editable mode for development
pip install -e .
```

**Expected Output:** The package and its dependencies will be installed. You should see installation messages confirming successful setup.

## Step 2: Creating a Sample Log File

### 2.1 Create Test Directory

```bash
mkdir test_logs
cd test_logs
```

### 2.2 Create Sample Log File

Create a file named `sample.log` with the following content:

```bash
cat > sample.log << 'EOF'
2025-08-19 10:15:30 INFO [auth.py:45] User john_doe logged in successfully from 192.168.1.100
2025-08-19 10:16:45 WARNING [security.py:23] Failed login attempt for user admin from 10.0.0.5
2025-08-19 10:17:12 ERROR [database.py:78] Connection timeout to database server
2025-08-19 10:18:30 INFO [file_monitor.py:12] File access: /etc/passwd by user root
2025-08-19 10:19:45 WARNING [network.py:56] Suspicious network activity detected from 172.16.0.50
2025-08-19 10:20:15 INFO [auth.py:45] User jane_smith logged in successfully from 192.168.1.101
2025-08-19 10:21:30 CRITICAL [security.py:89] Multiple failed login attempts from 10.0.0.5 - possible brute force attack
EOF
```

## Step 3: Creating and Running demo_ingest_parse.py

### 3.1 Create Demo Script

Create a file named `demo_ingest_parse.py` in the project root:

```python
#!/usr/bin/env python3
"""
Demo script for SIEM Log Analyzer - Ingestion and Parsing

This script demonstrates:
1. Creating an ingestor
2. Creating a parser
3. Processing log entries
4. Basic alert generation
"""

import sys
import os
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from sieman import create_ingestor, create_parser
    from sieman.alerts import AlertEngine
    print("✓ Successfully imported sieman modules")
except ImportError as e:
    print(f"✗ Import error: {e}")
    print("Make sure you've installed the package with 'pip install -e .'")
    sys.exit(1)

def main():
    """
    Main demo function
    """
    print("=== SIEM Log Analyzer Demo ===")
    print()
    
    # Check if log file exists
    log_file = Path("test_logs/sample.log")
    if not log_file.exists():
        print(f"✗ Log file not found: {log_file}")
        print("Please create the sample log file as described in Step 2")
        return
    
    print(f"✓ Found log file: {log_file}")
    
    try:
        # Step 1: Create ingestor
        print("\n1. Creating ingestor...")
        ingestor = create_ingestor('generic')
        print("✓ Ingestor created successfully")
        
        # Step 2: Create parser
        print("\n2. Creating parser...")
        parser = create_parser('generic')
        print("✓ Parser created successfully")
        
        # Step 3: Create alert engine
        print("\n3. Creating alert engine...")
        alert_engine = AlertEngine()
        print("✓ Alert engine created successfully")
        
        # Step 4: Process log file
        print(f"\n4. Processing log file: {log_file}")
        log_count = 0
        alert_count = 0
        
        for log_entry in ingestor.ingest_file(str(log_file)):
            log_count += 1
            print(f"  Raw log [{log_count}]: {log_entry.strip()}")
            
            # Parse the log entry
            parsed_entry = parser.parse(log_entry)
            print(f"  Parsed: {parsed_entry}")
            
            # Check for alerts
            alerts = alert_engine.evaluate(parsed_entry)
            if alerts:
                alert_count += 1
                print(f"  🚨 ALERT: {alerts}")
            
            print()  # Empty line for readability
        
        print(f"\n=== Summary ===")
        print(f"Total log entries processed: {log_count}")
        print(f"Total alerts generated: {alert_count}")
        print("\n✓ Demo completed successfully!")
        
    except Exception as e:
        print(f"✗ Error during processing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
```

### 3.2 Run the Demo Script

```bash
# Make sure you're in the project root and virtual environment is activated
python demo_ingest_parse.py
```

**Expected Output:** The script should successfully import modules, process the log file, and display parsed entries with any generated alerts.

## Step 4: Troubleshooting Common Issues

### 4.1 Import Errors

**Problem:** `ImportError: No module named 'sieman'`

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Reinstall the package
pip install -e .
```

### 4.2 Module Not Found Errors

**Problem:** `ModuleNotFoundError: No module named 'sieman.alerts'`

**Solution:**
```bash
# Check that all module files exist
ls src/sieman/

# Ensure __init__.py files are present
find src/sieman/ -name "__init__.py"

# If missing, create empty __init__.py files
touch src/sieman/__init__.py
touch src/sieman/alerts/__init__.py  # if alerts is a subdirectory
```

### 4.3 File Path Issues

**Problem:** `FileNotFoundError: [Errno 2] No such file or directory: 'test_logs/sample.log'`

**Solution:**
```bash
# Ensure you're in the correct directory
pwd

# Create the test directory and file if missing
mkdir -p test_logs
cd test_logs
# Create sample.log as shown in Step 2.2
```

### 4.4 Permission Errors

**Problem:** Permission denied when running scripts

**Solution:**
```bash
# Make script executable
chmod +x demo_ingest_parse.py

# Or run with python directly
python demo_ingest_parse.py
```

### 4.5 Virtual Environment Issues

**Problem:** Commands not found or wrong Python version

**Solution:**
```bash
# Verify virtual environment is activated (prompt should show (venv))
# If not activated:
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Verify Python version
python --version

# Verify pip is using virtual environment
which pip  # Should point to venv/bin/pip
```

## Step 5: Next Steps for Project Extension

### 5.1 Advanced Log Parsing

- **Custom Parsers:** Extend the parser module to handle specific log formats (Apache, Nginx, Windows Event Logs)
- **Regex Patterns:** Add custom regex patterns for extracting specific data fields
- **Structured Logging:** Implement JSON and XML log parsing

### 5.2 Enhanced Alert Rules

- **Rule Configuration:** Create YAML configuration files for custom alert rules
- **Threshold-based Alerts:** Implement rate-limiting and threshold-based alerting
- **Correlation Rules:** Add multi-event correlation for advanced threat detection

### 5.3 Real-time Processing

- **File Monitoring:** Implement real-time log file monitoring using `watchdog`
- **Stream Processing:** Add support for log streams from syslog or other sources
- **Performance Optimization:** Implement async processing for high-volume logs

### 5.4 Reporting and Visualization

- **Dashboard Creation:** Build web-based dashboards using Flask/Django
- **Report Generation:** Implement HTML, PDF, and JSON report outputs
- **Metrics and Statistics:** Add log analysis metrics and trend analysis

### 5.5 Integration Capabilities

- **API Development:** Create REST APIs for external integrations
- **Database Integration:** Add support for storing parsed logs in databases
- **SIEM Integration:** Develop connectors for popular SIEM platforms

### 5.6 Security Enhancements

- **Threat Intelligence:** Integrate with threat intelligence feeds
- **Machine Learning:** Add anomaly detection using ML algorithms
- **Incident Response:** Implement automated response capabilities

## Additional Resources

### Useful Commands

```bash
# Run tests (if test suite is available)
pytest

# Code formatting
black src/ tests/

# Type checking
mypy src/

# Generate documentation
sphinx-build -b html docs/ docs/_build/
```

### Configuration Examples

Create a `config.yml` file for advanced configuration:

```yaml
ingest:
  sources:
    - type: file
      path: /var/log/syslog
      format: syslog
    - type: directory
      path: /var/log/app/
      format: json
      recursive: true

alerts:
  rules:
    - name: "Failed Login"
      pattern: "Failed.*login"
      severity: medium
      threshold: 5
      window: 300  # 5 minutes

output:
  format: json
  destination: /var/log/siem/alerts.json
```

## Getting Help

- **GitHub Issues:** Report bugs and request features at the project repository
- **Documentation:** Check the project README and wiki for detailed information
- **Community:** Join discussions in the GitHub Discussions section

---

**Note:** This guide assumes you're working with the basic structure of the SIEM Log Analyzer project. Adjust paths and commands based on your specific setup and requirements.
