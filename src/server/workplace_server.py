import sys
from fastmcp import FastMCP
from src.utils.logging_utils import get_logger
from src.tools.workplace import register_workplace_tools

logger = get_logger(__name__)

app = FastMCP("clappia-workplace")


def register_all_tools():
    """Register all workplace-related tools"""
    register_workplace_tools(app)


def main():
    try:
        register_all_tools()
        app.run(transport="stdio")
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        sys.exit(1)
    finally:
        pass


def list_tools():
    register_all_tools()
    try:
        # Access tools from FastMCP instance
        tools = (
            app._tool_manager._tools
            if hasattr(app, "_tool_manager") and hasattr(app._tool_manager, "_tools")
            else {}
        )
        logger.info(f"Clappia Workplace MCP Tools ({len(tools)})")
        for tool_name in tools.keys():
            logger.info(f"• {tool_name}")
    except Exception as e:
        logger.error(f"Error listing tools: {e}")


if __name__ == "__main__":
    args = sys.argv[1:]

    if "--list-tools" in args:
        list_tools()
    elif "--help" in args or "-h" in args:
        print(
            """
        Clappia Workplace MCP Server
        
        Usage:
            uv run -m src.server.workplace_server                # Run server (default)
            uv run -m src.server.workplace_server --list-tools   # List all tools
            uv run -m src.server.workplace_server --help         # Show help
        
        Required Environment Variables:
            CLAPPIA_API_KEY
        
        This server provides tools for:
        - Managing workplace users and their details
        - Adding users to workplace and apps
        - Updating user roles, groups, and attributes
        - Managing app access and permissions
        """
        )
    else:
        main()
