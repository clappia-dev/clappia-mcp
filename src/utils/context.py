"""
Context utilities for API key authentication
"""
import os
from fastmcp.server.dependencies import get_http_headers
from src.utils.logging_utils import get_logger
from dotenv import load_dotenv

load_dotenv()

logger = get_logger(__name__)


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
    headers = get_http_headers()
    os_api_key = os.getenv("CLAPPIA_API_KEY")
    if os_api_key:
        return os_api_key
    elif headers.get("x-api-key"):
        return headers.get("x-api-key")
    else:
        raise ValueError("API key is required. Please set CLAPPIA_API_KEY environment variable.")
