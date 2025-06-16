import requests
import json
import os
import re
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

@dataclass
class UpdateFieldRequest:
    app_id: str
    workplace_id: str
    requesting_user_email_address: str
    field_name: str
    label: Optional[str] = None
    description: Optional[str] = None
    required: Optional[bool] = None
    block_width_percentage_desktop: Optional[int] = None
    block_width_percentage_mobile: Optional[int] = None
    display_condition: Optional[str] = None
    retain_values: Optional[bool] = None
    is_editable: Optional[bool] = None
    editability_condition: Optional[str] = None
    validation: Optional[str] = None
    default_value: Optional[str] = None
    options: Optional[List[str]] = None
    style: Optional[str] = None
    number_of_cols: Optional[int] = None
    allowed_file_types: Optional[List[str]] = None
    max_file_allowed: Optional[int] = None
    image_quality: Optional[str] = None
    image_text: Optional[str] = None
    file_name_prefix: Optional[str] = None
    formula: Optional[str] = None
    hidden: Optional[bool] = None

class ClappiaUpdateFieldValidator:
    
    VALID_VALIDATIONS = {"none", "number", "email", "url", "custom"}
    VALID_STYLES = {"Standard", "Chips"}
    VALID_IMAGE_QUALITIES = {"low", "medium", "high"}
    VALID_FILE_TYPES = {
        "images_camera_upload", "images_gallery_upload", "videos", "documents"
    }
    
    @staticmethod
    def validate_app_id(app_id: str) -> tuple[bool, str]:
        if not app_id or not app_id.strip():
            return False, "App ID is required and cannot be empty"
        
        if not re.match(r'^[A-Z0-9]+$', app_id.strip()):
            return False, "App ID must contain only uppercase letters and numbers"
        
        return True, ""
    
    @staticmethod
    def validate_workplace_id(workplace_id: str) -> tuple[bool, str]:
        if not workplace_id or not workplace_id.strip():
            return False, "Workplace ID is required and cannot be empty"
        
        if not re.match(r'^[A-Z0-9]+$', workplace_id.strip()):
            return False, "Workplace ID must contain only uppercase letters and numbers"
        
        return True, ""
    
    @staticmethod
    def validate_email(email: str) -> tuple[bool, str]:
        if not email or not email.strip():
            return False, "Email is required and cannot be empty"
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email.strip()):
            return False, "Invalid email format"
        
        return True, ""
    
    @staticmethod
    def validate_field_name(field_name: str) -> tuple[bool, str]:
        if not field_name or not field_name.strip():
            return False, "Field name is required and cannot be empty"
        
        return True, ""
    
    @staticmethod
    def validate_validation_type(validation: Optional[str]) -> tuple[bool, str]:
        if validation and validation not in ClappiaUpdateFieldValidator.VALID_VALIDATIONS:
            return False, f"Invalid validation type '{validation}'. Valid types: {', '.join(ClappiaUpdateFieldValidator.VALID_VALIDATIONS)}"
        
        return True, ""
    
    @staticmethod
    def validate_style(style: Optional[str]) -> tuple[bool, str]:
        if style and style not in ClappiaUpdateFieldValidator.VALID_STYLES:
            return False, f"Invalid style '{style}'. Valid styles: {', '.join(ClappiaUpdateFieldValidator.VALID_STYLES)}"
        
        return True, ""
    
    @staticmethod
    def validate_image_quality(image_quality: Optional[str]) -> tuple[bool, str]:
        if image_quality and image_quality not in ClappiaUpdateFieldValidator.VALID_IMAGE_QUALITIES:
            return False, f"Invalid image quality '{image_quality}'. Valid qualities: {', '.join(ClappiaUpdateFieldValidator.VALID_IMAGE_QUALITIES)}"
        
        return True, ""
    
    @staticmethod
    def validate_file_types(file_types: Optional[List[str]]) -> tuple[bool, str]:
        if file_types:
            for file_type in file_types:
                if file_type not in ClappiaUpdateFieldValidator.VALID_FILE_TYPES:
                    return False, f"Invalid file type '{file_type}'. Valid types: {', '.join(ClappiaUpdateFieldValidator.VALID_FILE_TYPES)}"
        
        return True, ""
    
    @staticmethod
    def validate_max_file_allowed(max_files: Optional[int]) -> tuple[bool, str]:
        if max_files is not None and (max_files < 1 or max_files > 10):
            return False, "Max file allowed must be between 1 and 10"
        
        return True, ""

