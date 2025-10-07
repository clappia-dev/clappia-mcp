#!/usr/bin/env python3
"""
Clappia MCP Server - Cloud Run Version
This is a dedicated server for Google Cloud Run deployment using streamable-http transport.
"""

import asyncio
import os
import sys
import logging
from mcp.server.fastmcp import FastMCP
from utils.logging_utils import get_logger
from tools.submissions import register_submission_tools
from tools.definitions import register_definition_tools
from tools.workflows import register_workflow_tools
from tools.analytics import register_analytics_tools
from tools.workplace import register_workplace_tools

# Configure logging for Cloud Run
logging.basicConfig(
    format="[%(levelname)s]: %(message)s",
    level=logging.INFO,
    stream=sys.stdout
)
logger = get_logger(__name__)

# Initialize FastMCP app
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


async def main():
    """Main function to run the Cloud Run server"""
    try:
        # Check for required environment variables
        if not os.getenv("CLAPPIA_API_KEY"):
            logger.error("CLAPPIA_API_KEY environment variable is required")
            sys.exit(1)

        # Register all tools
        register_all_tools()

        # Get configuration from environment
        host = os.getenv("HOST", "0.0.0.0")
        port = int(os.getenv("PORT", 8080))
        transport = os.getenv("TRANSPORT", "streamable-http")

        logger.info("Starting Clappia MCP server on Cloud Run")
        logger.info(f"Transport: {transport}")
        logger.info(f"Host: {host}")
        logger.info(f"Port: {port}")
        logger.info("CLAPPIA_API_KEY is set")

        # Run the server
        await app.run_async(
            transport=transport,
            host=host,
            port=port,
        )

    except KeyboardInterrupt:
        logger.info("Server shutdown requested by user")
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        sys.exit(1)
    finally:
        logger.info("MCP server shutdown complete")


if __name__ == "__main__":
    asyncio.run(main())
