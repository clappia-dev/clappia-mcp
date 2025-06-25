from mcp.server.fastmcp import FastMCP
import logging
import sys
import os
import re
from datetime import datetime
from typing import Dict, Any, Optional, List
from tools.get_submissions import get_app_submissions
from tools.get_submissions_aggregation import get_app_submissions_aggregation
from clappia_tools import ClappiaClient
from tools.create_app import create_app
from tools.add_field import add_field_to_app
from tools.update_field import update_field_in_app
from tools.create_app import Field, Section

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
    """
    Fetch Clappia app structure and field definitions.

    Required Parameters:
        requesting_user_email_address (str): Email address of the requesting user. Must be a valid email format.
        app_id (str): Application ID (e.g., "ODT537440"). Must be uppercase letters and numbers.

    Optional Parameters:
        language (str): Language code for translations.
        strip_html (bool): Remove HTML from text fields.
        include_tags (bool): Include metadata tags.

    Returns:
        JSON string with app metadata, fields, and structure or error message.

    Notes:
        - Requires CLAPPIA_API_KEY and CLAPPIA_WORKPLACE_ID environment variables.
    """
    # Validate required parameters
    is_valid, error_msg = validate_required_params(requesting_user_email_address)
    if not is_valid:
        return f"Error: {error_msg}"
    
    logger.info(f"Getting app definition for app: {app_id}")    
    client = get_clappia_client()
    return client.get_app_definition(app_id, language, strip_html, include_tags)

@mcp.tool()
def create_clappia_app_submission(app_id: str, data: Dict[str, Any], 
                                 requesting_user_email_address: str) -> str:
    """
    Create a new submission in a Clappia application.

    Required Parameters:
        requesting_user_email_address (str): Email address of the requesting user. Must be a valid email format.
        app_id (str): Application ID (e.g., "MFX093412"). Must be uppercase letters and numbers.
        data (Dict[str, Any]): Dictionary of field key-value pairs to submit.

    Returns:
        Success message with submission details or error message if the request fails.

    Notes:
        - Requires CLAPPIA_API_KEY and CLAPPIA_WORKPLACE_ID environment variables.
    """
    # Validate required parameters
    is_valid, error_msg = validate_required_params(requesting_user_email_address)
    if not is_valid:
        return f"Error: {error_msg}"
    
    logger.info(f"Creating submission for app: {app_id}, user: {requesting_user_email_address}")
    logger.info(f"Data fields: {list(data.keys()) if data else 'None'}")

    client = get_clappia_client()
    result = client.create_submission(app_id, data, requesting_user_email_address)
    
    logger.info(f"Submission creation result: {'Success' if 'successfully' in result.lower() else 'Failed'}")
    return result

@mcp.tool()
def edit_clappia_submission(app_id: str, submission_id: str, 
                           data: Dict[str, Any], requesting_user_email_address: str) -> str:
    """
    Edit an existing submission in a Clappia application.

    Required Parameters:
        requesting_user_email_address (str): Email address of the requesting user. Must be a valid email format.
        app_id (str): Application ID (e.g., "MFX093412"). Must be uppercase letters and numbers.
        submission_id (str): ID of the submission to be edited.
        data (Dict[str, Any]): Dictionary of field key-value pairs to update.

    Returns:
        Success message with updated submission details or error message if the request fails.

    Notes:
        - Requires CLAPPIA_API_KEY and CLAPPIA_WORKPLACE_ID environment variables.
    """
    # Validate required parameters
    is_valid, error_msg = validate_required_params(requesting_user_email_address)
    if not is_valid:
        return f"Error: {error_msg}"
    
    logger.info(f"Editing submission {submission_id} for app: {app_id}, user: {requesting_user_email_address}")
    logger.info(f"Data fields to update: {list(data.keys()) if data else 'None'}")
    
    client = get_clappia_client()
    result = client.edit_submission(app_id, submission_id, data, requesting_user_email_address)
    
    logger.info(f"Submission edit result: {'Success' if 'successfully' in result.lower() else 'Failed'}")
    return result

