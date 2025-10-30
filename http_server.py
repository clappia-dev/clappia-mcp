import sys
import logging
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
from src.tools.submissions import register_submission_tools
from src.tools.definitions import register_definition_tools
from src.tools.workflows import register_workflow_tools
from src.tools.analytics import register_analytics_tools
from src.tools.workplace import register_workplace_tools

logger = logging.getLogger(__name__)

ISSUER = "https://preprod-dev.clappia.com"
AUDIENCE = "https://clappia-mcp.loca.lt"
SECRET_KEY = "clappia_access_test_secret_key"  
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
            return AccessToken(
                token=token,
                client_id=payload.get("client_id", "unknown"),
                scopes=scopes,
                expires_at=payload.get("exp")
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
    for register_func in AVAILABLE_MODULES.values():
        try:
            register_func(app)
            logger.info(f"Tools registered for {register_func.__name__}")
        except Exception as e:
            logger.error(f"Failed to register tools for {register_func.__name__}: {e}")

register_all_tools()


async def protected_resource_metadata(request: Request):
    return JSONResponse({
        "resource": AUDIENCE,
        "authorization_servers": [ISSUER],
        "scopes_supported": ["mcp:tools", "mcp:resources"],
        "bearer_methods_supported": ["header"],
    })


class WWWAuthenticateMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        if response.status_code == 401 and "WWW-Authenticate" not in response.headers:
            response.headers["WWW-Authenticate"] = (
                f'Bearer realm="mcp", resource_metadata="{AUDIENCE}/.well-known/oauth-protected-resource"'
            )
        return response


def main():
    try:
        starlette_app = app.streamable_http_app()
        starlette_app.routes.append(Route("/.well-known/oauth-protected-resource", protected_resource_metadata))
        starlette_app.add_middleware(WWWAuthenticateMiddleware)
        
        uvicorn.run(starlette_app, host="0.0.0.0", port=3000, log_level="info")
        
    except KeyboardInterrupt:
        logger.info("Server stopped")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()