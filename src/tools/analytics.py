"""
analytics.py - Clappia MCP Analytics Module
Handles all analytics-related operations with clean Pydantic models
"""

import logging
from typing import Union

from clappia_api_tools import AnalyticsAuthTokenClient
from clappia_api_tools.models import (
    UpsertBarChartDefinitionRequest,
    UpsertDataTableChartDefinitionRequest,
    UpsertDoughnutChartDefinitionRequest,
    UpsertGanttChartDefinitionRequest,
    UpsertLineChartDefinitionRequest,
    UpsertMapChartDefinitionRequest,
    UpsertPieChartDefinitionRequest,
    UpsertSummaryChartDefinitionRequest,
)
from mcp.server.fastmcp import FastMCP

from src.utils.constants import ANALYTICS_API_BASE_URL
from src.utils.context import get_auth_token

logger = logging.getLogger(__name__)


ChartDefinitionRequestUnion = Union[
    UpsertSummaryChartDefinitionRequest,
    UpsertBarChartDefinitionRequest,
    UpsertPieChartDefinitionRequest,
    UpsertDoughnutChartDefinitionRequest,
    UpsertLineChartDefinitionRequest,
    UpsertDataTableChartDefinitionRequest,
    UpsertMapChartDefinitionRequest,
    UpsertGanttChartDefinitionRequest,
]


def _get_analytics_client(workplace_id: str) -> AnalyticsAuthTokenClient:
    auth_token = get_auth_token()
    return AnalyticsAuthTokenClient(
        auth_token=auth_token,
        workplace_id=workplace_id,
        base_url=ANALYTICS_API_BASE_URL,
    )


def register_analytics_tools(mcp: FastMCP):
    """Register all analytics-related tools with the FastMCP server"""

    @mcp.tool()
    async def add_chart(
        app_id: str,
        workplace_id: str,
        chart_index: int,
        chart_title: str,
        request: ChartDefinitionRequestUnion,
        version_variable_name: str | None = None,
    ):
        """Add chart to app analytics dashboard.

        Args:
            app_id: ASK USER - App identifier
            workplace_id: ASK USER - Workplace identifier
            chart_index: ASK USER - Position index in dashboard
            chart_title: ASK USER - Chart display title
            request: ASK USER - Chart definition request object (type determines chart type)
            version_variable_name: App version variable name (optional)
        """
        analytics_client = _get_analytics_client(workplace_id)
        try:
            return await analytics_client.add(
                app_id, chart_index, chart_title, request, version_variable_name
            )
        finally:
            await analytics_client.close()

    @mcp.tool()
    async def update_chart(
        app_id: str,
        workplace_id: str,
        chart_index: int,
        request: ChartDefinitionRequestUnion,
        version_variable_name: str | None = None,
    ):
        """Update chart in app analytics dashboard.

        Args:
            app_id: ASK USER - App identifier
            workplace_id: ASK USER - Workplace identifier
            chart_index: ASK USER - Position index of chart to update
            request: ASK USER - Chart definition request object with updated configuration
            version_variable_name: App version variable name (optional)
        """
        analytics_client = _get_analytics_client(workplace_id)
        try:
            return await analytics_client.update(
                app_id, chart_index, request, version_variable_name
            )
        finally:
            await analytics_client.close()

    @mcp.tool()
    async def reorder_chart(
        app_id: str,
        workplace_id: str,
        source_index: int,
        target_index: int,
        version_variable_name: str | None = None,
    ):
        """Reorder charts in app analytics dashboard.

        Args:
            app_id: ASK USER - App identifier
            workplace_id: ASK USER - Workplace identifier
            source_index: ASK USER - Current position index of chart to move
            target_index: ASK USER - New position index for chart
            version_variable_name: App version variable name (optional)
        """
        analytics_client = _get_analytics_client(workplace_id)
        try:
            return await analytics_client.reorder_chart(
                app_id=app_id,
                source_index=source_index,
                target_index=target_index,
                version_variable_name=version_variable_name,
            )
        finally:
            await analytics_client.close()

    @mcp.tool()
    async def get_app_charts(
        app_id: str, workplace_id: str, version_variable_name: str | None = None
    ):
        """Get all charts in app analytics dashboard.

        Args:
            app_id: ASK USER - App identifier
            workplace_id: ASK USER - Workplace identifier
            version_variable_name: App version variable name (optional)
        """
        analytics_client = _get_analytics_client(workplace_id)
        try:
            return await analytics_client.get_charts(
                app_id=app_id, version_variable_name=version_variable_name
            )
        finally:
            await analytics_client.close()
