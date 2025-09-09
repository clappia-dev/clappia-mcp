"""
workplace.py - Clappia MCP Workplace Module using Modern Pydantic Approach
Handles all workplace user management operations with clean Pydantic models
"""

from mcp.server.fastmcp import FastMCP
from utils import get_logger, workplace_client
from clappia_api_tools.models import (
    AddUserToWorkplaceRequest,
    UpdateWorkplaceUserDetailsRequest,
    UpdateWorkplaceUserAttributesRequest,
    UpdateWorkplaceUserRoleRequest,
    UpdateWorkplaceUserGroupsRequest,
    AddUserToAppRequest,
    GetWorkplaceAppsRequest,
    GetWorkplaceUserAppsRequest,
    GetWorkplaceUsersRequest,
    WorkplaceUserResponse,
    WorkplaceUserDetailsResponse,
    WorkplaceUserAttributesResponse,
    WorkplaceUserRoleResponse,
    WorkplaceUserGroupsResponse,
    AppUserResponse,
    WorkplaceAppResponse,
    WorkplaceUserAppsResponse,
    WorkplaceUsersResponse,
)

logger = get_logger(__name__)


def register_workplace_tools(mcp: FastMCP):

    @mcp.tool()
    def add_user_workplace(
        request: AddUserToWorkplaceRequest,
    ) -> WorkplaceUserResponse:
        """
        Add a new user to the Clappia workplace.

        Supports adding users with email or phone number, along with optional group assignments
        and custom attributes. Only one contact method (email or phone) is required.
        """
        return workplace_client.add_user_to_workplace(
            first_name=request.first_name,
            last_name=request.last_name,
            email_address=request.email_address,
            phone_number=request.phone_number,
            group_names=request.group_names,
            attributes=request.attributes,
        )

    @mcp.tool()
    def update_workplace_user_details(
        request: UpdateWorkplaceUserDetailsRequest,
    ) -> WorkplaceUserDetailsResponse:
        """
        Update workplace user details in Clappia.

        Allows modification of user information including first name, last name, email address,
        and phone number. Only one contact method (email or phone) is required for identification.
        """
        return workplace_client.update_workplace_user_details(
            updated_details=request.updated_details,
            email_address=request.email_address,
            phone_number=request.phone_number,
        )

    @mcp.tool()
    def update_workplace_user_attributes(
        request: UpdateWorkplaceUserAttributesRequest,
    ) -> WorkplaceUserAttributesResponse:
        """
        Update workplace user attributes in Clappia.

        Modifies custom attributes associated with a workplace user. Only one contact method
        (email or phone) is required for identification.
        """
        return workplace_client.update_workplace_user_attributes(
            attributes=request.attributes,
            email_address=request.email_address,
            phone_number=request.phone_number,
        )

    @mcp.tool()
    def update_workplace_user_role(
        request: UpdateWorkplaceUserRoleRequest,
    ) -> WorkplaceUserRoleResponse:
        """
        Update workplace user role in Clappia.

        Changes the role of a workplace user. Only one contact method (email or phone) is required
        for identification. Supports various role types including Admin, User, etc.
        """
        return workplace_client.update_workplace_user_role(
            role=request.role,
            email_address=request.email_address,
            phone_number=request.phone_number,
        )

    @mcp.tool()
    def update_workplace_user_groups(
        request: UpdateWorkplaceUserGroupsRequest,
    ) -> WorkplaceUserGroupsResponse:
        """
        Update workplace user groups in Clappia.

        Modifies the group assignments for a workplace user. Only one contact method (email or phone)
        is required for identification. Groups help organize and manage user access.
        """
        return workplace_client.update_workplace_user_groups(
            group_names=request.group_names,
            email_address=request.email_address,
            phone_number=request.phone_number,
        )

    @mcp.tool()
    def add_user(request: AddUserToAppRequest) -> AppUserResponse:
        """
        Add a user to a specific Clappia app with permissions.

        Grants app access to a workplace user with specific permissions. Only one contact method
        (email or phone) is required for identification. Supports various permission types.
        """
        return workplace_client.add_user_to_app(
            app_id=request.app_id,
            permissions=request.permissions.model_dump(),
            email_address=request.email_address,
            phone_number=request.phone_number,
        )

    @mcp.tool()
    def get_workplace_apps(
        request: GetWorkplaceAppsRequest,
    ) -> WorkplaceAppResponse:
        """
        Get all apps available in the Clappia workplace.

        Retrieves a list of all apps that exist in the workplace, including metadata
        such as app ID, name, creation date, and last update information.
        """
        return workplace_client.get_workplace_apps()

    @mcp.tool()
    def get_workplace_user_apps(
        request: GetWorkplaceUserAppsRequest,
    ) -> WorkplaceUserAppsResponse:
        """
        Get apps accessible to a specific workplace user.

        Retrieves the list of apps that a particular user has access to. Only one contact method
        (email or phone) is required for identification.
        """
        return workplace_client.get_workplace_user_apps(
            email_address=request.email_address, phone_number=request.phone_number
        )

    @mcp.tool()
    def get_workplace_users(
        request: GetWorkplaceUsersRequest,
    ) -> WorkplaceUsersResponse:
        """
        Get workplace users with pagination support.

        Retrieves a paginated list of all users in the workplace. Supports pagination
        with page size and token parameters for efficient data retrieval.
        """
        return workplace_client.get_workplace_users(
            page_size=request.page_size, token=request.token
        )
