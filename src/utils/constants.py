"""
Clappia MCP Constants

This module contains all the constant values used across the Clappia MCP server.
"""

from src.utils.enums import Environment

SERVER_ENV = Environment.from_env(default=Environment.DEV)

DEV_API_BASE_URL = "https://preprod-dev-public-v4.clappia.com"
QA_API_BASE_URL = "https://preprod-public-v4.clappia.com"
PROD_API_BASE_URL = "https://api-public-v4.clappia.com"

LOCAL_APP_DEFINITION_API_BASE_URLS = {
    Environment.DEV: f"{DEV_API_BASE_URL}/appdefinitionv2",
    Environment.QA: f"{QA_API_BASE_URL}/appdefinitionv2",
    Environment.PROD: f"{PROD_API_BASE_URL}/appdefinitionv2",
    Environment.LOCAL: f"{DEV_API_BASE_URL}/appdefinitionv2",
}

LOCAL_ANALYTICS_API_BASE_URLS = {
    Environment.DEV: f"{DEV_API_BASE_URL}/analytics",
    Environment.QA: f"{QA_API_BASE_URL}/analytics",
    Environment.PROD: f"{PROD_API_BASE_URL}/analytics",
    Environment.LOCAL: f"{DEV_API_BASE_URL}/analytics",
}

LOCAL_WORKPLACE_API_BASE_URLS = {
    Environment.DEV: f"{DEV_API_BASE_URL}/workplace",
    Environment.QA: f"{QA_API_BASE_URL}/workplace",
    Environment.PROD: f"{PROD_API_BASE_URL}/workplace",
    Environment.LOCAL: f"{DEV_API_BASE_URL}/workplace",
}

LOCAL_WORKFLOW_DEFINITION_API_BASE_URLS = {
    Environment.DEV: f"{DEV_API_BASE_URL}/workflowdefinitionv2",
    Environment.QA: f"{QA_API_BASE_URL}/workflowdefinitionv2",
    Environment.PROD: f"{PROD_API_BASE_URL}/workflowdefinitionv2",
    Environment.LOCAL: f"{DEV_API_BASE_URL}/workflowdefinitionv2",
}

LOCAL_SUBMISSIONS_API_BASE_URLS = {
    Environment.DEV: f"{DEV_API_BASE_URL}/submissions",
    Environment.QA: f"{QA_API_BASE_URL}/submissions",
    Environment.PROD: f"{PROD_API_BASE_URL}/submissions",
    Environment.LOCAL: f"{DEV_API_BASE_URL}/submissions",
}

LOCAL_FILE_MANAGEMENT_API_BASE_URLS = {
    Environment.DEV: f"{DEV_API_BASE_URL}/file",
    Environment.QA: f"{QA_API_BASE_URL}/file",
    Environment.PROD: f"{PROD_API_BASE_URL}/file",
    Environment.LOCAL: f"{DEV_API_BASE_URL}/file",
}

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
    Environment.LOCAL: "https://preprod-dev.clappia.com",
}

JWT_AUDIENCE_URLS = {
    Environment.DEV: "https://mcp-test.clappia.com",
    Environment.QA: "https://mcp-qa.clappia.com",
    Environment.PROD: "https://mcp.clappia.com",
    Environment.LOCAL: "https://mcp-test.clappia.com",
}


def _get_base_url(
    internal_urls: dict[Environment, str], local_urls: dict[Environment, str]
) -> str:
    if SERVER_ENV.is_local():
        return local_urls[SERVER_ENV]
    return internal_urls[SERVER_ENV]


APP_DEFINITION_API_BASE_URL = _get_base_url(
    APP_DEFINITION_API_BASE_URLS, LOCAL_APP_DEFINITION_API_BASE_URLS
)
ANALYTICS_API_BASE_URL = _get_base_url(
    ANALYTICS_API_BASE_URLS, LOCAL_ANALYTICS_API_BASE_URLS
)
WORKPLACE_API_BASE_URL = _get_base_url(
    WORKPLACE_API_BASE_URLS, LOCAL_WORKPLACE_API_BASE_URLS
)
WORKFLOW_DEFINITION_API_BASE_URL = _get_base_url(
    WORKFLOW_DEFINITION_API_BASE_URLS, LOCAL_WORKFLOW_DEFINITION_API_BASE_URLS
)
SUBMISSIONS_API_BASE_URL = _get_base_url(
    SUBMISSIONS_API_BASE_URLS, LOCAL_SUBMISSIONS_API_BASE_URLS
)
FILE_MANAGEMENT_API_BASE_URL = _get_base_url(
    FILE_MANAGEMENT_API_BASE_URLS, LOCAL_FILE_MANAGEMENT_API_BASE_URLS
)

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
