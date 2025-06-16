import requests
import json
import os
import re
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

@dataclass
class AddFieldRequest:
    app_id: str
    workplace_id: str
    requesting_user_email_address: str
    section_index: int
    field_index: int
    field_type: str
    label: str
    description: Optional[str] = None
    required: bool = False
    block_width_percentage_desktop: int = 100
    block_width_percentage_mobile: int = 100
    display_condition: Optional[str] = None
    retain_values: bool = False
    is_editable: bool = True
    editability_condition: Optional[str] = None
    validation: str = "none"
    default_value: Optional[str] = None
    options: Optional[List[str]] = None
    style: str = "Standard"
    number_of_cols: Optional[int] = None
    allowed_file_types: Optional[List[str]] = None
    max_file_allowed: int = 1
    image_quality: str = "medium"
    image_text: Optional[str] = None
    file_name_prefix: Optional[str] = None
    formula: Optional[str] = None
    hidden: Optional[bool] = None

class ClappiaAddFieldValidator:
    
    VALID_FIELD_TYPES = {
        "singleLineText", "multiLineText", "singleSelector", "multiSelector",
        "dropDown", "dateSelector", "timeSelector", "phoneNumber", "uniqueNumbering",
        "file", "gpsLocation", "html", "calculationsAndLogic", "codeScanner",
        "counter", "slider", "signature", "validation", "liveTracking", "nfcReader",
        "address"
    }
    
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
    def validate_field_type(field_type: str) -> tuple[bool, str]:
        if field_type not in ClappiaAddFieldValidator.VALID_FIELD_TYPES:
            return False, f"Invalid fieldType '{field_type}'. Valid types: {', '.join(ClappiaAddFieldValidator.VALID_FIELD_TYPES)}"
        
        return True, ""
    
    @staticmethod
    def validate_label(label: str) -> tuple[bool, str]:
        if not label or not label.strip():
            return False, "Field label is required and cannot be empty"
        
        return True, ""
    
    @staticmethod
    def validate_indices(section_index: int, field_index: int) -> tuple[bool, str]:
        if section_index < 0:
            return False, "Section index must be >= 0"
        
        if field_index < 0:
            return False, "Field index must be >= 0"
        
        return True, ""
    
    @staticmethod
    def validate_field_specific_options(field_type: str, options: Optional[List[str]], 
                                      formula: Optional[str]) -> tuple[bool, str]:
        # Selector fields require options
        if field_type in ["singleSelector", "multiSelector", "dropDown"]:
            if not options or len(options) == 0:
                return False, f"Field type '{field_type}' requires non-empty options list"
        
        # Formula fields require formula
        if field_type == "calculationsAndLogic":
            if not formula or not formula.strip():
                return False, "Field type 'calculationsAndLogic' requires a formula"
        
        return True, ""

