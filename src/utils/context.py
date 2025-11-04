"""
Context utilities for API key authentication
"""

import os
from typing import Optional
from mcp.server.auth.middleware.auth_context import get_access_token
from mcp.server.auth.provider import AccessToken
from src.utils.logging_utils import get_logger
from dotenv import load_dotenv

load_dotenv()

logger = get_logger(__name__)


def get_auth_token() -> str:
    """
    Unified authorization token resolver that automatically detects the transport mode:
    - For HTTP transport: gets authorization token from access token
    """
    token = get_token_from_headers()
    if token:
        return token
    else:
        raise ValueError("Authorization token is required.")


def get_token_from_headers() -> str | None:
    access_token = get_access_token()
    if access_token and access_token.token:
        return access_token.token
    else:
        return None


def get_access_token_object() -> Optional[AccessToken]:
    """
    Get the full AccessToken object with all token information.

    Returns:
        AccessToken object containing token, client_id, scopes, expires_at
        Returns None if no access token is available
    """
    return get_access_token()


def get_token_info() -> dict:
    """
    Get comprehensive token information as a dictionary.

    Returns:
        Dictionary containing:
        - token: The JWT token string
        - client_id: The client ID from the token
        - scopes: List of scopes granted to the token
        - expires_at: Token expiration timestamp (if available)
        - is_valid: Whether token is present and valid

    Raises:
        ValueError: If no access token is available
    """
    access_token = get_access_token()
    if not access_token:
        raise ValueError("No access token available.")

    return {
        "token": access_token.token,
        "client_id": access_token.client_id,
        "scopes": access_token.scopes,
        "expires_at": access_token.expires_at,
        "is_valid": True,
    }
