from mcp.server.fastmcp import FastMCP
from utils import get_logger, workflow_definition_client   
from clappia_api_tools.models import GetWorkflowRequest, AddWorkflowStepRequest, UpdateWorkflowStepRequest, ReorderWorkflowStepRequest, WorkflowResponse, WorkflowStepResponse

logger = get_logger(__name__)

def register_workflow_tools(mcp: FastMCP):
    """Register all workflow-related tools with the FastMCP server"""
  
    @mcp.tool()
    async def get_clappia_workflow(request: GetWorkflowRequest) -> WorkflowResponse:
        """Retrieve the workflow configuration for a Clappia app."""
        try:
            return workflow_definition_client.get_workflow(
                app_id=request.app_id,
                trigger_type=request.trigger_type
            )
        except Exception as e:
            logger.error(f"Error in get_clappia_workflow: {str(e)}")
            return WorkflowResponse(
                success=False,
                message=f"Error retrieving workflow: {str(e)}",
                app_id=request.app_id
            )

    @mcp.tool()
    async def add_workflow_step_to_clappia_app(request: AddWorkflowStepRequest) -> WorkflowStepResponse:
        """Add a new step to a Clappia app's workflow."""
        try:
            extra_fields = request.get_extra_fields()
            
            return workflow_definition_client.add_workflow_step(
                app_id=request.app_id,
                trigger_type=request.trigger_type,
                parent_variable_name=request.parent_variable_name,
                node_type=request.node_type,
                **extra_fields
            )
        except Exception as e:
            logger.error(f"Error in add_workflow_step_to_clappia_app: {str(e)}")
            return WorkflowStepResponse(
                success=False,
                message=f"Error adding workflow step: {str(e)}",
                app_id=request.app_id,
                trigger_type=request.trigger_type,
                operation="add"
            )

    @mcp.tool()
    async def update_workflow_step_in_clappia_app(request: UpdateWorkflowStepRequest) -> WorkflowStepResponse:
        """Update an existing step in a Clappia app's workflow."""
        try:
            extra_fields = request.get_extra_fields()
            
            return workflow_definition_client.update_workflow_step(
                app_id=request.app_id,
                trigger_type=request.trigger_type,
                step_variable_name=request.step_variable_name,
                update_data=extra_fields
            )
        except Exception as e:
            logger.error(f"Error in update_workflow_step_in_clappia_app: {str(e)}")
            return WorkflowStepResponse(
                success=False,
                message=f"Error updating workflow step: {str(e)}",
                app_id=request.app_id,
                trigger_type=request.trigger_type,
                operation="update"
            )

    @mcp.tool()
    async def reorder_workflow_step_in_clappia_app(request: ReorderWorkflowStepRequest) -> WorkflowStepResponse:
        """Reorder steps in a Clappia app's workflow."""
        try:
            return workflow_definition_client.reorder_workflow_step(
                app_id=request.app_id,
                trigger_type=request.trigger_type,
                step_variable_name=request.step_variable_name,
                parent_variable_name=request.parent_variable_name
            )
        except Exception as e:
            logger.error(f"Error in reorder_workflow_step_in_clappia_app: {str(e)}")
            return WorkflowStepResponse(
                success=False,
                message=f"Error reordering workflow step: {str(e)}",
                app_id=request.app_id,
                trigger_type=request.trigger_type,
                operation="reorder"
            )