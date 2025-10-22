"""
definitions.py - Clappia MCP Definitions Module
Handles all app definition-related operations with clean Pydantic models
"""

from mcp.server.fastmcp import FastMCP
from src.utils.logging_utils import get_logger
from src.utils.context import get_api_key
from src.utils.constants import (
    CLAPPIA_APP_DEFINITION_DEV_API_BASE_URL,
    CLAPPIA_APP_DEFINITION_PREPROD_API_BASE_URL,
    CLAPPIA_APP_DEFINITION_PROD_API_BASE_URL,
)
from clappia_api_tools import AppDefinitionAPIKeyClient as AppDefinitionClient
from typing import Union, Optional
from clappia_api_tools.models import (
    CreateAppRequest,
    AddPageBreakRequest,
    UpdatePageBreakRequest,
    ReorderSectionRequest,
    UpsertSectionRequest,
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
    UpdateAppMetadataRequest,
)

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

logger = get_logger(__name__)


def _get_app_definition_client() -> AppDefinitionClient:
    api_key = get_api_key()
    return AppDefinitionClient(
        api_key=api_key,
        base_url=CLAPPIA_APP_DEFINITION_DEV_API_BASE_URL,
    )


def register_definition_tools(mcp: FastMCP):

    @mcp.tool()
    def add_section(
        request: UpsertSectionRequest,
    ):
        """Add a new section to a Clappia application at a specified position."""
        app_definition_client = _get_app_definition_client()
        return app_definition_client.add_section(request=request)

    @mcp.tool()
    def update_section(
        request: UpsertSectionRequest,
    ):
        """Update an existing section in a Clappia application."""
        app_definition_client = _get_app_definition_client()
        return app_definition_client.update_section(request=request)

    @mcp.tool()
    def reorder_section(
        request: ReorderSectionRequest,
    ):
        """Reorder a section within a Clappia application."""
        app_definition_client = _get_app_definition_client()
        return app_definition_client.reorder_section(request=request)

    @mcp.tool()
    def add_field(
        app_id: str,
        section_index: int,
        field_index: int,
        page_index: int,
        field_name: str,
        request: FieldRequestUnion,
        version_variable_name: Optional[str] = None,
    ):
        """Add a field to a Clappia app. The field type is determined by the request object type."""
        app_definition_client = _get_app_definition_client()
        return app_definition_client.add_field(
            app_id=app_id,
            section_index=section_index,
            field_index=field_index,
            page_index=page_index,
            field_name=field_name,
            request=request,
            version_variable_name=version_variable_name,
        )

    @mcp.tool()
    def update_field(
        app_id: str,
        field_name: str,
        request: FieldRequestUnion,
        version_variable_name: Optional[str] = None,
    ):
        """Update a field in a Clappia app. The field type is determined by the request object type."""
        app_definition_client = _get_app_definition_client()
        return app_definition_client.update_field(
            app_id=app_id,
            field_name=field_name,
            request=request,
            version_variable_name=version_variable_name,
        )

    @mcp.tool()
    def reorder_field(
        app_id: str,
        source_page_index: int,
        target_page_index: int,
        source_section_index: int,
        target_section_index: int,
        index_in_target_section: int,
        field_name: str,
        version_variable_name: Optional[str] = None,
    ):
        """Reorder a field in a Clappia app."""
        app_definition_client = _get_app_definition_client()
        return app_definition_client.reorder_field(
            app_id=app_id,
            source_page_index=source_page_index,
            target_page_index=target_page_index,
            source_section_index=source_section_index,
            target_section_index=target_section_index,
            index_in_target_section=index_in_target_section,
            field_name=field_name,
            version_variable_name=version_variable_name,
        )

    @mcp.tool()
    def add_page_break(
        request: AddPageBreakRequest,
    ):
        """Add a page break to a Clappia application at a specified position."""
        app_definition_client = _get_app_definition_client()
        return app_definition_client.add_page_break(request=request)

    @mcp.tool()
    def update_page_break(
        request: UpdatePageBreakRequest,
    ):
        """Update an existing page break in a Clappia application."""
        app_definition_client = _get_app_definition_client()
        return app_definition_client.update_page(request=request)

    @mcp.tool()
    def get_app_definition(app_id: str, version_variable_name: Optional[str] = None):
        """Get the complete definition of a Clappia application, including forms, fields, sections, and metadata."""
        app_definition_client = _get_app_definition_client()
        return app_definition_client.get_definition(
            app_id=app_id,
            version_variable_name=version_variable_name,
        )

    @mcp.tool()
    def create_app(request: CreateAppRequest):
        """Create a new Clappia application with specified sections and fields."""
        app_definition_client = _get_app_definition_client()
        return app_definition_client.create_app(request=request)

    @mcp.tool()
    def update_app_metadata(
        app_id: str,
        request: UpdateAppMetadataRequest,
        version_variable_name: Optional[str] = None,
    ):
        """Update the metadata of a Clappia application."""
        app_definition_client = _get_app_definition_client()
        return app_definition_client.update_app_metadata(
            app_id=app_id, request=request, version_variable_name=version_variable_name
        )

    @mcp.tool()
    def get_app_versions(app_id: str):
        """Get the versions of a Clappia application."""
        app_definition_client = _get_app_definition_client()
        return app_definition_client.get_app_versions(app_id=app_id)

    @mcp.tool()
    def update_app_version(
        app_id: str, initial_version_name: str, new_version_name: str
    ):
        """Update a specific version of a Clappia application."""
        app_definition_client = _get_app_definition_client()
        return app_definition_client.update_app_version(
            app_id=app_id,
            initial_version_name=initial_version_name,
            new_version_name=new_version_name,
        )

    @mcp.tool()
    def update_live_version(app_id: str, version_variable_name: str):
        """Update the live version of a Clappia application."""
        app_definition_client = _get_app_definition_client()
        return app_definition_client.update_live_version(
            app_id=app_id, version_variable_name=version_variable_name
        )

    @mcp.tool()
    def create_app_version(app_id: str, version_name: str):
        """Create a new version of a Clappia application."""
        app_definition_client = _get_app_definition_client()
        return app_definition_client.create_new_app_version(
            app_id=app_id, version_name=version_name
        )
