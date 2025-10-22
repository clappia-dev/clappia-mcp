import sys
from mcp.server.fastmcp import FastMCP
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
if __name__ == "__main__":
    main()
