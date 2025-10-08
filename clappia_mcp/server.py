from mcp.server.fastmcp import FastMCP, Context
from smithery.decorators import smithery
from pydantic import BaseModel, Field

from utils.logging_utils import get_logger
from tools.submissions import register_submission_tools
from tools.definitions import register_definition_tools
from tools.workflows import register_workflow_tools
from tools.analytics import register_analytics_tools
from tools.workplace import register_workplace_tools

logger = get_logger(__name__)


class ConfigSchema(BaseModel):
    """Configuration schema for Clappia MCP server"""
    modules: list[str] = Field(
        default=["all"], 
        description="List of modules to load (submissions, definitions, workflows, analytics, workplace, or all)"
    )
    api_key: str = Field(
        description="Clappia API key for authentication"
    )


@smithery.server(config_schema=ConfigSchema)
def create_server():
    """Create and return a FastMCP server instance with session config."""
    
    server = FastMCP(name="Clappia MCP Server")
    
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
                register_func(server)
                logger.info(f"Registered {module_name} tools")
            except Exception as e:
                logger.error(f"Failed to register {module_name} tools: {str(e)}")

        logger.info("All Clappia MCP tools registered successfully")

    def register_specific_tools(modules):
        """Register tools from specific modules only"""
        for module in modules:
            if module in AVAILABLE_MODULES:
                try:
                    AVAILABLE_MODULES[module](server)
                    logger.info(f"Registered {module} tools")
                except Exception as e:
                    logger.error(f"Failed to register {module} tools: {str(e)}")
            else:
                logger.warning(f"Unknown module: {module}")

        logger.info(f"Registered tools from modules: {', '.join(modules)}")

    # Add a tool to configure which modules to load
    @server.tool()
    def configure_modules(modules: list[str], ctx: Context) -> str:
        """Configure which modules to load for this session"""
        session_config = ctx.session_config
        
        # Update the modules in session config
        session_config.modules = modules
        
        # Re-register tools based on new configuration
        if "all" in modules:
            register_all_tools()
        else:
            register_specific_tools(modules)
        
        return f"Configured modules: {', '.join(modules)}"

    @server.tool()
    def list_available_modules(ctx: Context) -> str:
        """List all available modules"""
        return "Available modules: submissions, definitions, workflows, analytics, workplace, all"

    # Register tools based on initial configuration
    # This will be called when the server starts
    def initialize_tools():
        session_config = getattr(server, '_session_config', None)
        if session_config and hasattr(session_config, 'modules'):
            modules = session_config.modules
        else:
            modules = ["all"]  # Default to all modules
        
        if "all" in modules:
            register_all_tools()
        else:
            register_specific_tools(modules)

    # Initialize tools
    initialize_tools()

    return server
