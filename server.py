import sys
from mcp.server.fastmcp import FastMCP
from utils import get_logger
from tools.submissions import register_submission_tools
from tools.definitions import register_definition_tools
from tools.workflows import register_workflow_tools
from tools.analytics import register_analytics_tools
from tools.workplace import register_workplace_tools

logger = get_logger(__name__)

app = FastMCP("clappia-mcp-server")

def register_all_tools():
    """Register all tools"""
    register_submission_tools(app)
    register_definition_tools(app)
    register_workflow_tools(app)
    register_analytics_tools(app)
    register_workplace_tools(app)
    logger.info("All Clappia MCP tools registered successfully")

def main():
    try:
        register_all_tools()
        logger.info("Starting Clappia MCP server")
        logger.info("CLAPPIA_API_KEY must be set as environment variable")
        app.run(transport='stdio')
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
        tools = app._tool_manager._tools if hasattr(app, '_tool_manager') and hasattr(app._tool_manager, '_tools') else {}
        print(f"\n=== Clappia MCP Tools ({len(tools)}) ===")
        for tool_name in tools.keys():
            print(f"• {tool_name}")
    except Exception as e:
        print(f"Error listing tools: {e}")

if __name__ == "__main__":
    args = sys.argv[1:]
    
    if "--list-tools" in args:
        list_tools()
    elif "--help" in args or "-h" in args:
        print("""
        Clappia MCP Server
        
        Usage:
            python server.py                # Run server (default)
            python server.py --list-tools   # List all tools
            python server.py --help         # Show help
        
        Required Environment Variables:
            CLAPPIA_API_KEY
        """)
    else:
        main()