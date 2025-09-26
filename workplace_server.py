import sys
from mcp.server.fastmcp import FastMCP
from utils import get_logger
from tools.workplace import register_workplace_tools

logger = get_logger(__name__)

app = FastMCP("clappia-workplace")


def register_all_tools():
    """Register all workplace-related tools"""
    register_workplace_tools(app)
    logger.info("All Clappia workplace tools registered successfully")


def main():
    try:
        register_all_tools()
        logger.info("Starting Clappia Workplace MCP server")
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
        print(f"\n=== Clappia Workplace MCP Tools ({len(tools)}) ===")
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
        Clappia Workplace MCP Server
        
        Usage:
            uv run workplace_server.py                # Run server (default)
            uv run workplace_server.py --list-tools   # List all tools
            uv run workplace_server.py --help         # Show help
        
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
