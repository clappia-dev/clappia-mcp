"""
definitions.py - Clappia MCP Definitions Module
Handles all app definition-related operations with clean Pydantic models
"""

import logging
from typing import Union

from clappia_api_tools import (
    AppDefinitionAuthTokenClient,
    FileManagementAuthTokenClient,
)
from clappia_api_tools.models import (
    AddPageBreakRequest,
    ExternalPageDefinition,
    UpdateAppMetadataRequest,
    UpdatePageBreakRequest,
    UpsertFieldAddressRequest,
    UpsertFieldAIRequest,
    UpsertFieldButtonRequest,
    UpsertFieldCheckboxRequest,
    UpsertFieldCodeReaderRequest,
    UpsertFieldCodeRequest,
    UpsertFieldCounterRequest,
    UpsertFieldDatabaseRequest,
    UpsertFieldDateRequest,
    UpsertFieldDependencyAppRequest,
    UpsertFieldDropdownRequest,
    UpsertFieldEazypayPaymentGatewayRequest,
    UpsertFieldEmailInputRequest,
    UpsertFieldEmojiRequest,
    UpsertFieldFileRequest,
    UpsertFieldFormulaRequest,
    UpsertFieldGpsLocationRequest,
    UpsertFieldImageViewerRequest,
    UpsertFieldLiveTrackingRequest,
    UpsertFieldManualAddressRequest,
    UpsertFieldNfcReaderRequest,
    UpsertFieldNumberInputRequest,
    UpsertFieldPaypalPaymentGatewayRequest,
    UpsertFieldPdfViewerRequest,
    UpsertFieldPhoneNumberRequest,
    UpsertFieldProgressBarRequest,
    UpsertFieldRadioRequest,
    UpsertFieldRazorpayPaymentGatewayRequest,
    UpsertFieldReadOnlyFileRequest,
    UpsertFieldReadOnlyTextRequest,
    UpsertFieldRestApiRequest,
    UpsertFieldRichTextEditorRequest,
    UpsertFieldSignatureRequest,
    UpsertFieldSliderRequest,
    UpsertFieldStripePaymentGatewayRequest,
    UpsertFieldTagsRequest,
    UpsertFieldTextAreaRequest,
    UpsertFieldTextRequest,
    UpsertFieldTimeRequest,
    UpsertFieldToggleRequest,
    UpsertFieldUniqueSequentialRequest,
    UpsertFieldUrlInputRequest,
    UpsertFieldValidationRequest,
    UpsertFieldVideoViewerRequest,
    UpsertFieldVoiceRequest,
    UpsertSectionRequest,
)
from clappia_api_tools.models.definition import ExternalTemplateDefinition
from mcp.server.fastmcp import FastMCP
from pydantic import EmailStr

from src.utils.constants import (
    APP_DEFINITION_API_BASE_URL,
    FILE_MANAGEMENT_API_BASE_URL,
)
from src.utils.context import get_auth_token

FieldRequestUnion = Union[
    UpsertFieldTextRequest,
    UpsertFieldTextAreaRequest,
    UpsertFieldDependencyAppRequest,
    UpsertFieldRestApiRequest,
    UpsertFieldAddressRequest,
    UpsertFieldDatabaseRequest,
    UpsertFieldDateRequest,
    UpsertFieldAIRequest,
    UpsertFieldCodeRequest,
    UpsertFieldCodeReaderRequest,
    UpsertFieldEmailInputRequest,
    UpsertFieldEmojiRequest,
    UpsertFieldFileRequest,
    UpsertFieldGpsLocationRequest,
    UpsertFieldLiveTrackingRequest,
    UpsertFieldManualAddressRequest,
    UpsertFieldPhoneNumberRequest,
    UpsertFieldProgressBarRequest,
    UpsertFieldSignatureRequest,
    UpsertFieldCounterRequest,
    UpsertFieldSliderRequest,
    UpsertFieldTimeRequest,
    UpsertFieldToggleRequest,
    UpsertFieldValidationRequest,
    UpsertFieldVideoViewerRequest,
    UpsertFieldVoiceRequest,
    UpsertFieldFormulaRequest,
    UpsertFieldImageViewerRequest,
    UpsertFieldRichTextEditorRequest,
    UpsertFieldNfcReaderRequest,
    UpsertFieldNumberInputRequest,
    UpsertFieldPdfViewerRequest,
    UpsertFieldReadOnlyFileRequest,
    UpsertFieldReadOnlyTextRequest,
    UpsertFieldTagsRequest,
    UpsertFieldUniqueSequentialRequest,
    UpsertFieldDropdownRequest,
    UpsertFieldRadioRequest,
    UpsertFieldUrlInputRequest,
    UpsertFieldCheckboxRequest,
    UpsertFieldRazorpayPaymentGatewayRequest,
    UpsertFieldEazypayPaymentGatewayRequest,
    UpsertFieldPaypalPaymentGatewayRequest,
    UpsertFieldStripePaymentGatewayRequest,
    UpsertFieldButtonRequest,
]

