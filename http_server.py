import logging
import os
import sys

import uvicorn
from mcp.server.auth.settings import AuthSettings
from mcp.server.fastmcp import FastMCP
from pydantic import AnyHttpUrl
from starlette.applications import Starlette
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from src.tools.analytics import register_analytics_tools
from src.tools.definitions import register_definition_tools
from src.tools.submissions import register_submission_tools
from src.tools.workflows import register_workflow_tools
from src.tools.workplace import register_workplace_tools
from src.utils.constants import OAUTH_CONSTANTS
from src.utils.jwt_utils import JWTTokenVerifier, get_jwt_config

logger = logging.getLogger(__name__)

jwt_config = get_jwt_config()
ISSUER = jwt_config["issuer"]
AUDIENCE = jwt_config["audience"]


mcp_app = FastMCP(
    "clappia-mcp-server",
    token_verifier=JWTTokenVerifier(),
    auth=AuthSettings(
        issuer_url=AnyHttpUrl(ISSUER),
        resource_server_url=AnyHttpUrl(AUDIENCE),
        required_scopes=["mcp:tools"],
    ),
)


def register_all_tools():
    AVAILABLE_MODULES = {
        "submissions": register_submission_tools,
        "definitions": register_definition_tools,
        "workflows": register_workflow_tools,
        "analytics": register_analytics_tools,
        "workplace": register_workplace_tools,
    }
    for register_func in AVAILABLE_MODULES.values():
        try:
            register_func(mcp_app)
            logger.info(f"✓ Registered tools: {register_func.__name__}")
        except Exception as e:
            logger.error(f"✗ Failed to register {register_func.__name__}: {e}")


register_all_tools()


async def health_check(_request: Request):
    return JSONResponse({"status": "ok"})


async def protected_resource_metadata(_request: Request):
    return JSONResponse(
        {
            "resource": AUDIENCE,
            "authorization_servers": [ISSUER],
            "scopes_supported": ["mcp:tools"],
            "bearer_methods_supported": ["header"],
        }
    )


async def oauth_authorization_server_metadata(_request: Request):
    return JSONResponse(
        {
            "issuer": OAUTH_CONSTANTS["DEFAULT_ISSUER"],
            "authorization_endpoint": OAUTH_CONSTANTS["AUTHORIZATION_ENDPOINT"],
            "token_endpoint": OAUTH_CONSTANTS["TOKEN_ENDPOINT"],
            "registration_endpoint": OAUTH_CONSTANTS["REGISTRATION_ENDPOINT"],
            "response_types_supported": OAUTH_CONSTANTS["RESPONSE_TYPES_SUPPORTED"],
            "grant_types_supported": OAUTH_CONSTANTS["GRANT_TYPES_SUPPORTED"],
            "code_challenge_methods_supported": OAUTH_CONSTANTS[
                "CODE_CHALLENGE_METHODS_SUPPORTED"
            ],
            "token_endpoint_auth_methods_supported": OAUTH_CONSTANTS[
                "TOKEN_ENDPOINT_AUTH_METHODS_SUPPORTED"
            ],
            "scopes_supported": OAUTH_CONSTANTS["SCOPES_SUPPORTED"],
        }
    )


async def openid_configuration(_request: Request):
    return JSONResponse(
        {
            "issuer": OAUTH_CONSTANTS["DEFAULT_ISSUER"],
            "authorization_endpoint": OAUTH_CONSTANTS["AUTHORIZATION_ENDPOINT"],
            "token_endpoint": OAUTH_CONSTANTS["TOKEN_ENDPOINT"],
            "registration_endpoint": OAUTH_CONSTANTS["REGISTRATION_ENDPOINT"],
            "response_types_supported": OAUTH_CONSTANTS["RESPONSE_TYPES_SUPPORTED"],
            "grant_types_supported": OAUTH_CONSTANTS["GRANT_TYPES_SUPPORTED"],
            "code_challenge_methods_supported": OAUTH_CONSTANTS[
                "CODE_CHALLENGE_METHODS_SUPPORTED"
            ],
            "token_endpoint_auth_methods_supported": OAUTH_CONSTANTS[
                "TOKEN_ENDPOINT_AUTH_METHODS_SUPPORTED"
            ],
            "scopes_supported": OAUTH_CONSTANTS["SCOPES_SUPPORTED"],
        }
    )


