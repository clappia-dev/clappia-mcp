import requests
import json
import os
import re
from typing import Dict, Any, Optional
from dataclasses import dataclass

from dotenv import load_dotenv
from .constants import CLAPPIA_EXTERNAL_API_BASE_URL

load_dotenv()

@dataclass
class UpdateStatusRequest:
    app_id: str
    workplace_id: str
    submission_id: str
    status: Dict[str, Any]
    email: str

class ClappiaUpdateStatusValidator:
    
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
    def validate_status(status: Dict[str, Any]) -> tuple[bool, str]:
        if not status:
            return False, "Status cannot be empty"
        
        if "name" not in status:
            return False, "Status must contain 'name' field"
        
        if not status["name"] or not str(status["name"]).strip():
            return False, "Status name is required and cannot be empty"
        
        return True, ""

class ClappiaUpdateStatusClient:
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
                return f"Submission status updated successfully:\n{json.dumps(response_data, indent=2)}"
            except json.JSONDecodeError:
                return f"Submission status updated successfully: {response.text}"
        
        elif response.status_code in [400, 401, 403, 404]:
            try:
                error_data = response.json()
                return f"API Error ({response.status_code}): {json.dumps(error_data, indent=2)}"
            except json.JSONDecodeError:
                return f"API Error ({response.status_code}): {response.text}"
        
        else:
            return f"Unexpected API response ({response.status_code}): {response.text}"
    
    def update_app_submission_status(self, app_id: str, submission_id: str, 
                                status_name: str, email: str, comments: Optional[str] = None) -> str:
        
        is_valid, error_msg = ClappiaUpdateStatusValidator.validate_app_id(app_id)
        if not is_valid:
            return f"Error: Invalid app_id - {error_msg}"
        
        is_valid, error_msg = ClappiaUpdateStatusValidator.validate_submission_id(submission_id)
        if not is_valid:
            return f"Error: Invalid submission_id - {error_msg}"
        
        is_valid, error_msg = ClappiaUpdateStatusValidator.validate_email(email)
        if not is_valid:
            return f"Error: Invalid email - {error_msg}"
        
        status = {"name": status_name.strip()}
        if comments:
            status["comments"] = comments.strip()
        
        is_valid, error_msg = ClappiaUpdateStatusValidator.validate_status(status)
        if not is_valid:
            return f"Error: Invalid status - {error_msg}"
        
        env_valid, env_error = self._validate_environment()
        if not env_valid:
            return f"Error: {env_error}"
        
        try:
            url = f"{CLAPPIA_EXTERNAL_API_BASE_URL}/submissions/updateStatus"
            headers = self._get_headers()
            
            payload = {
                "appId": app_id.strip(),
                "workplaceId": self.workplace_id,
                "submissionId": submission_id.strip(),
                "requestingUserEmailAddress": email.strip(),
                "status": status
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

def update_app_submission_status(app_id: str, submission_id: str, 
                                   status_name: str, email: str, comments: Optional[str] = None) -> str:
    """
    Update the status of an existing submission in a Clappia application.

    **Purpose**: Change the workflow status of a submission (e.g., pending → approved → completed) with optional comments for audit trail and workflow management.

    **Parameters**:
    - `app_id`: Unique app identifier (e.g., "MFX093412"). Must be uppercase letters and numbers.
    - `submission_id`: ID of the submission to update status (obtained from get_submissions or create response).
    - `status_name`: New status name (e.g., "Approved", "Rejected", "In Progress", "Completed").
    - `email`: Email address of the requesting user (must have status update permissions on the app).
    - `comments`: Optional comments explaining the status change (e.g., "Approved by manager", "Needs more information").

    **Returns**: Success message with updated status details, or error message if the request fails.

    **Usage Examples**:
    - **Approval Workflows**: Change status from "Pending" to "Approved" with approval comments.
    - **Quality Control**: Update status to "Under Review" with specific feedback.
    - **Process Tracking**: Move submissions through stages like "Draft" → "Submitted" → "Processed" → "Completed".
    - **Rejection Handling**: Set status to "Rejected" with detailed rejection reasons.

    **Notes**:
    - Requires CLAPPIA_API_KEY and CLAPPIA_WORKPLACE_ID environment variables.
    - User must have status update permissions on the target app.
    - Status names must match those defined in the app's workflow configuration.
    - Comments are optional but recommended for audit trail and transparency.
    - Validates all inputs: IDs (uppercase letters/numbers), email format, and status structure.
    """
    client = ClappiaUpdateStatusClient()
    return client.update_app_submission_status(app_id, submission_id, status_name, email, comments)