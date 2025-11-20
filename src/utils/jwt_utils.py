"""
JWT Utilities for Clappia MCP Server

Handles JWT token verification and related authentication logic.
"""

import logging

from jose import JWTError, jwt
from mcp.server.auth.provider import AccessToken, TokenVerifier

from .constants import JWT_ALGORITHM, JWT_AUDIENCE, JWT_ISSUER, JWT_SECRET_KEY

logger = logging.getLogger(__name__)


class JWTTokenVerifier(TokenVerifier):
    """Verifies JWT tokens for MCP OAuth flow"""

    async def verify_token(self, token: str) -> AccessToken | None:
        """
        Verify a JWT token and return an AccessToken if valid.

        Args:
            token: The JWT token string to verify

        Returns:
            AccessToken if token is valid, None otherwise
        """
        try:
            payload = jwt.decode(
                token,
                JWT_SECRET_KEY,
                algorithms=[JWT_ALGORITHM],
                issuer=JWT_ISSUER,
                audience=JWT_AUDIENCE,
                options={
                    "verify_signature": True,
                    "verify_exp": True,
                    "verify_iss": True,
                    "verify_aud": True,
                },
            )

            scopes = payload.get("scope", "").split() if payload.get("scope") else []

            return AccessToken(
                token=token,
                client_id=payload.get("client_id", "unknown"),
                scopes=scopes,
                expires_at=payload.get("exp"),
            )
        except JWTError as e:
            logger.warning(f"JWT verification failed: {type(e).__name__}: {e}")
            logger.debug(
                f"Expected issuer: {JWT_ISSUER}, audience: {JWT_AUDIENCE}, algorithm: {JWT_ALGORITHM}"
            )
            return None


def get_jwt_config() -> dict:
    """
    Get JWT configuration constants.

    Returns:
        Dictionary containing JWT configuration
    """
    return {
        "issuer": JWT_ISSUER,
        "audience": JWT_AUDIENCE,
        "secret_key": JWT_SECRET_KEY,
        "algorithm": JWT_ALGORITHM,
    }
