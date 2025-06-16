import requests
import json
import os
import re
from typing import Dict, Any
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

@dataclass
class SubmissionRequest:
    app_id: str
    data: Dict[str, Any]
    email: str
    workplace_id: str

class ClappiaSubmissionValidator:
    
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
    def validate_data(data: Dict[str, Any]) -> tuple[bool, str]:
        if not data:
            return False, "Data cannot be empty"
        
        return True, ""

class ClappiaSubmissionClient:
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
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()
                return f"Submission created successfully:\n{json.dumps(response_data, indent=2)}"
            except json.JSONDecodeError:
                return f"Submission created successfully: {response.text}"
        
        elif response.status_code in [400, 401, 403, 404]:
            try:
                error_data = response.json()
                return f"API Error ({response.status_code}): {json.dumps(error_data, indent=2)}"
            except json.JSONDecodeError:
                return f"API Error ({response.status_code}): {response.text}"
        
        else:
            return f"Unexpected API response ({response.status_code}): {response.text}"
    
    def create_app_submission(self, app_id: str, workplace_id: str, data: Dict[str, Any], email: str) -> str:
        
        is_valid, error_msg = ClappiaSubmissionValidator.validate_app_id(app_id)
        if not is_valid:
            return f"Error: Invalid app_id - {error_msg}"
    
        
        is_valid, error_msg = ClappiaSubmissionValidator.validate_email(email)
        if not is_valid:
            return f"Error: Invalid email - {error_msg}"
    
        is_valid, error_msg = ClappiaSubmissionValidator.validate_workplace_id(workplace_id)
        if not is_valid:
            return f"Error: Invalid workplace_id - {error_msg}"
        
        is_valid, error_msg = ClappiaSubmissionValidator.validate_data(data)
        if not is_valid:
            return f"Error: Invalid data - {error_msg}"
        
        env_valid, env_error = self._validate_environment()
        if not env_valid:
            return f"Error: {env_error}"
        
        try:
            url = f"{self.base_url}/submissions/create"
            headers = self._get_headers()
            
            payload = {
                "appId": app_id.strip(),
                "requestingUserEmailAddress": email.strip(),
                "data": data,
                "workplaceId": workplace_id.strip()
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

def create_app_submission(app_id: str, workplace_id: str, data: Dict[str, Any], email: str) -> str:
    """
    Creates a new submission in a Clappia application with the provided data.

    **Purpose**: Submit form data to a Clappia app, creating a new record with the specified field values and setting the requesting user as the submission owner.

    **Parameters**:
    - `app_id`: Unique app identifier (e.g., "MFX093412"). Must be uppercase letters and numbers.
    - `workplace_id`: Unique workplace identifier (e.g., "ON83542"). Must be uppercase letters and numbers.
    - `data`: Dictionary of field key-value pairs to submit (e.g., {"name": "John", "age": 30}).
    - `email`: Email address of the user creating the submission (becomes the submission owner).

    **Returns**: Success message with submission details, or error message if the request fails.

    **Usage Examples**:
    - **Form Submission**: Submit user data collected from a web form.
    - **Bulk Import**: Create multiple submissions from Excel/CSV data (process rows sequentially).
    - **Integration**: Push data from external systems into Clappia apps.

    **Notes**:
    - Requires DEV_API_KEY, CLAPPIA_EXTERNAL_API_BASE_URL environment variables.
    - Validates inputs: app_id (uppercase letters/numbers), email format, and data structure.
    - Handles API errors, timeouts, and invalid responses.
    - For bulk processing: process Excel rows sequentially, skip file upload fields if errors occur.
    """
    client = ClappiaSubmissionClient()
    return client.create_app_submission(app_id,workplace_id, data, email)