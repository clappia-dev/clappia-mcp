import sys
from mcp.server.fastmcp import FastMCP
from src.utils.logging_utils import get_logger
from src.tools.workflows import register_workflow_tools

logger = get_logger(__name__)

app = FastMCP("clappia-app-workflow")


def register_all_tools():
    """Register all workflow-related tools"""
    register_workflow_tools(app)


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
