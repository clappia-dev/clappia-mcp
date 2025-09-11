import sys
import argparse
from fastmcp import FastMCP
from utils import get_logger
from tools.submissions import register_submission_tools
from tools.definitions import register_definition_tools
from tools.workflows import register_workflow_tools
from tools.analytics import register_analytics_tools
from tools.workplace import register_workplace_tools

logger = get_logger(__name__)

app = FastMCP("clappia-mcp-server")

# Available server modules
AVAILABLE_MODULES = {
    "submissions": register_submission_tools,
    "definitions": register_definition_tools,
    "workflows": register_workflow_tools,
    "analytics": register_analytics_tools,
    "workplace": register_workplace_tools,
}


def register_all_tools():
    """Register all tools from all modules"""
    for module_name, register_func in AVAILABLE_MODULES.items():
        try:
            register_func(app)
            logger.info(f"Registered {module_name} tools")
        except Exception as e:
            logger.error(f"Failed to register {module_name} tools: {str(e)}")

    logger.info("All Clappia MCP tools registered successfully")

register_all_tools()

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

    args = parser.parse_args()

    try:
        if "all" in args.modules:
            register_all_tools()
        else:
            register_specific_tools(args.modules)

        if args.list_tools:
            list_tools()
            return

        logger.info("Starting Clappia MCP server")
        logger.info("CLAPPIA_API_KEY must be set as environment variable")
        app.run(transport="stdio")

    except KeyboardInterrupt:
        logger.info("Server shutdown requested by user")
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        sys.exit(1)
    finally:
        logger.info("MCP server shutdown complete")


def list_tools():
    try:
        # Access tools from FastMCP instance
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


if __name__ == "__main__":
    main()
