"""
definitions.py - Clappia MCP App Definitions Module using Modern Pydantic Approach
Handles all app definition and field management operations with clean Pydantic models
"""

from mcp.server.fastmcp import FastMCP
from utils import get_logger, app_definition_client
from clappia_api_tools.models import GetAppDefinitionRequest, CreateAppRequest, AddFieldRequest, UpdateFieldRequest, AppDefinitionResponse, AppCreationResponse, FieldOperationResponse, AddPageBreakRequest, UpdatePageBreakRequest, PageBreakOperationResponse, AddSectionRequest, UpdateSectionRequest, AddSectionResponse, UpdateSectionResponse, AddFieldTextRequest, AddFieldTextAreaRequest, AddFieldDependencyAppRequest, AddFieldRestApiRequest, AddFieldAddressRequest, UpdateFieldRequest, AddFieldAIRequest, AddFieldCodeReaderRequest, AddFieldEmailInputRequest, AddFieldEmojiRequest, AddFieldFileRequest, AddFieldGpsLocationRequest, AddFieldLiveTrackingRequest, AddFieldManualAddressRequest, AddFieldPhoneNumberRequest, AddFieldProgressBarRequest, AddFieldSignatureRequest, AddFieldRangeRequest, AddFieldCounterRequest, AddFieldSliderRequest, AddFieldTimeRequest, AddFieldToggleRequest, AddFieldValidationRequest, AddFieldVideoViewerRequest, AddFieldVoiceRequest, AddFieldFormulaRequest, AddFieldImageViewerRequest, AddFieldRichTextEditorRequest, AddFieldNfcReaderRequest, AddFieldNumberInputRequest, AddFieldPdfViewerRequest, AddFieldReadOnlyFileRequest, AddFieldReadOnlyTextRequest, AddFieldTagsRequest, AddFieldUniqueSequentialRequest, AddFieldDropdownRequest, AddFieldRadioRequest, AddFieldUrlInputRequest, AddFieldCheckboxRequest, AddFieldPaymentGatewayRequest, AddFieldRazorpayPaymentGatewayRequest, AddFieldEazypayPaymentGatewayRequest, AddFieldPaypalPaymentGatewayRequest, AddFieldStripePaymentGatewayRequest, AddFieldButtonRequest
logger = get_logger(__name__)

