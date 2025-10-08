import sys
from mcp.server.fastmcp import FastMCP
from src.utils.logging_utils import get_logger
from src.tools.analytics import register_analytics_tools

logger = get_logger(__name__)

app = FastMCP("clappia-app-charts")


def register_all_tools():
    """Register all analytics-related tools"""
    register_analytics_tools(app)
    logger.info("All Clappia analytics tools registered successfully")


def main():
    try:
        register_all_tools()
        logger.info("Starting Clappia Analytics MCP server")
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
        print(f"\n=== Clappia Analytics MCP Tools ({len(tools)}) ===")
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
        Clappia Analytics MCP Server
        
        Usage:
            uv run -m src.server.analytics_server                # Run server (default)
            uv run -m src.server.analytics_server --list-tools   # List all tools
            uv run -m src.server.analytics_server --help         # Show help
        
        Required Environment Variables:
            CLAPPIA_API_KEY
        
        This server provides tools for:
        - Creating and managing analytics charts (summary, bar, pie, line, etc.)
        - Configuring data tables and maps
        - Setting up Gantt charts and dashboards
        - Managing analytics visualizations
        """
        )
    else:
        main()
