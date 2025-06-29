from mcp.server.fastmcp import FastMCP
import logging
import sys
import os
import re
from datetime import datetime
from typing import Dict, Any, Optional, List
from tools.get_submissions_aggregation import get_app_submissions_aggregation
from tools.get_submissions import get_app_submissions
from utils.constants import CLAPPIA_EXTERNAL_API_BASE_URL
from clappia_tools import SubmissionClient, AppManagementClient, AppDefinitionClient

def setup_logging():
    """Configure file-only logging to avoid JSON-RPC interference."""
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_filename = f'{log_dir}/mcp_logs_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.FileHandler(log_filename)]
    )
    return logging.getLogger('clappia-mcp')

def get_submission_client():
    return SubmissionClient(
        api_key=os.getenv("CLAPPIA_API_KEY"),
        base_url=CLAPPIA_EXTERNAL_API_BASE_URL,
        workplace_id=os.getenv("CLAPPIA_WORKPLACE_ID")
    )

def get_app_definition_client():
    return AppDefinitionClient(
        api_key=os.getenv("CLAPPIA_API_KEY"),
        base_url=CLAPPIA_EXTERNAL_API_BASE_URL      ,
        workplace_id=os.getenv("CLAPPIA_WORKPLACE_ID")
    )
    
def get_app_management_client():
    return AppManagementClient(
        api_key=os.getenv("CLAPPIA_API_KEY"),
        base_url=CLAPPIA_EXTERNAL_API_BASE_URL,
        workplace_id=os.getenv("CLAPPIA_WORKPLACE_ID")
    )


logger = setup_logging()

mcp = FastMCP()

def validate_required_params(email: str) -> tuple[bool, str]:
    """
    Validate required email parameter.
    
    Args:
        email: Email address to validate
        
    Returns:
        tuple[bool, str]: (is_valid, error_message)
    """
    if not email or not email.strip():
        return False, "Email address is required. Please provide a valid email address."
    
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email.strip()):
        return False, "Invalid email format. Please provide a valid email address."
    
    return True, ""

@mcp.tool()
def get_clappia_submissions(app_id: str, 
                           requesting_user_email_address: str,
                           page_size: int = 10, filters: Optional[dict] = None) -> str:
    """
    Retrieve Clappia form submissions with optional filtering.

    Required Parameters:
        requesting_user_email_address (str): Email address of the requesting user. Must be a valid email format.
        app_id (str): Application identifier (e.g., "ODT537440"). Must be uppercase letters and numbers.

    Optional Parameters:
        page_size (int): Number of results to retrieve (1-1000, default: 10).
        filters (dict): Filter conditions.

    Returns:
        str: JSON string with submission records and metadata, or error message if the request fails.

    Notes:
        - Requires CLAPPIA_API_KEY and CLAPPIA_WORKPLACE_ID environment variables.
    """
    # Validate required parameters
    is_valid, error_msg = validate_required_params(requesting_user_email_address)
    if not is_valid:
        return f"Error: {error_msg}"
    
    logger.info(f"Getting submissions for app: {app_id}")
    return get_app_submissions(app_id, requesting_user_email_address, page_size, filters)

@mcp.tool()
def get_clappia_submissions_aggregation(app_id: str, requesting_user_email_address: str,
                                      dimensions: Optional[List[dict]] = None, 
                                      aggregation_dimensions: Optional[List[dict]] = None,
                                      x_axis_labels: Optional[List[str]] = None,
                                      forward: bool = True,
                                      page_size: int = 1000,
                                      filters: Optional[dict] = None) -> str:
    """
    Aggregate Clappia submission data for analytics.

    Required Parameters:
        requesting_user_email_address (str): Email address of the requesting user. Must be a valid email format.
        app_id (str): Application ID (e.g., "ODT537440"). Must be uppercase letters and numbers.

    Optional Parameters:
        dimensions (List[dict]): Fields to group by.
        aggregation_dimensions (List[dict]): Calculations.
        x_axis_labels (List[str]): Output column labels.
        forward (bool): Pagination direction.
        page_size (int): Max results (1-1000).
        filters (dict): Filter conditions.

    Returns:
        str: JSON string with tabular data or error message.

    Notes:
        - Requires CLAPPIA_API_KEY and CLAPPIA_WORKPLACE_ID environment variables.
    """
    # Validate required parameters
    is_valid, error_msg = validate_required_params(requesting_user_email_address)
    if not is_valid:
        return f"Error: {error_msg}"
    
    logger.info(f"Getting submissions aggregation for app: {app_id}")
    return get_app_submissions_aggregation(
        app_id=app_id,
        dimensions=dimensions or [],
        aggregation_dimensions=aggregation_dimensions or [],
        x_axis_labels=x_axis_labels or [],
        requesting_user_email_address=requesting_user_email_address,
        forward=forward,
        page_size=page_size,
        filters=filters
    )

@mcp.tool()
def get_clappia_app_definition(app_id: str,
                              requesting_user_email_address: str,
                              language: str = "en", strip_html: bool = True,
                              include_tags: bool = True) -> str:
    
    
    client = get_app_definition_client()
    return client.get_definition(app_id, language, strip_html, include_tags)


@mcp.tool()
def create_clappia_app_submission(app_id: str, data: Dict[str, Any], 
                                 requesting_user_email_address: str) -> str:
   
    client = get_submission_client()
    return client.create_submission(app_id, data, requesting_user_email_address)