async def root_endpoint(_request: Request):
    return JSONResponse(
        {
            "server": "clappia-mcp-server",
            "version": "1.0.0",
            "endpoints": {
                "health": "/health",
                "debug": "/debug",
                "oauth_protected_resource": "/.well-known/oauth-protected-resource",
                "oauth_authorization_server": "/.well-known/oauth-authorization-server",
                "openid_configuration": "/.well-known/openid-configuration",
            },
            "environment": os.getenv("ENVIRONMENT", "unknown"),
        }
    )


async def debug_info(_request: Request):
    try:
        tools = await mcp_app.list_tools()
        routes_list = []
        for route in app.routes:
            if hasattr(route, "path"):
                methods = getattr(route, "methods", None)
                methods_str = ",".join(str(m) for m in methods) if methods else "ANY"
                routes_list.append(f"{route.path} [{methods_str}]")
            else:
                routes_list.append(f"{type(route).__name__}")

        return JSONResponse(
            {
                "server": "clappia-mcp-server",
                "tools_count": len(tools),
                "tools": [
                    {
                        "name": tool.name,
                        "description": tool.description,
                    }
                    for tool in tools
                ],
                "routes": routes_list,
            }
        )
    except Exception as e:
        logger.error(f"Debug endpoint error: {e}", exc_info=True)
        return JSONResponse(
            {"error": str(e), "type": str(type(e).__name__)}, status_code=500
        )


class WWWAuthenticateMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        if response.status_code == 401 and "WWW-Authenticate" not in response.headers:
            response.headers["WWW-Authenticate"] = (
                f'Bearer realm="mcp", '
                f'resource_metadata="{AUDIENCE}/.well-known/oauth-protected-resource"'
            )

        return response


def create_app() -> Starlette:
    starlette_app = mcp_app.streamable_http_app()

    starlette_app.routes.insert(0, Route("/", root_endpoint))
    starlette_app.routes.insert(1, Route("/health", health_check))
    starlette_app.routes.insert(2, Route("/debug", debug_info))
    starlette_app.routes.insert(
        3, Route("/.well-known/oauth-protected-resource", protected_resource_metadata)
    )
    starlette_app.routes.insert(
        4,
        Route(
            "/.well-known/oauth-protected-resource/mcp",
            protected_resource_metadata,
        ),
    )
    starlette_app.routes.insert(
        5,
        Route(
            "/.well-known/oauth-authorization-server",
            oauth_authorization_server_metadata,
        ),
    )
    starlette_app.routes.insert(
        6,
        Route(
            "/.well-known/oauth-authorization-server/mcp",
            oauth_authorization_server_metadata,
        ),
    )
    starlette_app.routes.insert(
        7,
        Route(
            "/.well-known/openid-configuration",
            openid_configuration,
        ),
    )
    starlette_app.routes.insert(
        8,
        Route(
            "/.well-known/openid-configuration/mcp",
            openid_configuration,
        ),
    )
    starlette_app.routes.insert(
        9,
        Route(
            "/mcp/.well-known/openid-configuration",
            openid_configuration,
        ),
    )

    starlette_app.add_middleware(WWWAuthenticateMiddleware)

    return starlette_app


app = create_app()


print("\n" + "=" * 50)
print("REGISTERED ROUTES:")
for route in app.routes:
    if hasattr(route, "path"):
        methods = getattr(route, "methods", None)
        methods_str = ",".join(str(m) for m in methods) if methods else "ANY"
        print(f"  {route.path} - {methods_str}")
    else:
        print(f"  {type(route).__name__}")
print("=" * 50 + "\n")


def main():
    try:
        port = int(os.getenv("PORT", 8080))

        logger.info(f"🚀 Starting MCP server on http://0.0.0.0:{port}")
        logger.info(f"📋 Issuer: {ISSUER}")
        logger.info(f"🎯 Audience: {AUDIENCE}")

        uvicorn.run(
            app,
            host="0.0.0.0",
            port=port,
            log_level="info",
            limit_concurrency=1000,
            timeout_keep_alive=65,
        )
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
