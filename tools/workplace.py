"""
workplace.py - Clappia MCP Workplace Module using Modern Pydantic Approach
Handles all workplace user management operations with clean Pydantic models
"""

from mcp.server.fastmcp import FastMCP
from utils import get_logger, workplace_client
from clappia_api_tools.models import (
    AddUserToWorkplaceRequest, UpdateWorkplaceUserDetailsRequest, UpdateWorkplaceUserAttributesRequest,
    UpdateWorkplaceUserRoleRequest, UpdateWorkplaceUserGroupsRequest, AddUserToAppRequest,
    GetWorkplaceAppsRequest, GetWorkplaceUserAppsRequest, GetWorkplaceUsersRequest,
    WorkplaceUserResponse, WorkplaceUserDetailsResponse, WorkplaceUserAttributesResponse,
    WorkplaceUserRoleResponse, WorkplaceUserGroupsResponse, AppUserResponse,
    WorkplaceAppResponse, WorkplaceUserAppsResponse, WorkplaceUsersResponse
)

logger = get_logger(__name__)

def register_workplace_tools(mcp: FastMCP):
    
    @mcp.tool()
    def add_user_to_clappia_workplace(request: AddUserToWorkplaceRequest) -> WorkplaceUserResponse:
        """
        Add a new user to the Clappia workplace.
        
        Supports adding users with email or phone number, along with optional group assignments
        and custom attributes. Only one contact method (email or phone) is required.
        """
        try:
            return workplace_client.add_user_to_workplace(
                first_name=request.first_name,
                last_name=request.last_name,
                email_address=request.email_address,
                phone_number=request.phone_number,
                group_names=request.group_names,
                attributes=request.attributes
            )
        except Exception as e:
            logger.error(f"Error in add_user_to_clappia_workplace: {str(e)}")
            return WorkplaceUserResponse(
                success=False,
                message=f"Error adding user to workplace: {str(e)}",
                email_address=request.email_address,
                phone_number=request.phone_number,
                operation="add_user_to_workplace"
            )

    @mcp.tool()
    def update_clappia_workplace_user_details(request: UpdateWorkplaceUserDetailsRequest) -> WorkplaceUserDetailsResponse:
        """
        Update workplace user details in Clappia.
        
        Allows modification of user information including first name, last name, email address,
        and phone number. Only one contact method (email or phone) is required for identification.
        """
        try:
            return workplace_client.update_workplace_user_details(
                updated_details=request.updated_details,
                email_address=request.email_address,
                phone_number=request.phone_number
            )
        except Exception as e:
            logger.error(f"Error in update_clappia_workplace_user_details: {str(e)}")
            return WorkplaceUserDetailsResponse(
                success=False,
                message=f"Error updating workplace user details: {str(e)}",
                email_address=request.email_address,
                phone_number=request.phone_number,
                operation="update_workplace_user_details"
            )

    @mcp.tool()
    def update_clappia_workplace_user_attributes(request: UpdateWorkplaceUserAttributesRequest) -> WorkplaceUserAttributesResponse:
        """
        Update workplace user attributes in Clappia.
        
        Modifies custom attributes associated with a workplace user. Only one contact method
        (email or phone) is required for identification.
        """
        try:
            return workplace_client.update_workplace_user_attributes(
                attributes=request.attributes,
                email_address=request.email_address,
                phone_number=request.phone_number
            )
        except Exception as e:
            logger.error(f"Error in update_clappia_workplace_user_attributes: {str(e)}")
            return WorkplaceUserAttributesResponse(
                success=False,
                message=f"Error updating workplace user attributes: {str(e)}",
                email_address=request.email_address,
                phone_number=request.phone_number,
                operation="update_workplace_user_attributes"
            )

    @mcp.tool()
    def update_clappia_workplace_user_role(request: UpdateWorkplaceUserRoleRequest) -> WorkplaceUserRoleResponse:
        """
        Update workplace user role in Clappia.
        
        Changes the role of a workplace user. Only one contact method (email or phone) is required
        for identification. Supports various role types including Admin, User, etc.
        """
        try:
            return workplace_client.update_workplace_user_role(
                role=request.role,
                email_address=request.email_address,
                phone_number=request.phone_number
            )
        except Exception as e:
            logger.error(f"Error in update_clappia_workplace_user_role: {str(e)}")
            return WorkplaceUserRoleResponse(
                success=False,
                message=f"Error updating workplace user role: {str(e)}",
                email_address=request.email_address,
                phone_number=request.phone_number,
                operation="update_workplace_user_role"
            )

    @mcp.tool()
    def update_clappia_workplace_user_groups(request: UpdateWorkplaceUserGroupsRequest) -> WorkplaceUserGroupsResponse:
        """
        Update workplace user groups in Clappia.
        
        Modifies the group assignments for a workplace user. Only one contact method (email or phone)
        is required for identification. Groups help organize and manage user access.
        """
        try:
            return workplace_client.update_workplace_user_groups(
                group_names=request.group_names,
                email_address=request.email_address,
                phone_number=request.phone_number
            )
        except Exception as e:
            logger.error(f"Error in update_clappia_workplace_user_groups: {str(e)}")
            return WorkplaceUserGroupsResponse(
                success=False,
                message=f"Error updating workplace user groups: {str(e)}",
                email_address=request.email_address,
                phone_number=request.phone_number,
                operation="update_workplace_user_groups"
            )

    @mcp.tool()
    def add_user_to_clappia_app(request: AddUserToAppRequest) -> AppUserResponse:
        """
        Add a user to a specific Clappia app with permissions.
        
        Grants app access to a workplace user with specific permissions. Only one contact method
        (email or phone) is required for identification. Supports various permission types.
        """
        try:
            return workplace_client.add_user_to_app(
                app_id=request.app_id,
                permissions=request.permissions,
                email_address=request.email_address,
                phone_number=request.phone_number,
                role=request.role
            )
        except Exception as e:
            logger.error(f"Error in add_user_to_clappia_app: {str(e)}")
            return AppUserResponse(
                success=False,
                message=f"Error adding user to app: {str(e)}",
                email_address=request.email_address,
                phone_number=request.phone_number,
                app_id=request.app_id,
                operation="add_user_to_app"
            )

    @mcp.tool()
    def get_clappia_workplace_apps(request: GetWorkplaceAppsRequest) -> WorkplaceAppResponse:
        """
        Get all apps available in the Clappia workplace.
        
        Retrieves a list of all apps that exist in the workplace, including metadata
        such as app ID, name, creation date, and last update information.
        """
        try:
            return workplace_client.get_workplace_apps()
        except Exception as e:
            logger.error(f"Error in get_clappia_workplace_apps: {str(e)}")
            return WorkplaceAppResponse(
                success=False,
                message=f"Error retrieving workplace apps: {str(e)}",
                apps=[],
                operation="get_workplace_apps"
            )

    @mcp.tool()
    def get_clappia_workplace_user_apps(request: GetWorkplaceUserAppsRequest) -> WorkplaceUserAppsResponse:
        """
        Get apps accessible to a specific workplace user.
        
        Retrieves the list of apps that a particular user has access to. Only one contact method
        (email or phone) is required for identification.
        """
        try:
            return workplace_client.get_workplace_user_apps(
                email_address=request.email_address,
                phone_number=request.phone_number
            )
        except Exception as e:
            logger.error(f"Error in get_clappia_workplace_user_apps: {str(e)}")
            return WorkplaceUserAppsResponse(
                success=False,
                message=f"Error retrieving workplace user apps: {str(e)}",
                email_address=request.email_address,
                phone_number=request.phone_number,
                apps=[],
                operation="get_workplace_user_apps"
            )

    @mcp.tool()
    def get_clappia_workplace_users(request: GetWorkplaceUsersRequest) -> WorkplaceUsersResponse:
        """
        Get workplace users with pagination support.
        
        Retrieves a paginated list of all users in the workplace. Supports pagination
        with page size and token parameters for efficient data retrieval.
        """
        try:
            return workplace_client.get_workplace_users(
                page_size=request.page_size,
                token=request.token
            )
        except Exception as e:
            logger.error(f"Error in get_clappia_workplace_users: {str(e)}")
            return WorkplaceUsersResponse(
                success=False,
                message=f"Error retrieving workplace users: {str(e)}",
                users=[],
                operation="get_workplace_users"
            )