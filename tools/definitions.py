from typing import Union
from mcp.server.fastmcp import FastMCP
from utils import get_logger, app_definition_client
from clappia_api_tools.enums import FieldType
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
    AppCreationResponse,
    ReorderSectionOperationResponse,
)

# Union type for all field request types
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
    ) -> FieldOperationResponse:
        """
        Adds a field to a Clappia app. The field type is determined by the request object type.

        Args:
            app_id (str): The unique identifier for the target Clappia application.
            section_index (int): The zero-based index of the section where the new field will be inserted.
            field_index (int): The zero-based insertion index within that section.
            page_index (int): The zero-based index of the page where the new field will be inserted.
            field_name (str): The unique variable name for this field (e.g., `"text_field_1"`).
            request (FieldRequestUnion): The request object containing field configuration. The field type is determined by the specific request type.

        Returns:
            FieldOperationResponse: Feedback from Clappia indicating success or failure of the field addition.

        Raises:
            Exception: Any error raised by the underlying field addition method.
        """
        # Determine field type based on request type and call appropriate function
        if isinstance(request, UpsertFieldTextRequest):
            return add_text_field(app_id, section_index, field_index, page_index, field_name, request)
        elif isinstance(request, UpsertFieldTextAreaRequest):
            return add_textarea_field(app_id, section_index, field_index, page_index, field_name, request)
        elif isinstance(request, UpsertFieldDependencyAppRequest):
            return add_dependency_app_field(app_id, section_index, field_index, page_index, field_name, request)
        elif isinstance(request, UpsertFieldRestApiRequest):
            return add_rest_api_field(app_id, section_index, field_index, page_index, field_name, request)
        elif isinstance(request, UpsertFieldAddressRequest):
            return add_address_field(app_id, section_index, field_index, page_index, field_name, request)
        elif isinstance(request, UpsertFieldDatabaseRequest):
            return add_database_field(app_id, section_index, field_index, page_index, field_name, request)
        elif isinstance(request, UpsertFieldDateRequest):
            return add_date_field(app_id, section_index, field_index, page_index, field_name, request)
        elif isinstance(request, UpsertFieldAIRequest):
            return add_ai_field(app_id, section_index, field_index, page_index, field_name, request)
        elif isinstance(request, UpsertFieldCodeRequest):
            return add_code_field(app_id, section_index, field_index, page_index, field_name, request)
        elif isinstance(request, UpsertFieldCodeReaderRequest):
            return add_code_reader_field(app_id, section_index, field_index, page_index, field_name, request)
        elif isinstance(request, UpsertFieldEmailInputRequest):
            return add_email_input_field(app_id, section_index, field_index, field_name, page_index, request)
        elif isinstance(request, UpsertFieldEmojiRequest):
            return add_emoji_field(app_id, section_index, field_index, field_name, page_index, request)
        elif isinstance(request, UpsertFieldFileRequest):
            return add_file_field(app_id, section_index, field_index, field_name, page_index, request)
        elif isinstance(request, UpsertFieldGpsLocationRequest):
            return add_gps_location_field(app_id, section_index, field_index, field_name, page_index, request)
        elif isinstance(request, UpsertFieldLiveTrackingRequest):
            return add_live_tracking_field(app_id, section_index, field_index, field_name, page_index, request)
        elif isinstance(request, UpsertFieldManualAddressRequest):
            return add_manual_address_field(app_id, section_index, field_index, field_name, page_index, request)
        elif isinstance(request, UpsertFieldPhoneNumberRequest):
            return add_phone_number_field(app_id, section_index, field_index, field_name, page_index, request)
        elif isinstance(request, UpsertFieldProgressBarRequest):
            return add_progress_bar_field(app_id, section_index, field_index, field_name, page_index, request)
        elif isinstance(request, UpsertFieldSignatureRequest):
            return add_signature_field(app_id, section_index, field_index, field_name, page_index, request)
        elif isinstance(request, UpsertFieldCounterRequest):
            return add_counter_field(app_id, section_index, field_index, field_name, page_index, request)
        elif isinstance(request, UpsertFieldSliderRequest):
            return add_slider_field(app_id, section_index, field_index, field_name, page_index, request)
        elif isinstance(request, UpsertFieldTimeRequest):
            return add_time_field(app_id, section_index, field_index, field_name, page_index, request)
        elif isinstance(request, UpsertFieldToggleRequest):
            return add_toggle_field(app_id, section_index, field_index, field_name, page_index, request)
        elif isinstance(request, UpsertFieldValidationRequest):
            return add_validation_field(app_id, section_index, field_index, field_name, page_index, request)
        elif isinstance(request, UpsertFieldVideoViewerRequest):
            return add_video_viewer_field(app_id, section_index, field_index, field_name, page_index, request)
        elif isinstance(request, UpsertFieldVoiceRequest):
            return add_voice_field(app_id, section_index, field_index, field_name, page_index, request)
        elif isinstance(request, UpsertFieldFormulaRequest):
            return add_formula_field(app_id, section_index, field_index, field_name, page_index, request)
        elif isinstance(request, UpsertFieldImageViewerRequest):
            return add_image_field(app_id, section_index, field_index, field_name, page_index, request)
        elif isinstance(request, UpsertFieldRichTextEditorRequest):
            return add_rich_text_editor_field(app_id, section_index, field_index, field_name, page_index, request)
        elif isinstance(request, UpsertFieldNfcReaderRequest):
            return add_nfc_reader_field(app_id, section_index, field_index, field_name, page_index, request)
        elif isinstance(request, UpsertFieldNumberInputRequest):
            return add_number_field(app_id, section_index, field_index, field_name, page_index, request)
        elif isinstance(request, UpsertFieldPdfViewerRequest):
            return add_pdf_viewer_field(app_id, section_index, field_index, field_name, page_index, request)
        elif isinstance(request, UpsertFieldReadOnlyFileRequest):
            return add_read_only_file_field(app_id, section_index, field_index, field_name, page_index, request)
        elif isinstance(request, UpsertFieldReadOnlyTextRequest):
            return add_read_only_text_field(app_id, section_index, field_index, field_name, page_index, request)
        elif isinstance(request, UpsertFieldTagsRequest):
            return add_tag_field(app_id, section_index, field_index, field_name, page_index, request)
        elif isinstance(request, UpsertFieldUniqueSequentialRequest):
            return add_unique_sequential_field(app_id, section_index, field_index, field_name, page_index, request)
        elif isinstance(request, UpsertFieldDropdownRequest):
            return add_drop_down_field(app_id, section_index, field_index, field_name, page_index, request)
        elif isinstance(request, UpsertFieldRadioRequest):
            return add_radio_field(app_id, section_index, field_index, field_name, page_index, request)
        elif isinstance(request, UpsertFieldUrlInputRequest):
            return add_url_input_field(app_id, section_index, field_index, field_name, page_index, request)
        elif isinstance(request, UpsertFieldCheckboxRequest):
            return add_checkbox_field(app_id, section_index, field_index, field_name, page_index, request)
        elif isinstance(request, UpsertFieldRazorpayPaymentGatewayRequest):
            return add_razorpay_payment_gateway_field(app_id, section_index, field_index, field_name, page_index, request)
        elif isinstance(request, UpsertFieldEazypayPaymentGatewayRequest):
            return add_eazypay_payment_gateway_field(app_id, section_index, field_index, field_name, page_index, request)
        elif isinstance(request, UpsertFieldPaypalPaymentGatewayRequest):
            return add_paypal_payment_gateway_field(app_id, section_index, field_index, field_name, page_index, request)
        elif isinstance(request, UpsertFieldStripePaymentGatewayRequest):
            return add_stripe_payment_gateway_field(app_id, section_index, field_index, field_name, page_index, request)
        elif isinstance(request, UpsertFieldButtonRequest):
            return add_button_field(app_id, section_index, field_index, field_name, page_index, request)
        else:
            raise ValueError(f"Unsupported field request type: {type(request)}")

    @mcp.tool()
    def update_field(
        app_id: str,
        field_name: str,
        request: FieldRequestUnion,
    ) -> FieldOperationResponse:
        """
        Updates a field in a Clappia app. The field type is determined by the request object type.

        Args:
            app_id (str): The unique identifier for the target Clappia application.
            field_name (str): The unique variable name for this field (e.g., `"text_field_1"`).
            request (FieldRequestUnion): The request object containing field configuration. The field type is determined by the specific request type.

        Returns:
            FieldOperationResponse: Feedback from Clappia indicating success or failure of the field update.

        Raises:
            Exception: Any error raised by the underlying field update method.
        """
        # Determine field type based on request type and call appropriate function
        if isinstance(request, UpsertFieldTextRequest):
            return update_text_field(app_id, field_name, request)
        elif isinstance(request, UpsertFieldTextAreaRequest):
            return update_textarea_field(app_id, field_name, request)
        elif isinstance(request, UpsertFieldDependencyAppRequest):
            return update_dependency_app_field(app_id, field_name, request)
        elif isinstance(request, UpsertFieldRestApiRequest):
            return update_rest_api_field(app_id, field_name, request)
        elif isinstance(request, UpsertFieldAddressRequest):
            return update_address_field(app_id, field_name, request)
        elif isinstance(request, UpsertFieldDatabaseRequest):
            return update_database_field(app_id, field_name, request)
        elif isinstance(request, UpsertFieldDateRequest):
            return update_date_field(app_id, field_name, request)
        elif isinstance(request, UpsertFieldAIRequest):
            return update_ai_field(app_id, field_name, request)
        elif isinstance(request, UpsertFieldCodeRequest):
            return update_code_field(app_id, field_name, request)
        elif isinstance(request, UpsertFieldCodeReaderRequest):
            return update_code_reader_field(app_id, field_name, request)
        elif isinstance(request, UpsertFieldEmailInputRequest):
            return update_email_input_field(app_id, field_name, request)
        elif isinstance(request, UpsertFieldEmojiRequest):
            return update_emoji_field(app_id, field_name, request)
        elif isinstance(request, UpsertFieldFileRequest):
            return update_file_field(app_id, field_name, request)
        elif isinstance(request, UpsertFieldGpsLocationRequest):
            return update_gps_location_field(app_id, field_name, request)
        elif isinstance(request, UpsertFieldLiveTrackingRequest):
            return update_live_tracking_field(app_id, field_name, request)
        elif isinstance(request, UpsertFieldManualAddressRequest):
            return update_manual_address_field(app_id, field_name, request)
        elif isinstance(request, UpsertFieldPhoneNumberRequest):
            return update_phone_number_field(app_id, field_name, request)
        elif isinstance(request, UpsertFieldProgressBarRequest):
            return update_progress_bar_field(app_id, field_name, request)
        elif isinstance(request, UpsertFieldSignatureRequest):
            return update_signature_field(app_id, field_name, request)
        elif isinstance(request, UpsertFieldCounterRequest):
            return update_counter_field(app_id, field_name, request)
        elif isinstance(request, UpsertFieldSliderRequest):
            return update_slider_field(app_id, field_name, request)
        elif isinstance(request, UpsertFieldTimeRequest):
            return update_time_field(app_id, field_name, request)
        elif isinstance(request, UpsertFieldToggleRequest):
            return update_toggle_field(app_id, field_name, request)
        elif isinstance(request, UpsertFieldValidationRequest):
            return update_validation_field(app_id, field_name, request)
        elif isinstance(request, UpsertFieldVideoViewerRequest):
            return update_video_viewer_field(app_id, field_name, request)
        elif isinstance(request, UpsertFieldVoiceRequest):
            return update_voice_field(app_id, field_name, request)
        elif isinstance(request, UpsertFieldFormulaRequest):
            return update_formula_field(app_id, field_name, request)
        elif isinstance(request, UpsertFieldImageViewerRequest):
            return update_image_field(app_id, field_name, request)
        elif isinstance(request, UpsertFieldRichTextEditorRequest):
            return update_rich_text_editor_field(app_id, field_name, request)
        elif isinstance(request, UpsertFieldNfcReaderRequest):
            return update_nfc_reader_field(app_id, field_name, request)
        elif isinstance(request, UpsertFieldNumberInputRequest):
            return update_number_field(app_id, field_name, request)
        elif isinstance(request, UpsertFieldPdfViewerRequest):
            return update_pdf_viewer_field(app_id, field_name, request)
        elif isinstance(request, UpsertFieldReadOnlyFileRequest):
            return update_read_only_file_field(app_id, field_name, request)
        elif isinstance(request, UpsertFieldReadOnlyTextRequest):
            return update_read_only_text_field(app_id, field_name, request)
        elif isinstance(request, UpsertFieldTagsRequest):
            return update_tag_field(app_id, field_name, request)
        elif isinstance(request, UpsertFieldUniqueSequentialRequest):
            return update_unique_sequential_field(app_id, field_name, request)
        elif isinstance(request, UpsertFieldDropdownRequest):
            return update_drop_down_field(app_id, field_name, request)
        elif isinstance(request, UpsertFieldRadioRequest):
            return update_radio_field(app_id, field_name, request)
        elif isinstance(request, UpsertFieldUrlInputRequest):
            return update_url_input_field(app_id, field_name, request)
        elif isinstance(request, UpsertFieldCheckboxRequest):
            return update_checkbox_field(app_id, field_name, request)
        elif isinstance(request, UpsertFieldRazorpayPaymentGatewayRequest):
            return update_razorpay_payment_gateway_field(app_id, field_name, request)
        elif isinstance(request, UpsertFieldEazypayPaymentGatewayRequest):
            return update_eazypay_payment_gateway_field(app_id, field_name, request)
        elif isinstance(request, UpsertFieldPaypalPaymentGatewayRequest):
            return update_paypal_payment_gateway_field(app_id, field_name, request)
        elif isinstance(request, UpsertFieldStripePaymentGatewayRequest):
            return update_stripe_payment_gateway_field(app_id, field_name, request)
        elif isinstance(request, UpsertFieldButtonRequest):
            return update_button_field(app_id, field_name, request)
        else:
            raise ValueError(f"Unsupported field request type: {type(request)}")

    def add_text_field(
        app_id: str,
        section_index: int,
        field_index: int,
        page_index: int,
        field_name: str,
        request: UpsertFieldTextRequest,
    ) -> FieldOperationResponse:
        """
        Adds a Single Line Text field to a Clappia app, used for capturing short inputs like names, IDs, emails, or phone numbers.

        Args:
            app_id (str): The unique identifier for the target Clappia application.
            section_index (int): The zero-based index of the section where the new field will be inserted.
            field_index (int): The zero-based insertion index within that section.
            page_index (int): The zero-based index of the page where the new field will be inserted.
            field_name (str): The unique variable name for this field (e.g., `"text_field_1"`).
            request (UpsertFieldTextRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: Feedback from Clappia indicating success or failure of the field addition.

        Raises:
            Exception: Any error raised by `app_definition_client.add_text_field`.
        """
        return app_definition_client.add_text_field(
            app_id=app_id,
            section_index=section_index,
            field_index=field_index,
            page_index=page_index,
            field_name=field_name,
            request=request,
        )

    def update_text_field(
        app_id: str, field_name: str, request: UpsertFieldTextRequest
    ) -> FieldOperationResponse:
        """
        Updates a Single Line Text field in a Clappia app, typically used for modifying short inputs like names, IDs, emails, or phone numbers.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            field_name (str): The unique identifier of the field to be updated (e.g., `"text_field_1"`).
            request (UpsertFieldTextRequest): The request object containing updated field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the update operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_text_field`.
        """
        return app_definition_client.update_text_field(
            app_id=app_id, field_name=field_name, request=request
        )

    def add_textarea_field(
        app_id: str,
        section_index: int,
        field_index: int,
        page_index: int,
        field_name: str,
        request: UpsertFieldTextAreaRequest,
    ) -> FieldOperationResponse:
        """
        Adds a Multi Line Text (Textarea) field to a Clappia app, typically used for capturing longer inputs like comments, addresses, or detailed descriptions.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            section_index (int): The index of the section where the field should be added, should be greater than 0.
            field_index (int): The index position within the section to insert the field.
            field_name (str): The unique identifier of the field (e.g., `"textarea_field_1"`).
            page_index (int): The zero-based index of the page where the new field will be inserted.
            request (UpsertFieldTextAreaRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the add field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.add_textarea_field`.
        """
        return app_definition_client.add_textarea_field(
            app_id=app_id,
            section_index=section_index,
            field_index=field_index,
            page_index=page_index,
            field_name=field_name,
            request=request,
        )

    def update_textarea_field(
        app_id: str, field_name: str, request: UpsertFieldTextAreaRequest
    ) -> FieldOperationResponse:
        """
        Updates a Multi Line Text (Textarea) field in a Clappia app, typically used for modifying longer inputs like comments, addresses, or detailed descriptions.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            field_name (str): The unique identifier of the field to be updated (e.g., `"textarea_field_1"`).
            request (UpsertFieldTextAreaRequest): The request object containing updated field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the update field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_textarea_field`.
        """
        return app_definition_client.update_textarea_field(
            app_id=app_id, field_name=field_name, request=request
        )

    def add_dependency_app_field(
        app_id: str,
        section_index: int,
        field_index: int,
        page_index: int,
        field_name: str,
        request: UpsertFieldDependencyAppRequest,
    ) -> FieldOperationResponse:
        """
        Adds a Get Data from Other App field to a Clappia app, used for fetching data from a master app within the same Workplace.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            section_index (int): The index of the section where the field should be added (zero-based).
            field_index (int): The index position within the section to insert the field.
            page_index (int): The zero-based index of the page where the new field will be inserted.
            field_name (str): The unique variable name for the field (e.g., "dependency_app_field_1").
            request (UpsertFieldDependencyAppRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: Response object indicating success or failure of the add operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.add_dependency_app_field`.
        """
        return app_definition_client.add_dependency_app_field(
            app_id=app_id,
            section_index=section_index,
            field_index=field_index,
            page_index=page_index,
            field_name=field_name,
            request=request,
        )

    def update_dependency_app_field(
        app_id: str, field_name: str, request: UpsertFieldDependencyAppRequest
    ) -> FieldOperationResponse:
        """
        Updates a Get Data from Other App field in a Clappia app, used for modifying how data is fetched from a master app in the same Workplace.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            field_name (str): The unique variable name of the field to be updated (e.g., "dependency_app_field_1").
            request (UpsertFieldDependencyAppRequest): The request object containing updated field configuration.

        Returns:
            FieldOperationResponse: Response object indicating success or failure of the update operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_dependency_app_field`.
        """
        return app_definition_client.update_dependency_app_field(
            app_id=app_id, field_name=field_name, request=request
        )

    def add_rest_api_field(
        app_id: str,
        section_index: int,
        field_index: int,
        page_index: int,
        field_name: str,
        request: UpsertFieldRestApiRequest,
    ) -> FieldOperationResponse:
        """
        Adds a Get Data from REST APIs field to a Clappia app, used to pull data from any REST-based API (e.g., master data, exchange rates, weather).

        Args:
            app_id (str): The unique identifier of the Clappia application.
            section_index (int): The index of the section where the field should be added (zero-based).
            field_index (int): The position within the section to insert the field.
            page_index (int): The zero-based index of the page where the new field will be inserted.
            field_name (str): The unique variable name for the field (e.g., "rest_api_field_1").
            request (UpsertFieldRestApiRequest): The request object containing field configuration.

        Returns:
            FieldOperationResponse: Response indicating the result of the add operation.

        Raises:
            Exception: Propagates any exceptions from `app_definition_client.add_rest_api_field`.
        """
        return app_definition_client.add_rest_api_field(
            app_id=app_id,
            section_index=section_index,
            field_index=field_index,
            page_index=page_index,
            field_name=field_name,
            request=request,
        )

    def update_rest_api_field(
        app_id: str, field_name: str, request: UpsertFieldRestApiRequest
    ) -> FieldOperationResponse:
        """
        Updates a Get Data from REST APIs field in a Clappia app, used to modify how external API data (e.g., master data, live info) is retrieved.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            field_name (str): The unique variable name of the field to update (e.g., "rest_api_field_1").
            request (UpsertFieldRestApiRequest): The request object containing updated field configuration.

        Returns:
            FieldOperationResponse: Response indicating the result of the update operation.

        Raises:
            Exception: Propagates any exceptions from `app_definition_client.update_rest_api_field`.
        """
        return app_definition_client.update_rest_api_field(
            app_id=app_id, field_name=field_name, request=request
        )

    def add_address_field(
        app_id: str,
        section_index: int,
        field_index: int,
        page_index: int,
        field_name: str,
        request: UpsertFieldAddressRequest,
    ) -> FieldOperationResponse:
        """
        Adds a Geo-Address field to a Clappia app, used to capture detailed address information (e.g., location validation, GPS tagging).

        Args:
            app_id (str): The unique identifier of the Clappia application.
            section_index (int): The index of the section where the field should be added (zero-based).
            field_index (int): The position within the section to insert the field.
            page_index (int): The zero-based index of the page where the new field will be inserted.
            field_name (str): The unique variable name for the field (e.g., "address_field_1").
            request (UpsertFieldAddressRequest): The request object containing field configuration.

        Returns:
            FieldOperationResponse: Response indicating the result of the add operation.

        Raises:
            Exception: Propagates any exceptions from `app_definition_client.add_address_field`.
        """
        return app_definition_client.add_address_field(
            app_id=app_id,
            section_index=section_index,
            field_index=field_index,
            page_index=page_index,
            field_name=field_name,
            request=request,
        )

    def update_address_field(
        app_id: str, field_name: str, request: UpsertFieldAddressRequest
    ) -> FieldOperationResponse:
        """
        Updates a Geo-Address field in a Clappia application, typically used to modify how addresses and related GPS details
        (latitude, longitude, city, state, country, postal code) are captured or displayed.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            field_name (str): The unique variable name of the field to update (e.g., "address_field_1").
            request (UpsertFieldAddressRequest): The request object containing updated address field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the update operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_address_field`.
        """
        return app_definition_client.update_address_field(
            app_id=app_id, field_name=field_name, request=request
        )

    def add_database_field(
        app_id: str,
        section_index: int,
        field_index: int,
        page_index: int,
        field_name: str,
        request: UpsertFieldDatabaseRequest,
    ) -> FieldOperationResponse:
        """
        Adds a database field to a Clappia application at a specified section and field position.
        This field is used to fetch data from an external database, such as MySQL, PostgreSQL, or Azure SQL,
        enabling dynamic data integration into your app.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            section_index (int): The index of the section where the field should be added.
            field_index (int): The index position within the section to insert the field.
            page_index (int): The zero-based index of the page where the new field will be inserted.
            field_name (str): The unique identifier of the field.
            request (UpsertFieldDatabaseRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the add field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.add_database_field`.
        """
        return app_definition_client.add_database_field(
            app_id=app_id,
            section_index=section_index,
            field_index=field_index,
            page_index=page_index,
            field_name=field_name,
            request=request,
        )

    def update_database_field(
        app_id: str, field_name: str, request: UpsertFieldDatabaseRequest
    ) -> FieldOperationResponse:
        """
        Updates a database field in a Clappia application.
        This operation allows modifications to the configuration of a field that fetches data from an external database.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            field_name (str): The unique identifier of the field to be updated.
            request (UpsertFieldDatabaseRequest): The request object containing updated field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the update field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_database_field`.
        """
        return app_definition_client.update_database_field(
            app_id=app_id, field_name=field_name, request=request
        )

    def add_date_field(
        app_id: str,
        section_index: int,
        field_index: int,
        page_index: int,
        field_name: str,
        request: UpsertFieldDateRequest,
    ) -> FieldOperationResponse:
        """
        Adds a date field to a Clappia application at a specified section and field position.
        This field is used to capture date inputs from users, such as date of birth, event dates, or deadlines.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            section_index (int): The index of the section where the field should be added.
            field_index (int): The index position within the section to insert the field.
            page_index (int): The zero-based index of the page where the new field will be inserted.
            field_name (str): The unique identifier of the field.
            request (UpsertFieldDateRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the add field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.add_date_field`.
        """
        return app_definition_client.add_date_field(
            app_id=app_id,
            section_index=section_index,
            field_index=field_index,
            page_index=page_index,
            field_name=field_name,
            request=request,
        )

    def update_date_field(
        app_id: str, field_name: str, request: UpsertFieldDateRequest
    ) -> FieldOperationResponse:
        """
        Updates a date field in a Clappia application.
        This operation allows modifications to the configuration of a field that captures date inputs from users.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            field_name (str): The unique identifier of the field to be updated.
            request (UpsertFieldDateRequest): The request object containing updated field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the update field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_date_field`.
        """
        return app_definition_client.update_date_field(
            app_id=app_id, field_name=field_name, request=request
        )

    def add_ai_field(
        app_id: str,
        section_index: int,
        field_index: int,
        page_index: int,
        field_name: str,
        request: UpsertFieldAIRequest,
    ) -> FieldOperationResponse:
        """
        Adds an AI field to a Clappia application at a specified section and field position.
        Used to generate text based on the user's input using AI.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            section_index (int): The index of the section where the field should be added.
            field_index (int): The index position within the section to insert the field.
            page_index (int): The zero-based index of the page where the new field will be inserted.
            field_name (str): The unique identifier of the field.
            request (UpsertFieldAIRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the add field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.add_ai_field`.
        """
        return app_definition_client.add_ai_field(
            app_id=app_id,
            section_index=section_index,
            field_index=field_index,
            page_index=page_index,
            field_name=field_name,
            request=request,
        )

    def update_ai_field(
        app_id: str, field_name: str, request: UpsertFieldAIRequest
    ) -> FieldOperationResponse:
        """
        Updates an AI field in a Clappia application.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            field_name (str): The unique identifier of the field to be updated.
            request (UpsertFieldAIRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the update field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_ai_field`.
        """
        return app_definition_client.update_ai_field(
            app_id=app_id, field_name=field_name, request=request
        )

    def add_code_field(
        app_id: str,
        section_index: int,
        field_index: int,
        page_index: int,
        field_name: str,
        request: UpsertFieldCodeRequest,
    ) -> FieldOperationResponse:
        """
        Adds a code field to a Clappia application at a specified section and field position.
        Used to write custom JavaScript code, giving greater flexibility to handle advanced logic and calculations.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            section_index (int): The index of the section where the field should be added.
            field_index (int): The index position within the section to insert the field.
            page_index (int): The zero-based index of the page where the new field will be inserted.
            field_name (str): The unique identifier of the field.
            request (UpsertFieldCodeRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the add field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.add_code_field`.
        """
        return app_definition_client.add_code_field(
            app_id=app_id,
            section_index=section_index,
            field_index=field_index,
            page_index=page_index,
            field_name=field_name,
            request=request,
        )

    def update_code_field(
        app_id: str, field_name: str, request: UpsertFieldCodeRequest
    ) -> FieldOperationResponse:
        """
        Updates a code field in a Clappia application.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            field_name (str): The unique identifier of the field to be updated.
            request (UpsertFieldCodeRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the update field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_code_field`.
        """
        return app_definition_client.update_code_field(
            app_id=app_id, field_name=field_name, request=request
        )

    def add_code_reader_field(
        app_id: str,
        section_index: int,
        field_index: int,
        page_index: int,
        field_name: str,
        request: UpsertFieldCodeReaderRequest,
    ) -> FieldOperationResponse:
        """
        Adds a code reader field to a Clappia application at a specified section and field position.
        Used to read code from a barcode, QR code, or other sources.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            section_index (int): The index of the section where the field should be added.
            field_index (int): The index position within the section to insert the field.
            page_index (int): The zero-based index of the page where the new field will be inserted.
            field_name (str): The unique identifier of the field.
            request (UpsertFieldCodeReaderRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the add field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.add_code_reader_field`.
        """
        return app_definition_client.add_code_reader_field(
            app_id=app_id,
            section_index=section_index,
            field_index=field_index,
            page_index=page_index,
            field_name=field_name,
            request=request,
        )

    def update_code_reader_field(
        app_id: str, field_name: str, request: UpsertFieldCodeReaderRequest
    ) -> FieldOperationResponse:
        """
        Updates a code reader field in a Clappia application.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            field_name (str): The unique identifier of the field to be updated.
            request (UpsertFieldCodeReaderRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the update field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_code_reader_field`.
        """
        return app_definition_client.update_code_reader_field(
            app_id=app_id, field_name=field_name, request=request
        )

    def add_email_input_field(
        app_id: str,
        section_index: int,
        field_index: int,
        field_name: str,
        page_index: int,
        request: UpsertFieldEmailInputRequest,
    ) -> FieldOperationResponse:
        """
        Adds an email input field to a Clappia application at a specified section and field position. This field is used to capture email addresses from users with built-in validation.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            section_index (int): The index of the section where the field should be added, should be greater than 0.
            field_index (int): The index position within the section to insert the field.
            field_name (str): The unique identifier of the field. Example: email_field_1
            request (UpsertFieldEmailInputRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the add field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.add_email_input_field`.
        """
        return app_definition_client.add_email_input_field(
            app_id=app_id,
            section_index=section_index,
            field_index=field_index,
            page_index=page_index,
            field_name=field_name,
            request=request,
        )

    def update_email_input_field(
        app_id: str, field_name: str, request: UpsertFieldEmailInputRequest
    ) -> FieldOperationResponse:
        """
        Updates an email input field in a Clappia application.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            field_name (str): The unique identifier of the field which needs to be updated. Example: email_field_1
            request (UpsertFieldEmailInputRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the update field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_email_input_field`.
        """
        return app_definition_client.update_email_input_field(
            app_id=app_id, field_name=field_name, request=request
        )

    def add_emoji_field(
        app_id: str,
        section_index: int,
        field_index: int,
        field_name: str,
        page_index: int,
        request: UpsertFieldEmojiRequest,
    ) -> FieldOperationResponse:
        """
        Adds an emoji field to a Clappia application at a specified section and field position. This field allows users to select emojis as a form of feedback or rating.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            section_index (int): The index of the section where the field should be added, should be greater than 0.
            field_index (int): The index position within the section to insert the field.
            field_name (str): The unique identifier of the field. Example: emoji_field_1
            page_index (int): The zero-based index of the page where the new field will be inserted.
            request (UpsertFieldEmojiRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the add field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.add_emoji_field`.
        """
        return app_definition_client.add_emoji_field(
            app_id=app_id,
            section_index=section_index,
            field_index=field_index,
            page_index=page_index,
            field_name=field_name,
            request=request,
        )

    def update_emoji_field(
        app_id: str, field_name: str, request: UpsertFieldEmojiRequest
    ) -> FieldOperationResponse:
        """
        Updates an emoji field in a Clappia application.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            field_name (str): The unique identifier of the field which needs to be updated. Example: emoji_field_1
            request (UpsertFieldEmojiRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the update field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_emoji_field`.
        """
        return app_definition_client.update_emoji_field(
            app_id=app_id, field_name=field_name, request=request
        )

    def add_file_field(
        app_id: str,
        section_index: int,
        field_index: int,
        field_name: str,
        page_index: int,
        request: UpsertFieldFileRequest,
    ) -> FieldOperationResponse:
        """
        Adds a file upload field to a Clappia application at a specified section and field position. This field allows users to upload files as part of their submissions.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            section_index (int): The index of the section where the field should be added; should be greater than 0.
            field_index (int): The index position within the section to insert the field.
            field_name (str): The unique identifier of the field. Example: 'file_upload_1'.
            page_index (int): The zero-based index of the page where the new field will be inserted.
            request (UpsertFieldFileRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the add field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.add_file_field`.
        """
        return app_definition_client.add_file_field(
            app_id=app_id,
            section_index=section_index,
            field_index=field_index,
            page_index=page_index,
            field_name=field_name,
            request=request,
        )

    def update_file_field(
        app_id: str, field_name: str, request: UpsertFieldFileRequest
    ) -> FieldOperationResponse:
        """
        Updates a file field in a Clappia application.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            field_name (str): The unique identifier of the field which need to be updated. Example: text_field_1
            request (UpsertFieldFileRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the update field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_file_field`.
        """
        return app_definition_client.update_file_field(
            app_id=app_id, field_name=field_name, request=request
        )

    def add_gps_location_field(
        app_id: str,
        section_index: int,
        field_index: int,
        field_name: str,
        page_index: int,
        request: UpsertFieldGpsLocationRequest,
    ) -> FieldOperationResponse:
        """
        Adds a GPS location field to a Clappia application at a specified section and field position. This field captures and displays the user's coordinates (latitude and longitude), with optional features like map view and address fetching.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            section_index (int): The index of the section where the field should be added; should be greater than 0.
            field_index (int): The index position within the section to insert the field.
            field_name (str): The unique identifier of the field. Example: 'location_field_1'.
            page_index (int): The zero-based index of the page where the new field will be inserted.
            request (UpsertFieldGpsLocationRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the add field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.add_gps_location_field`.
        """
        return app_definition_client.add_gps_location_field(
            app_id=app_id,
            section_index=section_index,
            field_index=field_index,
            page_index=page_index,
            field_name=field_name,
            request=request,
        )

    def update_gps_location_field(
        app_id: str, field_name: str, request: UpsertFieldGpsLocationRequest
    ) -> FieldOperationResponse:
        """
        Updates a GPS location field in a Clappia application. This operation allows modification of the field's configuration, such as enabling map view or address fetching.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            field_name (str): The unique identifier of the field to be updated. Example: 'location_field_1'.
            request (UpsertFieldGpsLocationRequest): The request object containing updated field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the update field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_gps_location_field`.
        """
        return app_definition_client.update_gps_location_field(
            app_id=app_id, field_name=field_name, request=request
        )

    def add_live_tracking_field(
        app_id: str,
        section_index: int,
        field_index: int,
        field_name: str,
        page_index: int,
        request: UpsertFieldLiveTrackingRequest,
    ) -> FieldOperationResponse:
        """
        Adds a live tracking field to a Clappia application at a specified section and field position. This field captures the exact route taken by a user in real-time, from the starting point to the endpoint, along with the total distance traveled.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            section_index (int): The index of the section where the field should be added; should be greater than 0.
            field_index (int): The index position within the section to insert the field.
            field_name (str): The unique identifier of the field. Example: 'live_tracking_1'.
            page_index (int): The zero-based index of the page where the new field will be inserted.
            request (UpsertFieldLiveTrackingRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the add field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.add_live_tracking_field`.
        """
        return app_definition_client.add_live_tracking_field(
            app_id=app_id,
            section_index=section_index,
            field_index=field_index,
            page_index=page_index,
            field_name=field_name,
            request=request,
        )

    def update_live_tracking_field(
        app_id: str, field_name: str, request: UpsertFieldLiveTrackingRequest
    ) -> FieldOperationResponse:
        """
        Updates a live tracking field in a Clappia application. This operation allows modification of the field's configuration, such as setting the duration for automatic tracking stop or updating the description.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            field_name (str): The unique identifier of the field to be updated. Example: 'live_tracking_1'.
            request (UpsertFieldLiveTrackingRequest): The request object containing updated field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the update field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_live_tracking_field`.
        """
        return app_definition_client.update_live_tracking_field(
            app_id=app_id, field_name=field_name, request=request
        )

    def add_manual_address_field(
        app_id: str,
        section_index: int,
        field_index: int,
        field_name: str,
        page_index: int,
        request: UpsertFieldManualAddressRequest,
    ) -> FieldOperationResponse:
        """
        Adds a manual address field to a Clappia application at a specified section and field position. Its used to take address input from the user.
        This field is used to manually enter the address details. It doesn't fetch the address details from the map.


        Args:
            app_id (str): The unique identifier of the Clappia application.
            section_index (int): The index of the section where the field should be added, should be greater than 0.
            field_index (int): The index position within the section to insert the field.
            field_name (str): The unique identifier of the field. Example: text_field_1
            page_index (int): The zero-based index of the page where the new field will be inserted.
            request (UpsertFieldManualAddressRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the add field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.add_manual_address_field`.
        """
        return app_definition_client.add_manual_address_field(
            app_id=app_id,
            section_index=section_index,
            field_index=field_index,
            field_name=field_name,
            page_index=page_index,
            request=request,
        )

    def update_manual_address_field(
        app_id: str, field_name: str, request: UpsertFieldManualAddressRequest
    ) -> FieldOperationResponse:
        """
        Updates a manual address field in a Clappia application.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            field_name (str): The unique identifier of the field which need to be updated. Example: text_field_1
            request (UpsertFieldManualAddressRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the update field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_manual_address_field`.
        """
        return app_definition_client.update_manual_address_field(
            app_id=app_id, field_name=field_name, request=request
        )

    def add_phone_number_field(
        app_id: str,
        section_index: int,
        field_index: int,
        field_name: str,
        page_index: int,
        request: UpsertFieldPhoneNumberRequest,
    ) -> FieldOperationResponse:
        """
        Adds a phone number field to a Clappia application at a specified section and field position. Its used to take phone number input from the user.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            section_index (int): The index of the section where the field should be added, should be greater than 0.
            field_index (int): The index position within the section to insert the field.
            field_name (str): The unique identifier of the field. Example: text_field_1
            page_index (int): The zero-based index of the page where the new field will be inserted.
            request (UpsertFieldPhoneNumberRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the add field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.add_phone_number_field`.
        """
        return app_definition_client.add_phone_number_field(
            app_id=app_id,
            section_index=section_index,
            field_index=field_index,
            page_index=page_index,
            field_name=field_name,
            request=request,
        )

    def update_phone_number_field(
        app_id: str, field_name: str, request: UpsertFieldPhoneNumberRequest
    ) -> FieldOperationResponse:
        """
        Updates a phone number field in a Clappia application.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            field_name (str): The unique identifier of the field which need to be updated. Example: text_field_1
            request (UpsertFieldPhoneNumberRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the update field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_phone_number_field`.
        """
        return app_definition_client.update_phone_number_field(
            app_id=app_id, field_name=field_name, request=request
        )

    def add_progress_bar_field(
        app_id: str,
        section_index: int,
        field_index: int,
        field_name: str,
        page_index: int,
        request: UpsertFieldProgressBarRequest,
    ) -> FieldOperationResponse:
        """
        Adds a progress bar field to a Clappia application at a specified section and field position. Its used to show the progress of the user.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            section_index (int): The index of the section where the field should be added, should be greater than 0.
            field_index (int): The index position within the section to insert the field.
            field_name (str): The unique identifier of the field. Example: text_field_1
            page_index (int): The zero-based index of the page where the new field will be inserted.
            request (UpsertFieldProgressBarRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the add field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.add_progress_bar_field`.
        """
        return app_definition_client.add_progress_bar_field(
            app_id=app_id,
            section_index=section_index,
            field_index=field_index,
            page_index=page_index,
            field_name=field_name,
            request=request,
        )

    def update_progress_bar_field(
        app_id: str, field_name: str, request: UpsertFieldProgressBarRequest
    ) -> FieldOperationResponse:
        """
        Updates a progress bar field in a Clappia application.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            field_name (str): The unique identifier of the field which need to be updated. Example: text_field_1
            request (UpsertFieldProgressBarRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the update field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_progress_bar_field`.
        """
        return app_definition_client.update_progress_bar_field(
            app_id=app_id, field_name=field_name, request=request
        )

    def add_signature_field(
        app_id: str,
        section_index: int,
        field_index: int,
        field_name: str,
        page_index: int,
        request: UpsertFieldSignatureRequest,
    ) -> FieldOperationResponse:
        """
        Adds a signature field to a Clappia application at a specified section and field position. Its used to take signature input from the user.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            section_index (int): The index of the section where the field should be added, should be greater than 0.
            field_index (int): The index position within the section to insert the field.
            field_name (str): The unique identifier of the field. Example: text_field_1
            page_index (int): The zero-based index of the page where the new field will be inserted.
            request (UpsertFieldSignatureRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the add field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.add_signature_field`.
        """
        return app_definition_client.add_signature_field(
            app_id=app_id,
            section_index=section_index,
            field_index=field_index,
            page_index=page_index,
            field_name=field_name,
            request=request,
        )

    def update_signature_field(
        app_id: str, field_name: str, request: UpsertFieldSignatureRequest
    ) -> FieldOperationResponse:
        """
        Updates a signature field in a Clappia application.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            field_name (str): The unique identifier of the field which need to be updated. Example: text_field_1
            request (UpsertFieldSignatureRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the update field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_signature_field`.
        """
        return app_definition_client.update_signature_field(
            app_id=app_id, field_name=field_name, request=request
        )

    def add_counter_field(
        app_id: str,
        section_index: int,
        field_index: int,
        field_name: str,
        page_index: int,
        request: UpsertFieldCounterRequest,
    ) -> FieldOperationResponse:
        """
        Adds a counter field to a Clappia application at a specified section and field position. Its used to take the input in the form of a counter.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            section_index (int): The index of the section where the field should be added, should be greater than 0.
            field_index (int): The index position within the section to insert the field.
            field_name (str): The unique identifier of the field. Example: text_field_1
            page_index (int): The zero-based index of the page where the new field will be inserted.
            request (UpsertFieldCounterRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the add field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.add_counter_field`.
        """
        return app_definition_client.add_counter_field(
            app_id=app_id,
            section_index=section_index,
            field_index=field_index,
            page_index=page_index,
            field_name=field_name,
            request=request,
        )

    def update_counter_field(
        app_id: str, field_name: str, request: UpsertFieldCounterRequest
    ) -> FieldOperationResponse:
        """
        Updates a counter field in a Clappia application.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            field_name (str): The unique identifier of the field which need to be updated. Example: text_field_1
            request (UpsertFieldCounterRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the update field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_counter_field`.
        """
        return app_definition_client.update_counter_field(
            app_id=app_id, field_name=field_name, request=request
        )

    def add_slider_field(
        app_id: str,
        section_index: int,
        field_index: int,
        field_name: str,
        page_index: int,
        request: UpsertFieldSliderRequest,
    ) -> FieldOperationResponse:
        """
        Adds a slider field to a Clappia application at a specified section and field position. Its used to take the input in the form of a slider.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            section_index (int): The index of the section where the field should be added, should be greater than 0.
            field_index (int): The index position within the section to insert the field.
            field_name (str): The unique identifier of the field. Example: text_field_1
            page_index (int): The zero-based index of the page where the new field will be inserted.
            request (UpsertFieldSliderRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the add field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.add_slider_field`.
        """
        return app_definition_client.add_slider_field(
            app_id=app_id,
            section_index=section_index,
            field_index=field_index,
            page_index=page_index,
            field_name=field_name,
            request=request,
        )

    def update_slider_field(
        app_id: str, field_name: str, request: UpsertFieldSliderRequest
    ) -> FieldOperationResponse:
        """
        Updates a slider field in a Clappia application.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            field_name (str): The unique identifier of the field which need to be updated. Example: text_field_1
            request (UpsertFieldSliderRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the update field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_slider_field`.
        """
        return app_definition_client.update_slider_field(
            app_id=app_id, field_name=field_name, request=request
        )

    def add_time_field(
        app_id: str,
        section_index: int,
        field_index: int,
        field_name: str,
        page_index: int,
        request: UpsertFieldTimeRequest,
    ) -> FieldOperationResponse:
        """
        Adds a time field to a Clappia application at a specified section and field position. Its used to take the input in the form of a time.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            section_index (int): The index of the section where the field should be added, should be greater than 0.
            field_index (int): The index position within the section to insert the field.
            field_name (str): The unique identifier of the field. Example: text_field_1
            page_index (int): The zero-based index of the page where the new field will be inserted.
            request (UpsertFieldTimeRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the add field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.add_time_field`.
        """
        return app_definition_client.add_time_field(
            app_id=app_id,
            section_index=section_index,
            field_index=field_index,
            page_index=page_index,
            field_name=field_name,
            request=request,
        )

    def update_time_field(
        app_id: str, field_name: str, request: UpsertFieldTimeRequest
    ) -> FieldOperationResponse:
        """
        Updates a time field in a Clappia application.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            field_name (str): The unique identifier of the field which need to be updated. Example: text_field_1
            request (UpsertFieldTimeRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the update field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_time_field`.
        """
        return app_definition_client.update_time_field(
            app_id=app_id, field_name=field_name, request=request
        )

    def add_toggle_field(
        app_id: str,
        section_index: int,
        field_index: int,
        field_name: str,
        page_index: int,
        request: UpsertFieldToggleRequest,
    ) -> FieldOperationResponse:
        """
        Adds a toggle field to a Clappia application at a specified section and field position. Its used to take the input boolean value    .

        Args:
            app_id (str): The unique identifier of the Clappia application.
            section_index (int): The index of the section where the field should be added, should be greater than 0.
            field_index (int): The index position within the section to insert the field.
            field_name (str): The unique identifier of the field. Example: text_field_1
            page_index (int): The zero-based index of the page where the new field will be inserted.
            request (UpsertFieldToggleRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the add field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.add_toggle_field`.
        """
        return app_definition_client.add_toggle_field(
            app_id=app_id,
            section_index=section_index,
            field_index=field_index,
            page_index=page_index,
            field_name=field_name,
            request=request,
        )

    def update_toggle_field(
        app_id: str, field_name: str, request: UpsertFieldToggleRequest
    ) -> FieldOperationResponse:
        """
        Updates a toggle field in a Clappia application.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            field_name (str): The unique identifier of the field which need to be updated. Example: text_field_1
            request (UpsertFieldToggleRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the update field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_toggle_field`.
        """
        return app_definition_client.update_toggle_field(
            app_id=app_id, field_name=field_name, request=request
        )

    def add_validation_field(
        app_id: str,
        section_index: int,
        field_index: int,
        field_name: str,
        page_index: int,
        request: UpsertFieldValidationRequest,
    ) -> FieldOperationResponse:
        """
        Adds a validation field to a Clappia application at a specified section and field position. Its used to prevent or warn the end user from entering Invalid or Duplicate Inputs.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            section_index (int): The index of the section where the field should be added, should be greater than 0.
            field_index (int): The index position within the section to insert the field.
            field_name (str): The unique identifier of the field. Example: text_field_1
            page_index (int): The zero-based index of the page where the new field will be inserted.
            request (UpsertFieldValidationRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the add field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.add_validation_field`.
        """
        return app_definition_client.add_validation_field(
            app_id=app_id,
            section_index=section_index,
            field_index=field_index,
            page_index=page_index,
            field_name=field_name,
            request=request,
        )

    def update_validation_field(
        app_id: str, field_name: str, request: UpsertFieldValidationRequest
    ) -> FieldOperationResponse:
        """
        Updates a validation field in a Clappia application.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            field_name (str): The unique identifier of the field which need to be updated. Example: text_field_1
            request (UpsertFieldValidationRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the update field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_validation_field`.
        """
        return app_definition_client.update_validation_field(
            app_id=app_id, field_name=field_name, request=request
        )

    def add_video_viewer_field(
        app_id: str,
        section_index: int,
        field_index: int,
        field_name: str,
        page_index: int,
        request: UpsertFieldVideoViewerRequest,
    ) -> FieldOperationResponse:
        """
        Adds a video viewer field to a Clappia application at a specified section and field position. Its used to show the video to the end user.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            section_index (int): The index of the section where the field should be added, should be greater than 0.
            field_index (int): The index position within the section to insert the field.
            field_name (str): The unique identifier of the field. Example: text_field_1
            page_index (int): The zero-based index of the page where the new field will be inserted.
            request (UpsertFieldVideoViewerRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the add field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.add_video_viewer_field`.
        """
        return app_definition_client.add_video_viewer_field(
            app_id=app_id,
            section_index=section_index,
            field_index=field_index,
            page_index=page_index,
            field_name=field_name,
            request=request,
        )

    def update_video_viewer_field(
        app_id: str, field_name: str, request: UpsertFieldVideoViewerRequest
    ) -> FieldOperationResponse:
        """
        Updates a video viewer field in a Clappia application.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            field_name (str): The unique identifier of the field which need to be updated. Example: text_field_1
            request (UpsertFieldVideoViewerRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the update field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_video_viewer_field`.
        """
        return app_definition_client.update_video_viewer_field(
            app_id=app_id, field_name=field_name, request=request
        )

    def add_voice_field(
        app_id: str,
        section_index: int,
        field_index: int,
        field_name: str,
        page_index: int,
        request: UpsertFieldVoiceRequest,
    ) -> FieldOperationResponse:
        """
        Adds a voice field to a Clappia application at a specified section and field position. Its used to take the audio input from the user.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            section_index (int): The index of the section where the field should be added, should be greater than 0.
            field_index (int): The index position within the section to insert the field.
            field_name (str): The unique identifier of the field. Example: text_field_1
            page_index (int): The zero-based index of the page where the new field will be inserted.
            request (UpsertFieldVoiceRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the add field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.add_voice_field`.
        """
        return app_definition_client.add_voice_field(
            app_id=app_id,
            section_index=section_index,
            field_index=field_index,
            page_index=page_index,
            field_name=field_name,
            request=request,
        )

    def update_voice_field(
        app_id: str, field_name: str, request: UpsertFieldVoiceRequest
    ) -> FieldOperationResponse:
        """
        Updates a voice field in a Clappia application.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            field_name (str): The unique identifier of the field which need to be updated. Example: text_field_1
            request (UpsertFieldVoiceRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the update field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_voice_field`.
        """
        return app_definition_client.update_voice_field(
            app_id=app_id, field_name=field_name, request=request
        )

    def add_formula_field(
        app_id: str,
        section_index: int,
        field_index: int,
        field_name: str,
        page_index: int,
        request: UpsertFieldFormulaRequest,
    ) -> FieldOperationResponse:
        """
        Adds a formula field to a Clappia application at a specified section and field position. Clappia supports multiple arithmetic operations (SUM, DIFF, PRODUCT, LOG...), logical operations (IF/ELSE, AND, OR, XOR, ...), string operations (CONCATENATE, LEN, TRIM, ...) and DATE/TIME operations (TODAY, NOW, DATEDIF, FORMAT) that are supported by Microsoft Excel.

        This block is used to calculate the value of a field based on the formula provided.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            section_index (int): The index of the section where the field should be added, should be greater than 0.
            field_index (int): The index position within the section to insert the field.
            field_name (str): The unique identifier of the field. Example: text_field_1
            page_index (int): The zero-based index of the page where the new field will be inserted.
            request (UpsertFieldFormulaRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the add field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.add_formula_field`.
        """
        return app_definition_client.add_formula_field(
            app_id=app_id,
            section_index=section_index,
            field_index=field_index,
            page_index=page_index,
            field_name=field_name,
            request=request,
        )

    def update_formula_field(
        app_id: str, field_name: str, request: UpsertFieldFormulaRequest
    ) -> FieldOperationResponse:
        """
        Updates a formula field in a Clappia application.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            field_name (str): The unique identifier of the field which need to be updated. Example: text_field_1
            request (UpsertFieldFormulaRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the update field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_formula_field`.
        """
        return app_definition_client.update_formula_field(
            app_id=app_id, field_name=field_name, request=request
        )

    def add_image_field(
        app_id: str,
        section_index: int,
        field_index: int,
        field_name: str,
        page_index: int,
        request: UpsertFieldImageViewerRequest,
    ) -> FieldOperationResponse:
        """
        Adds an image field to a Clappia application at a specified section and field position. Its used to show the image to the end user.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            section_index (int): The index of the section where the field should be added, should be greater than 0.
            field_index (int): The index position within the section to insert the field.
            field_name (str): The unique identifier of the field. Example: text_field_1
            page_index (int): The zero-based index of the page where the new field will be inserted.
            request (UpsertFieldImageViewerRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the add field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.add_image_field`.
        """
        return app_definition_client.add_image_field(
            app_id=app_id,
            section_index=section_index,
            field_index=field_index,
            page_index=page_index,
            field_name=field_name,
            request=request,
        )

    def update_image_field(
        app_id: str, field_name: str, request: UpsertFieldImageViewerRequest
    ) -> FieldOperationResponse:
        """
        Updates an image field in a Clappia application.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            field_name (str): The unique identifier of the field which need to be updated. Example: text_field_1
            request (UpsertFieldImageViewerRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the update field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_image_field`.
        """
        return app_definition_client.update_image_field(
            app_id=app_id, field_name=field_name, request=request
        )

    def add_rich_text_editor_field(
        app_id: str,
        section_index: int,
        field_index: int,
        field_name: str,
        page_index: int,
        request: UpsertFieldRichTextEditorRequest,
    ) -> FieldOperationResponse:
        """
        Adds a rich text editor field to a Clappia application at a specified section and field position. Its used to take the input in the form of HTML, add formatted text with styles such as bold, italics, and underlines, add lists, and more.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            section_index (int): The index of the section where the field should be added, should be greater than 0.
            field_index (int): The index position within the section to insert the field.
            field_name (str): The unique identifier of the field. Example: text_field_1
            page_index (int): The zero-based index of the page where the new field will be inserted.
            request (UpsertFieldRichTextEditorRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the add field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.add_rich_text_editor_field`.
        """
        return app_definition_client.add_rich_text_editor_field(
            app_id=app_id,
            section_index=section_index,
            field_index=field_index,
            page_index=page_index,
            field_name=field_name,
            request=request,
        )

    def update_rich_text_editor_field(
        app_id: str, field_name: str, request: UpsertFieldRichTextEditorRequest
    ) -> FieldOperationResponse:
        """
        Updates a rich text editor field in a Clappia application.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            field_name (str): The unique identifier of the field which need to be updated. Example: text_field_1
            request (UpsertFieldRichTextEditorRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the update field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_rich_text_editor_field`.
        """
        return app_definition_client.update_rich_text_editor_field(
            app_id=app_id, field_name=field_name, request=request
        )

    def add_nfc_reader_field(
        app_id: str,
        section_index: int,
        field_index: int,
        field_name: str,
        page_index: int,
        request: UpsertFieldNfcReaderRequest,
    ) -> FieldOperationResponse:
        """
        Adds an NFC reader field to a Clappia application at a specified section and field position. Its used to read the NFC tag from the user.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            section_index (int): The index of the section where the field should be added, should be greater than 0.
            field_index (int): The index position within the section to insert the field.
            field_name (str): The unique identifier of the field. Example: text_field_1
            page_index (int): The zero-based index of the page where the new field will be inserted.
            request (UpsertFieldNfcReaderRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the add field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.add_nfc_reader_field`.
        """
        return app_definition_client.add_nfc_reader_field(
            app_id=app_id,
            section_index=section_index,
            field_index=field_index,
            page_index=page_index,
            field_name=field_name,
            request=request,
        )

    def update_nfc_reader_field(
        app_id: str, field_name: str, request: UpsertFieldNfcReaderRequest
    ) -> FieldOperationResponse:
        """
        Updates an NFC reader field in a Clappia application.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            field_name (str): The unique identifier of the field which need to be updated. Example: text_field_1
            request (UpsertFieldNfcReaderRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the update field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_nfc_reader_field`.
        """
        return app_definition_client.update_nfc_reader_field(
            app_id=app_id, field_name=field_name, request=request
        )

    def add_number_field(
        app_id: str,
        section_index: int,
        field_index: int,
        field_name: str,
        page_index: int,
        request: UpsertFieldNumberInputRequest,
    ) -> FieldOperationResponse:
        """
        Adds a number field to a Clappia application at a specified section and field position. Its used to take the number input from the user.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            section_index (int): The index of the section where the field should be added, should be greater than 0.
            field_index (int): The index position within the section to insert the field.
            field_name (str): The unique identifier of the field. Example: text_field_1
            page_index (int): The zero-based index of the page where the new field will be inserted.
            request (UpsertFieldNumberRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the add field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.add_number_field`.
        """
        return app_definition_client.add_number_field(
            app_id=app_id,
            section_index=section_index,
            field_index=field_index,
            page_index=page_index,
            field_name=field_name,
            request=request,
        )

    def update_number_field(
        app_id: str, field_name: str, request: UpsertFieldNumberInputRequest
    ) -> FieldOperationResponse:
        """
        Updates a number field in a Clappia application.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            field_name (str): The unique identifier of the field which need to be updated. Example: text_field_1
            request (UpsertFieldNumberRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the update field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_number_field`.
        """
        return app_definition_client.update_number_field(
            app_id=app_id, field_name=field_name, request=request
        )

    def add_pdf_viewer_field(
        app_id: str,
        section_index: int,
        field_index: int,
        field_name: str,
        page_index: int,
        request: UpsertFieldPdfViewerRequest,
    ) -> FieldOperationResponse:
        """
        Adds a PDF viewer field to a Clappia application at a specified section and field position. Its used to show the PDF to the end user.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            section_index (int): The index of the section where the field should be added, should be greater than 0.
            field_index (int): The index position within the section to insert the field.
            field_name (str): The unique identifier of the field. Example: text_field_1
            page_index (int): The zero-based index of the page where the new field will be inserted.
            request (UpsertFieldPdfViewerRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the add field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.add_pdf_viewer_field`.
        """
        return app_definition_client.add_pdf_viewer_field(
            app_id=app_id,
            section_index=section_index,
            field_index=field_index,
            page_index=page_index,
            field_name=field_name,
            request=request,
        )

    def update_pdf_viewer_field(
        app_id: str, field_name: str, request: UpsertFieldPdfViewerRequest
    ) -> FieldOperationResponse:
        """
        Updates a PDF viewer field in a Clappia application.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            field_name (str): The unique identifier of the field which need to be updated. Example: text_field_1
            request (UpsertFieldPdfViewerRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the update field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_pdf_viewer_field`.
        """
        return app_definition_client.update_pdf_viewer_field(
            app_id=app_id, field_name=field_name, request=request
        )

    def add_read_only_file_field(
        app_id: str,
        section_index: int,
        field_index: int,
        field_name: str,
        page_index: int,
        request: UpsertFieldReadOnlyFileRequest,
    ) -> FieldOperationResponse:
        """
        Adds a read only file field to a Clappia application at a specified section and field position. It is used to attach any reference documents, Ex. Policy Documents, Agreements, etc.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            section_index (int): The index of the section where the field should be added, should be greater than 0.
            field_index (int): The index position within the section to insert the field.
            field_name (str): The unique identifier of the field. Example: text_field_1
            page_index (int): The zero-based index of the page where the new field will be inserted.
            request (UpsertFieldReadOnlyFileRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the add field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.add_read_only_file_field`.
        """
        return app_definition_client.add_read_only_field(
            app_id=app_id,
            section_index=section_index,
            field_index=field_index,
            page_index=page_index,
            field_name=field_name,
            request=request,
        )

    def update_read_only_file_field(
        app_id: str, field_name: str, request: UpsertFieldReadOnlyFileRequest
    ) -> FieldOperationResponse:
        """
        Updates a read only file field in a Clappia application.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            field_name (str): The unique identifier of the field which need to be updated. Example: text_field_1
            request (UpsertFieldReadOnlyFileRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the update field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_read_only_file_field`.
        """
        return app_definition_client.update_read_only_field(
            app_id=app_id, field_name=field_name, request=request
        )

    def add_read_only_text_field(
        app_id: str,
        section_index: int,
        field_index: int,
        field_name: str,
        page_index: int,
        request: UpsertFieldReadOnlyTextRequest,
    ) -> FieldOperationResponse:
        """
        Adds a read only text field to a Clappia application at a specified section and field position. Its used to add read-only instruction, help text, formatted text, images, videos etc. to an app, any videos or external images or embed any other clappia app.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            section_index (int): The index of the section where the field should be added, should be greater than 0.
            field_index (int): The index position within the section to insert the field.
            field_name (str): The unique identifier of the field. Example: text_field_1
            page_index (int): The zero-based index of the page where the new field will be inserted.
            request (UpsertFieldReadOnlyTextRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the add field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.add_read_only_text_field`.
        """
        return app_definition_client.add_read_only_text_field(
            app_id=app_id,
            section_index=section_index,
            field_index=field_index,
            page_index=page_index,
            field_name=field_name,
            request=request,
        )

    def update_read_only_text_field(
        app_id: str, field_name: str, request: UpsertFieldReadOnlyTextRequest
    ) -> FieldOperationResponse:
        """
        Updates a read only text field in a Clappia application.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            field_name (str): The unique identifier of the field which need to be updated. Example: text_field_1
            request (UpsertFieldReadOnlyTextRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the update field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_read_only_text_field`.
        """
        return app_definition_client.update_read_only_text_field(
            app_id=app_id, field_name=field_name, request=request
        )

    def add_tag_field(
        app_id: str,
        section_index: int,
        field_index: int,
        field_name: str,
        page_index: int,
        request: UpsertFieldTagsRequest,
    ) -> FieldOperationResponse:
        """
        Adds a tag field to a Clappia application at a specified section and field position. Its used to add tags to a field, Ex. Categorizing inventory items, products, or employees with multiple labels, customers with multiple tags, etc.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            section_index (int): The index of the section where the field should be added, should be greater than 0.
            field_index (int): The index position within the section to insert the field.
            field_name (str): The unique identifier of the field. Example: text_field_1
            page_index (int): The zero-based index of the page where the new field will be inserted.
            request (UpsertFieldTagsRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the add field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.add_tag_field`.
        """
        return app_definition_client.add_tag_field(
            app_id=app_id,
            section_index=section_index,
            field_index=field_index,
            page_index=page_index,
            field_name=field_name,
            request=request,
        )

    def update_tag_field(
        app_id: str, field_name: str, request: UpsertFieldTagsRequest
    ) -> FieldOperationResponse:
        """
        Updates a tag field in a Clappia application.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            field_name (str): The unique identifier of the field which need to be updated. Example: text_field_1
            request (UpsertFieldTagsRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the update field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_tag_field`.
        """
        return app_definition_client.update_tag_field(
            app_id=app_id, field_name=field_name, request=request
        )

    def add_unique_sequential_field(
        app_id: str,
        section_index: int,
        field_index: int,
        field_name: str,
        page_index: int,
        request: UpsertFieldUniqueSequentialRequest,
    ) -> FieldOperationResponse:
        """
        Adds a unique sequential field to a Clappia application at a specified section and field position.It is used to automatically allot the Sequential Numbering to any entity.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            section_index (int): The index of the section where the field should be added, should be greater than 0.
            field_index (int): The index position within the section to insert the field.
            field_name (str): The unique identifier of the field. Example: text_field_1
            page_index (int): The zero-based index of the page where the new field will be inserted.
            request (UpsertFieldUniqueSequentialRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the add field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.add_unique_sequential_field`.
        """
        return app_definition_client.add_unique_sequential_field(
            app_id=app_id,
            section_index=section_index,
            field_index=field_index,
            page_index=page_index,
            field_name=field_name,
            request=request,
        )

    def update_unique_sequential_field(
        app_id: str, field_name: str, request: UpsertFieldUniqueSequentialRequest
    ) -> FieldOperationResponse:
        """
        Updates a unique sequential field in a Clappia application.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            field_name (str): The unique identifier of the field which need to be updated. Example: text_field_1
            request (UpsertFieldUniqueSequentialRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the update field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_unique_sequential_field`.
        """
        return app_definition_client.update_unique_sequential_field(
            app_id=app_id, field_name=field_name, request=request
        )

    def add_drop_down_field(
        app_id: str,
        section_index: int,
        field_index: int,
        field_name: str,
        page_index: int,
        request: UpsertFieldDropdownRequest,
    ) -> FieldOperationResponse:
        """
        Adds a drop down field to a Clappia application at a specified section and field position. Its used to add a drop down field to a field, Ex. Select a product, Select a category, etc.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            section_index (int): The index of the section where the field should be added, should be greater than 0.
            field_index (int): The index position within the section to insert the field.
            field_name (str): The unique identifier of the field. Example: text_field_1
            page_index (int): The zero-based index of the page where the new field will be inserted.
            request (UpsertFieldDropdownRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the add field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.add_drop_down_field`.
        """
        return app_definition_client.add_drop_down_field(
            app_id=app_id,
            section_index=section_index,
            field_index=field_index,
            page_index=page_index,
            field_name=field_name,
            request=request,
        )

    def update_drop_down_field(
        app_id: str, field_name: str, request: UpsertFieldDropdownRequest
    ) -> FieldOperationResponse:
        """
        Updates a drop down field in a Clappia application.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            field_name (str): The unique identifier of the field which need to be updated. Example: text_field_1
            request (UpsertFieldDropdownRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the update field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_drop_down_field`.
        """
        return app_definition_client.update_drop_down_field(
            app_id=app_id, field_name=field_name, request=request
        )

    def add_radio_field(
        app_id: str,
        section_index: int,
        field_index: int,
        field_name: str,
        page_index: int,
        request: UpsertFieldRadioRequest,
    ) -> FieldOperationResponse:
        """
        Adds a radio field to a Clappia application at a specified section and field position. Its used to add a radio field to a field, Ex. Select a product, Select a category, etc.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            section_index (int): The index of the section where the field should be added, should be greater than 0.
            field_index (int): The index position within the section to insert the field.
            field_name (str): The unique identifier of the field. Example: text_field_1
            page_index (int): The zero-based index of the page where the new field will be inserted.
            request (UpsertFieldRadioRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the add field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.add_radio_field`.
        """
        return app_definition_client.add_radio_field(
            app_id=app_id,
            section_index=section_index,
            field_index=field_index,
            page_index=page_index,
            field_name=field_name,
            request=request,
        )

    def update_radio_field(
        app_id: str, field_name: str, request: UpsertFieldRadioRequest
    ) -> FieldOperationResponse:
        """
        Updates a radio field in a Clappia application.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            field_name (str): The unique identifier of the field which need to be updated. Example: text_field_1
            request (UpsertFieldRadioRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the update field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_radio_field`.
        """
        return app_definition_client.update_radio_field(
            app_id=app_id, field_name=field_name, request=request
        )

    def add_url_input_field(
        app_id: str,
        section_index: int,
        field_index: int,
        field_name: str,
        page_index: int,
        request: UpsertFieldUrlInputRequest,
    ) -> FieldOperationResponse:
        """
        Adds a URL input field to a Clappia application at a specified section and field position. Its used to add a URL input field to a field, Ex. Enter a URL, Enter a link, etc.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            section_index (int): The index of the section where the field should be added, should be greater than 0.
            field_index (int): The index position within the section to insert the field.
            field_name (str): The unique identifier of the field. Example: text_field_1
            page_index (int): The zero-based index of the page where the new field will be inserted.
            request (UpsertFieldUrlInputRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the add field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.add_url_input_field`.
        """
        return app_definition_client.add_url_input_field(
            app_id=app_id,
            section_index=section_index,
            field_index=field_index,
            page_index=page_index,
            field_name=field_name,
            request=request,
        )

    def update_url_input_field(
        app_id: str, field_name: str, request: UpsertFieldUrlInputRequest
    ) -> FieldOperationResponse:
        """
        Updates a URL input field in a Clappia application.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            field_name (str): The unique identifier of the field which need to be updated. Example: text_field_1
            request (UpsertFieldUrlInputRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the update field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_url_input_field`.
        """
        return app_definition_client.update_url_input_field(
            app_id=app_id, field_name=field_name, request=request
        )

    def add_checkbox_field(
        app_id: str,
        section_index: int,
        field_index: int,
        field_name: str,
        page_index: int,
        request: UpsertFieldCheckboxRequest,
    ) -> FieldOperationResponse:
        """
        Adds a checkbox field to a Clappia application at a specified section and field position. Its used to add a checkbox field to a field, Ex. Select a product, Select a category, etc.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            section_index (int): The index of the section where the field should be added, should be greater than 0.
            field_index (int): The index position within the section to insert the field.
            field_name (str): The unique identifier of the field. Example: text_field_1
            page_index (int): The zero-based index of the page where the new field will be inserted.
            request (UpsertFieldCheckboxRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the add field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.add_checkbox_field`.
        """
        return app_definition_client.add_checkbox_field(
            app_id=app_id,
            section_index=section_index,
            field_index=field_index,
            page_index=page_index,
            field_name=field_name,
            request=request,
        )

    def update_checkbox_field(
        app_id: str, field_name: str, request: UpsertFieldCheckboxRequest
    ) -> FieldOperationResponse:
        """
        Updates a checkbox field in a Clappia application.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            field_name (str): The unique identifier of the field which need to be updated. Example: text_field_1
            request (UpsertFieldCheckboxRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the update field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_checkbox_field`.
        """
        return app_definition_client.update_checkbox_field(
            app_id=app_id, field_name=field_name, request=request
        )

    def add_razorpay_payment_gateway_field(
        app_id: str,
        section_index: int,
        field_index: int,
        field_name: str,
        page_index: int,
        request: UpsertFieldRazorpayPaymentGatewayRequest,
    ) -> FieldOperationResponse:
        """
        Adds a razorpay payment gateway field to a Clappia application at a specified section and field position. Its used to add a razorpay payment gateway field in the application. It is used to collect payments from customers.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            section_index (int): The index of the section where the field should be added, should be greater than 0.
            field_index (int): The index position within the section to insert the field.
            field_name (str): The unique identifier of the field. Example: text_field_1
            page_index (int): The zero-based index of the page where the new field will be inserted.
            request (UpsertFieldRazorpayPaymentGatewayRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the add field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.add_razorpay_payment_gateway_field`.
        """
        return app_definition_client.add_razorpay_payment_gateway_field(
            app_id=app_id,
            section_index=section_index,
            field_index=field_index,
            field_name=field_name,
            page_index=page_index,
            request=request,
        )

    def update_razorpay_payment_gateway_field(
        app_id: str, field_name: str, request: UpsertFieldRazorpayPaymentGatewayRequest
    ) -> FieldOperationResponse:
        """
        Updates a razorpay payment gateway field in a Clappia application.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            field_name (str): The unique identifier of the field which need to be updated. Example: text_field_1
            request (UpsertFieldRazorpayPaymentGatewayRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the update field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_razorpay_payment_gateway_field`.
        """
        return app_definition_client.update_razorpay_payment_gateway_field(
            app_id=app_id, field_name=field_name, request=request
        )

    def add_eazypay_payment_gateway_field(
        app_id: str,
        section_index: int,
        field_index: int,
        field_name: str,
        page_index: int,
        request: UpsertFieldEazypayPaymentGatewayRequest,
    ) -> FieldOperationResponse:
        """
        Adds a eazypay payment gateway field to a Clappia application at a specified section and field position. Its used to add a eazypay payment gateway field in the application. It is used to collect payments from customers.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            section_index (int): The index of the section where the field should be added, should be greater than 0.
            field_index (int): The index position within the section to insert the field.
            field_name (str): The unique identifier of the field. Example: text_field_1
            page_index (int): The zero-based index of the page where the new field will be inserted.
            request (UpsertFieldEazypayPaymentGatewayRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the add field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.add_eazypay_payment_gateway_field`.
        """
        return app_definition_client.add_eazypay_payment_gateway_field(
            app_id=app_id,
            section_index=section_index,
            field_index=field_index,
            page_index=page_index,
            field_name=field_name,
            request=request,
        )

    def update_eazypay_payment_gateway_field(
        app_id: str, field_name: str, request: UpsertFieldEazypayPaymentGatewayRequest
    ) -> FieldOperationResponse:
        """
        Updates a eazypay payment gateway field in a Clappia application.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            field_name (str): The unique identifier of the field which need to be updated. Example: text_field_1
            request (UpsertFieldEazypayPaymentGatewayRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the update field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_eazypay_payment_gateway_field`.
        """
        return app_definition_client.update_eazypay_payment_gateway_field(
            app_id=app_id, field_name=field_name, request=request
        )

    def add_paypal_payment_gateway_field(
        app_id: str,
        section_index: int,
        field_index: int,
        field_name: str,
        page_index: int,
        request: UpsertFieldPaypalPaymentGatewayRequest,
    ) -> FieldOperationResponse:
        """
        Adds a paypal payment gateway field to a Clappia application at a specified section and field position. Its used to add a paypal payment gateway field in the application. It is used to collect payments from customers.


        Args:
            app_id (str): The unique identifier of the Clappia application.
            section_index (int): The index of the section where the field should be added, should be greater than 0.
            field_index (int): The index position within the section to insert the field.
            field_name (str): The unique identifier of the field. Example: text_field_1
            page_index (int): The zero-based index of the page where the new field will be inserted.
            request (UpsertFieldPaypalPaymentGatewayRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the add field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.add_paypal_payment_gateway_field`.
        """
        return app_definition_client.add_paypal_payment_gateway_field(
            app_id=app_id,
            section_index=section_index,
            field_index=field_index,
            page_index=page_index,
            field_name=field_name,
            request=request,
        )

    def update_paypal_payment_gateway_field(
        app_id: str, field_name: str, request: UpsertFieldPaypalPaymentGatewayRequest
    ) -> FieldOperationResponse:
        """
        Updates a paypal payment gateway field in a Clappia application.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            field_name (str): The unique identifier of the field which need to be updated. Example: text_field_1
            request (UpsertFieldPaypalPaymentGatewayRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the update field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_paypal_payment_gateway_field`.
        """
        return app_definition_client.update_paypal_payment_gateway_field(
            app_id=app_id, field_name=field_name, request=request
        )

    def add_stripe_payment_gateway_field(
        app_id: str,
        section_index: int,
        field_index: int,
        field_name: str,
        page_index: int,
        request: UpsertFieldStripePaymentGatewayRequest,
    ) -> FieldOperationResponse:
        """
        Adds a stripe payment gateway field to a Clappia application at a specified section and field position. Its used to add a stripe payment gateway field in the application. It is used to collect payments from customers.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            section_index (int): The index of the section where the field should be added, should be greater than 0.
            field_index (int): The index position within the section to insert the field.
            field_name (str): The unique identifier of the field. Example: text_field_1
            page_index (int): The zero-based index of the page where the new field will be inserted.
            request (UpsertFieldStripePaymentGatewayRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the add field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.add_stripe_payment_gateway_field`.
        """
        return app_definition_client.add_stripe_payment_gateway_field(
            app_id=app_id,
            section_index=section_index,
            field_index=field_index,
            page_index=page_index,
            field_name=field_name,
            request=request,
        )

    def update_stripe_payment_gateway_field(
        app_id: str, field_name: str, request: UpsertFieldStripePaymentGatewayRequest
    ) -> FieldOperationResponse:
        """
        Updates a stripe payment gateway field in a Clappia application.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            field_name (str): The unique identifier of the field which need to be updated. Example: text_field_1
            request (UpsertFieldStripePaymentGatewayRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the update field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_stripe_payment_gateway_field`.
        """
        return app_definition_client.update_stripe_payment_gateway_field(
            app_id=app_id, field_name=field_name, request=request
        )

    def add_button_field(
        app_id: str,
        section_index: int,
        field_index: int,
        field_name: str,
        page_index: int,
        request: UpsertFieldButtonRequest,
    ) -> FieldOperationResponse:
        """
        Adds a button field to a Clappia application at a specified section and field position.  Its used to allow end-users to navigate to other Clappia apps within the workplace. It can navigate to the other app’s Home page, Submissions tab, and Analytics tab. The button can also be used to navigate to external sites.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            section_index (int): The index of the section where the field should be added, should be greater than 0.
            field_index (int): The index position within the section to insert the field.
            field_name (str): The unique identifier of the field. Example: text_field_1
            page_index (int): The zero-based index of the page where the new field will be inserted.
            request (UpsertFieldButtonRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the add field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.add_button_field`.
        """
        return app_definition_client.add_button_field(
            app_id=app_id,
            section_index=section_index,
            field_index=field_index,
            page_index=page_index,
            field_name=field_name,
            request=request,
        )

    def update_button_field(
        app_id: str, field_name: str, request: UpsertFieldButtonRequest
    ) -> FieldOperationResponse:
        """
        Updates a button field in a Clappia application.

        Args:
            app_id (str): The unique identifier of the Clappia application.
            field_name (str): The unique identifier of the field which need to be updated. Example: text_field_1
            request (UpsertFieldButtonRequest): The request object containing additional field configuration.

        Returns:
            FieldOperationResponse: The response object indicating the result of the update field operation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.update_button_field`.
        """
        return app_definition_client.update_button_field(
            app_id=app_id, field_name=field_name, request=request
        )

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
    def get_app_definition(app_id: str) -> AppDefinitionResponse:
        """
        Fetches the complete definition of a Clappia application, including forms, fields, sections, and metadata.

        Args:
            app_id (str): The unique identifier of the Clappia application.

        Returns:
            AppDefinitionResponse: The response object containing the full app definition.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.get_definition`.
        """
        return app_definition_client.get_definition(
            app_id=app_id,
        )

    @mcp.tool()
    def create_app(request: CreateAppRequest) -> AppCreationResponse:
        """
        Creates a new Clappia application with specified sections and fields.

        Args:
            request (CreateAppRequest): The request object containing app configuration details, sections, and fields.

        Returns:
            AppCreationResponse: The response object indicating the result of the app creation.

        Raises:
            Exception: Propagates any exceptions raised by `app_definition_client.create_app`.
        """
        return app_definition_client.create_app(request=request)
