import requests
import json
import os
import re
from typing import List
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

@dataclass
class UpdateOwnersRequest:
    app_id: str
    workplace_id: str
    submission_id: str
    email_ids: List[str]
    email: str

class ClappiaUpdateOwnersValidator:
    
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
    def validate_email_ids(email_ids: List[str]) -> tuple[bool, str]:
        if not email_ids:
            return False, "Email IDs list cannot be empty"
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        for i, email in enumerate(email_ids):
            if not email or not email.strip():
                return False, f"Email at index {i} is empty"
            
            if not re.match(email_pattern, email.strip()):
                return False, f"Invalid email format at index {i}: {email}"
        
        return True, ""

class ClappiaUpdateOwnersClient:
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
                return f"Submission owners updated successfully:\n{json.dumps(response_data, indent=2)}"
            except json.JSONDecodeError:
                return f"Submission owners updated successfully: {response.text}"
        
        elif response.status_code in [400, 401, 403, 404]:
            try:
                error_data = response.json()
                return f"API Error ({response.status_code}): {json.dumps(error_data, indent=2)}"
            except json.JSONDecodeError:
                return f"API Error ({response.status_code}): {response.text}"
        
        else:
            return f"Unexpected API response ({response.status_code}): {response.text}"
    
    def update_app_submission_owners(self, app_id: str, workplace_id: str, submission_id: str, 
                               email_ids: List[str], email: str) -> str:
        
        is_valid, error_msg = ClappiaUpdateOwnersValidator.validate_app_id(app_id)
        if not is_valid:
            return f"Error: Invalid app_id - {error_msg}"
        
        is_valid, error_msg = ClappiaUpdateOwnersValidator.validate_workplace_id(workplace_id)
        if not is_valid:
            return f"Error: Invalid workplace_id - {error_msg}"
        
        is_valid, error_msg = ClappiaUpdateOwnersValidator.validate_submission_id(submission_id)
        if not is_valid:
            return f"Error: Invalid submission_id - {error_msg}"
        
        is_valid, error_msg = ClappiaUpdateOwnersValidator.validate_email(email)
        if not is_valid:
            return f"Error: Invalid email - {error_msg}"
        
        is_valid, error_msg = ClappiaUpdateOwnersValidator.validate_email_ids(email_ids)
        if not is_valid:
            return f"Error: Invalid email_ids - {error_msg}"
        
        env_valid, env_error = self._validate_environment()
        if not env_valid:
            return f"Error: {env_error}"
        
        try:
            url = f"{self.base_url}/submissions/updateSubmissionOwners"
            headers = self._get_headers()
            
            cleaned_email_ids = [email_id.strip() for email_id in email_ids]
            
            payload = {
                "appId": app_id.strip(),
                "workplaceId": workplace_id.strip(),
                "submissionId": submission_id.strip(),
                "requestingUserEmailAddress": email.strip(),
                "emailIds": cleaned_email_ids
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

def update_app_submission_owners(app_id: str, workplace_id: str, submission_id: str, 
                                   email_ids: List[str], email: str) -> str:
    """
    Update the owners of an existing submission in a Clappia application.

    **Purpose**: Change ownership or add multiple owners to a submission for delegation, team collaboration, or workflow reassignment.

    **Parameters**:
    - `app_id`: Unique app identifier (e.g., "MFX093412"). Must be uppercase letters and numbers.
    - `workplace_id`: Workplace identifier (e.g., "ON83542"). Must be uppercase letters and numbers.
    - `submission_id`: ID of the submission to update owners (obtained from get_submissions or create response).
    - `email_ids`: List of email addresses to set as new owners (e.g., ["john@company.com", "jane@company.com"]).
    - `email`: Email address of the requesting user (must have Submit permissions on the app).

    **Returns**: Success message with updated ownership details, or error message if the request fails.

    **Usage Examples**:
    - **Task Delegation**: Reassign submission from one user to another.
    - **Team Collaboration**: Add multiple team members as co-owners of a submission.
    - **Manager Assignment**: Transfer ownership to a supervisor for review/approval.
    - **Department Transfer**: Move submissions between departments or teams.
    - **Backup Ownership**: Add secondary owners for continuity and coverage.

    **Notes**:
    - Requires DEV_API_KEY and CLAPPIA_EXTERNAL_API_BASE_URL environment variables.
    - Requesting user must have Submit permissions on the target app.
    - All email addresses in `email_ids` must be valid and have access to the app.
    - This replaces existing owners with the new list (not additive).
    - Validates all inputs: IDs (uppercase letters/numbers), email formats, and list structure.
    - Handles API errors, timeouts, and invalid responses.
    """
    client = ClappiaUpdateOwnersClient()
    return client.update_app_submission_owners(app_id, workplace_id, submission_id, email_ids, email)