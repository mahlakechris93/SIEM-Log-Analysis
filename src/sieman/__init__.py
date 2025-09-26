"""SIEM Log Analyzer Framework

A modular Python framework for ingesting, parsing, and analyzing
security logs for SIEM and Blue Team operations.
"""

__version__ = "0.1.0"
__author__ = "user"
__email__ = "user@example.com"

from . import ingest, parser, alerts, report, models, cli

__all__ = [
    "ingest",
    "parser", 
    "alerts",
    "report",
    "models",
    "cli",
    "__version__",
    "__author__",
    "__email__",
]
