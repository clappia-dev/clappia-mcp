import os
import sys
import argparse
from typing import Optional
from mcp.server.fastmcp import FastMCP, Context
from starlette.requests import Request
from starlette.responses import JSONResponse
import uvicorn
import traceback

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


class AuthLoggingMiddleware:
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        auth_token = None
        headers = dict(scope.get("headers", []))
        
        for header_key in [b"x-api-key", b"x-apikey"]:
            if header_key in headers:
                auth_token = headers[header_key].decode("utf-8")
                break
        
        if not auth_token and b"authorization" in headers:
            auth_header = headers[b"authorization"].decode("utf-8")
            if auth_header.startswith("Bearer "):
                auth_token = auth_header[7:]
        
        if not auth_token:
            await send({
                "type": "http.response.start",
                "status": 401,
                "headers": [[b"content-type", b"application/json"]],
            })
            await send({
                "type": "http.response.body",
                "body": b'{"error":"Authentication required","message":"Please provide X-API-Key header"}',
            })
            return
        
        os.environ["CLAPPIA_API_KEY"] = auth_token
        
        client = scope.get("client")
        client_ip = client[0] if client else "unknown"
        path = scope.get("path", "")
        method = scope.get("method", "")
        
        logger.info(
            f"Request: {method} {path} | "
            f"Client: {client_ip} | "
            f"Auth Token: {auth_token[:8]}..."
        )
        
        response_status = None
        
        async def send_wrapper(message):
            nonlocal response_status
            if message["type"] == "http.response.start":
                response_status = message.get("status")
            await send(message)
        
        try:
            await self.app(scope, receive, send_wrapper)
            
            if response_status:
                logger.info(
                    f"Response: {response_status} | "
                    f"Token: {auth_token[:8]}..."
                )
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            raise


def register_all_tools():
    for module_name, register_func in AVAILABLE_MODULES.items():
        try:
            register_func(app)
            logger.info(f"Registered {module_name} tools")
        except Exception as e:
            logger.error(f"Failed to register {module_name} tools: {str(e)}")

    logger.info("All Clappia MCP tools registered successfully")


def register_specific_tools(modules):
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
        logger.info("  - Header: X-API-Key: your-token")
        logger.info("  - Header: Authorization: Bearer your-token")
        logger.info("")
        logger.info("Note: Auth token will be stored in CLAPPIA_API_KEY env var")
        logger.info("      Authentication is REQUIRED for all requests")
        logger.info("")
        logger.info("Available Modules:")
        for module in AVAILABLE_MODULES.keys():
            logger.info(f"  - {module}")
        logger.info("=" * 70)
        
        sse_app = app.sse_app()
        wrapped_app = AuthLoggingMiddleware(sse_app)
        
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
        traceback.print_exc()
        sys.exit(1)
    finally:
        logger.info("MCP server shutdown complete")


if __name__ == "__main__":
    main()