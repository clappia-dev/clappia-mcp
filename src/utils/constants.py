"""
Clappia MCP Constants

This module contains all the constant values used across the Clappia MCP server.
"""

import os
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

_CLAPPIA_FILE_MANAGEMENT_API_BASE_URLS = {
    Environment.DEV: f"{CLAPPIA_EXTERNAL_DEV_API_BASE_URL}/file/internal",
    Environment.QA: f"{CLAPPIA_EXTERNAL_QA_API_BASE_URL}/file/internal",
    Environment.PROD: f"{CLAPPIA_EXTERNAL_PROD_API_BASE_URL}/file/internal",
}

CLAPPIA_APP_DEFINITION_API_BASE_URL = _CLAPPIA_APP_DEFINITION_API_BASE_URLS[_SERVER_ENV]
CLAPPIA_ANALYTICS_API_BASE_URL = _CLAPPIA_ANALYTICS_API_BASE_URLS[_SERVER_ENV]
CLAPPIA_WORKPLACE_API_BASE_URL = _CLAPPIA_WORKPLACE_API_BASE_URLS[_SERVER_ENV]
CLAPPIA_WORKFLOW_DEFINITION_API_BASE_URL = _CLAPPIA_WORKFLOW_DEFINITION_API_BASE_URLS[
    _SERVER_ENV
]
CLAPPIA_SUBMISSIONS_API_BASE_URL = _CLAPPIA_SUBMISSIONS_API_BASE_URLS[_SERVER_ENV]
CLAPPIA_FILE_MANAGEMENT_API_BASE_URL = _CLAPPIA_FILE_MANAGEMENT_API_BASE_URLS[
    _SERVER_ENV
]

JWT_ISSUER = "https://preprod-dev.clappia.com"
JWT_AUDIENCE = "https://mcp-test.clappia.com"
JWT_SECRET_KEY = "clappia_access_test_secret_key"
JWT_ALGORITHM = "HS256"

BASE_URL = os.getenv("OAUTH_BASE_URL", "https://preprod-dev.clappia.com")
RESOURCE_ENDPOINT = os.getenv(
    "OAUTH_RESOURCE_ENDPOINT",
    "https://mcp-test.clappia.com",
)

OAUTH_CONSTANTS = {
    "DEFAULT_ISSUER": BASE_URL,
    "AUTHORIZATION_ENDPOINT": f"{BASE_URL}/authorize",
    "TOKEN_ENDPOINT": f"{BASE_URL}/token",
    "REGISTRATION_ENDPOINT": f"{BASE_URL}/register",
    "INTROSPECTION_ENDPOINT": f"{BASE_URL}/introspect",
    "METADATA_ENDPOINT": f"{BASE_URL}/.well-known/oauth-authorization-server",
    "RESOURCE_ENDPOINT": RESOURCE_ENDPOINT,
    "RESPONSE_TYPES_SUPPORTED": ["code"],
    "GRANT_TYPES_SUPPORTED": ["authorization_code", "refresh_token"],
    "CODE_CHALLENGE_METHODS_SUPPORTED": ["S256"],
    "TOKEN_ENDPOINT_AUTH_METHODS_SUPPORTED": ["client_secret_post", "none"],
    "SCOPES_SUPPORTED": ["mcp:tools"],
    "TOKEN_TYPE": "Bearer",
    "ACCESS_TOKEN_EXPIRES_IN": 3600,
    "AUTH_CODE_EXPIRES_IN_MINUTES": 10,
    "DEFAULT_SCOPE": "mcp:tools",
    "OAUTH_BROWSER": "OAuth Client",
    "OAUTH_OS": "Unknown",
    "OAUTH_DEVICE": "Unknown",
    "CODE_CHALLENGE_METHOD_S256": "S256",
    "CLIENT_LOGIN_URL": os.getenv(
        "OAUTH_CLIENT_LOGIN_URL", "https://dev.auth.clappia.com/signin/oauth"
    ),
}