class ClappiaAddFieldClient:
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
                    return f"Field added successfully:\nField Name: {field_name}\nFull Response: {json.dumps(response_data, indent=2)}"
                else:
                    # If it's not a dict (maybe a string or other type), just return it
                    return f"Field added successfully: {json.dumps(response_data, indent=2)}"
            except json.JSONDecodeError:
                return f"Field added successfully: {response.text}"
        
        elif response.status_code in [400, 401, 403, 404]:
            try:
                error_data = response.json()
                return f"API Error ({response.status_code}): {json.dumps(error_data, indent=2)}"
            except json.JSONDecodeError:
                return f"API Error ({response.status_code}): {response.text}"
        
        else:
            return f"Unexpected API response ({response.status_code}): {response.text}"
    
    def _build_payload(self, request: AddFieldRequest) -> dict:
        """Build the API payload from the request object"""
        payload = {
            "appId": request.app_id.strip(),
            "workplaceId": request.workplace_id.strip(),
            "requestingUserEmailAddress": request.requesting_user_email_address.strip(),
            "sectionIndex": request.section_index,
            "fieldIndex": request.field_index,
            "fieldType": request.field_type,
            "label": request.label.strip(),
            "required": request.required,
            "blockWidthPercentageDesktop": request.block_width_percentage_desktop,
            "blockWidthPercentageMobile": request.block_width_percentage_mobile,
            "retainValues": request.retain_values,
            "isEditable": request.is_editable,
            "validation": request.validation,
        }

        if request.hidden is not None:
            payload["hidden"] = request.hidden
        
        if request.description:
            payload["description"] = request.description.strip()
        
        if request.display_condition:
            payload["displayCondition"] = request.display_condition.strip()
        
        if request.editability_condition:
            payload["editabilityCondition"] = request.editability_condition.strip()
        
        if request.default_value:
            payload["defaultValue"] = request.default_value.strip()
        
        if request.options:
            payload["options"] = request.options
        
        if request.field_type in ["singleSelector", "multiSelector"]:
            payload["style"] = request.style
            if request.number_of_cols:
                payload["numberOfCols"] = request.number_of_cols
        
        if request.field_type == "file":
            if request.allowed_file_types:
                payload["allowedFileTypes"] = request.allowed_file_types
            payload["maxFileAllowed"] = request.max_file_allowed
            payload["imageQuality"] = request.image_quality
            if request.image_text:
                payload["imageText"] = request.image_text.strip()
            if request.file_name_prefix:
                payload["fileNamePrefix"] = request.file_name_prefix.strip()
        
        if request.field_type == "calculationsAndLogic" and request.formula:
            payload["formula"] = request.formula.strip()
        
        return payload
    
    def add_field(self, app_id: str, workplace_id: str, requesting_user_email_address: str,
                  section_index: int, field_index: int, field_type: str, label: str,
                  **kwargs) -> str:
        
        # Validate required parameters
        is_valid, error_msg = ClappiaAddFieldValidator.validate_app_id(app_id)
        if not is_valid:
            return f"Error: Invalid app_id - {error_msg}"
        
        is_valid, error_msg = ClappiaAddFieldValidator.validate_workplace_id(workplace_id)
        if not is_valid:
            return f"Error: Invalid workplace_id - {error_msg}"
        
        is_valid, error_msg = ClappiaAddFieldValidator.validate_email(requesting_user_email_address)
        if not is_valid:
            return f"Error: Invalid email - {error_msg}"
        
        is_valid, error_msg = ClappiaAddFieldValidator.validate_field_type(field_type)
        if not is_valid:
            return f"Error: Invalid field_type - {error_msg}"
        
        is_valid, error_msg = ClappiaAddFieldValidator.validate_label(label)
        if not is_valid:
            return f"Error: Invalid label - {error_msg}"
        
        is_valid, error_msg = ClappiaAddFieldValidator.validate_indices(section_index, field_index)
        if not is_valid:
            return f"Error: Invalid indices - {error_msg}"
        
        # Check field-specific requirements
        options = kwargs.get('options')
        formula = kwargs.get('formula')
        is_valid, error_msg = ClappiaAddFieldValidator.validate_field_specific_options(
            field_type, options, formula)
        if not is_valid:
            return f"Error: Field validation failed - {error_msg}"
        
        env_valid, env_error = self._validate_environment()
        if not env_valid:
            return f"Error: {env_error}"
        
        try:
            # Create request object
            request = AddFieldRequest(
                app_id=app_id,
                workplace_id=workplace_id,
                requesting_user_email_address=requesting_user_email_address,
                section_index=section_index,
                field_index=field_index,
                field_type=field_type,
                label=label,
                **kwargs
            )
            
            url = f"{self.base_url}/appdefinitionv2/addField"
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

