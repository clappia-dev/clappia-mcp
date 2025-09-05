from mcp.server.fastmcp import FastMCP
from utils import get_logger, analytics_client
from clappia_api_tools.models import AddChartRequest, UpdateChartRequest, ReorderChartRequest, ChartResponse, GetAppChartsRequest, GetAppChartsResponse


logger = get_logger(__name__)


def register_analytics_tools(mcp: FastMCP):
    """Register all analytics-related tools with the FastMCP server"""
   
    
    @mcp.tool()
    def add_chart_to_clappia_app(request: AddChartRequest) -> ChartResponse:
        """Add a new chart to a Clappia app's analytics dashboard.
        """
        try:
            
            extra_fields = request.get_extra_fields()
            
            return analytics_client.add_chart(
                app_id=request.app_id,
                chart_type=request.chart_type,
                chart_index=request.chart_index,
                chart_title=request.chart_title,
                **extra_fields
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
    def update_chart_in_clappia_app(request: UpdateChartRequest) -> ChartResponse:
        """Update an existing chart in a Clappia app's analytics dashboard."""
        try:
            
            extra_fields = request.get_extra_fields()
            update_data = {}
            
            if request.chart_title is not None:
                update_data["chart_title"] = request.chart_title
            
            update_data.update(extra_fields)
            
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
    def reorder_chart_in_clappia_app(request: ReorderChartRequest) -> ChartResponse:
        """Reorder charts in a Clappia app's analytics dashboard."""
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
    def get_app_charts(request: GetAppChartsRequest) -> GetAppChartsResponse:
        """Get all charts for a Clappia app's analytics dashboard."""
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