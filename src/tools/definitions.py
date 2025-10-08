from mcp.server.fastmcp import FastMCP
from src.utils import get_logger, app_definition_client
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
    AppDefinitionResponse,
    PageBreakOperationResponse,
    FieldOperationResponse,
    UpsertSectionOperationResponse,
    ReorderSectionOperationResponse,
    UpdateAppMetadataRequest,
    BaseResponse

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


def register_definition_tools(mcp: FastMCP):

    @mcp.tool()
    def add_section(
        request: UpsertSectionRequest,
    ) -> UpsertSectionOperationResponse:
        """
        Adds a new section to a Clappia application at a specified position.

        Args:
            request (UpsertSectionRequest): The request object containing section details and the position
                                            where the section should be added.

        Returns:
            UpsertSectionOperationResponse: The response object indicating the result of the add section operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.add_section`.
        """
        return app_definition_client.add_section(request=request)

    @mcp.tool()
    def update_section(
        request: UpsertSectionRequest,
    ) -> UpsertSectionOperationResponse:
        """
        Updates an existing section in a Clappia application.

        Args:
            request (UpsertSectionRequest): The request object containing updated section details and the
                                            section identifier to be updated.

        Returns:
            UpsertSectionOperationResponse: The response object indicating the result of the update operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_section`.
        """
        return app_definition_client.update_section(request=request)

    @mcp.tool()
    def reorder_section(
        request: ReorderSectionRequest,
    ) -> ReorderSectionOperationResponse:
        """
        Reorders a section within a Clappia application.

        Args:
            request (ReorderSectionRequest): The request object containing the section identifier and the new
                                            position to reorder the section.

        Returns:
            ReorderSectionOperationResponse: The response object indicating the result of the reorder operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.reorder_section`.
        """
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
    ) -> FieldOperationResponse:
        """
        Adds a field to a Clappia app. The field type is determined by the request object type.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            section_index (int): The index of the section where the field will be added.
            field_index (int): The index position where the field will be placed.
            page_index (int): The index of the page where the field will be added.
            field_name (str): The name of the field.
            request (FieldRequestUnion): The request object containing field configuration. The field type is determined by the specific request type.
            version_variable_name (Optional[str]): The variable name representing the app version. If not specified, the live version is used.
        Returns:
            FieldOperationResponse: The response object containing the result of the field addition.

        Raises:
            Exception: Any error raised by the underlying field addition method.
        """
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
    ) -> FieldOperationResponse:
        """
        Updates a field in a Clappia app. The field type is determined by the request object type.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            field_name (str): The name of the field.
            request (FieldRequestUnion): The request object containing updated field configuration. The field type is determined by the specific request type.
            version_variable_name (Optional[str]): The variable name representing the app version. If not specified, the live version is used.
        Returns:
            FieldOperationResponse: The response object containing the result of the field update.

        Raises:
            Exception: Any error raised by the underlying field update method.
        """
        return app_definition_client.update_field(
            app_id=app_id,
            field_name=field_name,
            request=request,
            version_variable_name=version_variable_name,
        )
    

    @mcp.tool()
    def reorder_field(app_id: str, source_page_index: int, target_page_index: int, source_section_index: int, target_section_index: int, index_in_target_section: int, field_name: str, version_variable_name: Optional[str] = None) -> FieldOperationResponse:
        """
        Reorders a field in a Clappia app.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            source_page_index (int): The index of the page where the field is currently located.
            target_page_index (int): The index of the page where the field should be moved.
            source_section_index (int): The index of the section where the field is currently located.
            target_section_index (int): The index of the section where the field should be moved.
            index_in_target_section (int): The index of the field in the target section.
            field_name (str): The name of the field to reorder.
            version_variable_name (Optional[str]): The variable name representing the app version. If not specified, the live version is used.
        Returns:
            FieldOperationResponse: The response object containing the result of the field reordering.

        Raises:
                Exception: Any error raised by the underlying field reordering method.
        """
        return app_definition_client.reorder_field(app_id=app_id, source_page_index=source_page_index, target_page_index=target_page_index, source_section_index=source_section_index, target_section_index=target_section_index, index_in_target_section=index_in_target_section, field_name=field_name, version_variable_name=version_variable_name)

    @mcp.tool()
    def add_page_break(
        request: AddPageBreakRequest,
    ) -> PageBreakOperationResponse:
        """
        Adds a page break to a Clappia application at a specified position.

        Args:
            request (AddPageBreakRequest): The request object containing page break details and the position
                                        where it should be added.

        Returns:
            PageBreakOperationResponse: The response object indicating the result of the add page break operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.add_page_break`.
        """
        return app_definition_client.add_page_break(request=request)

    @mcp.tool()
    def update_page_break(
        request: UpdatePageBreakRequest,
    ) -> PageBreakOperationResponse:
        """
        Updates an existing page break in a Clappia application.

        Args:
            request (UpdatePageBreakRequest): The request object containing updated page break details
                                            and the identifier of the page break to update.

        Returns:
            PageBreakOperationResponse: The response object indicating the result of the update operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_page`.
        """
        return app_definition_client.update_page(request=request)

    @mcp.tool()
    def get_app_definition(app_id: str, version_variable_name: Optional[str] = None) -> AppDefinitionResponse:
        """
        Fetches the complete definition of a Clappia application, including forms, fields, sections, and metadata.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            version_variable_name (Optional[str]): The variable name representing the app version. If not specified, the live version is used.
        Returns:
            AppDefinitionResponse: The response object containing the full app definition.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.get_definition`.
        """
        return app_definition_client.get_definition(
            app_id=app_id,
            version_variable_name=version_variable_name,
        )

    @mcp.tool()
    def create_app(request: CreateAppRequest) -> BaseResponse:
        """
        Creates a new Clappia application with specified sections and fields.

        Args:
            request (CreateAppRequest): The request object containing app configuration details, sections, and fields.

        Returns:
            BaseResponse: The response object indicating the result of the app creation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.create_app`.
        """
        return app_definition_client.create_app(request=request)

    @mcp.tool()
    def update_app_metadata(app_id: str, request: UpdateAppMetadataRequest, version_variable_name: Optional[str] = None) -> AppDefinitionResponse:
        """
        Updates the metadata of a Clappia application.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            request (UpdateAppMetadataRequest): The request object containing updated metadata details.
            version_variable_name (Optional[str]): The variable name representing the app version. If not specified, the live version is used.
        Returns:
            AppMetadataUpdateResponse: The response object indicating the result of the metadata update.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_app_metadata`.
        """
        return app_definition_client.update_app_metadata(app_id=app_id, request=request, version_variable_name=version_variable_name)
    
    @mcp.tool()
    def get_app_versions(app_id: str) -> AppDefinitionResponse:
        """
        Gets the versions of a Clappia application.

        Args:
            app_id (str): The unique identifier of the Clappia application.

        Returns:
            AppDefinitionResponse: The response object containing the app versions.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.get_app_versions`.
        """
        return app_definition_client.get_app_versions(app_id=app_id)
    
    @mcp.tool()
    def update_app_version(app_id: str,initial_version_name: str, new_version_name: str) -> AppDefinitionResponse:
        """
        Updates a specific version of a Clappia application.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            initial_version_name (str): The name of the initial version, indentifier of the version to update.
            new_version_name (str): The name of the new version.

        Returns:
            AppDefinitionResponse: The response object containing the app versions.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_app_version`.
        """
        return app_definition_client.update_app_version(app_id=app_id, initial_version_name=initial_version_name, new_version_name=new_version_name)
    

    @mcp.tool()
    def update_live_version(app_id: str, version_variable_name: str) -> AppDefinitionResponse:
        """
        Updates the live version of a Clappia application.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            version_variable_name (str): The variable name representing the app version.

        Returns:
            AppDefinitionResponse: The response object containing the app versions.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_live_version`.
        """
        return app_definition_client.update_live_version(app_id=app_id, version_variable_name=version_variable_name)
    
    @mcp.tool()
    def create_app_version(app_id: str, version_name: str) -> AppDefinitionResponse:
        """
            Creates a new version of a Clappia application.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            version_name (str): The name of the new version.

        Returns:
            AppDefinitionResponse: The response object containing the app versions.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.create_app_version`.
        """
        return app_definition_client.create_new_app_version(app_id=app_id, version_name=version_name)