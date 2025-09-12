from mcp.server.fastmcp import FastMCP
from utils import get_logger, analytics_client
from clappia_api_tools.models import (
    BaseResponse,
    ChartResponse,
    UpsertSummaryChartDefinitionRequest,
    UpsertBarChartDefinitionRequest,
    UpsertPieChartDefinitionRequest,
    UpsertDoughnutChartDefinitionRequest,
    UpsertLineChartDefinitionRequest,
    UpsertDataTableChartDefinitionRequest,
    UpsertMapChartDefinitionRequest,
    UpsertGanttChartDefinitionRequest,
)
from typing import Union

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


def register_analytics_tools(mcp: FastMCP):
    """Register all analytics-related tools with the FastMCP server"""

    @mcp.tool()
    def add_chart(
        app_id: str,
        chart_index: int,
        chart_title: str,
        request: ChartDefinitionRequestUnion,
    ) -> ChartResponse:
        """
        Adds a chart to a Clappia app's analytics dashboard. The chart type is determined by the request object type.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            chart_index (int): The index where the chart should be placed.
            chart_title (str): The title of the chart.
            request (ChartDefinitionRequestUnion): The request object containing chart configuration. The chart type is determined by the specific request type.

        Returns:
            ChartResponse: The response object containing the result of the chart addition.

        Raises:
            Exception: Any error raised by the underlying chart addition method.
        """
        return analytics_client.add(app_id, chart_index, chart_title, request)

    @mcp.tool()
    def update_chart(
        app_id: str,
        chart_index: int,
        request: ChartDefinitionRequestUnion,
    ) -> ChartResponse:
        """
        Updates a chart in a Clappia app's analytics dashboard. The chart type is determined by the request object type.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            chart_index (int): The index of the chart to update.
            request (ChartDefinitionRequestUnion): The request object containing chart configuration. The chart type is determined by the specific request type.

        Returns:
            ChartResponse: The response object containing the result of the chart update.

        Raises:
            Exception: Any error raised by the underlying chart update method.
        """
        return analytics_client.update(app_id, chart_index, request)

    @mcp.tool()
    def reorder_chart(
        app_id: str, source_index: int, target_index: int
    ) -> ChartResponse:
        """Reorder charts in a Clappia app's analytics dashboard.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            source_index (int): The current index of the chart to move.
            target_index (int): The target index where the chart should be moved.
        """
        return analytics_client.reorder_chart(
            app_id=app_id, source_index=source_index, target_index=target_index
        )

    @mcp.tool()
    def get_app_charts(app_id: str) -> BaseResponse:
        """Get all charts for a Clappia app's analytics dashboard.

        Args:
            app_id (str): The unique identifier of the Clappia application.
        """
        return analytics_client.get_charts(app_id=app_id)