logger = logging.getLogger(__name__)


def _get_app_definition_client(workplace_id: str) -> AppDefinitionAuthTokenClient:
    auth_token = get_auth_token()
    file_management_client = FileManagementAuthTokenClient(
        auth_token=auth_token,
        workplace_id=workplace_id,
        base_url=FILE_MANAGEMENT_API_BASE_URL,
    )
    return AppDefinitionAuthTokenClient(
        auth_token=auth_token,
        workplace_id=workplace_id,
        base_url=APP_DEFINITION_API_BASE_URL,
        file_management_client=file_management_client,
    )


def register_definition_tools(mcp: FastMCP):
    @mcp.tool()
    async def add_section(
        app_id: str,
        page_index: int,
        section_index: int,
        workplace_id: str,
        request: UpsertSectionRequest,
        version_variable_name: str | None = None,
    ):
        """Add section to app.

        Args:
            app_id: ASK USER - App identifier
            page_index: ASK USER - Page index where section should be added
            section_index: ASK USER - Position index where section should be inserted
            workplace_id: ASK USER - Workplace identifier
            request: ASK USER - Section definition request object
            version_variable_name: App version variable name (optional)
        """
        app_definition_client = _get_app_definition_client(workplace_id)
        try:
            return await app_definition_client.add_section(
                app_id=app_id,
                page_index=page_index,
                section_index=section_index,
                request=request,
                version_variable_name=version_variable_name,
            )
        finally:
            await app_definition_client.close()

    @mcp.tool()
    async def update_section(
        app_id: str,
        page_index: int,
        section_index: int,
        workplace_id: str,
        request: UpsertSectionRequest,
        version_variable_name: str | None = None,
    ):
        """Update section in app.

        Args:
            app_id: ASK USER - App identifier
            page_index: ASK USER - Page index containing the section
            section_index: ASK USER - Position index of section to update
            workplace_id: ASK USER - Workplace identifier
            request: ASK USER - Section definition request object with updated configuration
            version_variable_name: App version variable name (optional)
        """
        app_definition_client = _get_app_definition_client(workplace_id)
        try:
            return await app_definition_client.update_section(
                app_id=app_id,
                page_index=page_index,
                section_index=section_index,
                request=request,
                version_variable_name=version_variable_name,
            )
        finally:
            await app_definition_client.close()

    @mcp.tool()
    async def reorder_section(
        app_id: str,
        workplace_id: str,
        section_index: int,
        page_index: int,
        source_section_index: int,
        target_section_index: int,
        source_page_index: int,
        target_page_index: int,
        version_variable_name: str | None = None,
    ):
        """Reorder section within app.

        Args:
            app_id: ASK USER - App identifier
            workplace_id: ASK USER - Workplace identifier
            section_index: ASK USER - Index of section being moved
            page_index: ASK USER - Page index containing the section
            source_section_index: ASK USER - Current section index before move
            target_section_index: ASK USER - New section index after move
            source_page_index: ASK USER - Current page index before move
            target_page_index: ASK USER - New page index after move
            version_variable_name: App version variable name (optional)
        """
        app_definition_client = _get_app_definition_client(workplace_id)
        try:
            return await app_definition_client.reorder_section(
                app_id=app_id,
                section_index=section_index,
                page_index=page_index,
                source_section_index=source_section_index,
                target_section_index=target_section_index,
                source_page_index=source_page_index,
                target_page_index=target_page_index,
                version_variable_name=version_variable_name,
            )
        finally:
            await app_definition_client.close()

    @mcp.tool()
    async def add_field(
        app_id: str,
        workplace_id: str,
        section_index: int,
        field_index: int,
        page_index: int,
        field_name: str,
        request: FieldRequestUnion,
        version_variable_name: str | None = None,
    ):
        """Add field to app. Field type determined by request object type.

        Args:
            app_id: ASK USER - App identifier
            workplace_id: ASK USER - Workplace identifier
            section_index: ASK USER - Section index where field should be added
            field_index: ASK USER - Position index within section
            page_index: ASK USER - Page index containing the section
            field_name: ASK USER - Unique name identifier for the field
            request: ASK USER - Field definition request object (type determines field type)
            version_variable_name: App version variable name (optional)
        """
        app_definition_client = _get_app_definition_client(workplace_id)
        try:
            return await app_definition_client.add_field(
                app_id=app_id,
                section_index=section_index,
                field_index=field_index,
                page_index=page_index,
                field_name=field_name,
                request=request,
                version_variable_name=version_variable_name,
            )
        finally:
            await app_definition_client.close()

    @mcp.tool()
    async def update_field(
        app_id: str,
        workplace_id: str,
        field_name: str,
        request: FieldRequestUnion,
        version_variable_name: str | None = None,
    ):
        """Update field in app. Field type must match existing type.

        Args:
            app_id: ASK USER - App identifier
            workplace_id: ASK USER - Workplace identifier
            field_name: ASK USER - Unique name identifier of field to update
            request: ASK USER - Field definition request object with updated configuration
            version_variable_name: App version variable name (optional)
        """
        app_definition_client = _get_app_definition_client(workplace_id)
        try:
            return await app_definition_client.update_field(
                app_id=app_id,
                field_name=field_name,
                request=request,
                version_variable_name=version_variable_name,
            )
        finally:
            await app_definition_client.close()

    @mcp.tool()
    async def reorder_field(
        app_id: str,
        source_page_index: int,
        target_page_index: int,
        source_section_index: int,
        target_section_index: int,
        index_in_target_section: int,
        field_name: str,
        workplace_id: str,
        version_variable_name: str | None = None,
    ):
        """Reorder field within app.

        Args:
            app_id: ASK USER - App identifier
            source_page_index: ASK USER - Current page index before move
            target_page_index: ASK USER - New page index after move
            source_section_index: ASK USER - Current section index before move
            target_section_index: ASK USER - New section index after move
            index_in_target_section: ASK USER - New position index within target section
            field_name: ASK USER - Unique name identifier of field to move
            workplace_id: ASK USER - Workplace identifier
            version_variable_name: App version variable name (optional)
        """
        app_definition_client = _get_app_definition_client(workplace_id)
        try:
            return await app_definition_client.reorder_field(
                app_id=app_id,
                source_page_index=source_page_index,
                target_page_index=target_page_index,
                source_section_index=source_section_index,
                target_section_index=target_section_index,
                index_in_target_section=index_in_target_section,
                field_name=field_name,
                version_variable_name=version_variable_name,
            )
        finally:
            await app_definition_client.close()

    @mcp.tool()
    async def add_page_break(
        app_id: str,
        workplace_id: str,
        request: AddPageBreakRequest,
        version_variable_name: str | None = None,
    ):
        """Add page break to app.

        Args:
            app_id: ASK USER - App identifier
            workplace_id: ASK USER - Workplace identifier
            request: ASK USER - Page break definition request object
            version_variable_name: App version variable name (optional)
        """
        app_definition_client = _get_app_definition_client(workplace_id)
        try:
            return await app_definition_client.add_page_break(
                app_id=app_id,
                request=request,
                version_variable_name=version_variable_name,
            )
        finally:
            await app_definition_client.close()

    @mcp.tool()
    async def update_page_break(
        app_id: str,
        workplace_id: str,
        request: UpdatePageBreakRequest,
        version_variable_name: str | None = None,
    ):
        """Update page break in app.

        Args:
            app_id: ASK USER - App identifier
            workplace_id: ASK USER - Workplace identifier
            request: ASK USER - Page break definition request object with updated configuration
            version_variable_name: App version variable name (optional)
        """
        app_definition_client = _get_app_definition_client(workplace_id)
        try:
            return await app_definition_client.update_page(
                app_id=app_id,
                request=request,
                version_variable_name=version_variable_name,
            )
        finally:
            await app_definition_client.close()

    @mcp.tool()
    async def get_app_definition(
        app_id: str,
        workplace_id: str,
        version_variable_name: str | None = None,
    ):
        """Get complete app definition.

        Args:
            app_id: ASK USER - App identifier
            workplace_id: ASK USER - Workplace identifier
            version_variable_name: App version variable name (optional)
        """
        app_definition_client = _get_app_definition_client(workplace_id)
        try:
            return await app_definition_client.get_definition(
                app_id=app_id,
                version_variable_name=version_variable_name,
            )
        finally:
            await app_definition_client.close()

    @mcp.tool()
    async def create_app(
        workplace_id: str,
        name: str,
        requesting_user_email_address: EmailStr,
        pages: list[ExternalPageDefinition],
        description: str | None = None,
    ):
        """Create new app from scratch.

        Args:
            workplace_id: ASK USER - Workplace identifier
            name: ASK USER - Display name for the app
            requesting_user_email_address: ASK USER - Email of user requesting app creation
            pages: ASK USER - List of page definitions containing sections and fields
            description: App description (optional)
        """
        app_definition_client = _get_app_definition_client(workplace_id)
        try:
            return await app_definition_client.create_app(
                name=name,
                requesting_user_email_address=requesting_user_email_address,
                pages=pages,
                description=description,
            )
        finally:
            await app_definition_client.close()

    @mcp.tool()
    async def update_app_metadata(
        app_id: str,
        workplace_id: str,
        request: UpdateAppMetadataRequest,
        version_variable_name: str | None = None,
    ):
        """Update app metadata (name, description, icon, category).

        Args:
            app_id: ASK USER - App identifier
            workplace_id: ASK USER - Workplace identifier
            request: ASK USER - App metadata request object with updated fields
            version_variable_name: App version variable name (optional)
        """
        app_definition_client = _get_app_definition_client(workplace_id)
        try:
            return await app_definition_client.update_app_metadata(
                app_id=app_id,
                request=request,
                version_variable_name=version_variable_name,
            )
        finally:
            await app_definition_client.close()

    @mcp.tool()
    async def get_app_versions(app_id: str, workplace_id: str):
        """Get all versions of app.

        Args:
            app_id: ASK USER - App identifier
        """
        app_definition_client = _get_app_definition_client(workplace_id)
        try:
            return await app_definition_client.get_app_versions(app_id=app_id)
        finally:
            await app_definition_client.close()

    @mcp.tool()
    async def update_app_version(
        app_id: str,
        workplace_id: str,
        initial_version_name: str,
        new_version_name: str,
    ):
        """Rename app version.

        Args:
            app_id: ASK USER - App identifier
            workplace_id: ASK USER - Workplace identifier
            initial_version_name: ASK USER - Current version name
            new_version_name: ASK USER - New version name
        """
        app_definition_client = _get_app_definition_client(workplace_id)
        try:
            return await app_definition_client.update_app_version(
                app_id=app_id,
                initial_version_name=initial_version_name,
                new_version_name=new_version_name,
            )
        finally:
            await app_definition_client.close()

    @mcp.tool()
    async def update_live_version(
        app_id: str, workplace_id: str, version_variable_name: str
    ):
        """Set live/published version of app.

        Args:
            app_id: ASK USER - App identifier
            workplace_id: ASK USER - Workplace identifier
            version_variable_name: ASK USER - Version name to set as live
        """
        app_definition_client = _get_app_definition_client(workplace_id)
        try:
            return await app_definition_client.update_live_version(
                app_id=app_id, version_variable_name=version_variable_name
            )
        finally:
            await app_definition_client.close()

    @mcp.tool()
    async def add_new_print_template(
        app_id: str,
        workplace_id: str,
        definition: ExternalTemplateDefinition,
        body_html_string: str,
        header_html_string: str | None = None,
        footer_html_string: str | None = None,
        version_variable_name: str | None = None,
    ):
        """Add new app template.

        Args:
            app_id: ASK USER - App identifier
            workplace_id: ASK USER - Workplace identifier
            definition: ASK USER - Template definition
            body_html_string: ASK USER - Template body HTML
            header_html_string: ASK USER - Template header HTML (optional)
            footer_html_string: ASK USER - Template footer HTML (optional)
            version_variable_name: App version variable name (optional)
        """
        app_definition_client = _get_app_definition_client(workplace_id)
        try:
            return await app_definition_client.add_new_print_template(
                app_id=app_id,
                definition=definition,
                body_html_string=body_html_string,
                header_html_string=header_html_string,
                footer_html_string=footer_html_string,
                version_variable_name=version_variable_name,
            )
        finally:
            await app_definition_client.close()

    @mcp.tool()
    async def update_app_template(
        app_id: str,
        workplace_id: str,
        index: int,
        definition: ExternalTemplateDefinition,
        body_html_string: str,
        header_html_string: str | None = None,
        footer_html_string: str | None = None,
        version_variable_name: str | None = None,
    ):
        """Update app template.

        Args:
            app_id: ASK USER - App identifier
            workplace_id: ASK USER - Workplace identifier
            index: ASK USER - Template index
            definition: ASK USER - Template definition
            body_html_string: ASK USER - Template body HTML
            header_html_string: ASK USER - Template header HTML (optional)
            footer_html: ASK USER - Template footer HTML (optional)
            version_variable_name: App version variable name (optional)
        """
        app_definition_client = _get_app_definition_client(workplace_id)
        try:
            return await app_definition_client.update_print_template(
                app_id=app_id,
                index=index,
                definition=definition,
                body_html_string=body_html_string,
                header_html_string=header_html_string,
                footer_html_string=footer_html_string,
                version_variable_name=version_variable_name,
            )
        finally:
            await app_definition_client.close()

    @mcp.tool()
    async def get_print_templates(
        app_id: str,
        workplace_id: str,
        version_variable_name: str | None = None,
    ):
        """Get print templates.

        Args:
            app_id: ASK USER - App identifier
            workplace_id: ASK USER - Workplace identifier
            version_variable_name: App version variable name (optional)
        """
        app_definition_client = _get_app_definition_client(workplace_id)
        try:
            return await app_definition_client.get_print_templates(
                app_id=app_id,
                version_variable_name=version_variable_name,
            )
        finally:
            await app_definition_client.close()

    @mcp.tool()
    async def update_app_icon(
        app_id: str,
        workplace_id: str,
        icon_public_url: str,
        version_variable_name: str | None = None,
    ):
        """Update app icon.

        Args:
            app_id: ASK USER - App identifier
            workplace_id: ASK USER - Workplace identifier
            icon_public_url: ASK USER - App icon public URL
            version_variable_name: App version variable name (optional)
        """
        app_definition_client = _get_app_definition_client(workplace_id)
        try:
            return await app_definition_client.update_app_icon(
                app_id=app_id,
                icon_public_url=icon_public_url,
                version_variable_name=version_variable_name,
            )
        finally:
            await app_definition_client.close()

    @mcp.tool()
    async def create_app_version(
        app_id: str,
        workplace_id: str,
        version_name: str,
    ):
        """Create new app version.

        Args:
            app_id: ASK USER - App identifier
            workplace_id: ASK USER - Workplace identifier
            version_name: ASK USER - Unique name for the new version
        """
        app_definition_client = _get_app_definition_client(workplace_id)
        try:
            return await app_definition_client.create_new_app_version(
                app_id=app_id,
                version_name=version_name,
            )
        finally:
            await app_definition_client.close()

    @mcp.tool()
    async def get_print_template_html_content(
        app_id: str,
        workplace_id: str,
        body_file_id: str,
        header_file_id: str | None = None,
        footer_file_id: str | None = None,
    ):
        """Get print template HTML content.

        Args:
            app_id: ASK USER - App identifier
            workplace_id: ASK USER - Workplace identifier
            body_file_id: ASK USER - Body file identifier
            header_file_id: ASK USER - Header file identifier (optional)
            footer_file_id: ASK USER - Footer file identifier (optional)
        """
        app_definition_client = _get_app_definition_client(workplace_id)
        try:
            return await app_definition_client.get_print_template_content(
                app_id=app_id,
                body_file_id=body_file_id,
                header_file_id=header_file_id,
                footer_file_id=footer_file_id,
            )
        finally:
            await app_definition_client.close()