@mcp.tool()
def update_clappia_submission_status(app_id: str, submission_id: str, 
                                   status_name: str, requesting_user_email_address: str, 
                                   comments: Optional[str] = None) -> str:
    """
    Update the status of an existing submission in a Clappia application.

    Required Parameters:
        requesting_user_email_address (str): Email address of the requesting user. Must be a valid email format.
        app_id (str): Application ID (e.g., "MFX093412"). Must be uppercase letters and numbers.
        submission_id (str): ID of the submission to update status.
        status_name (str): New status name (e.g., "Approved", "Rejected", "In Progress").

    Optional Parameters:
        comments (str): Optional comments explaining the status change.

    Returns:
        Success message with updated status details or error message if the request fails.

    Notes:
        - Requires CLAPPIA_API_KEY and CLAPPIA_WORKPLACE_ID environment variables.
    """
    # Validate required parameters
    is_valid, error_msg = validate_required_params(requesting_user_email_address)
    if not is_valid:
        return f"Error: {error_msg}"
    
    logger.info(f"Updating status for submission {submission_id} to '{status_name}' for app: {app_id}, user: {requesting_user_email_address}")
    if comments:
        logger.info(f"Status update comments: {comments[:100]}{'...' if len(comments) > 100 else ''}")
    
    client = get_clappia_client()   

    result = client.update_submission_status(app_id,submission_id,requesting_user_email_address,status_name,comments)
    
    logger.info(f"Status update result: {'Success' if 'successfully' in result.lower() else 'Failed'}")
    return result

@mcp.tool()
def update_clappia_submission_owners(app_id: str, submission_id: str, 
                                   email_ids: List[str], requesting_user_email_address: str) -> str:
    """
    Update the owners of an existing submission in a Clappia application.

    Required Parameters:
        requesting_user_email_address (str): Email address of the requesting user. Must be a valid email format.
        app_id (str): Application ID (e.g., "MFX093412"). Must be uppercase letters and numbers.
        submission_id (str): ID of the submission to update owners.
        email_ids (List[str]): List of email addresses to set as new owners.

    Returns:
        Success message with updated ownership details or error message if the request fails.

    Notes:
        - Requires CLAPPIA_API_KEY and CLAPPIA_WORKPLACE_ID environment variables.
    """
    # Validate required parameters
    is_valid, error_msg = validate_required_params(requesting_user_email_address)
    if not is_valid:
        return f"Error: {error_msg}"
    
    logger.info(f"Updating owners for submission {submission_id} for app: {app_id}, user: {requesting_user_email_address}")
    logger.info(f"New owners: {email_ids}")
    
    client = get_clappia_client()
    result = client.update_submission_owners(app_id, submission_id, requesting_user_email_address,email_ids)
    logger.info(f"Owners update result: {'Success' if 'successfully' in result.lower() else 'Failed'}")
    return result

@mcp.tool()
def create_clappia_app(app_name: str, requesting_user_email_address: str, 
                      sections: List[Dict[str, Any]]) -> str:
    """
    Create a new Clappia application with specified sections and fields.

    Required Parameters:
        requesting_user_email_address (str): Email address of the requesting user. Must be a valid email format.
        app_name (str): Name of the new application (e.g., "Employee Survey"). Minimum 3 characters.
        sections (List[Dict[str, Any]]): List of section dictionaries that define the app's structure.

    Returns:
        Success message with app ID and URL or error message if the request fails.

    Notes:
        - Requires CLAPPIA_API_KEY and CLAPPIA_WORKPLACE_ID environment variables.
    """
    # Validate required parameters
    is_valid, error_msg = validate_required_params(requesting_user_email_address)
    if not is_valid:
        return f"Error: {error_msg}"
    
    logger.info(f"Creating app '{app_name}' for user: {requesting_user_email_address}")
    logger.info(f"Sections count: {len(sections) if sections else 0}")
    
    try:
        section_objects = []
        for section_dict in sections:
            fields = []
            for field_dict in section_dict.get("fields", []):
                field = Field(
                    fieldType=field_dict["fieldType"],
                    label=field_dict["label"],
                    options=field_dict.get("options")
                )
                fields.append(field)
            
            section = Section(
                sectionName=section_dict["sectionName"],
                fields=fields
            )
            section_objects.append(section)
        
        result = create_app(app_name, requesting_user_email_address, section_objects)
        
    except Exception as e:
        result = f"Error converting sections: {str(e)}"
    
    logger.info(f"App creation result: {'Success' if 'successfully' in result.lower() else 'Failed'}")
    return result

