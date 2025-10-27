import sys
import uvicorn
from pydantic import AnyHttpUrl
from mcp.server.fastmcp import FastMCP
from mcp.server.auth.provider import AccessToken, TokenVerifier
from mcp.server.auth.settings import AuthSettings
from jose import jwt, JWTError
from fastapi.responses import JSONResponse
from starlette.routing import Route
from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware
from src.utils.logging_utils import get_logger

logger = get_logger(__name__)

# Configuration
ISSUER = "https://clappia-auth.loca.lt"
AUDIENCE = "https://clappia-mcp.loca.lt"
SECRET_KEY = "your-secret-key-min-32-chars-long!!"
ALGORITHM = "HS256"


class JWTTokenVerifier(TokenVerifier):
    async def verify_token(self, token: str) -> AccessToken | None:
        try:
            payload = jwt.decode(
                token, SECRET_KEY, algorithms=[ALGORITHM],
                issuer=ISSUER, audience=AUDIENCE,
                options={"verify_signature": True, "verify_exp": True, "verify_iss": True, "verify_aud": True}
            )
            scopes = payload.get("scope", "").split() if payload.get("scope") else []
            return AccessToken(token=token, client_id=payload.get("client_id", "unknown"),
                             scopes=scopes, expires_at=payload.get("exp"))
        except JWTError as e:
            logger.error(f"Token validation failed: {e}")
            return None


# Create FastMCP app
app = FastMCP(
    "clappia-mcp-server",
    token_verifier=JWTTokenVerifier(),
    auth=AuthSettings(
        issuer_url=AnyHttpUrl(ISSUER),
        resource_server_url=AnyHttpUrl(AUDIENCE),
        required_scopes=["mcp:tools", "mcp:resources"],
    ),
)


# =============================================================================
# TOOL REGISTRATION WITH DEBUG INFO
# =============================================================================

logger.info("=" * 80)
logger.info("🔧 Registering Clappia MCP Tools")
logger.info("=" * 80)

# Check what attributes FastMCP has for storing tools
logger.info(f"📊 FastMCP app attributes: {dir(app)}")
logger.info("")

# Try different ways to count tools
def count_tools():
    """Try to count registered tools"""
    for attr in ['_tools', 'tools', '_tool_handlers', 'tool_handlers']:
        if hasattr(app, attr):
            tools = getattr(app, attr)
            logger.info(f"   Found {attr}: {len(tools) if tools else 0} items")
            return len(tools) if tools else 0
    logger.warning("   No tool storage attribute found!")
    return 0

initial_count = count_tools()

# Register submissions tools
try:
    from src.tools.submissions import register_submission_tools
    logger.info("\n📦 Registering submissions tools...")
    register_submission_tools(app)
    logger.info("✅ Submissions tools registered")
    count_tools()
except Exception as e:
    logger.error(f"❌ Submissions tools failed: {e}")
    import traceback
    traceback.print_exc()

# Register definitions tools
try:
    from src.tools.definitions import register_definition_tools
    logger.info("\n📦 Registering definitions tools...")
    register_definition_tools(app)
    logger.info("✅ Definitions tools registered")
    count_tools()
except Exception as e:
    logger.error(f"❌ Definitions tools failed: {e}")

# Register workflows tools
try:
    from src.tools.workflows import register_workflow_tools
    logger.info("\n📦 Registering workflows tools...")
    register_workflow_tools(app)
    logger.info("✅ Workflows tools registered")
    count_tools()
except Exception as e:
    logger.error(f"❌ Workflows tools failed: {e}")

# Register analytics tools
try:
    from src.tools.analytics import register_analytics_tools
    logger.info("\n📦 Registering analytics tools...")
    register_analytics_tools(app)
    logger.info("✅ Analytics tools registered")
    count_tools()
except Exception as e:
    logger.error(f"❌ Analytics tools failed: {e}")

# Register workplace tools
try:
    from src.tools.workplace import register_workplace_tools
    logger.info("\n📦 Registering workplace tools...")
    register_workplace_tools(app)
    logger.info("✅ Workplace tools registered")
    count_tools()
except Exception as e:
    logger.error(f"❌ Workplace tools failed: {e}")

logger.info("=" * 80)


# =============================================================================
# CUSTOM ENDPOINTS
# =============================================================================

async def protected_resource_metadata(request: Request):
    return JSONResponse(content={
        "resource": AUDIENCE,
        "authorization_servers": [ISSUER],
        "scopes_supported": ["mcp:tools", "mcp:resources"],
        "bearer_methods_supported": ["header"],
    })


async def health_check(request: Request):
    tool_count = 0
    tool_names = []
    
    # Try to get tool count and names
    for attr in ['_tools', 'tools', '_tool_handlers', 'tool_handlers']:
        if hasattr(app, attr):
            tools = getattr(app, attr)
            if tools:
                tool_count = len(tools)
                if isinstance(tools, dict):
                    tool_names = list(tools.keys())
                break
    
    return JSONResponse(content={
        "status": "healthy",
        "server": "clappia-mcp-server",
        "auth": {"issuer": ISSUER, "audience": AUDIENCE},
        "tools_registered": tool_count,
        "tool_names": tool_names[:5] if tool_names else []  # First 5 tools
    })


class WWWAuthenticateMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        if response.status_code == 401 and "WWW-Authenticate" not in response.headers:
            response.headers["WWW-Authenticate"] = (
                f'Bearer realm="mcp", resource_metadata="{AUDIENCE}/.well-known/oauth-protected-resource"'
            )
        return response


# =============================================================================
# MAIN
# =============================================================================

def main():
    try:
        logger.info("\n🚀 Starting Clappia MCP Server")
        logger.info(f"   MCP:   {AUDIENCE}")
        logger.info(f"   Auth:  {ISSUER}")
        logger.info(f"   Login: user@example.com / password123")
        logger.info("")
        
        # Get Starlette app
        starlette_app = app.streamable_http_app()
        
        # Add custom routes
        starlette_app.routes.append(Route("/.well-known/oauth-protected-resource", protected_resource_metadata))
        starlette_app.routes.append(Route("/health", health_check))
        starlette_app.add_middleware(WWWAuthenticateMiddleware)
        
        # Run server
        uvicorn.run(starlette_app, host="0.0.0.0", port=3000, log_level="info")
        
    except KeyboardInterrupt:
        logger.info("\n👋 Server stopped")
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()