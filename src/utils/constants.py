"""
Clappia MCP Constants

This module contains all the constant values used across the Clappia MCP server.
"""

from src.utils.enums import Environment

_SERVER_ENV = Environment.from_env(default=Environment.DEV)

CLAPPIA_EXTERNAL_DEV_API_BASE_URL = "https://preprod-dev-public-v4.clappia.com"
CLAPPIA_EXTERNAL_QA_API_BASE_URL = "https://preprod-public-v4.clappia.com"
CLAPPIA_EXTERNAL_PROD_API_BASE_URL = "https://api-public-v4.clappia.com"

_CLAPPIA_APP_DEFINITION_API_BASE_URLS = {
    Environment.DEV: f"{CLAPPIA_EXTERNAL_DEV_API_BASE_URL}/appdefinitionv2/internal",
    Environment.QA: f"{CLAPPIA_EXTERNAL_QA_API_BASE_URL}/appdefinitionv2/internal",
    Environment.PROD: f"{CLAPPIA_EXTERNAL_PROD_API_BASE_URL}/appdefinitionv2/internal",
}

_CLAPPIA_ANALYTICS_API_BASE_URLS = {
    Environment.DEV: f"{CLAPPIA_EXTERNAL_DEV_API_BASE_URL}/analytics/internal",
    Environment.QA: f"{CLAPPIA_EXTERNAL_QA_API_BASE_URL}/analytics/internal",
    Environment.PROD: f"{CLAPPIA_EXTERNAL_PROD_API_BASE_URL}/analytics/internal",
}

_CLAPPIA_WORKPLACE_API_BASE_URLS = {
    Environment.DEV: f"{CLAPPIA_EXTERNAL_DEV_API_BASE_URL}/workplace/internal",
    Environment.QA: f"{CLAPPIA_EXTERNAL_QA_API_BASE_URL}/workplace/internal",
    Environment.PROD: f"{CLAPPIA_EXTERNAL_PROD_API_BASE_URL}/workplace/internal",
}

_CLAPPIA_WORKFLOW_DEFINITION_API_BASE_URLS = {
    Environment.DEV: f"{CLAPPIA_EXTERNAL_DEV_API_BASE_URL}/workflowdefinitionv2/internal",
    Environment.QA: f"{CLAPPIA_EXTERNAL_QA_API_BASE_URL}/workflowdefinitionv2/internal",
    Environment.PROD: f"{CLAPPIA_EXTERNAL_PROD_API_BASE_URL}/workflowdefinitionv2/internal",
}

_CLAPPIA_SUBMISSIONS_API_BASE_URLS = {
    Environment.DEV: f"{CLAPPIA_EXTERNAL_DEV_API_BASE_URL}/submissions/internal",
    Environment.QA: f"{CLAPPIA_EXTERNAL_QA_API_BASE_URL}/submissions/internal",
    Environment.PROD: f"{CLAPPIA_EXTERNAL_PROD_API_BASE_URL}/submissions/internal",
}

CLAPPIA_APP_DEFINITION_API_BASE_URL = _CLAPPIA_APP_DEFINITION_API_BASE_URLS[_SERVER_ENV]
CLAPPIA_ANALYTICS_API_BASE_URL = _CLAPPIA_ANALYTICS_API_BASE_URLS[_SERVER_ENV]
CLAPPIA_WORKPLACE_API_BASE_URL = _CLAPPIA_WORKPLACE_API_BASE_URLS[_SERVER_ENV]
CLAPPIA_WORKFLOW_DEFINITION_API_BASE_URL = _CLAPPIA_WORKFLOW_DEFINITION_API_BASE_URLS[
    _SERVER_ENV
]
CLAPPIA_SUBMISSIONS_API_BASE_URL = _CLAPPIA_SUBMISSIONS_API_BASE_URLS[_SERVER_ENV]


JWT_ISSUER = "https://preprod-dev.clappia.com"
JWT_AUDIENCE = "https://clappia-mcp.loca.lt"
JWT_SECRET_KEY = "clappia_access_test_secret_key"
JWT_ALGORITHM = "HS256"
