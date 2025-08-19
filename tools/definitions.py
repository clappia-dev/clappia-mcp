"""
definitions.py - Clappia MCP App Definitions Module using Modern Pydantic Approach
Handles all app definition and field management operations with clean Pydantic models
"""

from mcp.server.fastmcp import FastMCP
from utils import get_logger, app_definition_client
from clappia_api_tools.models import GetAppDefinitionRequest, CreateAppRequest, AddFieldRequest, UpdateFieldRequest, AppDefinitionResponse, AppCreationResponse, FieldOperationResponse
logger = get_logger(__name__)

def register_definition_tools(mcp: FastMCP):
    
    @mcp.tool()
    async def get_clappia_app_definition(request: GetAppDefinitionRequest) -> AppDefinitionResponse:
        """
        Fetches complete definition of a Clappia application including forms, fields, sections, and metadata.
        
        Retrieves structure and configuration of a Clappia app to understand available fields,
        validation rules, and workflow logic before creating charts, filtering submissions, or planning integrations.
        """
        try:
            return app_definition_client.get_definition(
                app_id=request.app_id,
                language=request.language,
                strip_html=request.strip_html,
                include_tags=request.include_tags
            )
                
        except Exception as e:
            logger.error(f"Error in get_clappia_app_definition: {str(e)}")
            return AppDefinitionResponse(
                success=False,
                message=f"Error retrieving app definition: {str(e)}",
                app_id=request.app_id
            )

    @mcp.tool()
    async def create_clappia_app(request: CreateAppRequest) -> AppCreationResponse:
        """
        Create a new Clappia app with specified sections and fields.
        """
        try:
            sections_data = [section.model_dump() for section in request.sections]
            
            return app_definition_client.create_app(
                app_name=request.app_name,
                requesting_user_email_address=str(request.requesting_user_email_address),
                sections=sections_data
            )
                
        except Exception as e:
            logger.error(f"Error in create_clappia_app: {str(e)}")
            return AppCreationResponse(
                success=False,
                message=f"Error creating app: {str(e)}",
                app_name=request.app_name
            )

    @mcp.tool()
    async def add_field_to_clappia_app(request: AddFieldRequest) -> FieldOperationResponse:
        """
        Add a new field to an existing Clappia application at a specific position.
        
        Supports 21 different field types including text, selectors, files, GPS, calculations, and more.
        """
        try:
            return app_definition_client.add_field(
                app_id=request.app_id,
                requesting_user_email_address=str(request.requesting_user_email_address),
                section_index=request.section_index,
                field_index=request.field_index,
                field_type=request.field_type,
                label=request.label,
                description=request.description,
                required=request.required,
                block_width_percentage_desktop=request.block_width_percentage_desktop,
                block_width_percentage_mobile=request.block_width_percentage_mobile,
                display_condition=request.display_condition,
                retain_values=request.retain_values,
                is_editable=request.is_editable,
                editability_condition=request.editability_condition,
                validation=request.validation,
                default_value=request.default_value,
                options=request.options,
                style=request.style,
                number_of_cols=request.number_of_cols,
                allowed_file_types=request.allowed_file_types,
                max_file_allowed=request.max_file_allowed,
                image_quality=request.image_quality,
                image_text=request.image_text,
                file_name_prefix=request.file_name_prefix,
                formula=request.formula,
                hidden=request.hidden
            )
          
        except Exception as e:
            logger.error(f"Error in add_field_to_clappia_app: {str(e)}")
            return FieldOperationResponse(
                success=False,
                message=f"Error adding field: {str(e)}",
                app_id=request.app_id,
                field_name=request.label,
                operation="add_field"
            )

    @mcp.tool()
    async def update_field_in_clappia_app(request: UpdateFieldRequest) -> FieldOperationResponse:
        """
        Updates an existing field in a Clappia application with new configuration.
        
        Modifies the properties of an existing field, enabling dynamic form updates,
        A/B testing, and iterative improvements without recreating the entire app.
        """
        try:
            return app_definition_client.update_field(
                app_id=request.app_id,
                requesting_user_email_address=str(request.requesting_user_email_address),
                field_name=request.field_name,
                label=request.label,
                description=request.description,
                required=request.required,
                block_width_percentage_desktop=request.block_width_percentage_desktop,
                block_width_percentage_mobile=request.block_width_percentage_mobile,
                display_condition=request.display_condition,
                retain_values=request.retain_values,
                is_editable=request.is_editable,
                editability_condition=request.editability_condition,
                validation=request.validation,
                default_value=request.default_value,
                options=request.options,
                style=request.style,
                number_of_cols=request.number_of_cols,
                allowed_file_types=request.allowed_file_types,
                max_file_allowed=request.max_file_allowed,
                image_quality=request.image_quality,
                image_text=request.image_text,
                file_name_prefix=request.file_name_prefix,
                formula=request.formula,
                hidden=request.hidden
            )
                
        except Exception as e:
            logger.error(f"Error in update_field_in_clappia_app: {str(e)}")
            return FieldOperationResponse(
                success=False,
                message=f"Error updating field: {str(e)}",
                app_id=request.app_id,
                field_name=request.field_name,
                operation="update_field"
            )