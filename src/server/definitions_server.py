import sys
from fastmcp import FastMCP
from src.utils.logging_utils import get_logger
from src.tools.definitions import register_definition_tools

logger = get_logger(__name__)

app = FastMCP("clappia-app-form")


def register_all_tools():
    """Register all app definition-related tools"""
    register_definition_tools(app)
    logger.info("All Clappia app definition tools registered successfully")


def main():
    try:
        register_all_tools()
        logger.info("Starting Clappia App Definitions MCP server")
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
    register_all_tools()
    try:
        # Access tools from FastMCP instance
        tools = (
            app._tool_manager._tools
            if hasattr(app, "_tool_manager") and hasattr(app._tool_manager, "_tools")
            else {}
        )
        print(f"\n=== Clappia App Form MCP Tools ({len(tools)}) ===")
        for tool_name in tools.keys():
            print(f"• {tool_name}")
    except Exception as e:
        print(f"Error listing tools: {e}")


if __name__ == "__main__":
    args = sys.argv[1:]

    if "--list-tools" in args:
        list_tools()
    elif "--help" in args or "-h" in args:
        print(
            """
        Clappia App Form MCP Server
        
        Usage:
            uv run -m src.server.definitions_server                # Run server (default)
            uv run -m src.server.definitions_server --list-tools   # List all tools
            uv run -m src.server.definitions_server --help         # Show help
        
        Required Environment Variables:
            CLAPPIA_API_KEY
        
        This server provides tools for:
        - Creating and managing Clappia apps
        - Adding and configuring various field types
        - Managing app structure (pages, sections, fields)
        - Updating app settings and configurations
        """
        )
    else:
        main()