class ClappiaUpdateFieldClient:
    def __init__(self):
        self.api_key = os.environ.get("DEV_API_KEY")
        self.base_url = os.environ.get('CLAPPIA_EXTERNAL_API_BASE_URL')
        self.timeout = 30
    
    def _validate_environment(self) -> tuple[bool, str]:
        if not self.api_key:
            return False, "DEV_API_KEY environment variable is not set"
        if not self.base_url:
            return False, "CLAPPIA_EXTERNAL_API_BASE_URL environment variable is not set"
        return True, ""
    
    def _get_headers(self, workplace_id: str) -> dict:
        return {
            "x-api-key": self.api_key,
            "workplaceId": workplace_id,
            "Content-Type": "application/json"
        }
    
    def _handle_response(self, response: requests.Response) -> str:
        if response.status_code == 200:
            try:
                response_data = response.json()
                # Check if response_data is a dict before calling .get()
                if isinstance(response_data, dict):
                    field_name = response_data.get('fieldName', 'Unknown')
                    return f"Field updated successfully:\nField Name: {field_name}\nFull Response: {json.dumps(response_data, indent=2)}"
                else:
                    # If it's not a dict (maybe a string or other type), just return it
                    return f"Field updated successfully: {json.dumps(response_data, indent=2)}"
            except json.JSONDecodeError:
                return f"Field updated successfully: {response.text}"
        
        elif response.status_code in [400, 401, 403, 404]:
            try:
                error_data = response.json()
                return f"API Error ({response.status_code}): {json.dumps(error_data, indent=2)}"
            except json.JSONDecodeError:
                return f"API Error ({response.status_code}): {response.text}"
        
        else:
            return f"Unexpected API response ({response.status_code}): {response.text}"
    
    def _build_payload(self, request: UpdateFieldRequest) -> dict:
        """Build the API payload from the request object, only including non-None values"""
        payload = {
            "appId": request.app_id.strip(),
            "workplaceId": request.workplace_id.strip(),
            "requestingUserEmailAddress": request.requesting_user_email_address.strip(),
            "fieldName": request.field_name.strip()
        }
        
        # Add optional fields only if they have values (not None)
        if request.label is not None:
            payload["label"] = request.label.strip()
        
        if request.description is not None:
            payload["description"] = request.description.strip()
        
        if request.required is not None:
            payload["required"] = request.required
        
        if request.block_width_percentage_desktop is not None:
            payload["blockWidthPercentageDesktop"] = request.block_width_percentage_desktop
        
        if request.block_width_percentage_mobile is not None:
            payload["blockWidthPercentageMobile"] = request.block_width_percentage_mobile
        
        if request.display_condition is not None:
            payload["displayCondition"] = request.display_condition.strip()
        
        if request.retain_values is not None:
            payload["retainValues"] = request.retain_values
        
        if request.is_editable is not None:
            payload["isEditable"] = request.is_editable
        
        if request.editability_condition is not None:
            payload["editabilityCondition"] = request.editability_condition.strip()
        
        if request.validation is not None:
            payload["validation"] = request.validation
        
        if request.default_value is not None:
            payload["defaultValue"] = request.default_value.strip()
        
        if request.options is not None:
            payload["options"] = request.options
        
        if request.style is not None:
            payload["style"] = request.style
        
        if request.number_of_cols is not None:
            payload["numberOfCols"] = request.number_of_cols
        
        if request.allowed_file_types is not None:
            payload["allowedFileTypes"] = request.allowed_file_types
        
        if request.max_file_allowed is not None:
            payload["maxFileAllowed"] = request.max_file_allowed
        
        if request.image_quality is not None:
            payload["imageQuality"] = request.image_quality
        
        if request.image_text is not None:
            payload["imageText"] = request.image_text.strip()
        
        if request.file_name_prefix is not None:
            payload["fileNamePrefix"] = request.file_name_prefix.strip()
        
        if request.formula is not None:
            payload["formula"] = request.formula.strip()
        
        if request.hidden is not None:
            payload["hidden"] = request.hidden
        
        return payload
    
    def update_field(self, app_id: str, workplace_id: str, requesting_user_email_address: str,
                     field_name: str, **kwargs) -> str:
        
        # Validate required parameters
        is_valid, error_msg = ClappiaUpdateFieldValidator.validate_app_id(app_id)
        if not is_valid:
            return f"Error: Invalid app_id - {error_msg}"
        
        is_valid, error_msg = ClappiaUpdateFieldValidator.validate_workplace_id(workplace_id)
        if not is_valid:
            return f"Error: Invalid workplace_id - {error_msg}"
        
        is_valid, error_msg = ClappiaUpdateFieldValidator.validate_email(requesting_user_email_address)
        if not is_valid:
            return f"Error: Invalid email - {error_msg}"
        
        is_valid, error_msg = ClappiaUpdateFieldValidator.validate_field_name(field_name)
        if not is_valid:
            return f"Error: Invalid field_name - {error_msg}"
        
        # Validate optional parameters
        validation = kwargs.get('validation')
        is_valid, error_msg = ClappiaUpdateFieldValidator.validate_validation_type(validation)
        if not is_valid:
            return f"Error: {error_msg}"
        
        style = kwargs.get('style')
        is_valid, error_msg = ClappiaUpdateFieldValidator.validate_style(style)
        if not is_valid:
            return f"Error: {error_msg}"
        
        image_quality = kwargs.get('image_quality')
        is_valid, error_msg = ClappiaUpdateFieldValidator.validate_image_quality(image_quality)
        if not is_valid:
            return f"Error: {error_msg}"
        
        file_types = kwargs.get('allowed_file_types')
        is_valid, error_msg = ClappiaUpdateFieldValidator.validate_file_types(file_types)
        if not is_valid:
            return f"Error: {error_msg}"
        
        max_files = kwargs.get('max_file_allowed')
        is_valid, error_msg = ClappiaUpdateFieldValidator.validate_max_file_allowed(max_files)
        if not is_valid:
            return f"Error: {error_msg}"
        
        env_valid, env_error = self._validate_environment()
        if not env_valid:
            return f"Error: {env_error}"
        
        try:
            # Create request object
            request = UpdateFieldRequest(
                app_id=app_id,
                workplace_id=workplace_id,
                requesting_user_email_address=requesting_user_email_address,
                field_name=field_name,
                **kwargs
            )
            
            url = f"{self.base_url}/appdefinitionv2/updateField"
            headers = self._get_headers(workplace_id)
            payload = self._build_payload(request)
            
            response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=self.timeout)
            return self._handle_response(response)
            
        except requests.exceptions.Timeout:
            return "Error: Request timeout - API took too long to respond"
        
        except requests.exceptions.ConnectionError:
            return "Error: Connection error - Could not reach the Clappia API"
        
        except requests.exceptions.RequestException as e:
            return f"Error: Request failed - {str(e)}"
        
        except Exception as e:
            return f"Error: An internal error occurred - {str(e)}"

