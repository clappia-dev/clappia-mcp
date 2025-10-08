"""
workplace.py - Clappia MCP Workplace Module using Modern Pydantic Approach
Handles all workplace user management operations with clean Pydantic models
"""

from typing import Literal
from pydantic import EmailStr

from mcp.server.fastmcp import FastMCP
from src.utils import get_logger, workplace_client
from clappia_api_tools.models.permissions import Permission

from clappia_api_tools.models.request import (
    AddUserToWorkplaceRequest,
    UpdateWorkplaceUserDetailsRequest,
    UpdateWorkplaceUserAttributesRequest,
)
from clappia_api_tools.models.response import (
    BaseResponse,
    AppUserResponse,
    WorkplaceUsersResponse,
)

logger = get_logger(__name__)


def register_workplace_tools(mcp: FastMCP):

    @mcp.tool()
    def add_user_to_workplace(
        first_name: str,
        last_name: str,
        email_address: EmailStr | None = None,
        phone_number: str | None = None,
        group_names: list[str] | None = None,
        attributes: dict[str, str] | None = None,
    ) -> BaseResponse:
        """
        Add a new user to the Clappia workplace.

        Supports adding users with email or phone number, along with optional group assignments
        and custom attributes. Only one contact method (email or phone) is required.
        """
        
        request = AddUserToWorkplaceRequest(
            first_name=first_name,
            last_name=last_name,
            email_address=email_address,
            phone_number=phone_number,
            group_names=group_names or [],
            attributes=attributes or {},
        )
        
        return workplace_client.add_user_to_workplace(request)

    @mcp.tool()
    def update_workplace_user_details(
        updated_details: dict[str, str],
        email_address: EmailStr | None = None,
        phone_number: str | None = None,
    ) -> BaseResponse:
        """
        Update workplace user details in Clappia.

        Allows modification of user information including first name, last name, email address,
        and phone number. Only one contact method (email or phone) is required for identification.
        """
        
        request = UpdateWorkplaceUserDetailsRequest(
            updated_details=updated_details,
            email_address=email_address,
            phone_number=phone_number,
        )
        
        return workplace_client.update_workplace_user_details(request)

    @mcp.tool()
    def update_workplace_user_attributes(
        attributes: dict[str, str],
        email_address: EmailStr | None = None,
        phone_number: str | None = None,
    ) -> BaseResponse:
        """
        Update workplace user attributes in Clappia.

        Modifies custom attributes associated with a workplace user. Only one contact method
        (email or phone) is required for identification.
        """
        
        request = UpdateWorkplaceUserAttributesRequest(
            attributes=attributes,
            email_address=email_address,
            phone_number=phone_number,
        )
        
        return workplace_client.update_workplace_user_attributes(request)

    @mcp.tool()
    def update_workplace_user_role(
        role: Literal["Workplace Manager", "App Builder", "User"] = "User",
        email_address: EmailStr | None = None,
        phone_number: str | None = None,
    ) -> BaseResponse:
        """
        Update workplace user role in Clappia.

        Changes the role of a workplace user. Only one contact method (email or phone) is required
        for identification. Supports various role types including Workplace Manager, App Builder, User.
        """
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
    ) -> BaseResponse:
        """
        Update workplace user groups in Clappia.

        Modifies the group assignments for a workplace user. Only one contact method (email or phone)
        is required for identification. Groups help organize and manage user access.
        """
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
    ) -> AppUserResponse:
        """
        Add a user to a specific Clappia app with permissions.

        Grants app access to a workplace user with specific permissions. Only one contact method
        (email or phone) is required for identification. Supports various permission types.
        """
        return workplace_client.add_user_to_app(
            app_id=app_id,
            permissions=permissions,
            email_address=email_address,
            phone_number=phone_number,
        )

    @mcp.tool()
    def get_workplace_apps() -> BaseResponse:
        """
        Get all apps available in the Clappia workplace.

        Retrieves a list of all apps that exist in the workplace, including metadata
        such as app ID, name, creation date, and last update information.
        """
        return workplace_client.get_workplace_apps()

    @mcp.tool()
    def get_workplace_user_apps(
        email_address: EmailStr | None = None,
        phone_number: str | None = None,
    ) -> BaseResponse:
        """
        Get apps accessible to a specific workplace user.

        Retrieves the list of apps that a particular user has access to. Only one contact method
        (email or phone) is required for identification.
        """
        return workplace_client.get_workplace_user_apps(
            email_address=email_address,
            phone_number=phone_number,
        )

    @mcp.tool()
    def get_workplace_users(
        page_size: int = 50,
        token: str | None = None,
    ) -> WorkplaceUsersResponse:
        """
        Get workplace users with pagination support.

        Retrieves a paginated list of all users in the workplace. Supports pagination
        with page size and token parameters for efficient data retrieval.
        """
        return workplace_client.get_workplace_users(
            page_size=page_size,
            token=token,
        )
