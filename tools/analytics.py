"""
analytics.py - Clappia MCP Analytics Module using Modern Pydantic Approach
"""

from mcp.server.fastmcp import FastMCP
from utils import get_logger, analytics_client
from clappia_api_tools.models import AddChartRequest, RemoveChartRequest, UpdateChartRequest, ReorderChartRequest, ChartResponse, GetAppChartsRequest, GetAppChartsResponse

logger = get_logger(__name__)

def register_analytics_tools(mcp: FastMCP):
    """Register all analytics-related tools with the FastMCP server"""
    
    @mcp.tool()
    async def add_chart_to_clappia_app(request: AddChartRequest) -> ChartResponse:
        """
        Add a new chart to a Clappia app's analytics dashboard.
        
        Supports various chart types including Summary, Pie, Doughnut, Bar, Line, Map, Geo, and Gantt charts.
        Charts can be added at specific positions in the dashboard.
        """
        try:
            return analytics_client.add_chart(
                app_id=request.app_id,
                chart_type=request.chart_type,
                chart_index=request.chart_index,
                chart_title=request.chart_title
            )
        except Exception as e:
            logger.error(f"Error in add_chart_to_clappia_app: {str(e)}")
            return ChartResponse(
                success=False,
                message=f"Error adding chart: {str(e)}",
                app_id=request.app_id,
                operation="add"
            )

    @mcp.tool()
    async def remove_chart_from_clappia_app(request: RemoveChartRequest) -> ChartResponse:
        """
        Remove a chart from a Clappia app's analytics dashboard.
        
        Charts are identified by their index position in the dashboard.
        """
        try:
            return analytics_client.remove_chart(
                app_id=request.app_id,
                chart_index=request.chart_index,
            )
        except Exception as e:
            logger.error(f"Error in remove_chart_from_clappia_app: {str(e)}")
            return ChartResponse(
                success=False,
                message=f"Error removing chart: {str(e)}",
                app_id=request.app_id,
                operation="remove"
            )

    @mcp.tool()
    async def update_chart_in_clappia_app(request: UpdateChartRequest) -> ChartResponse:
        """
        Update an existing chart in a Clappia app's analytics dashboard.
        
        Allows modification of chart properties such as title and configuration.
        """
        try:
            update_data = {}
            if request.chart_title is not None:
                update_data["chart_title"] = request.chart_title
            
            return analytics_client.update_chart(
                app_id=request.app_id,
                chart_index=request.chart_index,
                update_data=update_data
            )
        except Exception as e:
            logger.error(f"Error in update_chart_in_clappia_app: {str(e)}")
            return ChartResponse(
                success=False,
                message=f"Error updating chart: {str(e)}",
                app_id=request.app_id,
                operation="update"
            )

    @mcp.tool()
    async def reorder_chart_in_clappia_app(request: ReorderChartRequest) -> ChartResponse:
        """
        Reorder charts in a Clappia app's analytics dashboard.
        
        Move a chart from one position to another in the dashboard layout.
        """
        try:
            return analytics_client.reorder_chart(
                app_id=request.app_id,
                source_index=request.source_index,
                target_index=request.target_index,
            )
        except Exception as e:
            logger.error(f"Error in reorder_chart_in_clappia_app: {str(e)}")
            return ChartResponse(
                success=False,
                message=f"Error reordering chart: {str(e)}",
                app_id=request.app_id,
                operation="reorder"
            )

    @mcp.tool()
    async def get_app_charts(request: GetAppChartsRequest) -> GetAppChartsResponse:
        """
        Get all charts for a Clappia app's analytics dashboard.
        """
        try:
            return analytics_client.get_charts(
                app_id=request.app_id
            )   
        except Exception as e:
            logger.error(f"Error in get_app_charts: {str(e)}")
            return GetAppChartsResponse(
                success=False,
                message=f"Error getting app charts: {str(e)}",
                app_id=request.app_id,
                operation="get"
            )