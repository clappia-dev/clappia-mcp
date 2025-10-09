"""
Context utilities for API key authentication
"""
import os
from fastmcp.server.dependencies import get_http_headers
from src.utils.logging_utils import get_logger
from pydantic import BaseModel

logger = get_logger(__name__)

def get_api_key_from_headers() -> str:
    """
    Extracts and validates the API key from HTTP headers.
    
    Returns:
        str: The API key from the x-api-key header
        
    Raises:
        ValueError: If the API key is not found in headers
    """
    headers = get_http_headers()
    api_key = headers.get("x-api-key")
    
    if not api_key:
        logger.error("API key not found in headers")
        raise ValueError("API key is required. Please provide 'x-api-key' header.")
    
    logger.debug(f"API key found: {api_key[:10]}...")
    return api_key


def get_api_key_from_env() -> str:
    """
    Extracts and validates the API key from environment variables.
    
    Returns:
        str: The API key from the CLAPPIA_API_KEY environment variable
        
    Raises:
        ValueError: If the API key is not found in environment variables
    """
    api_key = os.getenv("CLAPPIA_API_KEY")
    
    if not api_key:
        logger.error("API key not found in environment variables")
        raise ValueError("API key is required. Please set CLAPPIA_API_KEY environment variable.")
    
    logger.debug(f"API key found in environment: {api_key[:10]}...")
    return api_key


def get_api_key() -> str:
    """
    Unified API key resolver that automatically detects the transport mode:
    - For stdio transport: gets API key from environment variable CLAPPIA_API_KEY
    - For HTTP transport: gets API key from x-api-key header
    
    Returns:
        str: The API key from the appropriate source
        
    Raises:
        ValueError: If the API key is not found in the appropriate source
    """
    try:
        return get_api_key_from_headers()
    except (ValueError, Exception) as e:
        logger.debug(f"Could not get API key from headers: {e}")
        try:
            return get_api_key_from_env()
        except ValueError as env_error:
            logger.error("Could not get API key from either headers or environment")
            raise ValueError(
                "API key is required. For HTTP transport, provide 'x-api-key' header. "
                "For stdio transport, set CLAPPIA_API_KEY environment variable."
            ) from env_error


def get_api_key_from_context() -> str:
    """
    Legacy function for backward compatibility.
    Now uses the unified API key resolver.
    
    Returns:
        str: The API key from the appropriate source (headers or env)
        
    Raises:
        ValueError: If the API key is not found in the appropriate source
    """
    return get_api_key()
