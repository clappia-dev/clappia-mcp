import os
import sys
import argparse
from fastmcp import FastMCP
from fastmcp.server.middleware import Middleware, MiddlewareContext
from fastmcp.server.dependencies import get_http_headers

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
        
        
        result = await call_next(context)
        return result


def register_all_tools():
    app.add_middleware(APIKeyAuthMiddleware())
    logger.info("✓ Registered API key authentication middleware")
    
    for module_name, register_func in AVAILABLE_MODULES.items():
        try:
            register_func(app)
        except Exception as e:
            logger.error(f"✗ Failed to register {module_name} tools: {str(e)}")



def register_specific_tools(modules):
    app.add_middleware(APIKeyAuthMiddleware())
    logger.info("✓ Registered API key authentication middleware")
    
    for module in modules:
        if module in AVAILABLE_MODULES:
            try:
                AVAILABLE_MODULES[module](app)
            except Exception as e:
                logger.error(f"✗ Failed to register {module} tools: {str(e)}")
        else:
            logger.warning(f"⚠ Unknown module: {module}")



def list_tools():
    try:
        tools = (
            app._tool_manager._tools
            if hasattr(app, "_tool_manager") and hasattr(app._tool_manager, "_tools")
            else {}
        )
        logger.info(f"Clappia MCP Tools ({len(tools)} tools registered)")
        
        if tools:
            for tool_name in sorted(tools.keys()):
                logger.info(f"  • {tool_name}")
        else:
            logger.info("  No tools registered")
    except Exception as e:
        logger.error(f"Error listing tools: {e}")


def print_startup_banner(args):
    logger.info(f"Starting Clappia MCP Server on http://{args.host}:{args.port}")


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
        app.run(transport="streamable-http")

    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        sys.exit(1)
    finally:
        pass


if __name__ == "__main__":
    main()