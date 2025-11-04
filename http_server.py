import sys
import os
import logging
import uvicorn
from pydantic import AnyHttpUrl
from mcp.server.fastmcp import FastMCP
from mcp.server.auth.settings import AuthSettings
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.applications import Starlette

from src.utils.jwt_utils import JWTTokenVerifier, get_jwt_config
from src.utils.enums import Environment
from src.tools.submissions import register_submission_tools
from src.tools.definitions import register_definition_tools
from src.tools.workflows import register_workflow_tools
from src.tools.analytics import register_analytics_tools
from src.tools.workplace import register_workplace_tools
from src.tools.auth import register_auth_tools


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
        "auth": register_auth_tools,
    }
    for register_func in AVAILABLE_MODULES.values():
        try:
            register_func(mcp_app)
            logger.info(f"✓ Registered tools: {register_func.__name__}")
        except Exception as e:
            logger.error(f"✗ Failed to register {register_func.__name__}: {e}")


register_all_tools()


async def health_check(request: Request):
    return JSONResponse({"status": "ok"})


async def protected_resource_metadata(request: Request):
    return JSONResponse(
        {
            "resource": AUDIENCE,
            "authorization_servers": [ISSUER],
            "scopes_supported": ["mcp:tools"],
            "bearer_methods_supported": ["header"],
        }
    )


async def debug_info(request: Request):
    try:
        tools = await mcp_app.list_tools()
        routes_list = []
        for route in app.routes:
            if hasattr(route, "path"):
                methods = getattr(route, "methods", None)
                if methods:
                    methods_str = ",".join(str(m) for m in methods)
                else:
                    methods_str = "ANY"
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

    starlette_app.routes.insert(0, Route("/health", health_check))
    starlette_app.routes.insert(1, Route("/debug", debug_info))
    starlette_app.routes.insert(
        2, Route("/.well-known/oauth-protected-resource", protected_resource_metadata)
    )

    starlette_app.add_middleware(WWWAuthenticateMiddleware)

    return starlette_app


app = create_app()


print("\n" + "=" * 50)
print("REGISTERED ROUTES:")
for route in app.routes:
    if hasattr(route, "path"):
        methods = getattr(route, "methods", None)
        if methods:
            methods_str = ",".join(str(m) for m in methods)
        else:
            methods_str = "ANY"
        print(f"  {route.path} - {methods_str}")
    else:
        print(f"  {type(route).__name__}")
print("=" * 50 + "\n")


def main():
    try:
        workers = int(os.getenv("WORKERS", 1))
        environment = Environment.from_env(default=Environment.DEV)
        is_production = environment.is_production()

        logger.info(f"🚀 Starting MCP server on http://0.0.0.0:8000")
        logger.info(f"📋 Issuer: {ISSUER}")
        logger.info(f"🎯 Audience: {AUDIENCE}")
        logger.info(f"🌍 Environment: {environment.value}")

        if is_production and workers > 1:
            logger.info(
                f"👷 Production mode: Using {workers} workers via import string"
            )
            logger.info(
                f"💡 Running with: uvicorn http_server:app --host 0.0.0.0 --port 8000 --workers {workers}"
            )
            uvicorn.run(
                "http_server:app",
                host="0.0.0.0",
                port=8000,
                workers=workers,
                log_level="info",
                limit_concurrency=1000,
                timeout_keep_alive=65,
            )
        else:
            if workers > 1:
                logger.warning(
                    "⚠️  Multiple workers require production mode. Using 1 worker for dev/qa."
                )
            logger.info("🔧 Dev/QA mode: Single worker with direct app object")
            uvicorn.run(
                app,
                host="0.0.0.0",
                port=8000,
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
