"""
Clappia MCP Utils Package

This package contains utility modules for the Clappia MCP server.
"""

from .logging_utils import get_logger
from .constants import (
    CLAPPIA_EXTERNAL_PREPROD_API_BASE_URL,
    CLAPPIA_EXTERNAL_API_BASE_URL,
    CLAPPIA_EXTERNAL_API_BASE_URL_V4,
    CLAPPIA_APP_DEFINITION_API_BASE_URL,
    CLAPPIA_API_KEY_ENV_VAR,
)

__all__ = [
    "get_logger",
    "CLAPPIA_EXTERNAL_PREPROD_API_BASE_URL",
    "CLAPPIA_EXTERNAL_API_BASE_URL", 
    "CLAPPIA_EXTERNAL_API_BASE_URL_V4",
    "CLAPPIA_APP_DEFINITION_API_BASE_URL",
    "CLAPPIA_API_KEY_ENV_VAR",
]
__version__ = "1.0.0"