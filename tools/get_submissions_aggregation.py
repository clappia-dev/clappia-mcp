import requests
import json
import os
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

from dotenv import load_dotenv

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

class AggregationType(Enum):
    COUNT = "count"
    SUM = "sum"
    AVERAGE = "average"
    MINIMUM = "minimum"
    MAXIMUM = "maximum"
    UNIQUE = "unique"

class DimensionType(Enum):
    STANDARD = "STANDARD"
    CUSTOM = "CUSTOM"

class SortDirection(Enum):
    ASC = "asc"
    DESC = "desc"

class DataType(Enum):
    TEXT = "text"
    NUMBER = "number"
    DATE = "date"
    BOOLEAN = "boolean"
    SELECT = "select"
    TEXT_INPUT = "textInput"

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

@dataclass
class Dimension:
    fieldName: str
    label: str
    dataType: str
    dimensionType: str = "CUSTOM"
    sortDirection: Optional[str] = None
    sortType: Optional[str] = None
    missingValue: Optional[str] = None
    interval: Optional[str] = None
    
    def to_dict(self) -> dict:
        result = {
            "fieldName": self.fieldName,
            "label": self.label,
            "dataType": self.dataType,
            "dimensionType": self.dimensionType
        }
        if self.sortDirection:
            result["sortDirection"] = self.sortDirection
        if self.sortType:
            result["sortType"] = self.sortType
        if self.missingValue is not None:
            result["missingValue"] = self.missingValue
        if self.interval:
            result["interval"] = self.interval
        return result

@dataclass
class AggregationOperand:
    fieldName: str
    label: str
    dataType: str
    dimensionType: str = "CUSTOM"
    
    def to_dict(self) -> dict:
        return {
            "fieldName": self.fieldName,
            "label": self.label,
            "dataType": self.dataType,
            "dimensionType": self.dimensionType
        }

@dataclass
class AggregationDimension:
    type: str
    operand: Optional[AggregationOperand] = None
    
    def to_dict(self) -> dict:
        result = {"type": self.type}
        if self.operand:
            result["operand"] = self.operand.to_dict()
        return result

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
    def validate_aggregation_type(agg_type: str) -> bool:
        return agg_type in [at.value for at in AggregationType]
    
    @staticmethod
    def validate_dimension_type(dim_type: str) -> bool:
        return dim_type in [dt.value for dt in DimensionType]

class ClappiaAggregationAPIClient:
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
                return f"Successfully retrieved aggregated data: {json.dumps(response_data, indent=2)}"
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
    
    def get_app_submissions_aggregation(self, workplace_id: str, app_id: str,
                                  dimensions: List[Dimension], 
                                  aggregation_dimensions: List[AggregationDimension],
                                  x_axis_labels: List[str],
                                  requesting_user_email_address: str = "dev@clappia.com",
                                  forward: bool = True,
                                  page_size: int = 1000,
                                  filters: Optional[Filters] = None) -> str:
        
        if not workplace_id or not workplace_id.strip():
            return "Error: workplace_id is required and cannot be empty"
        
        if not app_id or not app_id.strip():
            return "Error: app_id is required and cannot be empty"
        
        if not dimensions and not aggregation_dimensions:
            return "Error: At least one dimension or aggregation dimension must be provided"
        
        env_valid, env_error = self._validate_environment()
        if not env_valid:
            return f"Error: {env_error}"
        
        try:
            url = f"{self.base_url}/submissions/getSubmissionsAggregation"
            headers = self._get_headers()
            
            payload = {
                "workplaceId": workplace_id.strip(),
                "appId": app_id.strip(),
                "requestingUserEmailAddress": requesting_user_email_address,
                "forward": forward,
                "pageSize": page_size,
                "dimensions": dimensions,
                "aggregationDimensions": aggregation_dimensions,
                "xAxisLabels": x_axis_labels
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

def get_app_submissions_aggregation(workplace_id: str, app_id: str,
                                    dimensions: List[Dimension] = None, 
                                    aggregation_dimensions: List[AggregationDimension] = None,
                                    x_axis_labels: List[str] = None,
                                    requesting_user_email_address: str = "dev@clappia.com",
                                    forward: bool = True,
                                    page_size: int = 1000,
                                    filters: Optional[Filters] = None) -> str:
    """
    Aggregate Clappia submission data for analytics and reporting.

    Args:
        workplace_id (str): Workplace ID (e.g., "ON83542"). Uppercase letters/numbers.
        app_id (str): Application ID (e.g., "ODT537440"). Uppercase letters/numbers.
        dimensions (List[Dimension], optional): Fields to group by. Each Dimension should have:
            - fieldName (str): Name of the field to group by
            - label (str): Display label for the dimension
            - dataType (str): Type of data ("text", "number", "date", "boolean", "select", "textInput")
            - dimensionType (str, optional): "STANDARD" or "CUSTOM". Defaults to "CUSTOM"
            - sortDirection (str, optional): "asc" or "desc"
            - sortType (str, optional): Type of sorting
            - missingValue (str, optional): Value to use for missing data
            - interval (str, optional): Interval for date grouping
        aggregation_dimensions (List[AggregationDimension], optional): Calculations to perform. Each AggregationDimension should have:
            - type (str): One of "count", "sum", "average", "minimum", "maximum", "unique"
            - operand (AggregationOperand, optional): For aggregations that need a field:
                - fieldName (str): Name of the field to aggregate
                - label (str): Display label for the aggregation
                - dataType (str): Type of data
                - dimensionType (str): "STANDARD" or "CUSTOM"
        x_axis_labels (List[str], optional): Output column labels (e.g., ["Count", "Total Sales"]). Defaults to [].
        requesting_user_email_address (str, optional): User email. Defaults to "dev@clappia.com".
        forward (bool, optional): Pagination direction. Defaults to True.
        page_size (int, optional): Max results (1-1000). Defaults to 1000.
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
        str: JSON string with tabular data (e.g., '[["Region", "Count"], ["North", 10], ["South", 15]]') or error message.

    Notes:
        - Requires DEV_API_KEY and CLAPPIA_EXTERNAL_API_BASE_URL environment variables.
        - At least one dimension or aggregation_dimension is required.
        - The response format is a 2D array where the first row contains headers and subsequent rows contain data.
    """
    if dimensions is None:
        dimensions = []
    if aggregation_dimensions is None:
        aggregation_dimensions = []
    if x_axis_labels is None:
        x_axis_labels = []
    
    client = ClappiaAggregationAPIClient()
    return client.get_app_submissions_aggregation(
        workplace_id, app_id, dimensions, aggregation_dimensions, 
        x_axis_labels, requesting_user_email_address, forward, page_size, filters
    )