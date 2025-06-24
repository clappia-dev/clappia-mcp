import requests
import json
import os
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from dotenv import load_dotenv
from .constants import CLAPPIA_EXTERNAL_API_BASE_URL

load_dotenv()

@dataclass
class Field:
    fieldType: str
    label: str
    options: Optional[List[str]] = None
    required: bool = False
    
    def to_dict(self) -> dict:
        result = {
            "fieldType": self.fieldType,
            "label": self.label,
            "required": self.required
        }
        if self.options:
            result["options"] = self.options
        return result

@dataclass
class Section:
    sectionName: str
    fields: List[Field]
    
    def to_dict(self) -> dict:
        return {
            "sectionName": self.sectionName,
            "fields": [field.to_dict() for field in self.fields]
        }

@dataclass
class CreateAppRequest:
    app_name: str
    requesting_user_email_address: str
    sections: List[Section]

class ClappiaCreateAppValidator:
    
    VALID_FIELD_TYPES = {
        "singleLineText", "multiLineText", "singleSelector", "multiSelector",
        "dropDown", "dateSelector", "timeSelector", "phoneNumber"
    }
    
    @staticmethod
    def validate_app_name(app_name: str) -> tuple[bool, str]:
        if not app_name or not app_name.strip():
            return False, "App name is required and cannot be empty"
        
        if len(app_name.strip()) < 3:
            return False, "App name must be at least 3 characters long"
        
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
    def validate_sections(sections: List[Section]) -> tuple[bool, str]:
        if not sections:
            return False, "At least one section is required"
        
        for i, section in enumerate(sections):
            if not section.sectionName or not section.sectionName.strip():
                return False, f"Section at index {i} must have a non-empty sectionName"
            
            if not section.fields:
                return False, f"Section '{section.sectionName}' must have at least one field"
            
            for j, field in enumerate(section.fields):
                if field.fieldType not in ClappiaCreateAppValidator.VALID_FIELD_TYPES:
                    return False, f"Invalid fieldType '{field.fieldType}' in field at index {j}"
                
                if not field.label or not field.label.strip():
                    return False, f"Field at index {j} in section '{section.sectionName}' must have a non-empty label"
                
                if field.fieldType in ["singleSelector", "multiSelector", "dropDown"]:
                    if not field.options or len(field.options) == 0:
                        return False, f"Field '{field.label}' with type '{field.fieldType}' must have options"
        
        return True, ""

class ClappiaCreateAppClient:
    def __init__(self):
        self.api_key = os.environ.get("CLAPPIA_API_KEY")
        self.workplace_id = os.environ.get("CLAPPIA_WORKPLACE_ID")
        self.timeout = 30
    
    def _validate_environment(self) -> tuple[bool, str]:
        if not self.api_key:
            return False, "CLAPPIA_API_KEY environment variable is not set"
        if not self.workplace_id:
            return False, "CLAPPIA_WORKPLACE_ID environment variable is not set"
        return True, ""
    
    def _get_headers(self) -> dict:
        return {
            "x-api-key": self.api_key,
            "workplaceId": self.workplace_id,
            "Content-Type": "application/json"
        }
    
    def _handle_response(self, response: requests.Response) -> str:
        if response.status_code == 200:
            try:
                response_data = response.json()
                return f"App created successfully:\nApp ID: {response_data.get('appId')}\nApp URL: {response_data.get('appUrl')}\nFull Response: {json.dumps(response_data, indent=2)}"
            except json.JSONDecodeError:
                return f"App created successfully: {response.text}"
        
        elif response.status_code in [400, 401, 403, 404]:
            try:
                error_data = response.json()
                return f"API Error ({response.status_code}): {json.dumps(error_data, indent=2)}"
            except json.JSONDecodeError:
                return f"API Error ({response.status_code}): {response.text}"
        
        else:
            return f"Unexpected API response ({response.status_code}): {response.text}"
    
    def create_app(self, app_name: str, requesting_user_email_address: str, 
                  sections: List[Section]) -> str:
        
        is_valid, error_msg = ClappiaCreateAppValidator.validate_app_name(app_name)
        if not is_valid:
            return f"Error: Invalid app_name - {error_msg}"
        
        is_valid, error_msg = ClappiaCreateAppValidator.validate_email(requesting_user_email_address)
        if not is_valid:
            return f"Error: Invalid email - {error_msg}"
        
        is_valid, error_msg = ClappiaCreateAppValidator.validate_sections(sections)
        if not is_valid:
            return f"Error: Invalid sections - {error_msg}"
        
        env_valid, env_error = self._validate_environment()
        if not env_valid:
            return f"Error: {env_error}"
        
        try:
            url = f"{CLAPPIA_EXTERNAL_API_BASE_URL}/appdefinitionv2/createApp"
            headers = self._get_headers()
            
            payload = {
                "appName": app_name.strip(),
                "requestingUserEmailAddress": requesting_user_email_address.strip(),
                "sections": [section.to_dict() for section in sections]
            }

            
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