@mcp.tool()
def edit_clappia_submission(app_id: str, submission_id: str, 
                           data: Dict[str, Any], requesting_user_email_address: str) -> str:
    
    client = get_submission_client()
    return client.edit_submission(app_id, submission_id, data, requesting_user_email_address)

@mcp.tool()
def update_clappia_submission_status(app_id: str, submission_id: str, 
                                   status_name: str, requesting_user_email_address: str, 
                                   comments: Optional[str] = None) -> str:

    client = get_submission_client()
    return client.update_status(app_id,submission_id,requesting_user_email_address,status_name,comments)

@mcp.tool()
def update_clappia_submission_owners(app_id: str, submission_id: str, 
                                   email_ids: List[str], requesting_user_email_address: str) -> str:

    client = get_submission_client()
    return client.update_owners(app_id, submission_id, requesting_user_email_address,email_ids)

@mcp.tool()
def create_clappia_app(app_name: str, requesting_user_email_address: str, 
                      sections: List[Dict[str, Any]]) -> str:
    client = get_app_management_client()
    return client.create_app(app_name, requesting_user_email_address, sections)

@mcp.tool()
def add_field_to_clappia_app(app_id: str, requesting_user_email_address: str, section_index: int, field_index: int, field_type: str, label: Optional[str] = None,
                            description: Optional[str] = None,
                            required: Optional[bool] = None,
                            block_width_percentage_desktop: Optional[int] = None,
                            block_width_percentage_mobile: Optional[int] = None,
                            display_condition: Optional[str] = None,
                            retain_values: Optional[bool] = None,
                            is_editable: Optional[bool] = None,
                            editability_condition: Optional[str] = None,
                            validation: Optional[str] = None,
                            default_value: Optional[str] = None,
                            options: Optional[List[str]] = None,
                            style: Optional[str] = None,
                            number_of_cols: Optional[int] = None,
                            allowed_file_types: Optional[List[str]] = None,
                            max_file_allowed: Optional[int] = None,
                            image_quality: Optional[str] = None,
                            image_text: Optional[str] = None,
                            file_name_prefix: Optional[str] = None,
                            formula: Optional[str] = None,
                            hidden: Optional[bool] = None) -> str:
    client = get_app_management_client()
    return client.add_field(app_id=app_id, requesting_user_email_address=requesting_user_email_address, section_index=section_index, field_index=field_index, field_type=field_type, label=label,
                            description=description, required=required, block_width_percentage_desktop=block_width_percentage_desktop, block_width_percentage_mobile=block_width_percentage_mobile,
                            display_condition=display_condition, retain_values=retain_values, is_editable=is_editable, editability_condition=editability_condition, validation=validation,
                            default_value=default_value, options=options, style=style, number_of_cols=number_of_cols, allowed_file_types=allowed_file_types, max_file_allowed=max_file_allowed,
                            image_quality=image_quality, image_text=image_text, file_name_prefix=file_name_prefix, formula=formula, hidden=hidden)

@mcp.tool()
def update_field_in_clappia_app(app_id: str, requesting_user_email_address: str,
                               field_name: str,
                               label: Optional[str] = None,
                               description: Optional[str] = None,
                               required: Optional[bool] = None,
                               block_width_percentage_desktop: Optional[int] = None,
                               block_width_percentage_mobile: Optional[int] = None,
                               display_condition: Optional[str] = None,
                               retain_values: Optional[bool] = None,
                               is_editable: Optional[bool] = None,
                               editability_condition: Optional[str] = None,
                               validation: Optional[str] = None,
                               default_value: Optional[str] = None,
                               options: Optional[List[str]] = None,
                               style: Optional[str] = None,
                               number_of_cols: Optional[int] = None,
                               allowed_file_types: Optional[List[str]] = None,
                               max_file_allowed: Optional[int] = None,
                               image_quality: Optional[str] = None,
                               image_text: Optional[str] = None,
                               file_name_prefix: Optional[str] = None,
                               formula: Optional[str] = None,
                               hidden: Optional[bool] = None) -> str:
    client = get_app_management_client()
    return client.update_field(app_id=app_id, requesting_user_email_address=requesting_user_email_address, field_name=field_name, label=label,
                               description=description, required=required, block_width_percentage_desktop=block_width_percentage_desktop, block_width_percentage_mobile=block_width_percentage_mobile,
                               display_condition=display_condition, retain_values=retain_values, is_editable=is_editable, editability_condition=editability_condition, validation=validation,
                               default_value=default_value, options=options, style=style, number_of_cols=number_of_cols, allowed_file_types=allowed_file_types, max_file_allowed=max_file_allowed,
                               image_quality=image_quality, image_text=image_text, file_name_prefix=file_name_prefix, formula=formula, hidden=hidden)

def main():
    """Start Clappia MCP server with error handling."""
    try:
        logger.info("Starting Clappia MCP server")
        logger.info("IMPORTANT: All tools require requesting_user_email_address to be explicitly provided")
        logger.info("Do not use default values for this parameter")
        logger.info("requesting_user_email_address must be a valid email format")
        logger.info("CLAPPIA_API_KEY and CLAPPIA_WORKPLACE_ID must be set as environment variables")
        mcp.run(transport='stdio')
    except KeyboardInterrupt:
        logger.info("Server shutdown requested by user")
    except Exception as e:
        logger.error(f"Server startup failed: {str(e)}")
        sys.exit(1)
    finally:
        logger.info("MCP server shutdown complete")

if __name__ == "__main__":
    main()