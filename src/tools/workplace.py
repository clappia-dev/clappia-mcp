"""
workplace.py - Clappia MCP Workplace Module using Modern Pydantic Approach
Handles all workplace user management operations with clean Pydantic models
"""

from typing import Literal
from pydantic import EmailStr

from mcp.server.fastmcp import FastMCP
from src.utils.logging_utils import get_logger
from src.utils.context import get_api_key
from src.utils.constants import (
    CLAPPIA_EXTERNAL_DEV_API_BASE_URL,
    CLAPPIA_EXTERNAL_PREPROD_API_BASE_URL,
    CLAPPIA_EXTERNAL_PROD_API_BASE_URL,
)
from clappia_api_tools import WorkplaceAPIKeyClient as WorkplaceClient
from clappia_api_tools.models.permissions import Permission

from clappia_api_tools.models.request import (
    AddUserToWorkplaceRequest,
    UpdateWorkplaceUserDetailsRequest,
    UpdateWorkplaceUserAttributesRequest,
)


logger = get_logger(__name__)


def _get_workplace_client() -> WorkplaceClient:
    api_key = get_api_key()
    return WorkplaceClient(
        api_key=api_key,
        base_url=CLAPPIA_EXTERNAL_DEV_API_BASE_URL,
    )


def register_workplace_tools(mcp: FastMCP):

    @mcp.tool()
    def add_user_to_workplace(
        first_name: str,
        last_name: str,
        email_address: EmailStr | None = None,
        phone_number: str | None = None,
        group_names: list[str] | None = None,
        attributes: dict[str, str] | None = None,
    ):
        """Add a new user to the Clappia workplace."""

        request = AddUserToWorkplaceRequest(
            first_name=first_name,
            last_name=last_name,
            email_address=email_address,
            phone_number=phone_number,
            group_names=group_names or [],
            attributes=attributes or {},
        )

        workplace_client = _get_workplace_client()
        return workplace_client.add_user_to_workplace(request)

    @mcp.tool()
    def update_workplace_user_details(
        updated_details: dict[str, str],
        email_address: EmailStr | None = None,
        phone_number: str | None = None,
    ):
        """Update workplace user details in Clappia."""

        request = UpdateWorkplaceUserDetailsRequest(
            updated_details=updated_details,
            email_address=email_address,
            phone_number=phone_number,
        )

        workplace_client = _get_workplace_client()
        return workplace_client.update_workplace_user_details(request)

    @mcp.tool()
    def update_workplace_user_attributes(
        attributes: dict[str, str],
        email_address: EmailStr | None = None,
        phone_number: str | None = None,
    ):
        """Update workplace user attributes in Clappia."""

        request = UpdateWorkplaceUserAttributesRequest(
            attributes=attributes,
            email_address=email_address,
            phone_number=phone_number,
        )

        workplace_client = _get_workplace_client()
        return workplace_client.update_workplace_user_attributes(request)

    @mcp.tool()
    def update_workplace_user_role(
        role: Literal["Workplace Manager", "App Builder", "User"] = "User",
        email_address: EmailStr | None = None,
        phone_number: str | None = None,
    ):
        """Update workplace user role in Clappia."""
        workplace_client = _get_workplace_client()
        return workplace_client.update_workplace_user_role(
            email_address=email_address,
            phone_number=phone_number,
            role=role,
        )

    @mcp.tool()
    def update_workplace_user_groups(
        group_names: list[str],
        email_address: EmailStr | None = None,
        phone_number: str | None = None,
    ):
        """Update workplace user groups in Clappia."""
        workplace_client = _get_workplace_client()
        return workplace_client.update_workplace_user_groups(
            email_address=email_address,
            phone_number=phone_number,
            group_names=group_names,
        )

    @mcp.tool()
    def add_user_to_app(
        app_id: str,
        permissions: Permission,
        email_address: EmailStr | None = None,
        phone_number: str | None = None,
    ):
        """Add a user to a specific Clappia app with permissions."""
        workplace_client = _get_workplace_client()
        return workplace_client.add_user_to_app(
            app_id=app_id,
            permissions=permissions,
            email_address=email_address,
            phone_number=phone_number,
        )

    @mcp.tool()
    def get_workplace_apps():
        """Get all apps available in the Clappia workplace."""
        workplace_client = _get_workplace_client()
        return workplace_client.get_workplace_apps()

    @mcp.tool()
    def get_workplace_user_apps(
        email_address: EmailStr | None = None,
        phone_number: str | None = None,
    ):
        """Get apps accessible to a specific workplace user."""
        workplace_client = _get_workplace_client()
        return workplace_client.get_workplace_user_apps(
            email_address=email_address,
            phone_number=phone_number,
        )

    @mcp.tool()
    def get_workplace_users(
        page_size: int = 50,
        token: str | None = None,
    ):
        """Get workplace users with pagination support."""
        workplace_client = _get_workplace_client()
        return workplace_client.get_workplace_users(
            page_size=page_size,
            token=token,
        )
