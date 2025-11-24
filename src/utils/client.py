"""
Client factory utilities for creating Clappia API clients
"""

from clappia_api_tools import (
    AnalyticsAPIKeyClient,
    AnalyticsAuthTokenClient,
    AppDefinitionAPIKeyClient,
    AppDefinitionAuthTokenClient,
    FileManagementAPIKeyClient,
    FileManagementAuthTokenClient,
    SubmissionAPIKeyClient,
    SubmissionAuthTokenClient,
    WorkflowDefinitionAPIKeyClient,
    WorkflowDefinitionAuthTokenClient,
    WorkplaceAPIKeyClient,
    WorkplaceAuthTokenClient,
)

from src.utils.constants import (
    ANALYTICS_API_BASE_URL,
    APP_DEFINITION_API_BASE_URL,
    FILE_MANAGEMENT_API_BASE_URL,
    SUBMISSIONS_API_BASE_URL,
    WORKFLOW_DEFINITION_API_BASE_URL,
    WORKPLACE_API_BASE_URL,
)
from src.utils.context import get_api_key, get_auth_token, is_local_mode


def get_analytics_client(workplace_id: str):
    if is_local_mode():
        api_key = get_api_key()
        if not api_key:
            raise ValueError(
                "CLAPPIA_API_KEY environment variable is required for local mode"
            )
        return AnalyticsAPIKeyClient(
            api_key=api_key,
            base_url=ANALYTICS_API_BASE_URL,
        )
    else:
        auth_token = get_auth_token()
        return AnalyticsAuthTokenClient(
            auth_token=auth_token,
            workplace_id=workplace_id,
            base_url=ANALYTICS_API_BASE_URL,
        )


def get_submission_client(workplace_id: str):
    if is_local_mode():
        api_key = get_api_key()
        if not api_key:
            raise ValueError(
                "CLAPPIA_API_KEY environment variable is required for local mode"
            )
        return SubmissionAPIKeyClient(
            api_key=api_key,
            base_url=SUBMISSIONS_API_BASE_URL,
        )
    else:
        auth_token = get_auth_token()
        return SubmissionAuthTokenClient(
            auth_token=auth_token,
            workplace_id=workplace_id,
            base_url=SUBMISSIONS_API_BASE_URL,
        )


def get_app_definition_client(workplace_id: str):
    if is_local_mode():
        api_key = get_api_key()
        if not api_key:
            raise ValueError(
                "CLAPPIA_API_KEY environment variable is required for local mode"
            )
        file_management_client = FileManagementAPIKeyClient(
            api_key=api_key,
            base_url=FILE_MANAGEMENT_API_BASE_URL,
        )
        return AppDefinitionAPIKeyClient(
            api_key=api_key,
            base_url=APP_DEFINITION_API_BASE_URL,
            file_management_client=file_management_client,
        )
    else:
        auth_token = get_auth_token()
        file_management_client = FileManagementAuthTokenClient(
            auth_token=auth_token,
            workplace_id=workplace_id,
            base_url=FILE_MANAGEMENT_API_BASE_URL,
        )
        return AppDefinitionAuthTokenClient(
            auth_token=auth_token,
            workplace_id=workplace_id,
            base_url=APP_DEFINITION_API_BASE_URL,
            file_management_client=file_management_client,
        )


def get_workflow_definition_client(workplace_id: str):
    if is_local_mode():
        api_key = get_api_key()
        if not api_key:
            raise ValueError(
                "CLAPPIA_API_KEY environment variable is required for local mode"
            )
        return WorkflowDefinitionAPIKeyClient(
            api_key=api_key,
            base_url=WORKFLOW_DEFINITION_API_BASE_URL,
        )
    else:
        auth_token = get_auth_token()
        return WorkflowDefinitionAuthTokenClient(
            auth_token=auth_token,
            workplace_id=workplace_id,
            base_url=WORKFLOW_DEFINITION_API_BASE_URL,
        )


def get_workplace_client(workplace_id: str):
    if is_local_mode():
        api_key = get_api_key()
        if not api_key:
            raise ValueError(
                "CLAPPIA_API_KEY environment variable is required for local mode"
            )
        return WorkplaceAPIKeyClient(
            api_key=api_key,
            base_url=WORKPLACE_API_BASE_URL,
        )
    else:
        auth_token = get_auth_token()
        return WorkplaceAuthTokenClient(
            auth_token=auth_token,
            workplace_id=workplace_id,
            base_url=WORKPLACE_API_BASE_URL,
        )


def get_file_management_client(workplace_id: str):
    if is_local_mode():
        api_key = get_api_key()
        if not api_key:
            raise ValueError(
                "CLAPPIA_API_KEY environment variable is required for local mode"
            )
        return FileManagementAPIKeyClient(
            api_key=api_key,
            base_url=FILE_MANAGEMENT_API_BASE_URL,
        )
    else:
        auth_token = get_auth_token()
        return FileManagementAuthTokenClient(
            auth_token=auth_token,
            workplace_id=workplace_id,
            base_url=FILE_MANAGEMENT_API_BASE_URL,
        )
