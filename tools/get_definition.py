import requests
import json
import os
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

from dotenv import load_dotenv

load_dotenv()

class LanguageCode(Enum):
    ENGLISH = "en"
    SPANISH = "es"
    FRENCH = "fr"
    GERMAN = "de"

class FieldType(Enum):
    SINGLE_LINE_TEXT = "singleLineText"
    MULTI_LINE_TEXT = "multiLineText"
    RICH_TEXT_EDITOR = "miniRichTextEditor"
    NUMBER_INPUT = "numberInput"
    SINGLE_SELECTOR = "singleSelector"
    MULTI_SELECTOR = "multiSelector"
    DATE_TIME = "dateTime"
    FILE_UPLOAD = "fileUpload"
    LOCATION = "location"
    SIGNATURE = "signature"
    CAMERA = "camera"
    BARCODE_SCANNER = "barcodeScanner"
    NFC_READER = "nfcReader"
    BUTTON = "button"
    CALCULATIONS = "calculations"
    NESTED_FORM = "nestedForm"

@dataclass
class AppDefinitionRequest:
    app_id: str
    workplace_id: str
    language: str = "en"
    strip_html: bool = True
    include_tags: bool = True
    
    def to_query_params(self) -> dict:
        return {
            "appId": self.app_id,
            "workplaceId": self.workplace_id,
            "language": self.language,
            "stripHtml": str(self.strip_html).lower(),
            "includeTags": str(self.include_tags).lower()
        }

class ClappiaAppDefinitionValidator:
    VALID_LANGUAGES = {lang.value for lang in LanguageCode}
    
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
    def validate_language(language: str) -> tuple[bool, str]:
        if language not in ClappiaAppDefinitionValidator.VALID_LANGUAGES:
            return False, f"Language must be one of: {', '.join(ClappiaAppDefinitionValidator.VALID_LANGUAGES)}"
        
        return True, ""

class ClappiaAppDefinitionClient:
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
    
    
    def _get_headers(self) -> dict:
        return {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }
    
    def _handle_response(self, response: requests.Response) -> str:
        if response.status_code == 200:
            try:
                response_data = response.json()
                
                app_info = {
                    "appId": response_data.get("appId"),
                    "version": response_data.get("version"),
                    "state": response_data.get("state"),
                    "pageCount": len(response_data.get("pageIds", [])),
                    "sectionCount": len(response_data.get("sectionIds", [])),
                    "fieldCount": len(response_data.get("fieldDefinitions", {})),
                    "appName": response_data.get("metadata", {}).get("sectionName", "Unknown"),
                    "description": response_data.get("metadata", {}).get("description", "")
                }
                
                return f"Successfully retrieved app definition:\n\nSUMMARY:\n{json.dumps(app_info, indent=2)}\n\nFULL DEFINITION:\n{json.dumps(response_data, indent=2)}"
            except json.JSONDecodeError:
                return f"Success but invalid JSON response: {response.text}"
        
        elif response.status_code in [400, 401, 403, 404]:
            try:
                error_data = response.json()
                return f"API Error ({response.status_code}): {json.dumps(error_data, indent=2)}"
            except json.JSONDecodeError:
                return f"API Error ({response.status_code}): {response.text}"
        
        else:
            return f"Unexpected API response ({response.status_code}): {response.text}"
    
    def get_app_definition(self, app_id: str, workplace_id: str, requesting_user_email_address: str,
                          language: str = "en", strip_html: bool = True,
                          include_tags: bool = True) -> str:
        
        is_valid, error_msg = ClappiaAppDefinitionValidator.validate_app_id(app_id)
        if not is_valid:
            return f"Error: Invalid app_id - {error_msg}"
        
        is_valid, error_msg = ClappiaAppDefinitionValidator.validate_workplace_id(workplace_id)
        if not is_valid:
            return f"Error: Invalid workplace_id - {error_msg}"
        
        is_valid, error_msg = ClappiaAppDefinitionValidator.validate_language(language)
        if not is_valid:
            return f"Error: Invalid language - {error_msg}"
        
        env_valid, env_error = self._validate_environment()
        if not env_valid:
            return f"Error: {env_error}"
        
        try:
            url = f"{self.base_url}/appdefinition-external/getAppDefinition"
            headers = self._get_headers()
            
            params = {
                "appId": app_id.strip(),
                "workplaceId": workplace_id.strip(),
                "requestingUserEmailAddress": requesting_user_email_address,
                "language": language,
                "stripHtml": str(strip_html).lower(),
                "includeTags": str(include_tags).lower()
            }

            
            response = requests.get(url, headers=headers, params=params, timeout=self.timeout)
            return self._handle_response(response)
            
        except requests.exceptions.Timeout:
            return "Error: Request timeout - API took too long to respond"
        
        except requests.exceptions.ConnectionError:
            return "Error: Connection error - Could not reach the Clappia API"
        
        except requests.exceptions.RequestException as e:
            return f"Error: Request failed - {str(e)}"
        
        except Exception as e:
            return f"Error: An internal error occurred - {str(e)}"

def get_app_definition(app_id: str, workplace_id: str, requesting_user_email_address: str,
                      language: str = "en", strip_html: bool = True,
                      include_tags: bool = True) -> str:
    """
    Fetches the complete definition of a Clappia application, including forms, fields, sections, translations, and metadata, for analytics, integration, or reporting.

    **Purpose**: Retrieve the structure and configuration of a Clappia app to understand available fields, validation rules, and workflow logic before creating charts, filtering submissions, or planning integrations.

    **Key Components Returned**:
    - **Metadata**: App ID, version, state (Active/Draft/Archived), name, description, workplace ID.
    - **Structure**: Pages, sections, and field configurations (e.g., types, labels, validations).
    - **Field Types**: Text (singleLineText, multiLineText), numeric (numberInput, calculations), selectors (singleSelector, multiSelector), dateTime, media (fileUpload, camera, signature), location, barcodeScanner, nestedForm, button.
    - **Translations**: Field labels and text in specified language (en, es, fr, de).
    
    **Parameters**:
    - `app_id`: Unique app identifier (e.g., "QGU236634"). Must be uppercase letters and numbers.
    - `workplace_id`: Parent workplace identifier (e.g., "ON83542"). Must be uppercase letters and numbers.
    - `language`: Language code for translations ("en" [default], "es", "fr", "de").
    - `strip_html`: If True (default), removes HTML from text fields; if False, preserves HTML.
    - `include_tags`: If True (default), includes metadata tags; if False, returns basic structure.

    **Returns**: JSON string with a summary (app metrics) and full app definition, or an error message if the request fails.

    **Usage Examples**:
    - **Analytics**: Get app definition to identify fields (e.g., sales_amount, region) for a dashboard.
    - **Submissions**: Check status field values for filtering pending approvals.
    - **Integration**: Map app fields to external systems using the schema.
    - **Localization**: Fetch Spanish labels with `language="es"` for reports.

    **When to Use**:
    - Before creating charts or reports to know available fields.
    - To understand form structure, validations, or workflow logic.
    - For planning integrations or mapping data to other systems.

    **Notes**:
    - Requires DEV_API_KEY environment variable and CLAPPIA_EXTERNAL_API_BASE_URL environment variable
    - Validates inputs: app_id/workplace_id (uppercase letters/numbers), language (en/es/fr/de).
    - Handles API errors, timeouts, and invalid responses.
    """
    client = ClappiaAppDefinitionClient()
    return client.get_app_definition(app_id, workplace_id, requesting_user_email_address, language, strip_html, include_tags)