# Configuration Documentation

This directory contains documentation for configuring the SIEM Log Analyzer.

## Configuration Files

The SIEM Log Analyzer supports multiple configuration formats and methods:

### config.yml (Main Configuration)
The primary configuration file that defines:
- Log ingestion sources and formats
- Alert rules and thresholds
- Output destinations and formats
- Analysis parameters

### Environment Variables
The following environment variables can be used:
- `SIEMAN_CONFIG_PATH`: Path to configuration files
- `SIEMAN_LOG_PATH`: Path to log files to analyze
- `SIEMAN_OUTPUT_PATH`: Path for output files and reports
- `SIEMAN_LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

### Configuration Examples

Basic configuration structure:

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
  rules_file: rules/security_rules.yml
  severity_threshold: medium
  notification:
    email: admin@company.com
    webhook: https://hooks.slack.com/...

output:
  format: json
  destination: /opt/siem/reports/
  retention_days: 30

parsing:
  timeout: 30
  memory_limit: 1GB
  parallel_workers: 4
```

## Configuration Topics

- **Log Sources**: How to configure different log inputs
- **Parsers**: Setting up custom parsing rules
- **Alert Rules**: Defining security detection rules
- **Output Formats**: Configuring reports and exports
- **Performance Tuning**: Optimizing for large-scale deployments
- **Security Settings**: Securing the SIEM deployment

## Getting Started

1. Copy the example configuration from `config/examples/`
2. Modify paths and sources to match your environment
3. Test configuration with `sieman validate-config`
4. Deploy and monitor

## Configuration Validation

Use the built-in validator to check your configuration:

```bash
# Validate main configuration
sieman validate-config config.yml

# Validate with verbose output
sieman validate-config config.yml --verbose

# Check specific sections
sieman validate-config config.yml --section alerts
```

## Security Considerations

- Store sensitive configuration in environment variables
- Use proper file permissions (600) for config files
- Regularly rotate API keys and credentials
- Enable audit logging for configuration changes

## Further Reading

- [Installation Guide](../installation.md)
- [User Guide](../user-guide.md)
- [API Documentation](../api.md)
- [Troubleshooting](../troubleshooting.md)