def add_field_to_app(app_id: str, workplace_id: str, requesting_user_email_address: str,
                     section_index: int, field_index: int, field_type: str, label: str,
                     **kwargs) -> str:
    """
    Add a new field to an existing Clappia application at a specific position.

    **Purpose**: Dynamically extend existing Clappia apps by inserting new fields at precise locations within sections, enabling iterative form development and customization.

    **Parameters**:
    - `app_id`: Unique app identifier (e.g., "MFX093412"). Must be uppercase letters and numbers.
    - `workplace_id`: Workplace identifier (e.g., "DEV161318"). Must be uppercase letters and numbers.
    - `requesting_user_email_address`: Email address of the user adding the field (must have app edit permissions).
    - `section_index`: Index of the section to add the field to (starts from 0).
    - `field_index`: Position within the section where the field should be inserted (starts from 0).
    - `field_type`: Type of field to add (e.g., "singleLineText", "singleSelector", "dateSelector", "file", "calculationsAndLogic").
    - `label`: Display label for the field (required, non-empty).

    **Optional Parameters**:
    - `description`: Field description/help text.
    - `required`: Whether the field is mandatory (default: False).
    - `block_width_percentage_desktop`: Width percentage on desktop (default: 100).
    - `block_width_percentage_mobile`: Width percentage on mobile (default: 100).
    - `display_condition`: Condition for when to show the field.
    - `retain_values`: Whether to retain values when field is hidden (default: False).
    - `is_editable`: Whether the field can be edited (default: True).
    - `editability_condition`: Condition for when field is editable.
    - `validation`: Validation type - "none", "number", "email", "url", "custom" (default: "none").
    - `default_value`: Default value for the field.
    - `options`: List of options for selector fields (required for singleSelector, multiSelector, dropDown).
    - `style`: Style for selector fields - "Standard" or "Chips" (default: "Standard").
    - `number_of_cols`: Number of columns for selector fields.
    - `allowed_file_types`: List of allowed file types for file fields (e.g., ["images_camera_upload", "documents"]).
    - `max_file_allowed`: Maximum files allowed (1-10, default: 1).
    - `image_quality`: Image quality for file fields - "low", "medium", "high" (default: "medium").
    - `image_text`: Text overlay for image fields.
    - `file_name_prefix`: Prefix for uploaded file names.
    - `formula`: Formula for calculation fields (required for calculationsAndLogic).
    - `hidden`: Whether the field is hidden (default: False).

    **Field Types and Requirements**:
    - **Text Fields**: singleLineText, multiLineText (no special requirements)
    - **Selector Fields**: singleSelector, multiSelector, dropDown (require `options` list)
    - **Date/Time**: dateSelector, timeSelector (no special requirements)
    - **File Upload**: file (can specify `allowed_file_types`, `max_file_allowed`, etc.)
    - **Calculation**: calculationsAndLogic (requires `formula`)
    - **Location**: gpsLocation (no special requirements)
    - **Advanced**: signature, codeScanner, nfcReader, etc.

    **Returns**: Success message with generated field name, or error message if the request fails.

    **Usage Examples**:
    1. **Add Text Field**:
       ```python
       add_field_to_app("APP123", "WS456", "user@company.com", 0, 2, 
                       "singleLineText", "Employee ID", required=True)
       ```

    2. **Add Dropdown with Options**:
       ```python
       add_field_to_app("APP123", "WS456", "user@company.com", 1, 0,
                       "dropDown", "Department", 
                       options=["HR", "IT", "Finance", "Marketing"], required=True)
       ```

    3. **Add File Upload**:
       ```python
       add_field_to_app("APP123", "WS456", "user@company.com", 0, 1,
                       "file", "Resume Upload",
                       allowed_file_types=["documents"], max_file_allowed=1)
       ```

    4. **Add Calculation Field**:
       ```python
       add_field_to_app("APP123", "WS456", "user@company.com", 2, 0,
                       "calculationsAndLogic", "Total Amount",
                       formula="quantity * price", hidden=False)
       ```

    **Notes**:
    - Requires DEV_API_KEY and CLAPPIA_EXTERNAL_API_BASE_URL environment variables.
    - User must have edit permissions on the target app.
    - Section and field indices start from 0.
    - Field is inserted at the specified position, shifting existing fields down.
    - Validates all inputs and field-specific requirements.
    - Returns auto-generated field name for use in submissions and API calls.
    """
    client = ClappiaAddFieldClient()
    return client.add_field(app_id, workplace_id, requesting_user_email_address,
                           section_index, field_index, field_type, label, **kwargs)