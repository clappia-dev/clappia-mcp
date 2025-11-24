"""
workplace.py - Clappia MCP Workplace Module using Modern Pydantic Approach
Handles all workplace user management operations with clean Pydantic models
"""

import logging
from typing import Literal

from clappia_api_tools.models.request import (
    AddUserToWorkplaceRequest,
    UpdateWorkplaceUserAttributesRequest,
    UpdateWorkplaceUserDetailsRequest,
)
from clappia_api_tools.models.workplace import Permission
from mcp.server.fastmcp import FastMCP
from pydantic import EmailStr

from src.utils.client import get_workplace_client

logger = logging.getLogger(__name__)


def register_workplace_tools(mcp: FastMCP):

    @mcp.tool()
    async def add_user_to_workplace(
        workplace_id: str,
        first_name: str,
        last_name: str,
        email_address: EmailStr | None = None,
        phone_number: str | None = None,
        group_names: list[str] | None = None,
        attributes: dict[str, str] | None = None,
    ):
        """Add user to workplace.

        Args:
            workplace_id: ASK USER - Workplace identifier
            first_name: ASK USER - User's first name
            last_name: ASK USER - User's last name
            email_address: User email (required if phone_number not provided)
            phone_number: User phone number (required if email_address not provided)
            group_names: List of group names (optional)
            attributes: Custom attributes dict (optional)
        """

        request = AddUserToWorkplaceRequest(
            first_name=first_name,
            last_name=last_name,
            email_address=email_address,
            phone_number=phone_number,
            group_names=group_names or [],
            attributes=attributes or {},
        )

        workplace_client = get_workplace_client(workplace_id)
        try:
            return await workplace_client.add_user_to_workplace(request)
        finally:
            await workplace_client.close()

    @mcp.tool()
    async def update_workplace_user_details(
        workplace_id: str,
        updated_details: dict[str, str],
        email_address: EmailStr | None = None,
        phone_number: str | None = None,
    ):
        """Update workplace user details.

        Args:
            workplace_id: ASK USER - Workplace identifier
            updated_details: ASK USER - Dict of fields to update (e.g., {'first_name': 'John'})
            email_address: User email (required if phone_number not provided)
            phone_number: User phone number (required if email_address not provided)
        """

        request = UpdateWorkplaceUserDetailsRequest(
            updated_details=updated_details,
            email_address=email_address,
            phone_number=phone_number,
        )

        workplace_client = get_workplace_client(workplace_id)
        try:
            return await workplace_client.update_workplace_user_details(request)
        finally:
            await workplace_client.close()

    @mcp.tool()
    async def update_workplace_user_attributes(
        workplace_id: str,
        attributes: dict[str, str],
        email_address: EmailStr | None = None,
        phone_number: str | None = None,
    ):
        """Update workplace user custom attributes.

        Args:
            workplace_id: ASK USER - Workplace identifier
            attributes: ASK USER - Dict of attribute names and values to update
            email_address: User email (required if phone_number not provided)
            phone_number: User phone number (required if email_address not provided)
        """

        request = UpdateWorkplaceUserAttributesRequest(
            attributes=attributes,
            email_address=email_address,
            phone_number=phone_number,
        )

        workplace_client = get_workplace_client(workplace_id)
        try:
            return await workplace_client.update_workplace_user_attributes(request)
        finally:
            await workplace_client.close()

    @mcp.tool()
    async def update_workplace_user_role(
        workplace_id: str,
        role: Literal["Workplace Manager", "App Builder", "User"] = "User",
        email_address: EmailStr | None = None,
        phone_number: str | None = None,
    ):
        """Update workplace user role. Options: "Workplace Manager", "App Builder", "User".

        Args:
            workplace_id: ASK USER - Workplace identifier
            role: Role to assign (default: "User")
            email_address: User email (required if phone_number not provided)
            phone_number: User phone number (required if email_address not provided)
        """
        workplace_client = get_workplace_client(workplace_id)
        try:
            return await workplace_client.update_workplace_user_role(
                email_address=email_address,
                phone_number=phone_number,
                role=role,
            )
        finally:
            await workplace_client.close()

    @mcp.tool()
    async def update_workplace_user_groups(
        workplace_id: str,
        group_names: list[str],
        email_address: EmailStr | None = None,
        phone_number: str | None = None,
    ):
        """Update workplace user group membership.

        Args:
            workplace_id: ASK USER - Workplace identifier
            group_names: ASK USER - List of group names to assign
            email_address: User email (required if phone_number not provided)
            phone_number: User phone number (required if email_address not provided)
        """
        workplace_client = get_workplace_client(workplace_id)
        try:
            return await workplace_client.update_workplace_user_groups(
                email_address=email_address,
                phone_number=phone_number,
                group_names=group_names,
            )
        finally:
            await workplace_client.close()

    @mcp.tool()
    async def add_user_to_app(
        app_id: str,
        workplace_id: str,
        permissions: Permission,
        email_address: EmailStr | None = None,
        phone_number: str | None = None,
    ):
        """Grant workplace user access to app.

        Args:
            app_id: ASK USER - App identifier
            workplace_id: ASK USER - Workplace identifier
            permissions: ASK USER - Permission object specifying access level
            email_address: User email (required if phone_number not provided)
            phone_number: User phone number (required if email_address not provided)
        """
        workplace_client = get_workplace_client(workplace_id)
        try:
            return await workplace_client.add_user_to_app(
                app_id=app_id,
                permissions=permissions,
                email_address=email_address,
                phone_number=phone_number,
            )
        finally:
            await workplace_client.close()

    @mcp.tool()
    async def get_workplace_apps(workplace_id: str):
        """Get all apps in workplace.

        Args:
            workplace_id: ASK USER - Workplace identifier
        """
        workplace_client = get_workplace_client(workplace_id)
        try:
            return await workplace_client.get_workplace_apps()
        finally:
            await workplace_client.close()

    @mcp.tool()
    async def get_workplace_user_apps(
        workplace_id: str,
        email_address: EmailStr | None = None,
        phone_number: str | None = None,
    ):
        """Get apps accessible to workplace user.

        Args:
            workplace_id: ASK USER - Workplace identifier
            email_address: User email (required if phone_number not provided)
            phone_number: User phone number (required if email_address not provided)
        """
        workplace_client = get_workplace_client(workplace_id)
        try:
            return await workplace_client.get_workplace_user_apps(
                email_address=email_address,
                phone_number=phone_number,
            )
        finally:
            await workplace_client.close()

    @mcp.tool()
    async def get_workplace_users(
        workplace_id: str,
        page_size: int = 50,
        token: str | None = None,
    ):
        """Get paginated list of workplace users.

        Args:
            workplace_id: ASK USER - Workplace identifier
            page_size: Number of users per page (default: 50)
            token: Pagination token for next page (optional)
        """
        workplace_client = get_workplace_client(workplace_id)
        try:
            return await workplace_client.get_workplace_users(
                page_size=page_size,
                token=token,
            )
        finally:
            await workplace_client.close()
