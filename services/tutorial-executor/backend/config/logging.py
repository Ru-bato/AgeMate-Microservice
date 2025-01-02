# -*- coding: utf-8 -*-
"""
Logging Configuration

This module sets up the logging configuration for the application.
It defines a consistent logging format and level, and can be extended to include file handlers,
email alerts, or other logging features as needed.
"""

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logging(settings):
    """
    Sets up logging with a specified log level and log file.
    """
    # Ensure the log directory exists
    log_dir = Path(settings.LOG_FILE).parent
    if not log_dir.exists():
        log_dir.mkdir(parents=True)

    # Ensure LOG_LEVEL is a string and not an object
    log_level = settings.LOG_LEVEL.upper() if isinstance(settings.LOG_LEVEL, str) else logging.INFO

    # Define the logging format
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    print("level = ", log_level)
    # Configure the root logger
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout),  # Log to stdout
            RotatingFileHandler(settings.LOG_FILE, maxBytes=1024*1024*5, backupCount=3)  # Log to file with rotation
        ]
    )

    # Optionally, set up logging for specific libraries or modules
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('asyncio').setLevel(logging.WARNING)

    logging.info("Logging configured successfully.")


def setup_custom_logger(name, log_level=logging.INFO, log_file='app.log'):
    """
    Sets up a custom logger with handlers for both console and file outputs.
    """
    # Ensure the log directory exists
    log_dir = Path(log_file).parent
    if not log_dir.exists():
        log_dir.mkdir(parents=True)

    # Create a custom logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # Define the logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create handlers
    console_handler = logging.StreamHandler(sys.stdout)
    file_handler = RotatingFileHandler(log_file, maxBytes=1024*1024*5, backupCount=3)

    # Set level and formatter for handlers
    console_handler.setLevel(log_level)
    file_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to the logger
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


class LogLevelFilter(logging.Filter):
    """
    Custom filter to only allow log records with a specific log level.
    """
    def __init__(self, level):
        self.level = level

    def filter(self, record):
        return record.levelno == self.level


def add_log_level_filter(logger, level):
    """
    Adds a custom filter to a logger that only allows log records of a specific level.
    """
    log_level_filter = LogLevelFilter(level)
    for handler in logger.handlers:
        handler.addFilter(log_level_filter)


def setup_email_alerts(logger, email_to, mailhost="localhost", fromaddr="noreply@yourdomain.com"):
    """
    Configures a logger to send email alerts for critical errors.
    """
    from logging.handlers import SMTPHandler

    mail_handler = SMTPHandler(
        mailhost=mailhost,
        fromaddr=fromaddr,
        toaddrs=email_to,
        subject="Critical Error Alert",
        credentials=None,
        secure=None
    )
    mail_handler.setLevel(logging.CRITICAL)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    mail_handler.setFormatter(formatter)
    logger.addHandler(mail_handler)


if __name__ == '__main__':
    # Example usage of setting up a custom logger
    custom_logger = setup_custom_logger('my_module')
    custom_logger.info("This is an info message.")

    # Example of adding a log level filter
    add_log_level_filter(custom_logger, logging.WARNING)
    custom_logger.warning("This warning should appear.")
    custom_logger.info("This info message should NOT appear due to the filter.")

    # Example of setting up email alerts
    setup_email_alerts(custom_logger, ["admin@example.com"])
    custom_logger.critical("This critical error should trigger an email alert.")