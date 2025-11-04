from mcp.server.fastmcp import FastMCP
from src.utils.logging_utils import get_logger
from mcp.server.auth.middleware.auth_context import get_access_token
from datetime import datetime

logger = get_logger(__name__)


def register_auth_tools(mcp: FastMCP):
    @mcp.tool()
    def get_token_details():
        """Get the details of the access token"""
        try:
            access_token = get_access_token()
            if not access_token:
                return {
                    "error": "No access token available",
                }

            token_string = access_token.token
            expires_at = access_token.expires_at

            expires_datetime = None
            if expires_at:
                expires_datetime = datetime.fromtimestamp(expires_at)

            return {
                "token_preview": (
                    f"{token_string[:20]}..."
                    if token_string and len(token_string) > 20
                    else token_string
                ),
                "client_id": access_token.client_id,
                "scopes": access_token.scopes,
                "expires_at": expires_at,
                "expires_at_datetime": (
                    expires_datetime.isoformat() if expires_datetime else None
                ),
                "is_valid": True,
            }
        except Exception as e:
            logger.error(f"Error getting token details: {str(e)}")
            return {
                "error": f"Error getting token details: {str(e)}",
            }
