"""
submissions.py - Clappia MCP Submissions Module using Modern Pydantic Approach
Handles all submission management operations with clean Pydantic models
"""

from mcp.server.fastmcp import FastMCP
from clappia_api_tools import GetSubmissionsRequest, GetSubmissionsAggregationRequest, CreateSubmissionRequest, EditSubmissionRequest, UpdateSubmissionStatusRequest, UpdateSubmissionOwnersRequest, SubmissionResponse, SubmissionsResponse, GetSubmissionsInExcelRequest, SubmissionsExcelResponse
from utils import get_logger, submission_client

logger = get_logger(__name__)

def register_submission_tools(mcp: FastMCP):
    """Register all submission-related tools with the FastMCP server"""
    
    @mcp.tool()
    async def get_clappia_submissions(request: GetSubmissionsRequest) -> SubmissionsResponse:
        """
        Retrieve submissions from a Clappia app with optional filtering.
        
        Supports complex filtering with conditions, operators, and logical combinations.
        Fetch app definition first to see the fields and statuses in the app.
        """
        try:
            return submission_client.get_submissions(
                app_id=request.app_id,
                requesting_user_email_address=str(request.requesting_user_email_address),
                page_size=request.page_size,
                forward=request.forward,
                filters=request.filters
            )
        except Exception as e:
            logger.error(f"Error in get_clappia_submissions: {str(e)}")
            return SubmissionResponse(
                success=False,
                message=f"Error retrieving submissions: {str(e)}"
            )

    @mcp.tool()
    async def get_clappia_submissions_aggregation(
        request: GetSubmissionsAggregationRequest
    ) -> SubmissionResponse:
        """
        Aggregate and analyze Clappia submissions with various metrics and grouping options.
        
        Supports complex data analysis with filtering, dimensional grouping, and statistical calculations.
        Fetch app definition first to see the fields and statuses in the app.
        """
        try:
            
            return submission_client.get_submissions_aggregation(
                app_id=request.app_id,
                requesting_user_email_address=str(request.requesting_user_email_address),
                dimensions=request.dimensions,
                aggregation_dimensions=request.aggregation_dimensions,
                x_axis_labels=request.x_axis_labels,
                forward=request.forward,
                page_size=request.page_size,
                filters=request.filters
            )
                
        except Exception as e:
            logger.error(f"Error in get_clappia_submissions_aggregation: {str(e)}")
            return SubmissionResponse(
                success=False,
                message=f"Error retrieving aggregation data: {str(e)}"
            )

    @mcp.tool()
    async def create_clappia_submission(request: CreateSubmissionRequest) -> SubmissionResponse:
        """
        Create a new submission in a Clappia app.
        
        Fetch app definition first to see the fields in the app.
        """
        try:
            return submission_client.create_submission(
                app_id=request.app_id,
                data=request.data,
                requesting_user_email_address=str(request.requesting_user_email_address)
            )
                
        except Exception as e:
            logger.error(f"Error in create_clappia_submission: {str(e)}")
            return SubmissionResponse(
                success=False,
                message=f"Error creating submission: {str(e)}"
            )

    @mcp.tool()
    async def edit_clappia_submission(request: EditSubmissionRequest) -> SubmissionResponse:
        """
        Edit an existing submission in a Clappia app.
        
        Fetch app definition first to see the fields in the app.
        """
        try:
            return submission_client.edit_submission(
                app_id=request.app_id,
                submission_id=request.submission_id,
                data=request.data,
                requesting_user_email_address=str(request.requesting_user_email_address)
            )
                
        except Exception as e:
            logger.error(f"Error in edit_clappia_submission: {str(e)}")
            return SubmissionResponse(
                success=False,
                message=f"Error editing submission: {str(e)}"
            )

    @mcp.tool()
    async def update_clappia_submission_status(
        request: UpdateSubmissionStatusRequest
    ) -> SubmissionResponse:
        """
        Update the status of a submission in a Clappia app.
        
        Fetch app definition first to see the available statuses in the app.
        """
        try:
            return submission_client.update_status(
                app_id=request.app_id,
                submission_id=request.submission_id,
                requesting_user_email_address=str(request.requesting_user_email_address),
                status_name=request.status_name,
                comments=request.comments
            )
            
        except Exception as e:
            logger.error(f"Error in update_clappia_submission_status: {str(e)}")
            return SubmissionResponse(
                success=False,
                message=f"Error updating submission status: {str(e)}"
            )
    
    @mcp.tool()
    async def get_clappia_submissions_in_excel(request: GetSubmissionsInExcelRequest) -> SubmissionsExcelResponse:
        """
        Get submissions in Excel format from a Clappia app with optional filtering.
        
        Supports complex filtering with conditions, operators, and logical combinations.
        Fetch app definition first to see the fields and statuses in the app.
        """
        try:
            return submission_client.get_submissions_in_excel(
                app_id=request.app_id,
                requesting_user_email_address=str(request.requesting_user_email_address),
                filters=request.filters,
                field_names=request.field_names,
                format=request.format
            )
        except Exception as e:
            logger.error(f"Error in get_clappia_submissions_in_excel: {str(e)}")    
            return SubmissionsExcelResponse(
                success=False,
                message=f"Error getting submissions in Excel: {str(e)}"
            )

    @mcp.tool()
    async def update_clappia_submission_owners(
        request: UpdateSubmissionOwnersRequest
    ) -> SubmissionResponse:
        """
        Update the owners of a submission in a Clappia app.
        """
        try:
            email_ids = [str(email) for email in request.email_ids]
            
            return submission_client.update_owners(
                app_id=request.app_id,
                submission_id=request.submission_id,
                requesting_user_email_address=str(request.requesting_user_email_address),
                email_ids=email_ids
            )
                
        except Exception as e:
            logger.error(f"Error in update_clappia_submission_owners: {str(e)}")
            return SubmissionResponse(
                success=False,
                message=f"Error updating submission owners: {str(e)}"
            )