def create_app(app_name: str, requesting_user_email_address: str, 
                      sections: List[Section]) -> str:
    """
    Create a new Clappia application with specified sections and fields.

    **Purpose**: Build a new Clappia application from scratch with custom form structure, field types, and sections for business process automation.

    **Parameters**:
    - `app_name`: Name of the new application (e.g., "Employee Survey", "Inventory Management"). Minimum 3 characters.
    - `requesting_user_email_address`: Email address of the user creating the app (becomes the app owner).
    - `sections`: List of Section objects defining the app structure. Each section contains fields with specific types and properties.

    **Section Structure Example**:
    sections = [
        Section(
            sectionName="Personal Information",
            fields=[
                Field(
                    fieldType="singleLineText",
                    label="Full Name",
                    required=True
                ),
                Field(
                    fieldType="singleSelector",
                    label="Gender",
                    options=["Male", "Female", "Other"],
                    required=True
                ),
                Field(
                    fieldType="dateSelector",
                    label="Date of Birth"
                )
            ]
        ),
        Section(
            sectionName="Work Details",
            fields=[
                Field(
                    fieldType="singleLineText",
                    label="Department",
                    required=True
                ),
                Field(
                    fieldType="multiSelector",
                    label="Skills",
                    options=["Python", "Java", "JavaScript", "SQL"]
                ),
                Field(
                    fieldType="phoneNumber",
                    label="Work Phone"
                )
            ]
        )
    ]

    **Field Types and Properties**:
    - **Text Fields**:
        - `singleLineText`: Single line text input (e.g., name, title)
        - `multiLineText`: Multi-line text area (e.g., description, notes)
    - **Selection Fields**:
        - `singleSelector`: Radio buttons for single choice
        - `multiSelector`: Checkboxes for multiple choices
        - `dropDown`: Dropdown menu for single choice
    - **Date/Time Fields**:
        - `dateSelector`: Date picker
        - `timeSelector`: Time picker
    - **Contact Fields**:
        - `phoneNumber`: Formatted phone number input

    **Field Properties**:
    - `fieldType`: Type of input field (required)
    - `label`: Display name of the field (required)
    - `options`: List of choices for selector fields (required for singleSelector, multiSelector, dropDown)
    - `required`: Whether the field is mandatory (default: False)

    **Returns**: Success message with app ID and URL, or error message if the request fails.

    **Usage Examples**:
    1. **Employee Onboarding Form**:
       ```python
       sections = [
           Section("Personal Info", [
               Field("singleLineText", "Full Name", required=True),
               Field("singleSelector", "Employment Type", 
                     options=["Full-time", "Part-time", "Contract"])
           ]),
           Section("Documents", [
               Field("multiLineText", "Additional Notes"),
               Field("dateSelector", "Joining Date", required=True)
           ])
       ]
       ```

    2. **Inventory Management**:
       ```python
       sections = [
           Section("Item Details", [
               Field("singleLineText", "Item Name", required=True),
               Field("singleLineText", "SKU", required=True),
               Field("singleSelector", "Category", 
                     options=["Electronics", "Furniture", "Office Supplies"])
           ]),
           Section("Stock Information", [
               Field("singleLineText", "Quantity"),
               Field("singleSelector", "Unit", 
                     options=["Pieces", "Boxes", "Kg"])
           ])
       ]
       ```

    **Notes**:
    - Requires CLAPPIA_API_KEY and CLAPPIA_EXTERNAL_API_BASE_URL environment variables.
    - App name must be at least 3 characters long and unique within the workplace.
    - Each section must have at least one field.
    - Selection fields require a non-empty options array.
    - Field labels must be non-empty strings.
    - Returns app ID and URL for immediate access to the created application.
    """
    client = ClappiaCreateAppClient()
    return client.create_app(app_name, requesting_user_email_address, sections)