"""
workflows.py - Clappia MCP Workflows Module
Handles all workflow-related operations with clean Pydantic models
"""

import logging
from typing import Literal, Union

from clappia_api_tools import WorkflowDefinitionAuthTokenClient
from clappia_api_tools.models import (
    UpsertAiWorkflowStepRequest,
    UpsertApprovalWorkflowStepRequest,
    UpsertCodeWorkflowStepRequest,
    UpsertConditionWorkflowStepRequest,
    UpsertCreateSubmissionWorkflowStepRequest,
    UpsertDatabaseWorkflowStepRequest,
    UpsertDeleteSubmissionWorkflowStepRequest,
    UpsertEditSubmissionWorkflowStepRequest,
    UpsertEmailWorkflowStepRequest,
    UpsertFindSubmissionWorkflowStepRequest,
    UpsertLoopWorkflowStepRequest,
    UpsertMobileNotificationWorkflowStepRequest,
    UpsertRestApiWorkflowStepRequest,
    UpsertSlackWorkflowStepRequest,
    UpsertSmsWorkflowStepRequest,
    UpsertWaitWorkflowStepRequest,
    UpsertWhatsAppWorkflowStepRequest,
)
from mcp.server.fastmcp import FastMCP

from src.utils.constants import WORKFLOW_DEFINITION_API_BASE_URL
from src.utils.context import get_auth_token

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

logger = logging.getLogger(__name__)


def _get_workflow_definition_client(
    workplace_id: str,
) -> WorkflowDefinitionAuthTokenClient:
    auth_token = get_auth_token()
    return WorkflowDefinitionAuthTokenClient(
        auth_token=auth_token,
        workplace_id=workplace_id,
        base_url=WORKFLOW_DEFINITION_API_BASE_URL,
    )


def register_workflow_tools(mcp: FastMCP):
    """Register all workflow-related tools with the FastMCP server"""

    @mcp.tool()
    async def get_app_workflow(
        app_id: str,
        workplace_id: str,
        trigger_type: Literal["newSubmission", "editSubmission", "reviewSubmission"],
        version_variable_name: str | None = None,
    ):
        """Get workflow configuration for app.

        Args:
            app_id: ASK USER - App identifier
            workplace_id: ASK USER - Workplace identifier
            trigger_type: ASK USER - Trigger type: "newSubmission", "editSubmission", or "reviewSubmission"
            version_variable_name: App version variable name (optional)
        """

        workflow_definition_client = _get_workflow_definition_client(workplace_id)
        try:
            return await workflow_definition_client.get_workflow(
                app_id=app_id,
                trigger_type=trigger_type,
                version_variable_name=version_variable_name,
            )
        finally:
            await workflow_definition_client.close()

    @mcp.tool()
    async def add_workflow_step(
        app_id: str,
        workplace_id: str,
        trigger_type: Literal["newSubmission", "editSubmission", "reviewSubmission"],
        request: WorkflowStepRequestUnion,
        step_variable_name: str | None = None,
        parent_step_variable_name: str | None = None,
        version_variable_name: str | None = None,
    ):
        """Add workflow step to app. Step type determined by request object type.

        Args:
            app_id: ASK USER - App identifier
            workplace_id: ASK USER - Workplace identifier
            trigger_type: ASK USER - Trigger type: "newSubmission", "editSubmission", or "reviewSubmission"
            request: ASK USER - Workflow step definition request object (type determines step type)
            step_variable_name: Unique variable name for the step (optional)
            parent_step_variable_name: Parent step variable name if nested step (optional)
            version_variable_name: App version variable name (optional)
        """
        workflow_definition_client = _get_workflow_definition_client(workplace_id)
        try:
            return await workflow_definition_client.add(
                app_id=app_id,
                trigger_type=trigger_type,
                request=request,
                step_variable_name=step_variable_name,
                parent_step_variable_name=parent_step_variable_name,
                version_variable_name=version_variable_name,
            )
        finally:
            await workflow_definition_client.close()

    @mcp.tool()
    async def update_workflow_step(
        app_id: str,
        workplace_id: str,
        trigger_type: Literal["newSubmission", "editSubmission", "reviewSubmission"],
        step_variable_name: str,
        request: WorkflowStepRequestUnion,
        version_variable_name: str | None = None,
    ):
        """Update workflow step. Step type must match existing type.

        Args:
            app_id: ASK USER - App identifier
            workplace_id: ASK USER - Workplace identifier
            trigger_type: ASK USER - Trigger type: "newSubmission", "editSubmission", or "reviewSubmission"
            step_variable_name: ASK USER - Variable name of step to update
            request: ASK USER - Workflow step definition request object with updated configuration
            version_variable_name: App version variable name (optional)
        """
        workflow_definition_client = _get_workflow_definition_client(workplace_id)
        try:
            return await workflow_definition_client.update(
                app_id=app_id,
                trigger_type=trigger_type,
                step_variable_name=step_variable_name,
                request=request,
                version_variable_name=version_variable_name,
            )
        finally:
            await workflow_definition_client.close()

    @mcp.tool()
    async def reorder_step(
        app_id: str,
        workplace_id: str,
        trigger_type: Literal["newSubmission", "editSubmission", "reviewSubmission"],
        step_variable_name: str,
        parent_step_variable_name: str,
        version_variable_name: str | None = None,
    ):
        """Reorder workflow step.

        Args:
            app_id: ASK USER - App identifier
            workplace_id: ASK USER - Workplace identifier
            trigger_type: ASK USER - Trigger type: "newSubmission", "editSubmission", or "reviewSubmission"
            step_variable_name: ASK USER - Variable name of step to move
            parent_step_variable_name: ASK USER - Variable name of new parent step
            version_variable_name: App version variable name (optional)
        """
        workflow_definition_client = _get_workflow_definition_client(workplace_id)
        try:
            return await workflow_definition_client.reorder_step(
                app_id=app_id,
                trigger_type=trigger_type,
                step_variable_name=step_variable_name,
                parent_step_variable_name=parent_step_variable_name,
                version_variable_name=version_variable_name,
            )
        finally:
            await workflow_definition_client.close()
