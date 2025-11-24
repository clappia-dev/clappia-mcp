import logging

from mcp.server.fastmcp import FastMCP

from src.utils.client import get_file_management_client

logger = logging.getLogger(__name__)


def register_file_management_tools(mcp: FastMCP):
    @mcp.tool()
    async def get_read_only_file_public_url(
        app_id: str,
        file_id: str,
        workplace_id: str,
    ):
        """Get read-only file public URL.

        Args:
            app_id: ASK USER - App identifier
            file_id: ASK USER - File identifier
            workplace_id: ASK USER - Workplace identifier
        """
        file_management_client = get_file_management_client(workplace_id)
        try:
            return await file_management_client.get_attached_file_file_url(
                app_id=app_id, file_id=file_id
            )
        finally:
            await file_management_client.close()

    @mcp.tool()
    async def get_image_viewer_file_public_url(
        app_id: str,
        file_id: str,
        workplace_id: str,
    ):
        """Get image viewer file public URL.

        Args:
            app_id: ASK USER - App identifier
            file_id: ASK USER - File identifier
            workplace_id: ASK USER - Workplace identifier
        """
        file_management_client = get_file_management_client(workplace_id)
        try:
            return await file_management_client.get_image_viewer_file_url(
                app_id=app_id, file_id=file_id
            )
        finally:
            await file_management_client.close()

    @mcp.tool()
    async def get_pdf_viewer_file_public_url(
        app_id: str,
        file_id: str,
        workplace_id: str,
    ):
        """Get pdf viewer file public URL.

        Args:
            app_id: ASK USER - App identifier
            file_id: ASK USER - File identifier
            workplace_id: ASK USER - Workplace identifier
        """
        file_management_client = get_file_management_client(workplace_id)
        try:
            return await file_management_client.get_pdf_viewer_file_url(
                app_id=app_id, file_id=file_id
            )
        finally:
            await file_management_client.close()

    @mcp.tool()
    async def get_video_viewer_file_public_url(
        app_id: str,
        file_id: str,
        workplace_id: str,
    ):
        """Get read-only file public URL.

        Args:
            app_id: ASK USER - App identifier
            file_id: ASK USER - File identifier
            workplace_id: ASK USER - Workplace identifier
        """
        file_management_client = get_file_management_client(workplace_id)
        try:
            return await file_management_client.get_video_viewer_file_url(
                app_id=app_id, file_id=file_id
            )
        finally:
            await file_management_client.close()
