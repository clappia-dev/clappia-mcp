import requests
import json
import os
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

from dotenv import load_dotenv
from .constants import CLAPPIA_EXTERNAL_API_BASE_URL

load_dotenv()

class FilterOperator(Enum):
    CONTAINS = "CONTAINS"
    NOT_IN = "NOT_IN"
    EQ = "EQ"
    NEQ = "NEQ"
    EMPTY = "EMPTY"
    NON_EMPTY = "NON_EMPTY"
    STARTS_WITH = "STARTS_WITH"
    BETWEEN = "BETWEEN"
    GT = "GT"
    LT = "LT"
    GTE = "GTE"
    LTE = "LTE"

class LogicalOperator(Enum):
    AND = "AND"
    OR = "OR"

class FilterKeyType(Enum):
    STANDARD = "STANDARD"
    CUSTOM = "CUSTOM"

@dataclass
class Condition:
    operator: str
    filterKeyType: str
    key: str
    value: str
    
    def to_dict(self) -> dict:
        return {
            "operator": self.operator,
            "filterKeyType": self.filterKeyType,
            "key": self.key,
            "value": self.value
        }

@dataclass
class Query:
    conditions: List[Condition]
    operator: Optional[str] = None
    
    def to_dict(self) -> dict:
        result = {"conditions": [condition.to_dict() for condition in self.conditions]}
        if self.operator:
            result["operator"] = self.operator
        return result

@dataclass
class QueryGroup:
    queries: List[Query]
    
    def to_dict(self) -> dict:
        return {"queries": [query.to_dict() for query in self.queries]}

@dataclass
class Filters:
    queries: List[QueryGroup]
    
    def to_dict(self) -> dict:
        return {"queries": [query_group.to_dict() for query_group in self.queries]}

class ClappiaValidator:
    STANDARD_FIELDS = {
        "$submissionId", "$owner", "$status", "$createdAt", 
        "$updatedAt", "$state", "submissionId", "owner", 
        "status", "createdAt", "updatedAt", "state"
    }
    
    EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    @staticmethod
    def validate_email(email: str) -> bool:
        return bool(re.match(ClappiaValidator.EMAIL_PATTERN, email))
    
    @staticmethod
    def validate_condition(condition: dict) -> tuple[bool, str]:
        required_fields = ["operator", "filterKeyType", "key", "value"]
        for field in required_fields:
            if field not in condition:
                return False, f"Condition missing required field: {field}"
        
        if condition["operator"] not in [op.value for op in FilterOperator]:
            return False, f"Invalid operator: {condition['operator']}"
        
        if condition["filterKeyType"] not in [fkt.value for fkt in FilterKeyType]:
            return False, f"Invalid filterKeyType: {condition['filterKeyType']}"
        
        key = condition["key"]
        if len(key.strip()) == 0:
            return False, "Key must be a non-empty string"
        
        if condition["filterKeyType"] == FilterKeyType.STANDARD.value and key not in ClappiaValidator.STANDARD_FIELDS:
            return False, f"Standard filterKeyType used but key '{key}' is not a standard field"
        
        operator = condition["operator"]
        value = condition["value"]
        
        if operator in [FilterOperator.EMPTY.value, FilterOperator.NON_EMPTY.value]:
            if value and value.strip():
                return False, f"Operator {operator} should have empty value"
        else:
            if len(value.strip()) == 0:
                return False, f"Operator {operator} requires a non-empty value"
        
        return True, ""
    
    @staticmethod
    def validate_filters(filters: dict) -> tuple[bool, str]:
        if "queries" not in filters:
            return False, "Filters must contain 'queries' key"
        
        queries = filters["queries"]
        if len(queries) == 0:
            return False, "Queries must be a non-empty list"
        
        for query_group in queries:
            if "queries" not in query_group:
                return False, "Each query group must contain 'queries' key"
            
            inner_queries = query_group["queries"]
            for inner_query in inner_queries:
                if "conditions" not in inner_query:
                    return False, "Each query must contain 'conditions'"
                
                conditions = inner_query["conditions"]
                if len(conditions) == 0:
                    return False, "Conditions must be a non-empty list"
                
                for condition in conditions:
                    is_valid, error_msg = ClappiaValidator.validate_condition(condition)
                    if not is_valid:
                        return False, error_msg
                
                if "operator" in inner_query:
                    logical_op = inner_query["operator"]
                    if logical_op not in [op.value for op in LogicalOperator]:
                        return False, f"Invalid logical operator: {logical_op}"
        
        return True, ""

