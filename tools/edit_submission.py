import requests
import json
import os
import re
from typing import Dict, Any
from dataclasses import dataclass

from dotenv import load_dotenv
from .constants import CLAPPIA_EXTERNAL_API_BASE_URL

load_dotenv()

@dataclass
class EditSubmissionRequest:
    app_id: str
    workplace_id: str
    submission_id: str
    data: Dict[str, Any]
    email: str

class ClappiaEditSubmissionValidator:
    
    @staticmethod
    def validate_app_id(app_id: str) -> tuple[bool, str]:
        if not app_id or not app_id.strip():
            return False, "App ID is required and cannot be empty"
        
        if not re.match(r'^[A-Z0-9]+$', app_id.strip()):
            return False, "App ID must contain only uppercase letters and numbers"
        
        return True, ""
    
    @staticmethod
    def validate_submission_id(submission_id: str) -> tuple[bool, str]:
        if not submission_id or not submission_id.strip():
            return False, "Submission ID is required and cannot be empty"
        
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

class ClappiaEditSubmissionClient:
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
            "Content-Type": "application/json"
        }
    
    def _handle_response(self, response: requests.Response) -> str:
        if response.status_code == 200:
            try:
                response_data = response.json()
                return f"Submission edited successfully:\n{json.dumps(response_data, indent=2)}"
            except json.JSONDecodeError:
                return f"Submission edited successfully: {response.text}"
        
        elif response.status_code in [400, 401, 403, 404]:
            try:
                error_data = response.json()
                return f"API Error ({response.status_code}): {json.dumps(error_data, indent=2)}"
            except json.JSONDecodeError:
                return f"API Error ({response.status_code}): {response.text}"
        
        else:
            return f"Unexpected API response ({response.status_code}): {response.text}"
    
    def edit_app_submission(self, app_id: str, submission_id: str, 
                       data: Dict[str, Any], email: str) -> str:
        
        is_valid, error_msg = ClappiaEditSubmissionValidator.validate_app_id(app_id)
        if not is_valid:
            return f"Error: Invalid app_id - {error_msg}"
        
        is_valid, error_msg = ClappiaEditSubmissionValidator.validate_submission_id(submission_id)
        if not is_valid:
            return f"Error: Invalid submission_id - {error_msg}"
        
        is_valid, error_msg = ClappiaEditSubmissionValidator.validate_email(email)
        if not is_valid:
            return f"Error: Invalid email - {error_msg}"
        
        is_valid, error_msg = ClappiaEditSubmissionValidator.validate_data(data)
        if not is_valid:
            return f"Error: Invalid data - {error_msg}"
        
        env_valid, env_error = self._validate_environment()
        if not env_valid:
            return f"Error: {env_error}"
        
        try:
            url = f"{CLAPPIA_EXTERNAL_API_BASE_URL}/submissions/edit"
            headers = self._get_headers()
            
            payload = {
                "appId": app_id.strip(),
                "workplaceId": self.workplace_id,
                "submissionId": submission_id.strip(),
                "requestingUserEmailAddress": email.strip(),
                "data": data
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

def edit_app_submission(app_id: str, submission_id: str, 
                           data: Dict[str, Any], email: str) -> str:
    """
    Edit an existing submission in a Clappia application with updated field values.

    **Purpose**: Update specific fields in an existing submission while preserving other data, useful for corrections, status updates, or progressive form completion.

    **Parameters**:
    - `app_id`: Unique app identifier (e.g., "MFX093412"). Must be uppercase letters and numbers.
    - `submission_id`: ID of the submission to be edited (obtained from get_submissions or create response).
    - `data`: Dictionary of field key-value pairs to update (e.g., {"status": "approved", "notes": "Reviewed"}).
    - `email`: Email address of the requesting user (must have Submit permissions on the app).

    **Returns**: Success message with updated submission details, or error message if the request fails.

    **Usage Examples**:
    - **Status Updates**: Change submission status from "pending" to "approved".
    - **Data Corrections**: Fix typos or update incorrect information in submitted forms.
    - **Progressive Forms**: Add additional information to partially completed submissions.
    - **Workflow Updates**: Update assigned reviewers, priority levels, or completion dates.

    **Notes**:
    - Requires CLAPPIA_API_KEY, CLAPPIA_WORKPLACE_ID, and CLAPPIA_EXTERNAL_API_BASE_URL environment variables.
    - User must have Submit permissions on the target app.
    - Only specified fields in `data` will be updated; other fields remain unchanged.
    - Validates all inputs: IDs (uppercase letters/numbers), email format, and data structure.
    - Handles API errors, timeouts, and invalid responses.
    """
    client = ClappiaEditSubmissionClient()
    return client.edit_app_submission(app_id, submission_id, data, email)