def register_definition_tools(mcp: FastMCP):

    @mcp.tool()
    async def add_section_to_clappia_app(request: AddSectionRequest) -> AddSectionResponse:
        """
        Add a new section to a Clappia application at a specific position.
        """
        try:
            return app_definition_client.add_section(
                app_id=request.app_id,
                section_index=request.section_index,
                page_index=request.page_index,
                section_name=request.section_name,
                description=request.description,
                is_collapsed_by_default=request.is_collapsed_by_default,
                is_collapsible=request.is_collapsible,
            )
        except Exception as e:
            logger.error(f"Error in add_section_to_clappia_app: {str(e)}")
            return AddSectionResponse(
                success=False,
                message=f"Error adding section: {str(e)}",
                app_id=request.app_id,
            )
    
    @mcp.tool()
    async def update_section_in_clappia_app(request: UpdateSectionRequest) -> UpdateSectionResponse:
        """
        Update an existing section in a Clappia application at a specific position.
        """
        try:
            return app_definition_client.update_section(
                app_id=request.app_id,
                section_index=request.section_index,
                page_index=request.page_index,
                section_name=request.section_name,
                description=request.description,
                is_collapsed_by_default=request.is_collapsed_by_default,
                is_collapsible=request.is_collapsible,
            )
        except Exception as e:
            logger.error(f"Error in update_section_in_clappia_app: {str(e)}")
            return UpdateSectionResponse(
                success=False,
                message=f"Error updating section: {str(e)}",
                app_id=request.app_id,
            )
    
    @mcp.tool()
    async def add_page_break_to_clappia_app(request: AddPageBreakRequest) -> PageBreakOperationResponse:
        """
        Add a page break to a Clappia application at a specific position. 
        """
        try:
            return app_definition_client.add_page_break(
                app_id=request.app_id,
                page_index=request.page_index,
                section_index=request.section_index,
            )
        except Exception as e:
            logger.error(f"Error in add_page_break_to_clappia_app: {str(e)}")
            return PageBreakOperationResponse(
                success=False,
                message=f"Error adding page break: {str(e)}",
                app_id=request.app_id,
                page_index=request.page_index,
                section_index=request.section_index,
            )
            
    @mcp.tool()
    async def update_page_break_in_clappia_app(request: UpdatePageBreakRequest) -> PageBreakOperationResponse:
        """
        Update a page break in a Clappia application at a specific position.
        """
        try:
            return app_definition_client.update_page(
                app_id=request.app_id,
                page_index=request.page_index,
                show_submit_button=request.show_submit_button,
                previous_button_text=request.previous_button_text,
                next_button_text=request.next_button_text
            )
        except Exception as e:
            logger.error(f"Error in update_page_break_in_clappia_app: {str(e)}")
            return PageBreakOperationResponse(
                success=False,
                message=f"Error updating page break: {str(e)}",
                app_id=request.app_id,
                page_index=request.page_index,
            )
    
    @mcp.tool()
    async def get_clappia_app_definition(request: GetAppDefinitionRequest) -> AppDefinitionResponse:
        """
        Fetches complete definition of a Clappia application including forms, fields, sections, and metadata.
        
        Retrieves structure and configuration of a Clappia app to understand available fields and sections before creating charts, adding workflow steps, filtering submissions, or planning integrations.
        """
        try:
            return app_definition_client.get_definition(
                app_id=request.app_id,
                language=request.language,
            )
                
        except Exception as e:
            logger.error(f"Error in get_clappia_app_definition: {str(e)}")
            return AppDefinitionResponse(
                success=False,
                message=f"Error retrieving app definition: {str(e)}",
                app_id=request.app_id
            )

    @mcp.tool()
    async def create_clappia_app(request: CreateAppRequest) -> AppCreationResponse:
        """
        Create a new Clappia app with specified sections and fields.
        """
        try:
            sections_data = [section.model_dump() for section in request.sections]
            
            return app_definition_client.create_app(
                app_name=request.app_name,
                requesting_user_email_address=str(request.requesting_user_email_address),
                sections=sections_data
            )
                
        except Exception as e:
            logger.error(f"Error in create_clappia_app: {str(e)}")
            return AppCreationResponse(
                success=False,
                message=f"Error creating app: {str(e)}",
                app_name=request.app_name
            )

    @mcp.tool()
    async def add_text_field_to_clappia_app(request: AddFieldTextRequest) -> FieldOperationResponse:
        """
        Add a single line text input field to a Clappia application with validation options.
        """
        try:
            return app_definition_client.add_field_text(request)
        except Exception as e:
            logger.error(f"Error in add_text_field_to_clappia_app: {str(e)}")
            return FieldOperationResponse(
                success=False,
                message=f"Error adding text field: {str(e)}",
                app_id=request.app_id,
                field_name=request.field_name,
                operation="add_field_text"
            )


    @mcp.tool()
    async def add_textarea_field_to_clappia_app(request: AddFieldTextAreaRequest) -> FieldOperationResponse:
        """
        Add a multi-line textarea field to a Clappia application.
        """
        try:
            return app_definition_client.add_field_text_area(request)
        except Exception as e:
            logger.error(f"Error in add_textarea_field_to_clappia_app: {str(e)}")
            return FieldOperationResponse(
                success=False,
                message=f"Error adding textarea field: {str(e)}",
                app_id=request.app_id,
                field_name=request.field_name,
                operation="add_field_textarea"
            )


    @mcp.tool()
    async def add_dependency_app_field_to_clappia_app(request: AddFieldDependencyAppRequest) -> FieldOperationResponse:
        """
        Add a dependency app field to pull data from another Clappia application.
        """
        try:
            return app_definition_client.add_field_dependency_app(request)
        except Exception as e:
            logger.error(f"Error in add_dependency_app_field_to_clappia_app: {str(e)}")
            return FieldOperationResponse(
                success=False,
                message=f"Error adding dependency app field: {str(e)}",
                app_id=request.app_id,
                field_name=request.field_name,
                operation="add_field_dependency_app"
            )


    @mcp.tool()
    async def add_rest_api_field_to_clappia_app(request: AddFieldRestApiRequest) -> FieldOperationResponse:
        """
        Add a REST API field to pull data from external REST APIs.
        """
        try:
            return app_definition_client.add_field_rest_api(request)
        except Exception as e:
            logger.error(f"Error in add_rest_api_field_to_clappia_app: {str(e)}")
            return FieldOperationResponse(
                success=False,
                message=f"Error adding REST API field: {str(e)}",
                app_id=request.app_id,
                field_name=request.field_name,
                operation="add_field_rest_api"
            )


    @mcp.tool()
    async def add_address_field_to_clappia_app(request: AddFieldAddressRequest) -> FieldOperationResponse:
        """
        Add an address field to a Clappia application with optional country restrictions.
        """
        try:
            return app_definition_client.add_field_address(request)
        except Exception as e:
            logger.error(f"Error in add_address_field_to_clappia_app: {str(e)}")
            return FieldOperationResponse(
                success=False,
                message=f"Error adding address field: {str(e)}",
                app_id=request.app_id,
                field_name=request.field_name,
                operation="add_field_address"
            )

    @mcp.tool()
    async def add_ai_field_to_clappia_app(request: AddFieldAIRequest) -> FieldOperationResponse:
        """
        Add an AI field to a Clappia application.
        """
        try:
            return app_definition_client.add_field_ai(request)
        except Exception as e:
            logger.error(f"Error in add_ai_field_to_clappia_app: {str(e)}")
            return FieldOperationResponse(
                success=False,
                message=f"Error adding AI field: {str(e)}",
                app_id=request.app_id,
                field_name=request.field_name,
                operation="add_field_ai"
            )

    @mcp.tool()
    async def add_code_reader_field_to_clappia_app(request: AddFieldCodeReaderRequest) -> FieldOperationResponse:
        """
        Add a code reader field to a Clappia application.
        """
        try:
            return app_definition_client.add_field_code_reader(request)
        except Exception as e:
            logger.error(f"Error in add_code_reader_field_to_clappia_app: {str(e)}")
            return FieldOperationResponse(
                success=False,
                message=f"Error adding code reader field: {str(e)}",
                app_id=request.app_id,
                field_name=request.field_name,
                operation="add_field_code_reader"
            )

    @mcp.tool()
    async def add_email_input_field_to_clappia_app(request: AddFieldEmailInputRequest) -> FieldOperationResponse:
        """
        Add an email input field to a Clappia application.
        """
        try:
            return app_definition_client.add_field_email_input(request)
        except Exception as e:
            logger.error(f"Error in add_email_input_field_to_clappia_app: {str(e)}")
            return FieldOperationResponse(
                success=False,
                message=f"Error adding email input field: {str(e)}",
                app_id=request.app_id,
                field_name=request.field_name,
                operation="add_field_email_input"
            )

    @mcp.tool()
    async def add_emoji_field_to_clappia_app(request: AddFieldEmojiRequest) -> FieldOperationResponse:
        """
        Add an emoji field to a Clappia application.
        """
        try:
            return app_definition_client.add_field_emoji(request)
        except Exception as e:
            logger.error(f"Error in add_emoji_field_to_clappia_app: {str(e)}")
            return FieldOperationResponse(
                success=False,
                message=f"Error adding emoji field: {str(e)}",
                app_id=request.app_id,
                field_name=request.field_name,
                operation="add_field_emoji"
            )

    @mcp.tool()
    async def add_file_field_to_clappia_app(request: AddFieldFileRequest) -> FieldOperationResponse:
        """
        Add a file field to a Clappia application.
        """
        try:
            return app_definition_client.add_field_file(request)
        except Exception as e:
            logger.error(f"Error in add_file_field_to_clappia_app: {str(e)}")
            return FieldOperationResponse(
                success=False,
                message=f"Error adding file field: {str(e)}",
                app_id=request.app_id,
                field_name=request.field_name,
                operation="add_field_file"
            )

    @mcp.tool()
    async def add_gps_location_field_to_clappia_app(request: AddFieldGpsLocationRequest) -> FieldOperationResponse:
        """
        Add a GPS location field to a Clappia application.
        """
        try:
            return app_definition_client.add_field_gps_location(request)
        except Exception as e:
            logger.error(f"Error in add_gps_location_field_to_clappia_app: {str(e)}")
            return FieldOperationResponse(
                success=False,
                message=f"Error adding GPS location field: {str(e)}",
                app_id=request.app_id,
                field_name=request.field_name,
                operation="add_field_gps_location"
            )

    @mcp.tool()
    async def add_live_tracking_field_to_clappia_app(request: AddFieldLiveTrackingRequest) -> FieldOperationResponse:
        """
        Add a live tracking field to a Clappia application.
        """
        try:
            return app_definition_client.add_field_live_tracking(request)
        except Exception as e:
            logger.error(f"Error in add_live_tracking_field_to_clappia_app: {str(e)}")
            return FieldOperationResponse(
                success=False,
                message=f"Error adding live tracking field: {str(e)}",
                app_id=request.app_id,
                field_name=request.field_name,
                operation="add_field_live_tracking"
            )

    @mcp.tool()
    async def add_manual_address_field_to_clappia_app(request: AddFieldManualAddressRequest) -> FieldOperationResponse:
        """
        Add a manual address field to a Clappia application.
        """
        try:
            return app_definition_client.add_field_manual_address(request)
        except Exception as e:
            logger.error(f"Error in add_manual_address_field_to_clappia_app: {str(e)}")
            return FieldOperationResponse(
                success=False,
                message=f"Error adding manual address field: {str(e)}",
                app_id=request.app_id,
                field_name=request.field_name,
                operation="add_field_manual_address"
            )

    @mcp.tool()
    async def add_phone_number_field_to_clappia_app(request: AddFieldPhoneNumberRequest) -> FieldOperationResponse:
        """
        Add a phone number field to a Clappia application.
        """
        try:
            return app_definition_client.add_field_phone_number(request)
        except Exception as e:
            logger.error(f"Error in add_phone_number_field_to_clappia_app: {str(e)}")
            return FieldOperationResponse(
                success=False,
                message=f"Error adding phone number field: {str(e)}",
                app_id=request.app_id,
                field_name=request.field_name,
                operation="add_field_phone_number"
            )

    @mcp.tool()
    async def add_progress_bar_field_to_clappia_app(request: AddFieldProgressBarRequest) -> FieldOperationResponse:
        """
        Add a progress bar field to a Clappia application.
        """
        try:
            return app_definition_client.add_field_progress_bar(request)
        except Exception as e:
            logger.error(f"Error in add_progress_bar_field_to_clappia_app: {str(e)}")
            return FieldOperationResponse(
                success=False,
                message=f"Error adding progress bar field: {str(e)}",
                app_id=request.app_id,
                field_name=request.field_name,
                operation="add_field_progress_bar"
            )

    @mcp.tool()
    async def add_signature_field_to_clappia_app(request: AddFieldSignatureRequest) -> FieldOperationResponse:
        """
        Add a signature field to a Clappia application.
        """
        try:
            return app_definition_client.add_field_signature(request)
        except Exception as e:
            logger.error(f"Error in add_signature_field_to_clappia_app: {str(e)}")
            return FieldOperationResponse(
                success=False,
                message=f"Error adding signature field: {str(e)}",
                app_id=request.app_id,
                field_name=request.field_name,
                operation="add_field_signature"
            )

    @mcp.tool()
    async def add_range_field_to_clappia_app(request: AddFieldRangeRequest) -> FieldOperationResponse:
        """
        Add a range field to a Clappia application.
        """
        try:
            return app_definition_client.add_field_range(request)
        except Exception as e:
            logger.error(f"Error in add_range_field_to_clappia_app: {str(e)}")
            return FieldOperationResponse(
                success=False,
                message=f"Error adding range field: {str(e)}",
                app_id=request.app_id,
                field_name=request.field_name,
                operation="add_field_range"
            )

    @mcp.tool()
    async def add_counter_field_to_clappia_app(request: AddFieldCounterRequest) -> FieldOperationResponse:
        """
        Add a counter field to a Clappia application.
        """
        try:
            return app_definition_client.add_field_counter(request)
        except Exception as e:
            logger.error(f"Error in add_counter_field_to_clappia_app: {str(e)}")
            return FieldOperationResponse(
                success=False,
                message=f"Error adding counter field: {str(e)}",
                app_id=request.app_id,
                field_name=request.field_name,
                operation="add_field_counter"
            )

    @mcp.tool()
    async def add_slider_field_to_clappia_app(request: AddFieldSliderRequest) -> FieldOperationResponse:
        """
        Add a slider field to a Clappia application.
        """
        try:
            return app_definition_client.add_field_slider(request)
        except Exception as e:
            logger.error(f"Error in add_slider_field_to_clappia_app: {str(e)}")
            return FieldOperationResponse(
                success=False,
                message=f"Error adding slider field: {str(e)}",
                app_id=request.app_id,
                field_name=request.field_name,
                operation="add_field_slider"
            )

    @mcp.tool()
    async def add_time_field_to_clappia_app(request: AddFieldTimeRequest) -> FieldOperationResponse:
        """
        Add a time field to a Clappia application.
        """
        try:
            return app_definition_client.add_field_time(request)
        except Exception as e:
            logger.error(f"Error in add_time_field_to_clappia_app: {str(e)}")
            return FieldOperationResponse(
                success=False,
                message=f"Error adding time field: {str(e)}",
                app_id=request.app_id,
                field_name=request.field_name,
                operation="add_field_time"
            )

    @mcp.tool()
    async def add_toggle_field_to_clappia_app(request: AddFieldToggleRequest) -> FieldOperationResponse:
        """
        Add a toggle field to a Clappia application.
        """
        try:
            return app_definition_client.add_field_toggle(request)
        except Exception as e:
            logger.error(f"Error in add_toggle_field_to_clappia_app: {str(e)}")
            return FieldOperationResponse(
                success=False,
                message=f"Error adding toggle field: {str(e)}",
                app_id=request.app_id,
                field_name=request.field_name,
                operation="add_field_toggle"
            )

    @mcp.tool()
    async def add_validation_field_to_clappia_app(request: AddFieldValidationRequest) -> FieldOperationResponse:
        """
        Add a validation field to a Clappia application.
        """
        try:
            return app_definition_client.add_field_validation(request)
        except Exception as e:
            logger.error(f"Error in add_validation_field_to_clappia_app: {str(e)}")
            return FieldOperationResponse(
                success=False,
                message=f"Error adding validation field: {str(e)}",
                app_id=request.app_id,
                field_name=request.field_name,
                operation="add_field_validation"
            )

    @mcp.tool()
    async def add_video_viewer_field_to_clappia_app(request: AddFieldVideoViewerRequest) -> FieldOperationResponse:
        """
        Add a video viewer field to a Clappia application.
        """
        try:
            return app_definition_client.add_field_video_viewer(request)
        except Exception as e:
            logger.error(f"Error in add_video_viewer_field_to_clappia_app: {str(e)}")
            return FieldOperationResponse(
                success=False,
                message=f"Error adding video viewer field: {str(e)}",
                app_id=request.app_id,
                field_name=request.field_name,
                operation="add_field_video_viewer"
            )

    @mcp.tool()
    async def add_voice_field_to_clappia_app(request: AddFieldVoiceRequest) -> FieldOperationResponse:
        """
        Add a voice field to a Clappia application.
        """
        try:
            return app_definition_client.add_field_voice(request)
        except Exception as e:
            logger.error(f"Error in add_voice_field_to_clappia_app: {str(e)}")
            return FieldOperationResponse(
                success=False,
                message=f"Error adding voice field: {str(e)}",
                app_id=request.app_id,
                field_name=request.field_name,
                operation="add_field_voice"
            )

    @mcp.tool()
    async def add_formula_field_to_clappia_app(request: AddFieldFormulaRequest) -> FieldOperationResponse:
        """
        Add a formula field to a Clappia application.
        """
        try:
            return app_definition_client.add_field_formula(request)
        except Exception as e:
            logger.error(f"Error in add_formula_field_to_clappia_app: {str(e)}")
            return FieldOperationResponse(
                success=False,
                message=f"Error adding formula field: {str(e)}",
                app_id=request.app_id,
                field_name=request.field_name,
                operation="add_field_formula"
            )

    @mcp.tool()
    async def add_image_viewer_field_to_clappia_app(request: AddFieldImageViewerRequest) -> FieldOperationResponse:
        """
        Add an image viewer field to a Clappia application.
        """
        try:
            return app_definition_client.add_field_image_viewer(request)
        except Exception as e:
            logger.error(f"Error in add_image_viewer_field_to_clappia_app: {str(e)}")
            return FieldOperationResponse(
                success=False,
                message=f"Error adding image viewer field: {str(e)}",
                app_id=request.app_id,
                field_name=request.field_name,
                operation="add_field_image_viewer"
            )

    @mcp.tool()
    async def add_rich_text_editor_field_to_clappia_app(request: AddFieldRichTextEditorRequest) -> FieldOperationResponse:
        """
        Add a rich text editor field to a Clappia application.
        """
        try:
            return app_definition_client.add_field_rich_text_editor(request)
        except Exception as e:
            logger.error(f"Error in add_rich_text_editor_field_to_clappia_app: {str(e)}")
            return FieldOperationResponse(
                success=False,
                message=f"Error adding rich text editor field: {str(e)}",
                app_id=request.app_id,
                field_name=request.field_name,
                operation="add_field_rich_text_editor"
            )

    @mcp.tool()
    async def add_nfc_reader_field_to_clappia_app(request: AddFieldNfcReaderRequest) -> FieldOperationResponse:
        """
        Add an NFC reader field to a Clappia application.
        """
        try:
            return app_definition_client.add_field_nfc_reader(request)
        except Exception as e:
            logger.error(f"Error in add_nfc_reader_field_to_clappia_app: {str(e)}")
            return FieldOperationResponse(
                success=False,
                message=f"Error adding NFC reader field: {str(e)}",
                app_id=request.app_id,
                field_name=request.field_name,
                operation="add_field_nfc_reader"
            )

    @mcp.tool()
    async def add_number_input_field_to_clappia_app(request: AddFieldNumberInputRequest) -> FieldOperationResponse:
        """
        Add a number input field to a Clappia application.
        """
        try:
            return app_definition_client.add_field_number_input(request)
        except Exception as e:
            logger.error(f"Error in add_number_input_field_to_clappia_app: {str(e)}")
            return FieldOperationResponse(
                success=False,
                message=f"Error adding number input field: {str(e)}",
                app_id=request.app_id,
                field_name=request.field_name,
                operation="add_field_number_input"
            )

    @mcp.tool()
    async def add_pdf_viewer_field_to_clappia_app(request: AddFieldPdfViewerRequest) -> FieldOperationResponse:
        """
        Add a PDF viewer field to a Clappia application.
        """
        try:
            return app_definition_client.add_field_pdf_viewer(request)
        except Exception as e:
            logger.error(f"Error in add_pdf_viewer_field_to_clappia_app: {str(e)}")
            return FieldOperationResponse(
                success=False,
                message=f"Error adding PDF viewer field: {str(e)}",
                app_id=request.app_id,
                field_name=request.field_name,
                operation="add_field_pdf_viewer"
            )

    @mcp.tool()
    async def add_read_only_file_field_to_clappia_app(request: AddFieldReadOnlyFileRequest) -> FieldOperationResponse:
        """
        Add a read-only file field to a Clappia application.
        """
        try:
            return app_definition_client.add_field_read_only_file(request)
        except Exception as e:
            logger.error(f"Error in add_read_only_file_field_to_clappia_app: {str(e)}")
            return FieldOperationResponse(
                success=False,
                message=f"Error adding read-only file field: {str(e)}",
                app_id=request.app_id,
                field_name=request.field_name,
                operation="add_field_read_only_file"
            )

    @mcp.tool()
    async def add_read_only_text_field_to_clappia_app(request: AddFieldReadOnlyTextRequest) -> FieldOperationResponse:
        """
        Add a read-only text field to a Clappia application.
        """
        try:
            return app_definition_client.add_field_read_only_text(request)
        except Exception as e:
            logger.error(f"Error in add_read_only_text_field_to_clappia_app: {str(e)}")
            return FieldOperationResponse(
                success=False,
                message=f"Error adding read-only text field: {str(e)}",
                app_id=request.app_id,
                field_name=request.field_name,
                operation="add_field_read_only_text"
            )

    @mcp.tool()
    async def add_tags_field_to_clappia_app(request: AddFieldTagsRequest) -> FieldOperationResponse:
        """
        Add a tags field to a Clappia application.
        """
        try:
            return app_definition_client.add_field_tags(request)
        except Exception as e:
            logger.error(f"Error in add_tags_field_to_clappia_app: {str(e)}")
            return FieldOperationResponse(
                success=False,
                message=f"Error adding tags field: {str(e)}",
                app_id=request.app_id,
                field_name=request.field_name,
                operation="add_field_tags"
            )

    @mcp.tool()
    async def add_unique_sequential_field_to_clappia_app(request: AddFieldUniqueSequentialRequest) -> FieldOperationResponse:
        """
        Add a unique sequential field to a Clappia application.
        """
        try:
            return app_definition_client.add_field_unique_sequential(request)
        except Exception as e:
            logger.error(f"Error in add_unique_sequential_field_to_clappia_app: {str(e)}")
            return FieldOperationResponse(
                success=False,
                message=f"Error adding unique sequential field: {str(e)}",
                app_id=request.app_id,
                field_name=request.field_name,
                operation="add_field_unique_sequential"
            )

    @mcp.tool()
    async def add_dropdown_field_to_clappia_app(request: AddFieldDropdownRequest) -> FieldOperationResponse:
        """
        Add a dropdown field to a Clappia application.
        """
        try:
            return app_definition_client.add_field_dropdown(request)
        except Exception as e:
            logger.error(f"Error in add_dropdown_field_to_clappia_app: {str(e)}")
            return FieldOperationResponse(
                success=False,
                message=f"Error adding dropdown field: {str(e)}",
                app_id=request.app_id,
                field_name=request.field_name,
                operation="add_field_dropdown"
            )

    @mcp.tool()
    async def add_radio_field_to_clappia_app(request: AddFieldRadioRequest) -> FieldOperationResponse:
        """
        Add a radio field to a Clappia application.
        """
        try:
            return app_definition_client.add_field_radio(request)
        except Exception as e:
            logger.error(f"Error in add_radio_field_to_clappia_app: {str(e)}")
            return FieldOperationResponse(
                success=False,
                message=f"Error adding radio field: {str(e)}",
                app_id=request.app_id,
                field_name=request.field_name,
                operation="add_field_radio"
            )

    @mcp.tool()
    async def add_url_input_field_to_clappia_app(request: AddFieldUrlInputRequest) -> FieldOperationResponse:
        """
        Add a URL input field to a Clappia application.
        """
        try:
            return app_definition_client.add_field_url_input(request)
        except Exception as e:
            logger.error(f"Error in add_url_input_field_to_clappia_app: {str(e)}")
            return FieldOperationResponse(
                success=False,
                message=f"Error adding URL input field: {str(e)}",
                app_id=request.app_id,
                field_name=request.field_name,
                operation="add_field_url_input"
            )

    @mcp.tool()
    async def add_checkbox_field_to_clappia_app(request: AddFieldCheckboxRequest) -> FieldOperationResponse:
        """
        Add a checkbox field to a Clappia application.
        """
        try:
            return app_definition_client.add_field_checkbox(request)
        except Exception as e:
            logger.error(f"Error in add_checkbox_field_to_clappia_app: {str(e)}")
            return FieldOperationResponse(
                success=False,
                message=f"Error adding checkbox field: {str(e)}",
                app_id=request.app_id,
                field_name=request.field_name,
                operation="add_field_checkbox"
            )

    @mcp.tool()
    async def add_payment_gateway_field_to_clappia_app(request: AddFieldPaymentGatewayRequest) -> FieldOperationResponse:
        """
        Add a payment gateway field to a Clappia application.
        """
        try:
            return app_definition_client.add_field_payment_gateway(request)
        except Exception as e:
            logger.error(f"Error in add_payment_gateway_field_to_clappia_app: {str(e)}")
            return FieldOperationResponse(
                success=False,
                message=f"Error adding payment gateway field: {str(e)}",
                app_id=request.app_id,
                field_name=request.field_name,
                operation="add_field_payment_gateway"
            )

    @mcp.tool()
    async def add_razorpay_payment_gateway_field_to_clappia_app(request: AddFieldRazorpayPaymentGatewayRequest) -> FieldOperationResponse:
        """
        Add a Razorpay payment gateway field to a Clappia application.
        """
        try:
            return app_definition_client.add_field_razorpay_payment_gateway(request)
        except Exception as e:
            logger.error(f"Error in add_razorpay_payment_gateway_field_to_clappia_app: {str(e)}")
            return FieldOperationResponse(
                success=False,
                message=f"Error adding Razorpay payment gateway field: {str(e)}",
                app_id=request.app_id,
                field_name=request.field_name,
                operation="add_field_razorpay_payment_gateway"
            )

    @mcp.tool()
    async def add_eazypay_payment_gateway_field_to_clappia_app(request: AddFieldEazypayPaymentGatewayRequest) -> FieldOperationResponse:
        """
        Add an Eazypay payment gateway field to a Clappia application.
        """
        try:
            return app_definition_client.add_field_eazypay_payment_gateway(request)
        except Exception as e:
            logger.error(f"Error in add_eazypay_payment_gateway_field_to_clappia_app: {str(e)}")
            return FieldOperationResponse(
                success=False,
                message=f"Error adding Eazypay payment gateway field: {str(e)}",
                app_id=request.app_id,
                field_name=request.field_name,
                operation="add_field_eazypay_payment_gateway"
            )

    @mcp.tool()
    async def add_paypal_payment_gateway_field_to_clappia_app(request: AddFieldPaypalPaymentGatewayRequest) -> FieldOperationResponse:
        """
        Add a PayPal payment gateway field to a Clappia application.
        """
        try:
            return app_definition_client.add_field_paypal_payment_gateway(request)
        except Exception as e:
            logger.error(f"Error in add_paypal_payment_gateway_field_to_clappia_app: {str(e)}")
            return FieldOperationResponse(
                success=False,
                message=f"Error adding PayPal payment gateway field: {str(e)}",
                app_id=request.app_id,
                field_name=request.field_name,
                operation="add_field_paypal_payment_gateway"
            )

    @mcp.tool()
    async def add_stripe_payment_gateway_field_to_clappia_app(request: AddFieldStripePaymentGatewayRequest) -> FieldOperationResponse:
        """
        Add a Stripe payment gateway field to a Clappia application.
        """
        try:
            return app_definition_client.add_field_stripe_payment_gateway(request)
        except Exception as e:
            logger.error(f"Error in add_stripe_payment_gateway_field_to_clappia_app: {str(e)}")
            return FieldOperationResponse(
                success=False,
                message=f"Error adding Stripe payment gateway field: {str(e)}",
                app_id=request.app_id,
                field_name=request.field_name,
                operation="add_field_stripe_payment_gateway"
            )

    @mcp.tool()
    async def add_button_field_to_clappia_app(request: AddFieldButtonRequest) -> FieldOperationResponse:
        """
        Add a button field to a Clappia application.
        """
        try:
            return app_definition_client.add_field_button(request)
        except Exception as e:
            logger.error(f"Error in add_button_field_to_clappia_app: {str(e)}")
            return FieldOperationResponse(
                success=False,
                message=f"Error adding button field: {str(e)}",
                app_id=request.app_id,
                field_name=request.field_name,
                operation="add_field_button"
            )

    @mcp.tool()
    async def update_field_in_clappia_app(request: UpdateFieldRequest) -> FieldOperationResponse:
        """
        Updates an existing field in a Clappia application with new configuration.
        
        Modifies the properties of an existing field, enabling dynamic form updates,
        A/B testing, and iterative improvements without recreating the entire app.
        """
        try:
            return app_definition_client.update_field(
                app_id=request.app_id,
                field_name=request.field_name,
                label=request.label,
                description=request.description,
                required=request.required,
                block_width_percentage_desktop=request.block_width_percentage_desktop,
                block_width_percentage_mobile=request.block_width_percentage_mobile,
                display_condition=request.display_condition,
                retain_values=request.retain_values,
                is_editable=request.is_editable,
                editability_condition=request.editability_condition,
                validation=request.validation,
                default_value=request.default_value,
                options=request.options,
                style=request.style,
                number_of_cols=request.number_of_cols,
                allowed_file_types=request.allowed_file_types,
                max_file_allowed=request.max_file_allowed,
                image_quality=request.image_quality,
                image_text=request.image_text,
                file_name_prefix=request.file_name_prefix,
                formula=request.formula,
                hidden=request.hidden
            )
                
        except Exception as e:
            logger.error(f"Error in update_field_in_clappia_app: {str(e)}")
            return FieldOperationResponse(
                success=False,
                message=f"Error updating field: {str(e)}",
                app_id=request.app_id,
                field_name=request.field_name,
                operation="update_field"
            )