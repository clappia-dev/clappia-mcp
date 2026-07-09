"""
submissions.py - Clappia MCP Submissions Module using Modern Pydantic Approach
Handles all submission management operations with clean Pydantic models
"""

import logging
import json
import time
import sys

from clappia_api_tools.models import (
    CreateSubmissionRequest,
    EditSubmissionRequest,
    GetSubmissionRequest,
    GetSubmissionsAggregationRequest,
    GetSubmissionsInExcelRequest,
    GetSubmissionsRequest,
    UpdateSubmissionOwnersRequest,
    UpdateSubmissionStatusRequest,
)
from mcp.server.fastmcp import FastMCP

from src.utils.client import get_submission_client

logger = logging.getLogger(__name__)


def register_submission_tools(mcp: FastMCP):
    """Register all submission-related tools with the FastMCP server"""

    @mcp.tool()
    async def get_submissions(
        app_id: str,
        workplace_id: str,
        request: GetSubmissionsRequest,
    ):
        """Get submissions from app with filtering and pagination.

        Args:
            app_id: ASK USER - App identifier
            workplace_id: ASK USER - Workplace identifier
            request: ASK USER - GetSubmissionsRequest object with filters, pagination, sorting, and field selection
        """
        submission_client = get_submission_client(workplace_id)
        try:
            logger.info(f"[get_submissions] Calling API: app={app_id}, page_size={request.page_size}, last_id={request.last_submission_id}, fields={request.fields}")
            
            result = await submission_client.get_submissions(
                app_id=app_id,
                request=request,
            )
            logger.info(f"[get_submissions] Result type: {type(result).__name__}")

            # Force fully plain Python types — handles nested Pydantic models too
            result_plain = json.loads(result.model_dump_json())
            logger.info(f"[get_submissions] Converted OK, returning")
            return result_plain
        finally:
            await submission_client.close()

    @mcp.tool()
    async def get_submissions_aggregation(
        app_id: str,
        workplace_id: str,
        request: GetSubmissionsAggregationRequest,
    ):
        """Aggregate submissions with metrics and grouping.

        Args:
            app_id: ASK USER - App identifier
            workplace_id: ASK USER - Workplace identifier
            request: ASK USER - GetSubmissionsAggregationRequest object with aggregation config, grouping, and filters
        """
        submission_client = get_submission_client(workplace_id)
        try:
            return await submission_client.get_submissions_aggregation(
                app_id=app_id,
                request=request,
            )
        finally:
            await submission_client.close()

    @mcp.tool()
    async def get_submission(
        app_id: str,
        workplace_id: str,
        request: GetSubmissionRequest,
    ):
        """Get a single submission by ID.

        Args:
            app_id: ASK USER - App identifier
            workplace_id: ASK USER - Workplace identifier
            request: ASK USER - GetSubmissionRequest object with submission ID
        """
        submission_client = get_submission_client(workplace_id)
        try:
            return await submission_client.get_submission(
                app_id=app_id,
                request=request,
            )
        finally:
            await submission_client.close()

    @mcp.tool()
    async def create_submission(
        app_id: str,
        workplace_id: str,
        request: CreateSubmissionRequest,
    ):
        """Create new submission in app.

        Args:
            app_id: ASK USER - App identifier
            workplace_id: ASK USER - Workplace identifier
            request: ASK USER - CreateSubmissionRequest object with field values and submission metadata
        """
        submission_client = get_submission_client(workplace_id)
        try:
            return await submission_client.create_submission(
                app_id=app_id,
                request=request,
            )
        finally:
            await submission_client.close()

    @mcp.tool()
    async def edit_submission(
        app_id: str,
        workplace_id: str,
        request: EditSubmissionRequest,
    ):
        """Edit existing submission in app.

        Args:
            app_id: ASK USER - App identifier
            workplace_id: ASK USER - Workplace identifier
            request: ASK USER - EditSubmissionRequest object with submission ID and updated field values
        """
        submission_client = get_submission_client(workplace_id)
        try:
            return await submission_client.edit_submission(
                app_id=app_id,
                request=request,
            )
        finally:
            await submission_client.close()

    @mcp.tool()
    async def update_submission_status(
        app_id: str,
        workplace_id: str,
        request: UpdateSubmissionStatusRequest,
    ):
        """Update submission status.

        Args:
            app_id: ASK USER - App identifier
            workplace_id: ASK USER - Workplace identifier
            request: ASK USER - UpdateSubmissionStatusRequest object with submission ID and new status
        """
        submission_client = get_submission_client(workplace_id)
        try:
            return await submission_client.update_status(
                app_id=app_id,
                request=request,
            )
        finally:
            await submission_client.close()

    @mcp.tool()
    async def get_submissions_in_excel(
        app_id: str,
        workplace_id: str,
        request: GetSubmissionsInExcelRequest,
    ):
        """Export submissions to Excel format.

        Args:
            app_id: ASK USER - App identifier
            workplace_id: ASK USER - Workplace identifier
            request: ASK USER - GetSubmissionsInExcelRequest object with filters and export configuration
        """
        submission_client = get_submission_client(workplace_id)
        try:
            return await submission_client.get_submissions_in_excel(
                app_id=app_id,
                request=request,
            )
        finally:
            await submission_client.close()

    @mcp.tool()
    async def update_submission_owners(
        app_id: str,
        workplace_id: str,
        request: UpdateSubmissionOwnersRequest,
    ):
        """Update owners assigned to submission.

        Args:
            app_id: ASK USER - App identifier
            workplace_id: ASK USER - Workplace identifier
            request: ASK USER - UpdateSubmissionOwnersRequest object with submission ID and new owner email addresses
        """
        submission_client = get_submission_client(workplace_id)
        try:
            return await submission_client.update_owners(
                app_id=app_id,
                request=request,
            )
        finally:
            await submission_client.close()