class ClappiaAPIClient:
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
                submissions_count = len(response_data.get("submissions", []))
                return f"Successfully retrieved {submissions_count} submissions: {json.dumps(response_data, indent=2)}"
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
    
    def get_app_submissions(self, app_id: str, requesting_user_email_address: str,
                       page_size: int = 10, filters: Optional[Filters] = None) -> str:
        
        if not app_id or not app_id.strip():
            return "Error: app_id is required and cannot be empty"
        
        if not requesting_user_email_address or not requesting_user_email_address.strip():
            return "Error: requesting_user_email_address is required and cannot be empty"
        
        if not ClappiaValidator.validate_email(requesting_user_email_address):
            return "Error: requesting_user_email_address must be a valid email address"
        
        if page_size <= 0:
            return "Error: page_size must be a positive integer"
        
        if page_size > 1000:
            return "Error: page_size cannot exceed 1000"
        
        if filters is not None:
            is_valid, error_msg = ClappiaValidator.validate_filters(filters)
            if not is_valid:
                return f"Error: Invalid filters - {error_msg}"
        
        env_valid, env_error = self._validate_environment()
        if not env_valid:
            return f"Error: {env_error}"
        
        try:
            url = f"{CLAPPIA_EXTERNAL_API_BASE_URL}/submissions/getSubmissions"
            headers = self._get_headers()
            
            payload = {
                "workplaceId": self.workplace_id,
                "appId": app_id.strip(),
                "requestingUserEmailAddress": requesting_user_email_address.strip(),
                "pageSize": page_size,
                "forward": True
            }
            
            if filters:
                payload["filters"] = filters

            
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

def get_app_submissions(app_id: str, requesting_user_email_address: str, 
                   page_size: int = 10, filters: Optional[Filters] = None) -> str:
    """
    Retrieve Clappia form submissions with optional filtering.

    Args:
        app_id (str): Application identifier (e.g., "ODT537440"). Must be uppercase letters and numbers.
        requesting_user_email_address (str): Email address of the requesting user (must have access to the app).
        page_size (int, optional): Number of results to retrieve (1-1000, default: 10).
        filters (Optional[Filters], optional): Filter conditions using the Filters class:
            - queries (List[QueryGroup]): Groups of queries
            - Each QueryGroup contains queries (List[Query])
            - Each Query contains conditions (List[Condition])
            - Each Condition has:
                - operator (str): One of "CONTAINS", "NOT_IN", "EQ", "NEQ", "EMPTY", "NON_EMPTY", "STARTS_WITH", "BETWEEN", "GT", "LT", "GTE", "LTE"
                - filterKeyType (str): "STANDARD" or "CUSTOM"
                - key (str): Field name to filter on
                - value (str): Value to filter by

    Returns:
        str: JSON string with submission records and metadata, or error message if the request fails.

    Notes:
        - Requires CLAPPIA_API_KEY and CLAPPIA_WORKPLACE_ID environment variables.
        - Validates workplace_id and app_id format (uppercase letters/numbers).
        - Page size is limited to 1000 records per request for performance.
        - Filters support various operators for flexible querying.
        - Handles API errors, timeouts, and invalid responses.
        - The response includes submission count and full submission data.
        - Standard fields available for filtering: $submissionId, $owner, $status, $createdAt, $updatedAt, $state
    """
    client = ClappiaAPIClient()
    return client.get_app_submissions(app_id, requesting_user_email_address, page_size, filters)