"""
Logger utility for the Age of Empires 2 Team Balancing Bot.
Provides structured logging with different formats based on configuration.
"""

import logging
import sys
from typing import Optional

import structlog

import config

def setup_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Set up and configure a logger instance.
    
    Args:
        name: The name of the logger. If None, the root logger is returned.
        
    Returns:
        A configured logger instance.
    """
    # Set up basic configuration
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Choose the appropriate formatter based on configuration
    if config.LOG_FORMAT.lower() == "json":
        formatter = structlog.processors.JSONRenderer()
    else:
        formatter = structlog.dev.ConsoleRenderer()
    
    # Create and configure the logger
    logger = logging.getLogger(name)
    
    # Return the configured logger
    return logger

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the given name.
    
    Args:
        name: The name of the logger.
        
    Returns:
        A configured logger instance.
    """
    return setup_logger(name) 