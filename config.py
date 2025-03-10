"""
Configuration module for the Age of Empires 2 Team Balancing Bot.

Loads configuration from environment variables with sensible defaults.
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Bot configuration
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "")
"""str: Discord bot token.  Set to empty string if not provided."""

COMMAND_PREFIX = os.getenv("COMMAND_PREFIX", "!")
"""str: Prefix for bot commands. Defaults to '!'."""

BOT_STATUS = os.getenv("BOT_STATUS", "Balancing AoE2 Teams")
"""str: Status message for the bot. Defaults to 'Balancing AoE2 Teams'."""

# API configuration
AOE2_GG_API_BASE_URL = os.getenv("AOE2_GG_API_BASE_URL", "https://aoe2.gg/api")
"""str: Base URL for the AoE2.GG API. Defaults to 'https://aoe2.gg/api'."""

AOE_NEXUS_API_BASE_URL = os.getenv("AOE_NEXUS_API_BASE_URL", "https://aoenexus.com/api")
"""str: Base URL for the AoE Nexus API. Defaults to 'https://aoenexus.com/api'."""

AOCREC_API_BASE_URL = os.getenv("AOCREC_API_BASE_URL", "https://aocrec.com/api")
"""str: Base URL for the AoCRec API. Defaults to 'https://aocrec.com/api'."""

API_TIMEOUT = int(os.getenv("API_TIMEOUT", "10"))
"""int: Timeout for API requests in seconds. Defaults to 10."""

API_CACHE_TTL = int(os.getenv("API_CACHE_TTL", "3600"))
"""int: Cache time-to-live for API responses in seconds. Defaults to 3600 (1 hour)."""

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///aoe2_team_balancer.db")
"""str: Database connection URL. Defaults to 'sqlite:///aoe2_team_balancer.db'."""

# Team balancing configuration
ELO_1V1_WEIGHT = float(os.getenv("ELO_1V1_WEIGHT", "0.4"))
"""float: Weight of 1v1 ELO in team balancing. Defaults to 0.4."""

ELO_TEAM_WEIGHT = float(os.getenv("ELO_TEAM_WEIGHT", "0.6"))
"""float: Weight of team ELO in team balancing. Defaults to 0.6."""

POSITION_FACTOR_MIN = float(os.getenv("POSITION_FACTOR_MIN", "0.9"))
"""float: Minimum position factor. Defaults to 0.9."""

POSITION_FACTOR_MAX = float(os.getenv("POSITION_FACTOR_MAX", "1.1"))
"""float: Maximum position factor. Defaults to 1.1."""

ACCEPTABLE_TEAM_DIFF_PERCENT = float(os.getenv("ACCEPTABLE_TEAM_DIFF_PERCENT", "3.0"))
"""float: Acceptable team difference percentage. Defaults to 3.0."""

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
"""str: Logging level. Defaults to 'INFO'."""

LOG_FORMAT = os.getenv("LOG_FORMAT", "console")
"""str: Log format. Can be 'console' or 'json'. Defaults to 'console'."""

# Development mode flag
DEV_MODE = os.getenv("DEV_MODE", "False").lower() in ("true", "1", "t")
"""bool: Whether development mode is enabled. Defaults to False."""

# Feature flags
ENABLE_ML_BALANCER = os.getenv("ENABLE_ML_BALANCER", "False").lower() in ("true", "1", "t")
"""bool: Whether the ML balancer is enabled. Defaults to False."""

def get_all_config() -> Dict[str, Any]:
    """Return all configuration variables as a dictionary.

    Returns:
        Dict[str, Any]: All configuration variables.
    """
    return {
        "DISCORD_TOKEN": bool(DISCORD_TOKEN),  # Just show if it's set, not the actual token
        "COMMAND_PREFIX": COMMAND_PREFIX,
        "BOT_STATUS": BOT_STATUS,
        "AOE2_GG_API_BASE_URL": AOE2_GG_API_BASE_URL,
        "AOE_NEXUS_API_BASE_URL": AOE_NEXUS_API_BASE_URL,
        "AOCREC_API_BASE_URL": AOCREC_API_BASE_URL,
        "API_TIMEOUT": API_TIMEOUT,
        "API_CACHE_TTL": API_CACHE_TTL,
        "DATABASE_URL": DATABASE_URL,
        "ELO_1V1_WEIGHT": ELO_1V1_WEIGHT,
        "ELO_TEAM_WEIGHT": ELO_TEAM_WEIGHT,
        "POSITION_FACTOR_MIN": POSITION_FACTOR_MIN,
        "POSITION_FACTOR_MAX": POSITION_FACTOR_MAX,
        "ACCEPTABLE_TEAM_DIFF_PERCENT": ACCEPTABLE_TEAM_DIFF_PERCENT,
        "LOG_LEVEL": LOG_LEVEL,
        "LOG_FORMAT": LOG_FORMAT,
        "DEV_MODE": DEV_MODE,
        "ENABLE_ML_BALANCER": ENABLE_ML_BALANCER,
    }