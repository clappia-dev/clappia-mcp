import os
import sys
import argparse
from typing import Optional
from mcp.server.fastmcp import FastMCP, Context
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import uvicorn
from starlette.applications import Starlette
from starlette.middleware import Middleware

from src.utils.logging_utils import get_logger
from src.tools.submissions import register_submission_tools
from src.tools.definitions import register_definition_tools
from src.tools.workflows import register_workflow_tools
from src.tools.analytics import register_analytics_tools
from src.tools.workplace import register_workplace_tools

logger = get_logger(__name__)

app = FastMCP("clappia-mcp-server")

AVAILABLE_MODULES = {
    "submissions": register_submission_tools,
    "definitions": register_definition_tools,
    "workflows": register_workflow_tools,
    "analytics": register_analytics_tools,
    "workplace": register_workplace_tools,
}


class AuthLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to extract and log auth tokens from requests"""
    
    async def dispatch(self, request: Request, call_next):
        auth_token = None
        
        api_key_headers = [
            "x-api-key",
            "X-API-Key", 
            "X-API-KEY",
            "X-Api-Key",
            "x-apikey",
            "X-Apikey",
            "X-APIKEY"
        ]
        
        for header_name in api_key_headers:
            if header_name in request.headers:
                auth_token = request.headers[header_name]
                break
        
        if not auth_token:
            from starlette.responses import JSONResponse
            return JSONResponse(
                status_code=401,
                content={
                    "error": "Authentication required",
                    "message": "No API key found in request headers. Please provide an API key using one of these headers: " + ", ".join(api_key_headers)
                }
            )
        
        os.environ["CLAPPIA_API_KEY"] = auth_token
        
        client_ip = request.client.host if request.client else "unknown"
        logger.info(
            f"Request: {request.method} {request.url.path} | "
            f"Client: {client_ip} | "
            f"Auth Token: {auth_token[:8]}..."  
        )
        
        request.state.auth_token = auth_token
        response = await call_next(request)
        
        logger.info(
            f"Response: {response.status_code} | "
            f"Token: {auth_token[:8]}..."
        )
        
        return response


def register_all_tools():
    """Register all tools from all modules"""
    for module_name, register_func in AVAILABLE_MODULES.items():
        try:
            register_func(app)
            logger.info(f"Registered {module_name} tools")
        except Exception as e:
            logger.error(f"Failed to register {module_name} tools: {str(e)}")

    logger.info("All Clappia MCP tools registered successfully")


def register_specific_tools(modules):
    """Register tools from specific modules only"""
    for module in modules:
        if module in AVAILABLE_MODULES:
            try:
                AVAILABLE_MODULES[module](app)
                logger.info(f"Registered {module} tools")
            except Exception as e:
                logger.error(f"Failed to register {module} tools: {str(e)}")
        else:
            logger.warning(f"Unknown module: {module}")

    logger.info(f"Registered tools from modules: {', '.join(modules)}")


def list_tools():
    try:
        tools = (
            app._tool_manager._tools
            if hasattr(app, "_tool_manager") and hasattr(app._tool_manager, "_tools")
            else {}
        )
        print(f"\n=== Clappia MCP Tools ({len(tools)}) ===")
        for tool_name in tools.keys():
            print(f"• {tool_name}")
    except Exception as e:
        print(f"Error listing tools: {e}")


def main():
    parser = argparse.ArgumentParser(description="Clappia MCP Server")
    parser.add_argument(
        "--modules",
        nargs="+",
        choices=list(AVAILABLE_MODULES.keys()) + ["all"],
        default=["all"],
        help="Specify which modules to load (default: all)",
    )
    parser.add_argument(
        "--list-tools", action="store_true", help="List all available tools and exit"
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host to bind to"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind to"
    )

    args = parser.parse_args()

    try:
        if "all" in args.modules:
            register_all_tools()
        else:
            register_specific_tools(args.modules)

        if args.list_tools:
            list_tools()
            return
        logger.info("=" * 70)
        logger.info("Starting Clappia MCP Server [SSE TRANSPORT]")
        logger.info("=" * 70)
        logger.info(f"Listening: http://{args.host}:{args.port}")
        logger.info("")
        logger.info("SSE Endpoint: /sse")
        logger.info("")
        logger.info("Authentication: Pass token via:")
        logger.info("  - Header: X-API-Key: your-token (or any case variation)")
        logger.info("")
        logger.info("Note: Auth token will be stored in CLAPPIA_API_KEY env var")
        logger.info("      Authentication is REQUIRED for all requests")
        logger.info("")
        logger.info("Available Modules:")
        for module in AVAILABLE_MODULES.keys():
            logger.info(f"  - {module}")
        logger.info("=" * 70)
        
        sse_app = app.sse_app()
        
        wrapped_app = Starlette(
            routes=sse_app.routes,
            middleware=[
                Middleware(AuthLoggingMiddleware)
            ],
            lifespan=sse_app.router.lifespan_context
        )
        
        uvicorn.run(
            wrapped_app,
            host=args.host,
            port=args.port,
            log_level="info"
        )

    except KeyboardInterrupt:
        logger.info("Server shutdown requested by user")
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        sys.exit(1)
    finally:
        logger.info("MCP server shutdown complete")


if __name__ == "__main__":
    main()
