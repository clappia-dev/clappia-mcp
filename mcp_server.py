import sys
import argparse
from fastmcp import FastMCP
from src.utils.logging_utils import get_logger
from src.tools.submissions import register_submission_tools
from src.tools.definitions import register_definition_tools
from src.tools.workflows import register_workflow_tools
from src.tools.analytics import register_analytics_tools
from src.tools.workplace import register_workplace_tools

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
        except Exception as e:
            logger.error(f"Failed to register {module_name} tools: {str(e)}")



def register_specific_tools(modules):
    """Register tools from specific modules only"""
    for module in modules:
        if module in AVAILABLE_MODULES:
            try:
                AVAILABLE_MODULES[module](app)
            except Exception as e:
                logger.error(f"Failed to register {module} tools: {str(e)}")
        else:
            logger.warning(f"Unknown module: {module}")



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

        app.run(transport="stdio")

    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        sys.exit(1)
    finally:
        pass


def list_tools():
    try:
        # Access tools from FastMCP instance
        tools = (
            app._tool_manager._tools
            if hasattr(app, "_tool_manager") and hasattr(app._tool_manager, "_tools")
            else {}
        )
        logger.info(f"Clappia MCP Tools ({len(tools)})")
        for tool_name in tools.keys():
            logger.info(f"• {tool_name}")
    except Exception as e:
        logger.error(f"Error listing tools: {e}")


if __name__ == "__main__":
    main()