def update_field_in_app(app_id: str, workplace_id: str, requesting_user_email_address: str,
                        field_name: str, **kwargs) -> str:
    """
    Update an existing field in a Clappia application with new configuration.

    **Purpose**: Modify the properties of an existing field in a Clappia app, enabling dynamic form updates, A/B testing, and iterative improvements without recreating the entire app.

    **Parameters**:
    - `app_id`: Unique app identifier (e.g., "MFX093412"). Must be uppercase letters and numbers.
    - `workplace_id`: Workplace identifier (e.g., "DEV161318"). Must be uppercase letters and numbers.
    - `requesting_user_email_address`: Email address of the user updating the field (must have app edit permissions).
    - `field_name`: Variable name of the existing field to update (e.g., "employeeName", "department").

    **Optional Parameters (only specify what you want to change)**:
    - `label`: New display label for the field.
    - `description`: New field description/help text.
    - `required`: Whether the field is mandatory (True/False).
    - `block_width_percentage_desktop`: Width percentage on desktop (1-100).
    - `block_width_percentage_mobile`: Width percentage on mobile (1-100).
    - `display_condition`: Condition for when to show the field.
    - `retain_values`: Whether to retain values when field is hidden (True/False).
    - `is_editable`: Whether the field can be edited (True/False).
    - `editability_condition`: Condition for when field is editable.
    - `validation`: Validation type - "none", "number", "email", "url", "custom".
    - `default_value`: Default value for the field (for singleLineText fields).
    - `options`: List of options for selector fields (for singleSelector, multiSelector, dropDown).
    - `style`: Style for selector fields - "Standard" or "Chips".
    - `number_of_cols`: Number of columns for selector fields.
    - `allowed_file_types`: List of allowed file types for file fields (e.g., ["images_camera_upload", "documents"]).
    - `max_file_allowed`: Maximum files allowed (1-10).
    - `image_quality`: Image quality for file fields - "low", "medium", "high".
    - `image_text`: Text overlay for image fields.
    - `file_name_prefix`: Prefix for uploaded file names.
    - `formula`: Formula for calculation fields.
    - `hidden`: Whether the field is hidden (True/False).

    **Returns**: Success message with field name confirmation, or error message if the request fails.

    **Usage Examples**:
    1. **Update Field Label and Make Required**:
       ```python
       update_field_in_app("APP123", "WS456", "user@company.com", 
                          "employeeName", label="Full Employee Name", required=True)
       ```

    2. **Update Dropdown Options**:
       ```python
       update_field_in_app("APP123", "WS456", "user@company.com",
                          "department", 
                          options=["HR", "IT", "Finance", "Marketing", "Operations"])
       ```

    3. **Change Validation and Add Description**:
       ```python
       update_field_in_app("APP123", "WS456", "user@company.com",
                          "emailField", 
                          validation="email", 
                          description="Enter your corporate email address")
       ```

    4. **Update File Upload Settings**:
       ```python
       update_field_in_app("APP123", "WS456", "user@company.com",
                          "documentUpload",
                          allowed_file_types=["documents", "images_gallery_upload"],
                          max_file_allowed=3,
                          file_name_prefix="DOC_")
       ```

    5. **Update Layout and Conditional Logic**:
       ```python
       update_field_in_app("APP123", "WS456", "user@company.com",
                          "additionalInfo",
                          block_width_percentage_desktop=50,
                          display_condition="department == 'IT'",
                          is_editable=False)
       ```

    6. **Update Calculation Formula**:
       ```python
       update_field_in_app("APP123", "WS456", "user@company.com",
                          "totalCost",
                          formula="(base_price + tax_amount) * quantity",
                          hidden=False)
       ```  

    **Key Benefits**:
    - **Incremental Updates**: Change only specific properties without affecting others.
    - **A/B Testing**: Modify field labels, validations, or options for testing.
    - **Dynamic Forms**: Update forms based on user feedback or business requirements.
    - **Workflow Optimization**: Adjust field visibility and editability conditions.

    **Notes**:
    - Requires DEV_API_KEY and CLAPPIA_EXTERNAL_API_BASE_URL environment variables.
    - User must have edit permissions on the target app.
    - Only specify parameters you want to change; omitted parameters remain unchanged.
    - Field name must match an existing field's variable name in the app.
    - Validates all inputs and field-specific requirements.
    - Use `get_app_definition()` to find existing field names before updating.
    """
    client = ClappiaUpdateFieldClient()
    return client.update_field(app_id, workplace_id, requesting_user_email_address,
                              field_name, **kwargs)