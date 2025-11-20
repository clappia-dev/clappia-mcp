"""
Clappia MCP Constants

This module contains all the constant values used across the Clappia MCP server.
"""

from src.utils.enums import Environment

SERVER_ENV = Environment.from_env(default=Environment.DEV)

DEV_API_BASE_URL = "https://preprod-dev-public-v4.clappia.com"
QA_API_BASE_URL = "https://preprod-public-v4.clappia.com"
PROD_API_BASE_URL = "https://api-public-v4.clappia.com"

APP_DEFINITION_API_BASE_URLS = {
    Environment.DEV: f"{DEV_API_BASE_URL}/appdefinitionv2/internal",
    Environment.QA: f"{QA_API_BASE_URL}/appdefinitionv2/internal",
    Environment.PROD: f"{PROD_API_BASE_URL}/appdefinitionv2/internal",
}

ANALYTICS_API_BASE_URLS = {
    Environment.DEV: f"{DEV_API_BASE_URL}/analytics/internal",
    Environment.QA: f"{QA_API_BASE_URL}/analytics/internal",
    Environment.PROD: f"{PROD_API_BASE_URL}/analytics/internal",
}

WORKPLACE_API_BASE_URLS = {
    Environment.DEV: f"{DEV_API_BASE_URL}/workplace/internal",
    Environment.QA: f"{QA_API_BASE_URL}/workplace/internal",
    Environment.PROD: f"{PROD_API_BASE_URL}/workplace/internal",
}

WORKFLOW_DEFINITION_API_BASE_URLS = {
    Environment.DEV: f"{DEV_API_BASE_URL}/workflowdefinitionv2/internal",
    Environment.QA: f"{QA_API_BASE_URL}/workflowdefinitionv2/internal",
    Environment.PROD: f"{PROD_API_BASE_URL}/workflowdefinitionv2/internal",
}

SUBMISSIONS_API_BASE_URLS = {
    Environment.DEV: f"{DEV_API_BASE_URL}/submissions/internal",
    Environment.QA: f"{QA_API_BASE_URL}/submissions/internal",
    Environment.PROD: f"{PROD_API_BASE_URL}/submissions/internal",
}

FILE_MANAGEMENT_API_BASE_URLS = {
    Environment.DEV: f"{DEV_API_BASE_URL}/file/internal",
    Environment.QA: f"{QA_API_BASE_URL}/file/internal",
    Environment.PROD: f"{PROD_API_BASE_URL}/file/internal",
}

JWT_ISSUER_URLS = {
    Environment.DEV: "https://preprod-dev.clappia.com",
    Environment.QA: "https://preprod.clappia.com",
    Environment.PROD: "https://apiv2.clappia.com",
}

JWT_AUDIENCE_URLS = {
    Environment.DEV: "https://mcp-test.clappia.com",
    Environment.QA: "https://mcp-qa.clappia.com",
    Environment.PROD: "https://mcp.clappia.com",
}

APP_DEFINITION_API_BASE_URL = APP_DEFINITION_API_BASE_URLS[SERVER_ENV]
ANALYTICS_API_BASE_URL = ANALYTICS_API_BASE_URLS[SERVER_ENV]
WORKPLACE_API_BASE_URL = WORKPLACE_API_BASE_URLS[SERVER_ENV]
WORKFLOW_DEFINITION_API_BASE_URL = WORKFLOW_DEFINITION_API_BASE_URLS[SERVER_ENV]
SUBMISSIONS_API_BASE_URL = SUBMISSIONS_API_BASE_URLS[SERVER_ENV]
FILE_MANAGEMENT_API_BASE_URL = FILE_MANAGEMENT_API_BASE_URLS[SERVER_ENV]

JWT_ISSUER = JWT_ISSUER_URLS[SERVER_ENV]
JWT_AUDIENCE = JWT_AUDIENCE_URLS[SERVER_ENV]
JWT_SECRET_KEY = "clappia_access_test_secret_key"
JWT_ALGORITHM = "HS256"

BASE_URL = JWT_ISSUER_URLS[SERVER_ENV]

OAUTH_CONSTANTS = {
    "DEFAULT_ISSUER": BASE_URL,
    "AUTHORIZATION_ENDPOINT": f"{BASE_URL}/authorize",
    "TOKEN_ENDPOINT": f"{BASE_URL}/token",
    "REGISTRATION_ENDPOINT": f"{BASE_URL}/register",
    "RESPONSE_TYPES_SUPPORTED": ["code"],
    "GRANT_TYPES_SUPPORTED": ["authorization_code", "refresh_token"],
    "CODE_CHALLENGE_METHODS_SUPPORTED": ["S256"],
    "TOKEN_ENDPOINT_AUTH_METHODS_SUPPORTED": ["client_secret_post", "none"],
    "SCOPES_SUPPORTED": ["mcp:tools"],
}
