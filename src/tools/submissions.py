"""
submissions.py - Clappia MCP Submissions Module using Modern Pydantic Approach
Handles all submission management operations with clean Pydantic models
"""

from mcp.server.fastmcp import FastMCP
from src.utils.logging_utils import get_logger
from src.utils.context import get_api_key
from src.utils.constants import (
    CLAPPIA_EXTERNAL_DEV_API_BASE_URL,
    CLAPPIA_EXTERNAL_PREPROD_API_BASE_URL,
    CLAPPIA_EXTERNAL_PROD_API_BASE_URL,
)
from clappia_api_tools import SubmissionAPIKeyClient as SubmissionClient
from clappia_api_tools.models import (
    GetSubmissionsRequest,
    GetSubmissionsAggregationRequest,
    CreateSubmissionRequest,
    EditSubmissionRequest,
    UpdateSubmissionStatusRequest,
    UpdateSubmissionOwnersRequest,
    GetSubmissionsInExcelRequest,
)

logger = get_logger(__name__)


def _get_submission_client() -> SubmissionClient:
    api_key = get_api_key()
    return SubmissionClient(
        api_key=api_key,
        base_url=CLAPPIA_EXTERNAL_DEV_API_BASE_URL,
    )


def register_submission_tools(mcp: FastMCP):
    """Register all submission-related tools with the FastMCP server"""

    @mcp.tool()
    def get_submissions(request: GetSubmissionsRequest):
        """Retrieve submissions from a Clappia app with optional filtering."""
        submission_client = _get_submission_client()
        return submission_client.get_submissions(
            app_id=request.app_id,
            page_size=request.page_size,
            forward=request.forward,
            filters=request.filters,
            requesting_user_email_address=request.requesting_user_email_address,
        )

    @mcp.tool()
    def get_submissions_aggregation(
        request: GetSubmissionsAggregationRequest,
    ):
        """Aggregate and analyze Clappia submissions with various metrics and grouping options."""
        submission_client = _get_submission_client()
        return submission_client.get_submissions_aggregation(
            app_id=request.app_id,
            dimensions=request.dimensions,
            aggregation_dimensions=request.aggregation_dimensions,
            x_axis_labels=request.x_axis_labels,
            forward=request.forward,
            page_size=request.page_size,
            filters=request.filters,
            requesting_user_email_address=request.requesting_user_email_address,
        )

    @mcp.tool()
    def create_submission(
        request: CreateSubmissionRequest,
    ):
        """Create a new submission in a Clappia app."""
        submission_client = _get_submission_client()
        return submission_client.create_submission(
            app_id=request.app_id,
            data=request.data,
            requesting_user_email_address=request.requesting_user_email_address,
        )

    @mcp.tool()
    def edit_submission(request: EditSubmissionRequest):
        """Edit an existing submission in a Clappia app."""
        submission_client = _get_submission_client()
        return submission_client.edit_submission(
            app_id=request.app_id,
            submission_id=request.submission_id,
            data=request.data,
            requesting_user_email_address=request.requesting_user_email_address,
        )

    @mcp.tool()
    def update_submission_status(
        request: UpdateSubmissionStatusRequest,
    ):
        """Update the status of a submission in a Clappia app."""
        submission_client = _get_submission_client()
        return submission_client.update_status(
            app_id=request.app_id,
            submission_id=request.submission_id,
            status_name=request.status_name,
            comments=request.comments,
            requesting_user_email_address=request.requesting_user_email_address,
        )

    @mcp.tool()
    def get_submissions_in_excel(
        request: GetSubmissionsInExcelRequest,
    ):
        """Get submissions in Excel format from a Clappia app with optional filtering."""
        submission_client = _get_submission_client()
        return submission_client.get_submissions_in_excel(
            app_id=request.app_id,
            requesting_user_email_address=str(request.requesting_user_email_address),
            filters=request.filters,
            field_names=request.field_names,
            format=request.format,
        )

    @mcp.tool()
    def update_submission_owners(
        request: UpdateSubmissionOwnersRequest,
    ):
        """Update the owners of a submission in a Clappia app."""
        email_ids = [str(email) for email in request.email_ids]

        submission_client = _get_submission_client()
        return submission_client.update_owners(
            app_id=request.app_id,
            submission_id=request.submission_id,
            email_ids=email_ids,
            requesting_user_email_address=request.requesting_user_email_address,
        )
