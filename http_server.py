import sys
import uvicorn
from pydantic import AnyHttpUrl
from mcp.server.fastmcp import FastMCP
from mcp.server.auth.provider import AccessToken, TokenVerifier
from mcp.server.auth.settings import AuthSettings
from jose import jwt, JWTError
from src.utils.logging_utils import get_logger
from src.tools.submissions import register_submission_tools
from src.tools.definitions import register_definition_tools
from src.tools.workflows import register_workflow_tools
from src.tools.analytics import register_analytics_tools
from src.tools.workplace import register_workplace_tools

logger = get_logger(__name__)

SECRET_KEY = "your-secret-key-min-32-chars-long!!"
ALGORITHM = "HS256"
ISSUER = "http://localhost:9000"
AUDIENCE = "http://localhost:3000"


class JWTTokenVerifier(TokenVerifier):
    async def verify_token(self, token: str) -> AccessToken | None:
        try:
            payload = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=[ALGORITHM],
                issuer=ISSUER,
                audience=AUDIENCE,
            )

            scopes = payload.get("scope", "").split() if payload.get("scope") else []

            return AccessToken(
                token=token,
                client_id=payload.get("client_id", "unknown"),
                scopes=scopes,
                expires_at=payload.get("exp"),
            )
        except JWTError:
            return None


app = FastMCP(
    "clappia-mcp-server",
    token_verifier=JWTTokenVerifier(),
    auth=AuthSettings(
        issuer_url=AnyHttpUrl(ISSUER),
        resource_server_url=AnyHttpUrl(AUDIENCE),
        required_scopes=["mcp:tools", "mcp:resources"],
    ),
)

AVAILABLE_MODULES = {
    "submissions": register_submission_tools,
    "definitions": register_definition_tools,
    "workflows": register_workflow_tools,
    "analytics": register_analytics_tools,
    "workplace": register_workplace_tools,
}


def register_all_tools():
    logger.info("✓ Registered OAuth authentication")

    for module_name, register_func in AVAILABLE_MODULES.items():
        try:
            register_func(app)
            logger.info(f"✓ Registered {module_name} tools")
        except Exception as e:
            logger.error(f"✗ Failed to register {module_name} tools: {str(e)}")


def main():
    try:
        register_all_tools()

        logger.info("🚀 Starting MCP Server on http://localhost:3000")
        logger.info("🔐 OAuth enabled - Auth server: http://localhost:9000")
        logger.info("📡 MCP endpoint: http://localhost:3000/mcp")

        starlette_app = app.streamable_http_app()
        uvicorn.run(starlette_app, host="0.0.0.0", port=3000, log_level="info")
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
