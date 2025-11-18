"""
Clappia MCP Utils Package

This package contains utility modules for the Clappia MCP server.
"""

from .logging_utils import get_logger
from .jwt_utils import JWTTokenVerifier, get_jwt_config
from .enums import Environment
from .constants import (
    CLAPPIA_APP_DEFINITION_API_BASE_URL,
    CLAPPIA_ANALYTICS_API_BASE_URL,
    CLAPPIA_WORKPLACE_API_BASE_URL,
    CLAPPIA_WORKFLOW_DEFINITION_API_BASE_URL,
    CLAPPIA_SUBMISSIONS_API_BASE_URL,
    CLAPPIA_FILE_MANAGEMENT_API_BASE_URL,   
    JWT_ISSUER,
    JWT_AUDIENCE,
    JWT_SECRET_KEY,
    JWT_ALGORITHM,
)

__all__ = [
    "get_logger",
    "JWTTokenVerifier",
    "get_jwt_config",
    "Environment",
    "CLAPPIA_APP_DEFINITION_API_BASE_URL",
    "CLAPPIA_ANALYTICS_API_BASE_URL",
    "CLAPPIA_WORKPLACE_API_BASE_URL",
    "CLAPPIA_WORKFLOW_DEFINITION_API_BASE_URL",
    "CLAPPIA_SUBMISSIONS_API_BASE_URL",
    "CLAPPIA_FILE_MANAGEMENT_API_BASE_URL",
    "JWT_ISSUER",
    "JWT_AUDIENCE",
    "JWT_SECRET_KEY",
    "JWT_ALGORITHM",
]
__version__ = "1.0.0"