@mcp.tool()
def add_field_to_clappia_app(app_id: str, requesting_user_email_address: str,
                            section_index: int, field_index: int, field_type: str, label: str,
                            description: Optional[str] = None,
                            required: bool = False,
                            block_width_percentage_desktop: int = 100,
                            block_width_percentage_mobile: int = 100,
                            display_condition: Optional[str] = None,
                            retain_values: bool = False,
                            is_editable: bool = True,
                            editability_condition: Optional[str] = None,
                            validation: str = "none",
                            default_value: Optional[str] = None,
                            options: Optional[List[str]] = None,
                            style: str = "Standard",
                            number_of_cols: Optional[int] = None,
                            allowed_file_types: Optional[List[str]] = None,
                            max_file_allowed: int = 1,
                            image_quality: str = "medium",
                            image_text: Optional[str] = None,
                            file_name_prefix: Optional[str] = None,
                            formula: Optional[str] = None,
                            hidden: Optional[bool] = None) -> str:
    """
    Add a new field to an existing Clappia application at a specific position.

    Required Parameters:
        requesting_user_email_address (str): Email address of the requesting user. Must be a valid email format.
        app_id (str): Application ID (e.g., "MFX093412"). Must be uppercase letters and numbers.
        section_index (int): Index of the section to add the field to (starts from 0).
        field_index (int): Position within the section for the new field (starts from 0).
        field_type (str): Type of field ("singleLineText", "singleSelector", "dateSelector", "file", etc.).
        label (str): Display label for the field.

    Optional Parameters:
        description (str): Optional field description/help text.
        required (bool): Whether the field is mandatory.
        block_width_percentage_desktop (int): Width percentage on desktop. Allowed values are (25, 50, 75, 100).
        block_width_percentage_mobile (int): Width percentage on mobile. Allowed values are (50, 100).
        display_condition (str): Condition for when to show the field.
        retain_values (bool): Whether to retain values when field is hidden.
        is_editable (bool): Whether the field can be edited.
        editability_condition (str): Condition for when field is editable.
        validation (str): Validation type - "none", "number", "email", "url", "custom".
        default_value (str): Default value for the field.
        options (List[str]): List of options for selector fields.
        style (str): Style for selector fields - "Standard" or "Chips".
        number_of_cols (int): Number of columns for selector fields.
        allowed_file_types (List[str]): List of allowed file types for file fields.
        max_file_allowed (int): Maximum files allowed (1-10).
        image_quality (str): Image quality for file fields - "low", "medium", "high".
        image_text (str): Text overlay for image fields.
        file_name_prefix (str): Prefix for uploaded file names.
        formula (str): Formula for calculation fields.
        hidden (bool): Whether the field is hidden.

    Returns:
        Success message with generated field name or error message if the request fails.

    Notes:
        - Requires CLAPPIA_API_KEY and CLAPPIA_WORKPLACE_ID environment variables.
    """
    # Validate required parameters
    is_valid, error_msg = validate_required_params(requesting_user_email_address)
    if not is_valid:
        return f"Error: {error_msg}"
    
    logger.info(f"Adding field '{label}' of type '{field_type}' to app: {app_id}, section: {section_index}, position: {field_index}")
    
    kwargs = {}
    if description is not None:
        kwargs['description'] = description
    if required is not False:
        kwargs['required'] = required
    if block_width_percentage_desktop != 100:
        kwargs['block_width_percentage_desktop'] = block_width_percentage_desktop
    if block_width_percentage_mobile != 100:
        kwargs['block_width_percentage_mobile'] = block_width_percentage_mobile
    if display_condition is not None:
        kwargs['display_condition'] = display_condition
    if retain_values is not False:
        kwargs['retain_values'] = retain_values
    if is_editable is not True:
        kwargs['is_editable'] = is_editable
    if editability_condition is not None:
        kwargs['editability_condition'] = editability_condition
    if validation != "none":
        kwargs['validation'] = validation
    if default_value is not None:
        kwargs['default_value'] = default_value
    if options is not None:
        kwargs['options'] = options
    if style != "Standard":
        kwargs['style'] = style
    if number_of_cols is not None:
        kwargs['number_of_cols'] = number_of_cols
    if allowed_file_types is not None:
        kwargs['allowed_file_types'] = allowed_file_types
    if max_file_allowed != 1:
        kwargs['max_file_allowed'] = max_file_allowed
    if image_quality != "medium":
        kwargs['image_quality'] = image_quality
    if image_text is not None:
        kwargs['image_text'] = image_text
    if file_name_prefix is not None:
        kwargs['file_name_prefix'] = file_name_prefix
    if formula is not None:
        kwargs['formula'] = formula
    if hidden is not None:
        kwargs['hidden'] = hidden
    
    result = add_field_to_app(
        app_id=app_id,
        requesting_user_email_address=requesting_user_email_address,
        section_index=section_index,
        field_index=field_index,
        field_type=field_type,
        label=label,
        **kwargs
    )
    
    logger.info(f"Add field result: {'Success' if 'successfully' in result.lower() else 'Failed'}")
    return result

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
    """
    Update an existing field in a Clappia application with new configuration.

    Required Parameters:
        requesting_user_email_address (str): Email address of the requesting user. Must be a valid email format.
        app_id (str): Application ID (e.g., "MFX093412"). Must be uppercase letters and numbers.
        field_name (str): Variable name of the existing field to update.

    Optional Parameters:
        label (str): New display label for the field.
        description (str): New field description/help text.
        required (bool): Whether the field is mandatory.
        block_width_percentage_desktop (int): Width percentage on desktop. Allowed values are (25, 50, 75, 100).
        block_width_percentage_mobile (int): Width percentage on mobile. Allowed values are (50, 100).
        display_condition (str): Condition for when to show the field.
        retain_values (bool): Whether to retain values when field is hidden.
        is_editable (bool): Whether the field can be edited.
        editability_condition (str): Condition for when field is editable.
        validation (str): Validation type - "none", "number", "email", "url", "custom".
        default_value (str): Default value for the field.
        options (List[str]): List of options for selector fields.
        style (str): Style for selector fields - "Standard" or "Chips".
        number_of_cols (int): Number of columns for selector fields.
        allowed_file_types (List[str]): List of allowed file types for file fields.
        max_file_allowed (int): Maximum files allowed (1-10).
        image_quality (str): Image quality for file fields - "low", "medium", "high".
        image_text (str): Text overlay for image fields.
        file_name_prefix (str): Prefix for uploaded file names.
        formula (str): Formula for calculation fields.
        hidden (bool): Whether the field is hidden.

    Returns:
        Success message with field name confirmation or error message if the request fails.

    Notes:
        - Requires CLAPPIA_API_KEY and CLAPPIA_WORKPLACE_ID environment variables.
    """
    # Validate required parameters
    is_valid, error_msg = validate_required_params(requesting_user_email_address)
    if not is_valid:
        return f"Error: {error_msg}"
    
    logger.info(f"Updating field '{field_name}' in app: {app_id}, user: {requesting_user_email_address}")
    
    kwargs = {}
    if label is not None:
        kwargs['label'] = label
    if description is not None:
        kwargs['description'] = description
    if required is not None:
        kwargs['required'] = required
    if block_width_percentage_desktop is not None:
        kwargs['block_width_percentage_desktop'] = block_width_percentage_desktop
    if block_width_percentage_mobile is not None:
        kwargs['block_width_percentage_mobile'] = block_width_percentage_mobile
    if display_condition is not None:
        kwargs['display_condition'] = display_condition
    if retain_values is not None:
        kwargs['retain_values'] = retain_values
    if is_editable is not None:
        kwargs['is_editable'] = is_editable
    if editability_condition is not None:
        kwargs['editability_condition'] = editability_condition
    if validation is not None:
        kwargs['validation'] = validation
    if default_value is not None:
        kwargs['default_value'] = default_value
    if options is not None:
        kwargs['options'] = options
    if style is not None:
        kwargs['style'] = style
    if number_of_cols is not None:
        kwargs['number_of_cols'] = number_of_cols
    if allowed_file_types is not None:
        kwargs['allowed_file_types'] = allowed_file_types
    if max_file_allowed is not None:
        kwargs['max_file_allowed'] = max_file_allowed
    if image_quality is not None:
        kwargs['image_quality'] = image_quality
    if image_text is not None:
        kwargs['image_text'] = image_text
    if file_name_prefix is not None:
        kwargs['file_name_prefix'] = file_name_prefix
    if formula is not None:
        kwargs['formula'] = formula
    if hidden is not None:
        kwargs['hidden'] = hidden
    
    update_properties = list(kwargs.keys())
    logger.info(f"Updating properties: {update_properties}")
    
    result = update_field_in_app(
        app_id=app_id,
        requesting_user_email_address=requesting_user_email_address,
        field_name=field_name,
        **kwargs
    )
    
    logger.info(f"Update field result: {'Success' if 'successfully' in result.lower() else 'Failed'}")
    return result

def get_clappia_client():
    return ClappiaClient(
        api_key=os.getenv("CLAPPIA_API_KEY"),
        base_url=os.getenv("CLAPPIA_BASE_URL"),
        workplace_id=os.getenv("CLAPPIA_WORKPLACE_ID")
    )

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