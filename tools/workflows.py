from typing import Union, Optional
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

# Union type for all workflow step request types
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

from typing import Optional


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

    def add_ai_step(
        app_id: str,
        trigger_type: str,
        request: UpsertAiWorkflowStepRequest,
        step_variable_name: Optional[str] = None,
        parent_step_variable_name: Optional[str] = None,
    ) -> WorkflowStepResponse:
        """Add an AI step to a Clappia app's workflow.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            trigger_type (str): The trigger type of the workflow. allowed values are newSubmission, editSubmission, reviewSubmission.
            request (UpsertAiWorkflowStepRequest): The request object containing the AI step details.
            step_variable_name (Optional[str]): The variable name of the step, if not provided, a random variable name will be generated.
            parent_step_variable_name (Optional[str]): The variable name of the parent step, below which the new step will be added. If not provided, the new step will be added to the start of the workflow, else it will be added below the parent step.

        """

        return workflow_definition_client.add_ai_step(
            app_id=app_id,
            trigger_type=trigger_type,
            request=request,
            step_variable_name=step_variable_name,
            parent_step_variable_name=parent_step_variable_name,
        )

    def update_ai_step(
        app_id: str,
        trigger_type: str,
        step_variable_name: str,
        request: UpsertAiWorkflowStepRequest,
    ) -> WorkflowStepResponse:
        """Update an AI step in a Clappia app's workflow.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            trigger_type (str): The trigger type of the workflow. allowed values are newSubmission, editSubmission, reviewSubmission. allowed values are newSubmission, editSubmission, reviewSubmission.
            step_variable_name (str): The variable name of the step to update.
            request (UpsertAiWorkflowStepRequest): The request object containing the updated AI step details.
        """
        return workflow_definition_client.update_ai_step(
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

    @mcp.tool()
    def add_workflow_step(
        app_id: str,
        trigger_type: str,
        request: WorkflowStepRequestUnion,
        step_variable_name: Optional[str] = None,
        parent_step_variable_name: Optional[str] = None,
    ) -> WorkflowStepResponse:
        """
        Adds a workflow step to a Clappia app. The step type is determined by the request object type.

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
        # Determine step type based on request type and call appropriate function
        if isinstance(request, UpsertAiWorkflowStepRequest):
            return add_ai_step(app_id, trigger_type, request, step_variable_name, parent_step_variable_name)
        elif isinstance(request, UpsertApprovalWorkflowStepRequest):
            return add_approval_step(app_id, trigger_type, request, step_variable_name, parent_step_variable_name)
        elif isinstance(request, UpsertCodeWorkflowStepRequest):
            return add_code_step(app_id, trigger_type, request, step_variable_name, parent_step_variable_name)
        elif isinstance(request, UpsertConditionWorkflowStepRequest):
            return add_condition_step(app_id, trigger_type, request, step_variable_name, parent_step_variable_name)
        elif isinstance(request, UpsertDatabaseWorkflowStepRequest):
            return add_database_step(app_id, trigger_type, request, step_variable_name, parent_step_variable_name)
        elif isinstance(request, UpsertEmailWorkflowStepRequest):
            return add_email_step(app_id, trigger_type, request, step_variable_name, parent_step_variable_name)
        elif isinstance(request, UpsertLoopWorkflowStepRequest):
            return add_loop_step(app_id, trigger_type, request, step_variable_name, parent_step_variable_name)
        elif isinstance(request, UpsertMobileNotificationWorkflowStepRequest):
            return add_mobile_notification_step(app_id, trigger_type, request, step_variable_name, parent_step_variable_name)
        elif isinstance(request, UpsertRestApiWorkflowStepRequest):
            return add_rest_api_step(app_id, trigger_type, request, step_variable_name, parent_step_variable_name)
        elif isinstance(request, UpsertSlackWorkflowStepRequest):
            return add_slack_step(app_id, trigger_type, request, step_variable_name, parent_step_variable_name)
        elif isinstance(request, UpsertSmsWorkflowStepRequest):
            return add_sms_step(app_id, trigger_type, request, step_variable_name, parent_step_variable_name)
        elif isinstance(request, UpsertWaitWorkflowStepRequest):
            return add_wait_step(app_id, trigger_type, request, step_variable_name, parent_step_variable_name)
        elif isinstance(request, UpsertWhatsAppWorkflowStepRequest):
            return add_whatsapp_step(app_id, trigger_type, request, step_variable_name, parent_step_variable_name)
        elif isinstance(request, UpsertCreateSubmissionWorkflowStepRequest):
            return add_create_submission_step(app_id, trigger_type, request, step_variable_name, parent_step_variable_name)
        elif isinstance(request, UpsertDeleteSubmissionWorkflowStepRequest):
            return add_delete_submission_step(app_id, trigger_type, request, step_variable_name, parent_step_variable_name)
        elif isinstance(request, UpsertFindSubmissionWorkflowStepRequest):
            return add_find_submission_step(app_id, trigger_type, request, step_variable_name, parent_step_variable_name)
        elif isinstance(request, UpsertEditSubmissionWorkflowStepRequest):
            return add_edit_submission_step(app_id, trigger_type, request, step_variable_name, parent_step_variable_name)
        else:
            raise ValueError(f"Unsupported workflow step request type: {type(request)}")

    @mcp.tool()
    def update_workflow_step(
        app_id: str,
        trigger_type: str,
        step_variable_name: str,
        request: WorkflowStepRequestUnion,
    ) -> WorkflowStepResponse:
        """
        Updates a workflow step in a Clappia app. The step type is determined by the request object type.

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
        # Determine step type based on request type and call appropriate function
        if isinstance(request, UpsertAiWorkflowStepRequest):
            return update_ai_step(app_id, trigger_type, step_variable_name, request)
        elif isinstance(request, UpsertApprovalWorkflowStepRequest):
            return update_approval_step(app_id, trigger_type, step_variable_name, request)
        elif isinstance(request, UpsertCodeWorkflowStepRequest):
            return update_code_step(app_id, trigger_type, step_variable_name, request)
        elif isinstance(request, UpsertConditionWorkflowStepRequest):
            return update_condition_step(app_id, trigger_type, step_variable_name, request)
        elif isinstance(request, UpsertDatabaseWorkflowStepRequest):
            return update_database_step(app_id, trigger_type, step_variable_name, request)
        elif isinstance(request, UpsertEmailWorkflowStepRequest):
            return update_email_step(app_id, trigger_type, step_variable_name, request)
        elif isinstance(request, UpsertLoopWorkflowStepRequest):
            return update_loop_step(app_id, trigger_type, step_variable_name, request)
        elif isinstance(request, UpsertMobileNotificationWorkflowStepRequest):
            return update_mobile_notification_step(app_id, trigger_type, step_variable_name, request)
        elif isinstance(request, UpsertRestApiWorkflowStepRequest):
            return update_rest_api_step(app_id, trigger_type, step_variable_name, request)
        elif isinstance(request, UpsertSlackWorkflowStepRequest):
            return update_slack_step(app_id, trigger_type, step_variable_name, request)
        elif isinstance(request, UpsertSmsWorkflowStepRequest):
            return update_sms_step(app_id, trigger_type, step_variable_name, request)
        elif isinstance(request, UpsertWaitWorkflowStepRequest):
            return update_wait_step(app_id, trigger_type, step_variable_name, request)
        elif isinstance(request, UpsertWhatsAppWorkflowStepRequest):
            return update_whatsapp_step(app_id, trigger_type, step_variable_name, request)
        elif isinstance(request, UpsertCreateSubmissionWorkflowStepRequest):
            return update_create_submission_step(app_id, trigger_type, step_variable_name, request)
        elif isinstance(request, UpsertDeleteSubmissionWorkflowStepRequest):
            return update_delete_submission_step(app_id, trigger_type, step_variable_name, request)
        elif isinstance(request, UpsertFindSubmissionWorkflowStepRequest):
            return update_find_submission_step(app_id, trigger_type, step_variable_name, request)
        elif isinstance(request, UpsertEditSubmissionWorkflowStepRequest):
            return update_edit_submission_step(app_id, trigger_type, step_variable_name, request)
        else:
            raise ValueError(f"Unsupported workflow step request type: {type(request)}")

    # Approval Workflow Step Tools
    def add_approval_step(
        app_id: str,
        trigger_type: str,
        request: UpsertApprovalWorkflowStepRequest,
        step_variable_name: Optional[str] = None,
        parent_step_variable_name: Optional[str] = None,
    ) -> WorkflowStepResponse:
        """Add an approval step to a Clappia app's workflow.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            trigger_type (str): The trigger type of the workflow. allowed values are newSubmission, editSubmission, reviewSubmission.
            request (UpsertApprovalWorkflowStepRequest): The request object containing the approval step details.
            step_variable_name (Optional[str]): The variable name of the step, if not provided, a random variable name will be generated.
            parent_step_variable_name (Optional[str]): The variable name of the parent step, below which the new step will be added. If not provided, the new step will be added to the start of the workflow, else it will be added below the parent step..
        """
        return workflow_definition_client.add_approval_step(
            app_id=app_id,
            trigger_type=trigger_type,
            request=request,
            step_variable_name=step_variable_name,
            parent_step_variable_name=parent_step_variable_name,
        )

    def update_approval_step(
        app_id: str,
        trigger_type: str,
        step_variable_name: str,
        request: UpsertApprovalWorkflowStepRequest,
    ) -> WorkflowStepResponse:
        """Update an approval step in a Clappia app's workflow.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            trigger_type (str): The trigger type of the workflow. allowed values are newSubmission, editSubmission, reviewSubmission. allowed values are newSubmission, editSubmission, reviewSubmission.
            step_variable_name (str): The variable name of the step to update.
            request (UpsertApprovalWorkflowStepRequest): The request object containing the updated approval step details.
        """
        return workflow_definition_client.update_approval_step(
            app_id=app_id,
            trigger_type=trigger_type,
            step_variable_name=step_variable_name,
            request=request,
        )

    # Code Workflow Step Tools
    def add_code_step(
        app_id: str,
        trigger_type: str,
        request: UpsertCodeWorkflowStepRequest,
        step_variable_name: Optional[str] = None,
        parent_step_variable_name: Optional[str] = None,
    ) -> WorkflowStepResponse:
        """Add a code step to a Clappia app's workflow.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            trigger_type (str): The trigger type of the workflow. allowed values are newSubmission, editSubmission, reviewSubmission.
            request (UpsertCodeWorkflowStepRequest): The request object containing the code step details.
            step_variable_name (Optional[str]): The variable name of the step, if not provided, a random variable name will be generated.
            parent_step_variable_name (Optional[str]): The variable name of the parent step, below which the new step will be added. If not provided, the new step will be added to the start of the workflow, else it will be added below the parent step..
        """
        return workflow_definition_client.add_code_step(
            app_id=app_id,
            trigger_type=trigger_type,
            request=request,
            step_variable_name=step_variable_name,
            parent_step_variable_name=parent_step_variable_name,
        )

    def update_code_step(
        app_id: str,
        trigger_type: str,
        step_variable_name: str,
        request: UpsertCodeWorkflowStepRequest,
    ) -> WorkflowStepResponse:
        """Update a code step in a Clappia app's workflow.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            trigger_type (str): The trigger type of the workflow. allowed values are newSubmission, editSubmission, reviewSubmission. allowed values are newSubmission, editSubmission, reviewSubmission.
            step_variable_name (str): The variable name of the step to update.
            request (UpsertCodeWorkflowStepRequest): The request object containing the updated code step details.
        """
        return workflow_definition_client.update_code_step(
            app_id=app_id,
            trigger_type=trigger_type,
            step_variable_name=step_variable_name,
            request=request,
        )

    # Condition Workflow Step Tools
    def add_condition_step(
        app_id: str,
        trigger_type: str,
        request: UpsertConditionWorkflowStepRequest,
        step_variable_name: Optional[str] = None,
        parent_step_variable_name: Optional[str] = None,
    ) -> WorkflowStepResponse:
        """Add a condition step to a Clappia app's workflow.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            trigger_type (str): The trigger type of the workflow. allowed values are newSubmission, editSubmission, reviewSubmission.
            request (UpsertConditionWorkflowStepRequest): The request object containing the condition step details.
            step_variable_name (Optional[str]): The variable name of the step, if not provided, a random variable name will be generated.
            parent_step_variable_name (Optional[str]): The variable name of the parent step, below which the new step will be added. If not provided, the new step will be added to the start of the workflow, else it will be added below the parent step..
        """
        return workflow_definition_client.add_condition_step(
            app_id=app_id,
            trigger_type=trigger_type,
            request=request,
            step_variable_name=step_variable_name,
            parent_step_variable_name=parent_step_variable_name,
        )

    def update_condition_step(
        app_id: str,
        trigger_type: str,
        step_variable_name: str,
        request: UpsertConditionWorkflowStepRequest,
    ) -> WorkflowStepResponse:
        """Update a condition step in a Clappia app's workflow.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            trigger_type (str): The trigger type of the workflow. allowed values are newSubmission, editSubmission, reviewSubmission. allowed values are newSubmission, editSubmission, reviewSubmission.
            step_variable_name (str): The variable name of the step to update.
            request (UpsertConditionWorkflowStepRequest): The request object containing the updated condition step details.
        """
        return workflow_definition_client.update_condition_step(
            app_id=app_id,
            trigger_type=trigger_type,
            step_variable_name=step_variable_name,
            request=request,
        )

    # Database Workflow Step Tools
    def add_database_step(
        app_id: str,
        trigger_type: str,
        request: UpsertDatabaseWorkflowStepRequest,
        step_variable_name: Optional[str] = None,
        parent_step_variable_name: Optional[str] = None,
    ) -> WorkflowStepResponse:
        """Add a database step to a Clappia app's workflow.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            trigger_type (str): The trigger type of the workflow. allowed values are newSubmission, editSubmission, reviewSubmission.
            request (UpsertDatabaseWorkflowStepRequest): The request object containing the database step details.
            step_variable_name (Optional[str]): The variable name of the step, if not provided, a random variable name will be generated.
            parent_step_variable_name (Optional[str]): The variable name of the parent step, below which the new step will be added. If not provided, the new step will be added to the start of the workflow, else it will be added below the parent step..
        """
        return workflow_definition_client.add_database_step(
            app_id=app_id,
            trigger_type=trigger_type,
            request=request,
            step_variable_name=step_variable_name,
            parent_step_variable_name=parent_step_variable_name,
        )

    def update_database_step(
        app_id: str,
        trigger_type: str,
        step_variable_name: str,
        request: UpsertDatabaseWorkflowStepRequest,
    ) -> WorkflowStepResponse:
        """Update a database step in a Clappia app's workflow.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            trigger_type (str): The trigger type of the workflow. allowed values are newSubmission, editSubmission, reviewSubmission. allowed values are newSubmission, editSubmission, reviewSubmission.
            step_variable_name (str): The variable name of the step to update.
            request (UpsertDatabaseWorkflowStepRequest): The request object containing the updated database step details.
        """
        return workflow_definition_client.update_database_step(
            app_id=app_id,
            trigger_type=trigger_type,
            step_variable_name=step_variable_name,
            request=request,
        )

    # Email Workflow Step Tools
    def add_email_step(
        app_id: str,
        trigger_type: str,
        request: UpsertEmailWorkflowStepRequest,
        step_variable_name: Optional[str] = None,
        parent_step_variable_name: Optional[str] = None,
    ) -> WorkflowStepResponse:
        """Add an email step to a Clappia app's workflow.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            trigger_type (str): The trigger type of the workflow. allowed values are newSubmission, editSubmission, reviewSubmission.
            request (UpsertEmailWorkflowStepRequest): The request object containing the email step details.
            step_variable_name (Optional[str]): The variable name of the step, if not provided, a random variable name will be generated.
            parent_step_variable_name (Optional[str]): The variable name of the parent step, below which the new step will be added. If not provided, the new step will be added to the start of the workflow, else it will be added below the parent step..
        """
        return workflow_definition_client.add_email_step(
            app_id=app_id,
            trigger_type=trigger_type,
            request=request,
            step_variable_name=step_variable_name,
            parent_step_variable_name=parent_step_variable_name,
        )

    def update_email_step(
        app_id: str,
        trigger_type: str,
        step_variable_name: str,
        request: UpsertEmailWorkflowStepRequest,
    ) -> WorkflowStepResponse:
        """Update an email step in a Clappia app's workflow.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            trigger_type (str): The trigger type of the workflow. allowed values are newSubmission, editSubmission, reviewSubmission. allowed values are newSubmission, editSubmission, reviewSubmission.
            step_variable_name (str): The variable name of the step to update.
            request (UpsertEmailWorkflowStepRequest): The request object containing the updated email step details.
        """
        return workflow_definition_client.update_email_step(
            app_id=app_id,
            trigger_type=trigger_type,
            step_variable_name=step_variable_name,
            request=request,
        )

    # Loop Workflow Step Tools
    def add_loop_step(
        app_id: str,
        trigger_type: str,
        request: UpsertLoopWorkflowStepRequest,
        step_variable_name: Optional[str] = None,
        parent_step_variable_name: Optional[str] = None,
    ) -> WorkflowStepResponse:
        """Add a loop step to a Clappia app's workflow.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            trigger_type (str): The trigger type of the workflow. allowed values are newSubmission, editSubmission, reviewSubmission.
            request (UpsertLoopWorkflowStepRequest): The request object containing the loop step details.
            step_variable_name (Optional[str]): The variable name of the step, if not provided, a random variable name will be generated.
            parent_step_variable_name (Optional[str]): The variable name of the parent step, below which the new step will be added. If not provided, the new step will be added to the start of the workflow, else it will be added below the parent step..
        """
        return workflow_definition_client.add_loop_step(
            app_id=app_id,
            trigger_type=trigger_type,
            request=request,
            step_variable_name=step_variable_name,
            parent_step_variable_name=parent_step_variable_name,
        )

    def update_loop_step(
        app_id: str,
        trigger_type: str,
        step_variable_name: str,
        request: UpsertLoopWorkflowStepRequest,
    ) -> WorkflowStepResponse:
        """Update a loop step in a Clappia app's workflow.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            trigger_type (str): The trigger type of the workflow. allowed values are newSubmission, editSubmission, reviewSubmission. allowed values are newSubmission, editSubmission, reviewSubmission.
            step_variable_name (str): The variable name of the step to update.
            request (UpsertLoopWorkflowStepRequest): The request object containing the updated loop step details.
        """
        return workflow_definition_client.update_loop_step(
            app_id=app_id,
            trigger_type=trigger_type,
            step_variable_name=step_variable_name,
            request=request,
        )

    # Mobile Notification Workflow Step Tools
    def add_mobile_notification_step(
        app_id: str,
        trigger_type: str,
        request: UpsertMobileNotificationWorkflowStepRequest,
        step_variable_name: Optional[str] = None,
        parent_step_variable_name: Optional[str] = None,
    ) -> WorkflowStepResponse:
        """Add a mobile notification step to a Clappia app's workflow.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            trigger_type (str): The trigger type of the workflow. allowed values are newSubmission, editSubmission, reviewSubmission.
            request (UpsertMobileNotificationWorkflowStepRequest): The request object containing the mobile notification step details.
            step_variable_name (Optional[str]): The variable name of the step, if not provided, a random variable name will be generated.
            parent_step_variable_name (Optional[str]): The variable name of the parent step, below which the new step will be added. If not provided, the new step will be added to the start of the workflow, else it will be added below the parent step..
        """
        return workflow_definition_client.add_mobile_notification_step(
            app_id=app_id,
            trigger_type=trigger_type,
            request=request,
            step_variable_name=step_variable_name,
            parent_step_variable_name=parent_step_variable_name,
        )

    def update_mobile_notification_step(
        app_id: str,
        trigger_type: str,
        step_variable_name: str,
        request: UpsertMobileNotificationWorkflowStepRequest,
    ) -> WorkflowStepResponse:
        """Update a mobile notification step in a Clappia app's workflow.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            trigger_type (str): The trigger type of the workflow. allowed values are newSubmission, editSubmission, reviewSubmission. allowed values are newSubmission, editSubmission, reviewSubmission.
            step_variable_name (str): The variable name of the step to update.
            request (UpsertMobileNotificationWorkflowStepRequest): The request object containing the updated mobile notification step details.
        """
        return workflow_definition_client.update_mobile_notification_step(
            app_id=app_id,
            trigger_type=trigger_type,
            step_variable_name=step_variable_name,
            request=request,
        )

    # REST API Workflow Step Tools
    def add_rest_api_step(
        app_id: str,
        trigger_type: str,
        request: UpsertRestApiWorkflowStepRequest,
        step_variable_name: Optional[str] = None,
        parent_step_variable_name: Optional[str] = None,
    ) -> WorkflowStepResponse:
        """Add a REST API step to a Clappia app's workflow.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            trigger_type (str): The trigger type of the workflow. allowed values are newSubmission, editSubmission, reviewSubmission.
            request (UpsertRestApiWorkflowStepRequest): The request object containing the REST API step details.
            step_variable_name (Optional[str]): The variable name of the step, if not provided, a random variable name will be generated.
            parent_step_variable_name (Optional[str]): The variable name of the parent step, below which the new step will be added. If not provided, the new step will be added to the start of the workflow, else it will be added below the parent step..
        """
        return workflow_definition_client.add_rest_api_step(
            app_id=app_id,
            trigger_type=trigger_type,
            request=request,
            step_variable_name=step_variable_name,
            parent_step_variable_name=parent_step_variable_name,
        )

    def update_rest_api_step(
        app_id: str,
        trigger_type: str,
        step_variable_name: str,
        request: UpsertRestApiWorkflowStepRequest,
    ) -> WorkflowStepResponse:
        """Update a REST API step in a Clappia app's workflow.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            trigger_type (str): The trigger type of the workflow. allowed values are newSubmission, editSubmission, reviewSubmission. allowed values are newSubmission, editSubmission, reviewSubmission.
            step_variable_name (str): The variable name of the step to update.
            request (UpsertRestApiWorkflowStepRequest): The request object containing the updated REST API step details.
        """
        return workflow_definition_client.update_rest_api_step(
            app_id=app_id,
            trigger_type=trigger_type,
            step_variable_name=step_variable_name,
            request=request,
        )

    # Slack Workflow Step Tools
    def add_slack_step(
        app_id: str,
        trigger_type: str,
        request: UpsertSlackWorkflowStepRequest,
        step_variable_name: Optional[str] = None,
        parent_step_variable_name: Optional[str] = None,
    ) -> WorkflowStepResponse:
        """Add a Slack step to a Clappia app's workflow.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            trigger_type (str): The trigger type of the workflow. allowed values are newSubmission, editSubmission, reviewSubmission.
            request (UpsertSlackWorkflowStepRequest): The request object containing the Slack step details.
            step_variable_name (Optional[str]): The variable name of the step, if not provided, a random variable name will be generated.
            parent_step_variable_name (Optional[str]): The variable name of the parent step, below which the new step will be added. If not provided, the new step will be added to the start of the workflow, else it will be added below the parent step..
        """
        return workflow_definition_client.add_slack_step(
            app_id=app_id,
            trigger_type=trigger_type,
            request=request,
            step_variable_name=step_variable_name,
            parent_step_variable_name=parent_step_variable_name,
        )

    def update_slack_step(
        app_id: str,
        trigger_type: str,
        step_variable_name: str,
        request: UpsertSlackWorkflowStepRequest,
    ) -> WorkflowStepResponse:
        """Update a Slack step in a Clappia app's workflow.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            trigger_type (str): The trigger type of the workflow. allowed values are newSubmission, editSubmission, reviewSubmission. allowed values are newSubmission, editSubmission, reviewSubmission.
            step_variable_name (str): The variable name of the step to update.
            request (UpsertSlackWorkflowStepRequest): The request object containing the updated Slack step details.
        """
        return workflow_definition_client.update_slack_step(
            app_id=app_id,
            trigger_type=trigger_type,
            step_variable_name=step_variable_name,
            request=request,
        )

    # SMS Workflow Step Tools
    def add_sms_step(
        app_id: str,
        trigger_type: str,
        request: UpsertSmsWorkflowStepRequest,
        step_variable_name: Optional[str] = None,
        parent_step_variable_name: Optional[str] = None,
    ) -> WorkflowStepResponse:
        """Add an SMS step to a Clappia app's workflow.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            trigger_type (str): The trigger type of the workflow. allowed values are newSubmission, editSubmission, reviewSubmission.
            request (UpsertSmsWorkflowStepRequest): The request object containing the SMS step details.
            step_variable_name (Optional[str]): The variable name of the step, if not provided, a random variable name will be generated.
            parent_step_variable_name (Optional[str]): The variable name of the parent step, below which the new step will be added. If not provided, the new step will be added to the start of the workflow, else it will be added below the parent step..
        """
        return workflow_definition_client.add_sms_step(
            app_id=app_id,
            trigger_type=trigger_type,
            request=request,
            step_variable_name=step_variable_name,
            parent_step_variable_name=parent_step_variable_name,
        )

    def update_sms_step(
        app_id: str,
        trigger_type: str,
        step_variable_name: str,
        request: UpsertSmsWorkflowStepRequest,
    ) -> WorkflowStepResponse:
        """Update an SMS step in a Clappia app's workflow.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            trigger_type (str): The trigger type of the workflow. allowed values are newSubmission, editSubmission, reviewSubmission. allowed values are newSubmission, editSubmission, reviewSubmission.
            step_variable_name (str): The variable name of the step to update.
            request (UpsertSmsWorkflowStepRequest): The request object containing the updated SMS step details.
        """
        return workflow_definition_client.update_sms_step(
            app_id=app_id,
            trigger_type=trigger_type,
            step_variable_name=step_variable_name,
            request=request,
        )

    # Wait Workflow Step Tools
    def add_wait_step(
        app_id: str,
        trigger_type: str,
        request: UpsertWaitWorkflowStepRequest,
        step_variable_name: Optional[str] = None,
        parent_step_variable_name: Optional[str] = None,
    ) -> WorkflowStepResponse:
        """Add a wait step to a Clappia app's workflow.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            trigger_type (str): The trigger type of the workflow. allowed values are newSubmission, editSubmission, reviewSubmission.
            request (UpsertWaitWorkflowStepRequest): The request object containing the wait step details.
            step_variable_name (Optional[str]): The variable name of the step, if not provided, a random variable name will be generated.
            parent_step_variable_name (Optional[str]): The variable name of the parent step, below which the new step will be added. If not provided, the new step will be added to the start of the workflow, else it will be added below the parent step..
        """
        return workflow_definition_client.add_wait_step(
            app_id=app_id,
            trigger_type=trigger_type,
            request=request,
            step_variable_name=step_variable_name,
            parent_step_variable_name=parent_step_variable_name,
        )

    def update_wait_step(
        app_id: str,
        trigger_type: str,
        step_variable_name: str,
        request: UpsertWaitWorkflowStepRequest,
    ) -> WorkflowStepResponse:
        """Update a wait step in a Clappia app's workflow.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            trigger_type (str): The trigger type of the workflow. allowed values are newSubmission, editSubmission, reviewSubmission. allowed values are newSubmission, editSubmission, reviewSubmission.
            step_variable_name (str): The variable name of the step to update.
            request (UpsertWaitWorkflowStepRequest): The request object containing the updated wait step details.
        """
        return workflow_definition_client.update_wait_step(
            app_id=app_id,
            trigger_type=trigger_type,
            step_variable_name=step_variable_name,
            request=request,
        )

    # WhatsApp Workflow Step Tools
    def add_whatsapp_step(
        app_id: str,
        trigger_type: str,
        request: UpsertWhatsAppWorkflowStepRequest,
        step_variable_name: Optional[str] = None,
        parent_step_variable_name: Optional[str] = None,
    ) -> WorkflowStepResponse:
        """Add a WhatsApp step to a Clappia app's workflow.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            trigger_type (str): The trigger type of the workflow. allowed values are newSubmission, editSubmission, reviewSubmission.
            request (UpsertWhatsAppWorkflowStepRequest): The request object containing the WhatsApp step details.
            step_variable_name (Optional[str]): The variable name of the step, if not provided, a random variable name will be generated.
            parent_step_variable_name (Optional[str]): The variable name of the parent step, below which the new step will be added. If not provided, the new step will be added to the start of the workflow, else it will be added below the parent step..
        """
        return workflow_definition_client.add_whatsapp_step(
            app_id=app_id,
            trigger_type=trigger_type,
            request=request,
            step_variable_name=step_variable_name,
            parent_step_variable_name=parent_step_variable_name,
        )

    def update_whatsapp_step(
        app_id: str,
        trigger_type: str,
        step_variable_name: str,
        request: UpsertWhatsAppWorkflowStepRequest,
    ) -> WorkflowStepResponse:
        """Update a WhatsApp step in a Clappia app's workflow.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            trigger_type (str): The trigger type of the workflow. allowed values are newSubmission, editSubmission, reviewSubmission. allowed values are newSubmission, editSubmission, reviewSubmission.
            step_variable_name (str): The variable name of the step to update.
            request (UpsertWhatsAppWorkflowStepRequest): The request object containing the updated WhatsApp step details.
        """
        return workflow_definition_client.update_whatsapp_step(
            app_id=app_id,
            trigger_type=trigger_type,
            step_variable_name=step_variable_name,
            request=request,
        )

    # Create Submission Workflow Step Tools
    def add_create_submission_step(
        app_id: str,
        trigger_type: str,
        request: UpsertCreateSubmissionWorkflowStepRequest,
        step_variable_name: Optional[str] = None,
        parent_step_variable_name: Optional[str] = None,
    ) -> WorkflowStepResponse:
        """Add a create submission step to a Clappia app's workflow.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            trigger_type (str): The trigger type of the workflow. allowed values are newSubmission, editSubmission, reviewSubmission.
            request (UpsertCreateSubmissionWorkflowStepRequest): The request object containing the create submission step details.
            step_variable_name (Optional[str]): The variable name of the step, if not provided, a random variable name will be generated.
            parent_step_variable_name (Optional[str]): The variable name of the parent step, below which the new step will be added. If not provided, the new step will be added to the start of the workflow, else it will be added below the parent step..
        """
        return workflow_definition_client.add_create_submission_step(
            app_id=app_id,
            trigger_type=trigger_type,
            request=request,
            step_variable_name=step_variable_name,
            parent_step_variable_name=parent_step_variable_name,
        )

    def update_create_submission_step(
        app_id: str,
        trigger_type: str,
        step_variable_name: str,
        request: UpsertCreateSubmissionWorkflowStepRequest,
    ) -> WorkflowStepResponse:
        """Update a create submission step in a Clappia app's workflow.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            trigger_type (str): The trigger type of the workflow. allowed values are newSubmission, editSubmission, reviewSubmission. allowed values are newSubmission, editSubmission, reviewSubmission.
            step_variable_name (str): The variable name of the step to update.
            request (UpsertCreateSubmissionWorkflowStepRequest): The request object containing the updated create submission step details.
        """
        return workflow_definition_client.update_create_submission_step(
            app_id=app_id,
            trigger_type=trigger_type,
            step_variable_name=step_variable_name,
            request=request,
        )

    # Delete Submission Workflow Step Tools
    def add_delete_submission_step(
        app_id: str,
        trigger_type: str,
        request: UpsertDeleteSubmissionWorkflowStepRequest,
        step_variable_name: Optional[str] = None,
        parent_step_variable_name: Optional[str] = None,
    ) -> WorkflowStepResponse:
        """Add a delete submission step to a Clappia app's workflow.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            trigger_type (str): The trigger type of the workflow. allowed values are newSubmission, editSubmission, reviewSubmission.
            request (UpsertDeleteSubmissionWorkflowStepRequest): The request object containing the delete submission step details.
            step_variable_name (Optional[str]): The variable name of the step, if not provided, a random variable name will be generated.
            parent_step_variable_name (Optional[str]): The variable name of the parent step, below which the new step will be added. If not provided, the new step will be added to the start of the workflow, else it will be added below the parent step..
        """
        return workflow_definition_client.add_delete_submission_step(
            app_id=app_id,
            trigger_type=trigger_type,
            request=request,
            step_variable_name=step_variable_name,
            parent_step_variable_name=parent_step_variable_name,
        )

    def update_delete_submission_step(
        app_id: str,
        trigger_type: str,
        step_variable_name: str,
        request: UpsertDeleteSubmissionWorkflowStepRequest,
    ) -> WorkflowStepResponse:
        """Update a delete submission step in a Clappia app's workflow.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            trigger_type (str): The trigger type of the workflow. allowed values are newSubmission, editSubmission, reviewSubmission. allowed values are newSubmission, editSubmission, reviewSubmission.
            step_variable_name (str): The variable name of the step to update.
            request (UpsertDeleteSubmissionWorkflowStepRequest): The request object containing the updated delete submission step details.
        """
        return workflow_definition_client.update_delete_submission_step(
            app_id=app_id,
            trigger_type=trigger_type,
            step_variable_name=step_variable_name,
            request=request,
        )

    # Find Submission Workflow Step Tools
    def add_find_submission_step(
        app_id: str,
        trigger_type: str,
        request: UpsertFindSubmissionWorkflowStepRequest,
        step_variable_name: Optional[str] = None,
        parent_step_variable_name: Optional[str] = None,
    ) -> WorkflowStepResponse:
        """Add a find submission step to a Clappia app's workflow.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            trigger_type (str): The trigger type of the workflow. allowed values are newSubmission, editSubmission, reviewSubmission.
            request (UpsertFindSubmissionWorkflowStepRequest): The request object containing the find submission step details.
            step_variable_name (Optional[str]): The variable name of the step, if not provided, a random variable name will be generated.
            parent_step_variable_name (Optional[str]): The variable name of the parent step, below which the new step will be added. If not provided, the new step will be added to the start of the workflow, else it will be added below the parent step..
        """
        return workflow_definition_client.add_find_submission_step(
            app_id=app_id,
            trigger_type=trigger_type,
            request=request,
            step_variable_name=step_variable_name,
            parent_step_variable_name=parent_step_variable_name,
        )

    def update_find_submission_step(
        app_id: str,
        trigger_type: str,
        step_variable_name: str,
        request: UpsertFindSubmissionWorkflowStepRequest,
    ) -> WorkflowStepResponse:
        """Update a find submission step in a Clappia app's workflow.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            trigger_type (str): The trigger type of the workflow. allowed values are newSubmission, editSubmission, reviewSubmission. allowed values are newSubmission, editSubmission, reviewSubmission.
            step_variable_name (str): The variable name of the step to update.
            request (UpsertFindSubmissionWorkflowStepRequest): The request object containing the updated find submission step details.
        """
        return workflow_definition_client.update_find_submission_step(
            app_id=app_id,
            trigger_type=trigger_type,
            step_variable_name=step_variable_name,
            request=request,
        )

    # Edit Submission Workflow Step Tools
    def add_edit_submission_step(
        app_id: str,
        trigger_type: str,
        request: UpsertEditSubmissionWorkflowStepRequest,
        step_variable_name: Optional[str] = None,
        parent_step_variable_name: Optional[str] = None,
    ) -> WorkflowStepResponse:
        """Add an edit submission step to a Clappia app's workflow.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            trigger_type (str): The trigger type of the workflow. allowed values are newSubmission, editSubmission, reviewSubmission.
            request (UpsertEditSubmissionWorkflowStepRequest): The request object containing the edit submission step details.
            step_variable_name (Optional[str]): The variable name of the step, if not provided, a random variable name will be generated.
            parent_step_variable_name (Optional[str]): The variable name of the parent step, below which the new step will be added. If not provided, the new step will be added to the start of the workflow, else it will be added below the parent step..
        """
        return workflow_definition_client.add_edit_submission_step(
            app_id=app_id,
            trigger_type=trigger_type,
            request=request,
            step_variable_name=step_variable_name,
            parent_step_variable_name=parent_step_variable_name,
        )

    def update_edit_submission_step(
        app_id: str,
        trigger_type: str,
        step_variable_name: str,
        request: UpsertEditSubmissionWorkflowStepRequest,
    ) -> WorkflowStepResponse:
        """Update an edit submission step in a Clappia app's workflow.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            trigger_type (str): The trigger type of the workflow. allowed values are newSubmission, editSubmission, reviewSubmission. allowed values are newSubmission, editSubmission, reviewSubmission.
            step_variable_name (str): The variable name of the step to update.
            request (UpsertEditSubmissionWorkflowStepRequest): The request object containing the updated edit submission step details.
        """
        return workflow_definition_client.update_edit_submission_step(
            app_id=app_id,
            trigger_type=trigger_type,
            step_variable_name=step_variable_name,
            request=request,
        )
