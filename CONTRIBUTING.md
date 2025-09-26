# Contributing to SIEM Log Analyzer

We welcome contributions to the SIEM Log Analyzer project! This document provides guidelines for contributing to make the process smooth and collaborative.

## How to Contribute

### Reporting Issues
- Use GitHub Issues to report bugs or request features
- Provide detailed information including steps to reproduce
- Include relevant log samples (anonymized) when applicable

### Pull Requests
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`pytest`)
6. Run linting (`black src/ tests/ && mypy src/`)
7. Commit your changes (`git commit -m 'Add amazing feature'`)
8. Push to the branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

## Development Setup

```bash
# Clone the repository
git clone https://github.com/Akhilkrishna1/siem-log-analyzer.git
cd siem-log-analyzer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

## Code Standards

- Follow PEP 8 style guidelines
- Use type hints for all functions
- Write docstrings for public functions and classes
- Keep functions focused and testable
- Maintain test coverage above 80%

## Testing

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=sieman

# Run specific test file
pytest tests/test_parser.py
```

## Security Considerations

- Never commit sensitive information (credentials, real log data)
- Sanitize any example log data
- Follow responsible disclosure for security vulnerabilities
- Test security features thoroughly

## Questions?

If you have questions, feel free to:
- Open an issue for discussion
- Start a GitHub Discussion
- Contact the maintainers

Thank you for contributing to making SIEM log analysis better for everyone!
