from typing import Union
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

# Union type for all chart definition request types
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

logger = get_logger(__name__)


def register_analytics_tools(mcp: FastMCP):
    """Register all analytics-related tools with the FastMCP server"""

    # Summary Chart Tools
    def add_summary_chart(
        app_id: str,
        chart_index: int,
        chart_title: str,
        request: UpsertSummaryChartDefinitionRequest,
    ) -> ChartResponse:
        """Add a summary chart to a Clappia app's analytics dashboard.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            chart_index (int): The index where the chart should be placed.
            chart_title (str): The title of the chart.
            request (UpsertSummaryChartDefinitionRequest): The request object containing the chart configuration.
        """
        return analytics_client.add_summary_chart(
            app_id=app_id,
            chart_index=chart_index,
            chart_title=chart_title,
            request=request,
        )

    def update_summary_chart(
        app_id: str, chart_index: int, request: UpsertSummaryChartDefinitionRequest
    ) -> ChartResponse:
        """Update a summary chart in a Clappia app's analytics dashboard.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            chart_index (int): The index of the chart to update.
            request (UpsertSummaryChartDefinitionRequest): The request object containing the updated chart configuration.
        """
        return analytics_client.update_summary_chart(
            app_id=app_id, chart_index=chart_index, request=request
        )

    # Bar Chart Tools
    def add_bar_chart(
        app_id: str,
        chart_index: int,
        chart_title: str,
        request: UpsertBarChartDefinitionRequest,
    ) -> ChartResponse:
        """Add a bar chart to a Clappia app's analytics dashboard.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            chart_index (int): The index where the chart should be placed.
            chart_title (str): The title of the chart.
            request (UpsertBarChartDefinitionRequest): The request object containing the chart configuration.
        """
        return analytics_client.add_bar_chart(
            app_id=app_id,
            chart_index=chart_index,
            chart_title=chart_title,
            request=request,
        )

    def update_bar_chart(
        app_id: str, chart_index: int, request: UpsertBarChartDefinitionRequest
    ) -> ChartResponse:
        """Update a bar chart in a Clappia app's analytics dashboard.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            chart_index (int): The index of the chart to update.
            request (UpsertBarChartDefinitionRequest): The request object containing the updated chart configuration.
        """
        return analytics_client.update_bar_chart(
            app_id=app_id, chart_index=chart_index, request=request
        )

    # Pie Chart Tools
    def add_pie_chart(
        app_id: str,
        chart_index: int,
        chart_title: str,
        request: UpsertPieChartDefinitionRequest,
    ) -> ChartResponse:
        """Add a pie chart to a Clappia app's analytics dashboard.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            chart_index (int): The index where the chart should be placed.
            chart_title (str): The title of the chart.
            request (UpsertPieChartDefinitionRequest): The request object containing the chart configuration.
        """
        return analytics_client.add_pie_chart(
            app_id=app_id,
            chart_index=chart_index,
            chart_title=chart_title,
            request=request,
        )

    def update_pie_chart(
        app_id: str, chart_index: int, request: UpsertPieChartDefinitionRequest
    ) -> ChartResponse:
        """Update a pie chart in a Clappia app's analytics dashboard.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            chart_index (int): The index of the chart to update.
            request (UpsertPieChartDefinitionRequest): The request object containing the updated chart configuration.
        """
        return analytics_client.update_pie_chart(
            app_id=app_id, chart_index=chart_index, request=request
        )

    # Doughnut Chart Tools
    def add_doughnut_chart(
        app_id: str,
        chart_index: int,
        chart_title: str,
        request: UpsertDoughnutChartDefinitionRequest,
    ) -> ChartResponse:
        """Add a doughnut chart to a Clappia app's analytics dashboard.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            chart_index (int): The index where the chart should be placed.
            chart_title (str): The title of the chart.
            request (UpsertDoughnutChartDefinitionRequest): The request object containing the chart configuration.
        """
        return analytics_client.add_doughnut_chart(
            app_id=app_id,
            chart_index=chart_index,
            chart_title=chart_title,
            request=request,
        )

    def update_doughnut_chart(
        app_id: str, chart_index: int, request: UpsertDoughnutChartDefinitionRequest
    ) -> ChartResponse:
        """Update a doughnut chart in a Clappia app's analytics dashboard.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            chart_index (int): The index of the chart to update.
            request (UpsertDoughnutChartDefinitionRequest): The request object containing the updated chart configuration.
        """
        return analytics_client.update_doughnut_chart(
            app_id=app_id, chart_index=chart_index, request=request
        )

    # Line Chart Tools
    def add_line_chart(
        app_id: str,
        chart_index: int,
        chart_title: str,
        request: UpsertLineChartDefinitionRequest,
    ) -> ChartResponse:
        """Add a line chart to a Clappia app's analytics dashboard.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            chart_index (int): The index where the chart should be placed.
            chart_title (str): The title of the chart.
            request (UpsertLineChartDefinitionRequest): The request object containing the chart configuration.
        """
        return analytics_client.add_line_chart(
            app_id=app_id,
            chart_index=chart_index,
            chart_title=chart_title,
            request=request,
        )

    def update_line_chart(
        app_id: str, chart_index: int, request: UpsertLineChartDefinitionRequest
    ) -> ChartResponse:
        """Update a line chart in a Clappia app's analytics dashboard.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            chart_index (int): The index of the chart to update.
            request (UpsertLineChartDefinitionRequest): The request object containing the updated chart configuration.
        """
        return analytics_client.update_line_chart(
            app_id=app_id, chart_index=chart_index, request=request
        )

    # Data Table Chart Tools
    def add_data_table_chart(
        app_id: str,
        chart_index: int,
        chart_title: str,
        request: UpsertDataTableChartDefinitionRequest,
    ) -> ChartResponse:
        """Add a data table chart to a Clappia app's analytics dashboard.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            chart_index (int): The index where the chart should be placed.
            chart_title (str): The title of the chart.
            request (UpsertDataTableChartDefinitionRequest): The request object containing the chart configuration.
        """
        return analytics_client.add_data_table_chart(
            app_id=app_id,
            chart_index=chart_index,
            chart_title=chart_title,
            request=request,
        )

    def update_data_table_chart(
        app_id: str, chart_index: int, request: UpsertDataTableChartDefinitionRequest
    ) -> ChartResponse:
        """Update a data table chart in a Clappia app's analytics dashboard.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            chart_index (int): The index of the chart to update.
            request (UpsertDataTableChartDefinitionRequest): The request object containing the updated chart configuration.
        """
        return analytics_client.update_data_table_chart(
            app_id=app_id, chart_index=chart_index, request=request
        )

    # Map Chart Tools
    def add_map_chart(
        app_id: str,
        chart_index: int,
        chart_title: str,
        request: UpsertMapChartDefinitionRequest,
    ) -> ChartResponse:
        """Add a map chart to a Clappia app's analytics dashboard.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            chart_index (int): The index where the chart should be placed.
            chart_title (str): The title of the chart.
            request (UpsertMapChartDefinitionRequest): The request object containing the chart configuration.
        """
        return analytics_client.add_map_chart(
            app_id=app_id,
            chart_index=chart_index,
            chart_title=chart_title,
            request=request,
        )

    def update_map_chart(
        app_id: str, chart_index: int, request: UpsertMapChartDefinitionRequest
    ) -> ChartResponse:
        """Update a map chart in a Clappia app's analytics dashboard.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            chart_index (int): The index of the chart to update.
            request (UpsertMapChartDefinitionRequest): The request object containing the updated chart configuration.
        """
        return analytics_client.update_map_chart(
            app_id=app_id, chart_index=chart_index, request=request
        )

    # Gantt Chart Tools
    def add_gantt_chart(
        app_id: str,
        chart_index: int,
        chart_title: str,
        request: UpsertGanttChartDefinitionRequest,
    ) -> ChartResponse:
        """Add a Gantt chart to a Clappia app's analytics dashboard.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            chart_index (int): The index where the chart should be placed.
            chart_title (str): The title of the chart.
            request (UpsertGanttChartDefinitionRequest): The request object containing the chart configuration.
        """
        return analytics_client.add_gantt_chart(
            app_id=app_id,
            chart_index=chart_index,
            chart_title=chart_title,
            request=request,
        )

    def update_gantt_chart(
        app_id: str, chart_index: int, request: UpsertGanttChartDefinitionRequest
    ) -> ChartResponse:
        """Update a Gantt chart in a Clappia app's analytics dashboard.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            chart_index (int): The index of the chart to update.
            request (UpsertGanttChartDefinitionRequest): The request object containing the updated chart configuration.
        """
        return analytics_client.update_gantt_chart(
            app_id=app_id, chart_index=chart_index, request=request
        )

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
        # Determine chart type based on request type and call appropriate function
        if isinstance(request, UpsertSummaryChartDefinitionRequest):
            return add_summary_chart(app_id, chart_index, chart_title, request)
        elif isinstance(request, UpsertBarChartDefinitionRequest):
            return add_bar_chart(app_id, chart_index, chart_title, request)
        elif isinstance(request, UpsertPieChartDefinitionRequest):
            return add_pie_chart(app_id, chart_index, chart_title, request)
        elif isinstance(request, UpsertDoughnutChartDefinitionRequest):
            return add_doughnut_chart(app_id, chart_index, chart_title, request)
        elif isinstance(request, UpsertLineChartDefinitionRequest):
            return add_line_chart(app_id, chart_index, chart_title, request)
        elif isinstance(request, UpsertDataTableChartDefinitionRequest):
            return add_data_table_chart(app_id, chart_index, chart_title, request)
        elif isinstance(request, UpsertMapChartDefinitionRequest):
            return add_map_chart(app_id, chart_index, chart_title, request)
        elif isinstance(request, UpsertGanttChartDefinitionRequest):
            return add_gantt_chart(app_id, chart_index, chart_title, request)
        else:
            raise ValueError(f"Unsupported chart definition request type: {type(request)}")

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
        # Determine chart type based on request type and call appropriate function
        if isinstance(request, UpsertSummaryChartDefinitionRequest):
            return update_summary_chart(app_id, chart_index, request)
        elif isinstance(request, UpsertBarChartDefinitionRequest):
            return update_bar_chart(app_id, chart_index, request)
        elif isinstance(request, UpsertPieChartDefinitionRequest):
            return update_pie_chart(app_id, chart_index, request)
        elif isinstance(request, UpsertDoughnutChartDefinitionRequest):
            return update_doughnut_chart(app_id, chart_index, request)
        elif isinstance(request, UpsertLineChartDefinitionRequest):
            return update_line_chart(app_id, chart_index, request)
        elif isinstance(request, UpsertDataTableChartDefinitionRequest):
            return update_data_table_chart(app_id, chart_index, request)
        elif isinstance(request, UpsertMapChartDefinitionRequest):
            return update_map_chart(app_id, chart_index, request)
        elif isinstance(request, UpsertGanttChartDefinitionRequest):
            return update_gantt_chart(app_id, chart_index, request)
        else:
            raise ValueError(f"Unsupported chart definition request type: {type(request)}")

    @mcp.tool()
    def get_app_charts(app_id: str) -> BaseResponse:
        """Get all charts for a Clappia app's analytics dashboard.

        Args:
            app_id (str): The unique identifier of the Clappia application.
        """
        return analytics_client.get_charts(app_id=app_id)
