"""
workflows.py - Clappia MCP Workflows Module
Handles all workflow-related operations with clean Pydantic models
"""

from mcp.server.fastmcp import FastMCP
from src.utils.logging_utils import get_logger
from src.utils.context import get_api_key
from src.utils.constants import (
    CLAPPIA_EXTERNAL_DEV_API_BASE_URL,
    CLAPPIA_EXTERNAL_PREPROD_API_BASE_URL,
    CLAPPIA_EXTERNAL_PROD_API_BASE_URL,
)
from clappia_api_tools import WorkflowDefinitionAPIKeyClient as WorkflowDefinitionClient
from clappia_api_tools.models import (
    UpsertAiWorkflowStepRequest,
    UpsertApprovalWorkflowStepRequest,
    UpsertCodeWorkflowStepRequest,
    UpsertConditionWorkflowStepRequest,
    UpsertDatabaseWorkflowStepRequest,
    UpsertEmailWorkflowStepRequest,
    UpsertLoopWorkflowStepRequest,
    UpsertMobileNotificationWorkflowStepRequest,
    UpsertRestApiWorkflowStepRequest,
    UpsertSlackWorkflowStepRequest,
    UpsertSmsWorkflowStepRequest,
    UpsertWaitWorkflowStepRequest,
    UpsertWhatsAppWorkflowStepRequest,
    UpsertCreateSubmissionWorkflowStepRequest,
    UpsertDeleteSubmissionWorkflowStepRequest,
    UpsertFindSubmissionWorkflowStepRequest,
    UpsertEditSubmissionWorkflowStepRequest,
)

from typing import Literal, Optional, Union

WorkflowStepRequestUnion = Union[
    UpsertAiWorkflowStepRequest,
    UpsertApprovalWorkflowStepRequest,
    UpsertCodeWorkflowStepRequest,
    UpsertConditionWorkflowStepRequest,
    UpsertDatabaseWorkflowStepRequest,
    UpsertEmailWorkflowStepRequest,
    UpsertLoopWorkflowStepRequest,
    UpsertMobileNotificationWorkflowStepRequest,
    UpsertRestApiWorkflowStepRequest,
    UpsertSlackWorkflowStepRequest,
    UpsertSmsWorkflowStepRequest,
    UpsertWaitWorkflowStepRequest,
    UpsertWhatsAppWorkflowStepRequest,
    UpsertCreateSubmissionWorkflowStepRequest,
    UpsertDeleteSubmissionWorkflowStepRequest,
    UpsertFindSubmissionWorkflowStepRequest,
    UpsertEditSubmissionWorkflowStepRequest,
]

logger = get_logger(__name__)


def _get_workflow_definition_client() -> WorkflowDefinitionClient:
    api_key = get_api_key()
    return WorkflowDefinitionClient(
        api_key=api_key,
        base_url=CLAPPIA_EXTERNAL_DEV_API_BASE_URL,
    )


def register_workflow_tools(mcp: FastMCP):
    """Register all workflow-related tools with the FastMCP server"""

    @mcp.tool()
    def get_app_workflow(
        app_id: str,
        trigger_type: Literal["newSubmission", "editSubmission", "reviewSubmission"],
        version_variable_name: Optional[str] = None,
    ):
        """Retrieve the workflow configuration for a Clappia app."""

        workflow_definition_client = _get_workflow_definition_client()
        return workflow_definition_client.get_workflow(
            app_id=app_id,
            trigger_type=trigger_type,
            version_variable_name=version_variable_name,
        )

    @mcp.tool()
    def add_workflow_step(
        app_id: str,
        trigger_type: Literal["newSubmission", "editSubmission", "reviewSubmission"],
        request: WorkflowStepRequestUnion,
        step_variable_name: Optional[str] = None,
        parent_step_variable_name: Optional[str] = None,
        version_variable_name: Optional[str] = None,
    ):
        """Add a workflow step to a Clappia app's workflow. The step type is determined by the request object type."""
        workflow_definition_client = _get_workflow_definition_client()
        return workflow_definition_client.add(
            app_id=app_id,
            trigger_type=trigger_type,
            request=request,
            step_variable_name=step_variable_name,
            parent_step_variable_name=parent_step_variable_name,
            version_variable_name=version_variable_name,
        )

    @mcp.tool()
    def update_workflow_step(
        app_id: str,
        trigger_type: Literal["newSubmission", "editSubmission", "reviewSubmission"],
        step_variable_name: str,
        request: WorkflowStepRequestUnion,
        version_variable_name: Optional[str] = None,
    ):
        """Update a workflow step in a Clappia app's workflow. The step type is determined by the request object type."""
        workflow_definition_client = _get_workflow_definition_client()
        return workflow_definition_client.update(
            app_id=app_id,
            trigger_type=trigger_type,
            step_variable_name=step_variable_name,
            request=request,
            version_variable_name=version_variable_name,
        )

    @mcp.tool()
    def reorder_step(
        app_id: str,
        trigger_type: Literal["newSubmission", "editSubmission", "reviewSubmission"],
        step_variable_name: str,
        parent_step_variable_name: str,
        version_variable_name: Optional[str] = None,
    ):
        """Reorder a step in a Clappia app's workflow."""
        workflow_definition_client = _get_workflow_definition_client()
        return workflow_definition_client.reorder_step(
            app_id=app_id,
            trigger_type=trigger_type,
            step_variable_name=step_variable_name,
            parent_step_variable_name=parent_step_variable_name,
            version_variable_name=version_variable_name,
        )
