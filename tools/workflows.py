from mcp.server.fastmcp import FastMCP
from utils import get_logger, workflow_definition_client
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
    WorkflowResponse,
    WorkflowStepResponse,
)

from typing import Optional, Union

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


def register_workflow_tools(mcp: FastMCP):
    """Register all workflow-related tools with the FastMCP server"""

    @mcp.tool()
    def get_app_workflow(app_id: str, trigger_type: str) -> WorkflowResponse:
        """Retrieve the workflow configuration for a Clappia app.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            trigger_type (str): The trigger type of the workflow. allowed values are newSubmission, editSubmission, reviewSubmission. allowed values are newSubmission, editSubmission, reviewSubmission.

        Returns:
            WorkflowResponse: The response object containing the workflow configuration.
        """

        return workflow_definition_client.get_workflow(
            app_id=app_id, trigger_type=trigger_type
        )

    @mcp.tool()
    def add_workflow_step(
        app_id: str,
        trigger_type: str,
        request: WorkflowStepRequestUnion,
        step_variable_name: Optional[str] = None,
        parent_step_variable_name: Optional[str] = None,
    ) -> WorkflowStepResponse:
        """
        Adds a workflow step to a Clappia app's workflow. The step type is determined by the request object type.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            trigger_type (str): The trigger type of the workflow. allowed values are newSubmission, editSubmission, reviewSubmission.
            request (WorkflowStepRequestUnion): The request object containing step configuration. The step type is determined by the specific request type.
            step_variable_name (Optional[str]): The variable name of the step, if not provided, a random variable name will be generated.
            parent_step_variable_name (Optional[str]): The variable name of the parent step, below which the new step will be added. If not provided, the new step will be added to the start of the workflow, else it will be added below the parent step.

        Returns:
            WorkflowStepResponse: The response object containing the result of the step addition.

        Raises:
            Exception: Any error raised by the underlying step addition method.
        """
        return workflow_definition_client.add(
            app_id=app_id,
            trigger_type=trigger_type,
            request=request,
            step_variable_name=step_variable_name,
            parent_step_variable_name=parent_step_variable_name,
        )

    @mcp.tool()
    def update_workflow_step(
        app_id: str,
        trigger_type: str,
        step_variable_name: str,
        request: WorkflowStepRequestUnion,
    ) -> WorkflowStepResponse:
        """
        Updates a workflow step in a Clappia app's workflow. The step type is determined by the request object type.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            trigger_type (str): The trigger type of the workflow. allowed values are newSubmission, editSubmission, reviewSubmission.
            step_variable_name (str): The variable name of the step to update.
            request (WorkflowStepRequestUnion): The request object containing step configuration. The step type is determined by the specific request type.

        Returns:
            WorkflowStepResponse: The response object containing the result of the step update.

        Raises:
            Exception: Any error raised by the underlying step update method.
        """
        return workflow_definition_client.update(
            app_id=app_id,
            trigger_type=trigger_type,
            step_variable_name=step_variable_name,
            request=request,
        )


    @mcp.tool()
    def reorder_step(
        app_id: str,
        trigger_type: str,
        step_variable_name: str,
        parent_step_variable_name: str,
    ) -> WorkflowStepResponse:
        """Reorder steps in a Clappia app's workflow.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            trigger_type (str): The trigger type of the workflow. allowed values are newSubmission, editSubmission, reviewSubmission. allowed values are newSubmission, editSubmission, reviewSubmission.
            step_variable_name (str): The variable name of the step to reorder.
            parent_step_variable_name (str): The variable name of the parent step, below which the step will be moved.
        """
        return workflow_definition_client.reorder_step(
            app_id=app_id,
            trigger_type=trigger_type,
            step_variable_name=step_variable_name,
            parent_step_variable_name=parent_step_variable_name,
        )


