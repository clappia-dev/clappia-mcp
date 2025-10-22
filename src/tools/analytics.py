"""
analytics.py - Clappia MCP Analytics Module
Handles all analytics-related operations with clean Pydantic models
"""

from mcp.server.fastmcp import FastMCP
from src.utils.logging_utils import get_logger
from src.utils.context import get_api_key
from src.utils.constants import (
    CLAPPIA_EXTERNAL_DEV_API_BASE_URL,
    CLAPPIA_EXTERNAL_PREPROD_API_BASE_URL,
    CLAPPIA_EXTERNAL_PROD_API_BASE_URL,
)
from clappia_api_tools import AnalyticsAPIKeyClient as AnalyticsClient
from clappia_api_tools.models import (
    UpsertSummaryChartDefinitionRequest,
    UpsertBarChartDefinitionRequest,
    UpsertPieChartDefinitionRequest,
    UpsertDoughnutChartDefinitionRequest,
    UpsertLineChartDefinitionRequest,
    UpsertDataTableChartDefinitionRequest,
    UpsertMapChartDefinitionRequest,
    UpsertGanttChartDefinitionRequest,
)
from typing import Union, Optional

logger = get_logger(__name__)


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


def _get_analytics_client() -> AnalyticsClient:
    api_key = get_api_key()
    return AnalyticsClient(
        api_key=api_key,
        base_url=CLAPPIA_EXTERNAL_DEV_API_BASE_URL,
    )


def register_analytics_tools(mcp: FastMCP):
    """Register all analytics-related tools with the FastMCP server"""

    @mcp.tool()
    def add_chart(
        app_id: str,
        chart_index: int,
        chart_title: str,
        request: ChartDefinitionRequestUnion,
        version_variable_name: Optional[str] = None,
    ):
        """Add a chart to a Clappia app's analytics dashboard. The chart type is determined by the request object type."""
        analytics_client = _get_analytics_client()
        return analytics_client.add(
            app_id, chart_index, chart_title, request, version_variable_name
        )

    @mcp.tool()
    def update_chart(
        app_id: str,
        chart_index: int,
        request: ChartDefinitionRequestUnion,
        version_variable_name: Optional[str] = None,
    ):
        """Update a chart in a Clappia app's analytics dashboard. The chart type is determined by the request object type."""
        analytics_client = _get_analytics_client()
        return analytics_client.update(
            app_id, chart_index, request, version_variable_name
        )

    @mcp.tool()
    def reorder_chart(
        app_id: str,
        source_index: int,
        target_index: int,
        version_variable_name: Optional[str] = None,
    ):
        """Reorder a chart in a Clappia app's analytics dashboard."""
        analytics_client = _get_analytics_client()
        return analytics_client.reorder_chart(
            app_id=app_id,
            source_index=source_index,
            target_index=target_index,
            version_variable_name=version_variable_name,
        )

    @mcp.tool()
    def get_app_charts(app_id: str, version_variable_name: Optional[str] = None):
        """Get all charts in a Clappia app's analytics dashboard."""
        analytics_client = _get_analytics_client()
        return analytics_client.get_charts(
            app_id=app_id, version_variable_name=version_variable_name
        )
