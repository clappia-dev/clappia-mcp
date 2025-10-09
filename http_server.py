import os
import sys
import argparse
from fastmcp.server.http import create_sse_app
from fastmcp import FastMCP
from fastmcp.server.middleware import Middleware, MiddlewareContext
from fastmcp.server.dependencies import get_http_headers
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


class APIKeyAuthMiddleware(Middleware):
    
    async def on_request(self, context: MiddlewareContext, call_next):
        headers = get_http_headers()
        
        api_key = headers.get("x-api-key") or headers.get("x-api-key")
        
        if not api_key:
            logger.warning("Request rejected: Missing API key")
            raise ValueError("API key is required. Please provide X-API-Key header")
        
        logger.debug(f"Request authenticated with key: {api_key[:10]}...")
        
        result = await call_next(context)
        return result


def register_all_tools():
    app.add_middleware(APIKeyAuthMiddleware())
    logger.info("✓ Registered API key authentication middleware")
    
    for module_name, register_func in AVAILABLE_MODULES.items():
        try:
            register_func(app)
            logger.info(f"✓ Registered {module_name} tools")
        except Exception as e:
            logger.error(f"✗ Failed to register {module_name} tools: {str(e)}")
            logger.error(traceback.format_exc())

    logger.info("All Clappia MCP tools registered successfully")


def register_specific_tools(modules):
    app.add_middleware(APIKeyAuthMiddleware())
    logger.info("✓ Registered API key authentication middleware")
    
    for module in modules:
        if module in AVAILABLE_MODULES:
            try:
                AVAILABLE_MODULES[module](app)
                logger.info(f"✓ Registered {module} tools")
            except Exception as e:
                logger.error(f"✗ Failed to register {module} tools: {str(e)}")
                logger.error(traceback.format_exc())
        else:
            logger.warning(f"⚠ Unknown module: {module}")
            logger.info(f"Available modules: {', '.join(AVAILABLE_MODULES.keys())}")

    logger.info(f"Registered tools from modules: {', '.join(modules)}")


def list_tools():
    try:
        tools = (
            app._tool_manager._tools
            if hasattr(app, "_tool_manager") and hasattr(app._tool_manager, "_tools")
            else {}
        )
        print(f"\n{'='*60}")
        print(f"Clappia MCP Tools ({len(tools)} tools registered)")
        print(f"{'='*60}")
        
        if tools:
            for tool_name in sorted(tools.keys()):
                print(f"  • {tool_name}")
        else:
            print("  No tools registered")
        
        print(f"{'='*60}\n")
    except Exception as e:
        logger.error(f"Error listing tools: {e}")
        print(f"Error listing tools: {e}")


def print_startup_banner(args):
    logger.info("=" * 70)
    logger.info("Starting Clappia MCP Server [SSE TRANSPORT]")
    logger.info("=" * 70)
    logger.info(f"Listening: http://{args.host}:{args.port}")
    logger.info("")
    logger.info("SSE Endpoint: /sse")
    logger.info("")
    logger.info("Authentication: Pass token via:")
    logger.info("  - Header: X-API-Key: your-token")
    logger.info("  - Header: X-Api-Key: your-token")
    logger.info("")
    logger.info("⚠ Authentication is REQUIRED for all requests")
    logger.info("")
    logger.info("Available Modules:")
    for module in AVAILABLE_MODULES.keys():
        logger.info(f"  • {module}")
    logger.info("=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="Clappia MCP Server - Model Context Protocol server for Clappia API"
    )
    parser.add_argument(
        "--modules",
        nargs="+",
        choices=list(AVAILABLE_MODULES.keys()) + ["all"],
        default=["all"],
        help="Specify which modules to load (default: all)",
    )
    parser.add_argument(
        "--list-tools", 
        action="store_true", 
        help="List all available tools and exit"
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host to bind to (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind to (default: 8000)"
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
        
        print_startup_banner(args)
        app.run(transport="http")

    except KeyboardInterrupt:
        logger.info("\n" + "=" * 70)
        logger.info("Server shutdown requested by user")
        logger.info("=" * 70)
    except Exception as e:
        logger.error("=" * 70)
        logger.error(f"Server error: {str(e)}")
        logger.error("=" * 70)
        logger.error(traceback.format_exc())
        sys.exit(1)
    finally:
        logger.info("MCP server shutdown complete")


if __name__ == "__main__":
    main()