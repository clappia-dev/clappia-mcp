import sys
from mcp import types
from mcp.server import Server
from mcp.server.stdio import stdio_server
from utils import get_logger, submission_client, app_definition_client

logger = get_logger(__name__)

app = Server("clappia-mcp-server")

@app.list_tools()
async def list_tools() -> list[types.Tool]:
    """List all available Clappia tools."""
    return [
        # Submission Management Tools
        types.Tool(
            name="get_clappia_submissions",
            description="Retrieve submissions from a Clappia app with optional filtering. Supports complex filtering with conditions, operators, and logical combinations. Fetch app definition first to see the fields and statuses in the app.",
            inputSchema={
                "type": "object",
                "properties": {
                    "app_id": {
                        "type": "string", 
                        "description": "The Clappia app ID (uppercase letters and numbers only)",
                    },
                    "requesting_user_email_address": {
                        "type": "string", 
                        "description": "Email of the requesting user",
                    },
                    "page_size": {
                        "type": "integer", 
                        "default": 10, 
                        "description": "Number of submissions per page (1-1000)"
                    },
                    "forward": {
                        "type": "boolean",
                        "default": True,
                        "description": "Direction for pagination (true for forward, false for backward)"
                    },
                    "filters": {
                        "type": "object",
                        "description": "Optional filters to apply to submissions",
                        "properties": {
                            "queries": {
                                "type": "array",
                                "description": "Array of query groups",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "queries": {
                                            "type": "array",
                                            "description": "Array of individual queries within this group",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "conditions": {
                                                        "type": "array",
                                                        "description": "Array of filter conditions",
                                                        "items": {
                                                            "type": "object",
                                                            "properties": {
                                                                "operator": {
                                                                    "type": "string",
                                                                    "description": "Filter operator to apply",
                                                                    "enum": [
                                                                        "CONTAINS",
                                                                        "NOT_IN", 
                                                                        "EQ",
                                                                        "NEQ",
                                                                        "EMPTY",
                                                                        "NON_EMPTY",
                                                                        "STARTS_WITH",
                                                                        "BETWEEN",
                                                                        "GT",
                                                                        "LT",
                                                                        "GTE",
                                                                        "LTE"
                                                                    ]
                                                                },
                                                                "filterKeyType": {
                                                                    "type": "string",
                                                                    "description": "Type of field being filtered",
                                                                    "enum": ["STANDARD", "CUSTOM"]
                                                                },
                                                                "key": {
                                                                    "type": "string",
                                                                    "description": "Field key to filter on. For STANDARD type: use $submissionId, $owner, $status, $createdAt, $lastUpdatedAt, $state. For CUSTOM type: use your app's field names",
                                                                },
                                                                "value": {
                                                                    "type": "string",
                                                                    "description": "Value to filter by. Leave empty for EMPTY/NON_EMPTY operators"
                                                                }
                                                            },
                                                            "required": ["operator", "filterKeyType", "key", "value"],
                                                            "additionalProperties": False
                                                        }
                                                    },
                                                    "operator": {
                                                        "type": "string",
                                                        "description": "Logical operator to combine conditions within this query",
                                                        "enum": ["AND", "OR"],
                                                        "default": "AND"
                                                    }
                                                },
                                                "required": ["conditions"],
                                                "additionalProperties": False
                                            }
                                        }
                                    },
                                    "required": ["queries"],
                                    "additionalProperties": False
                                }
                            }
                        },
                        "required": ["queries"],
                        "additionalProperties": False
                    }
                },
                "required": ["app_id", "requesting_user_email_address"],
                "additionalProperties": False
            },
            annotations={
                "title": "Get Clappia Submissions",
                "readOnlyHint": True,
                "openWorldHint": True,
                "idempotentHint": True
            }
        ),
        # Additional tools for comprehensive Clappia management
        types.Tool(
            name="get_clappia_submissions_aggregation",
            description="Aggregate and analyze Clappia submissions with various metrics, dimensions, and grouping options. Supports complex data analysis with filtering, dimensional grouping, and statistical calculations. Fetch app definition first to see the fields and statuses in the app.",
            inputSchema={
                "type": "object",
                "properties": {
                    "app_id": {
                        "type": "string",
                        "description": "The Clappia app ID (uppercase letters and numbers only)",
                    },
                    "requesting_user_email_address": {
                        "type": "string",
                        "description": "Email of the requesting user",
                    },
                    "forward": {
                        "type": "boolean",
                        "default": True,
                        "description": "Direction for pagination (true for forward, false for backward)"
                    },
                    "dimensions": {
                        "type": "array",
                        "description": "Fields to group by for aggregation analysis",
                        "items": {
                            "type": "object",
                            "properties": {
                                "fieldName": {
                                    "type": "string",
                                    "description": "Name of the field to group by",
                                },
                                "label": {
                                    "type": "string", 
                                    "description": "Display label for the dimension",
                                },
                                "dataType": {
                                    "type": "string",
                                    "description": "Data type of the field",
                                },
                                "dimensionType": {
                                    "type": "string",
                                    "description": "Type of dimension field",
                                    "enum": ["STANDARD", "CUSTOM"],
                                    "default": "CUSTOM"
                                },
                                "sortDirection": {
                                    "type": "string",
                                    "description": "Sort direction for this dimension",
                                    "enum": ["asc", "desc"]
                                },
                                "sortType": {
                                    "type": "string",
                                    "description": "Type of sorting to apply",
                                    "enum": ["number", "string"]
                                },
                                "missingValue": {
                                    "type": "string",
                                    "description": "Value to use when field data is missing"
                                },
                                "interval": {
                                    "type": "string",
                                    "description": "Interval for date/time grouping (e.g., 'day', 'week', 'month', 'year')"
                                }
                            },
                            "required": ["fieldName", "label", "dataType"],
                            "additionalProperties": False
                        }
                    },
                    "aggregation_dimensions": {
                        "type": "array",
                        "description": "Aggregation calculations to perform on the data",
                        "items": {
                            "type": "object",
                            "properties": {
                                "type": {
                                    "type": "string",
                                    "description": "Type of aggregation to perform",
                                    "enum": ["count", "sum", "average", "minimum", "maximum", "unique"]
                                },
                                "operand": {
                                    "type": "object",
                                    "description": "Field to perform aggregation on (optional for count)",
                                    "properties": {
                                        "fieldName": {
                                            "type": "string",
                                            "description": "Name of the field to aggregate",
                                        },
                                        "label": {
                                            "type": "string",
                                            "description": "Display label for the operand",
                                        },
                                        "dataType": {
                                            "type": "string",
                                            "description": "Data type of the operand field",
                                        },
                                        "dimensionType": {
                                            "type": "string",
                                            "description": "Type of operand field",
                                            "enum": ["STANDARD", "CUSTOM"],
                                            "default": "CUSTOM"
                                        }
                                    },
                                    "required": ["fieldName", "label", "dataType"],
                                    "additionalProperties": False
                                }
                            },
                            "required": ["type"],
                            "additionalProperties": False
                        }
                    },
                    "x_axis_labels": {
                        "type": "array",
                        "description": "Labels for X-axis in chart representations",
                        "items": {
                            "type": "string"
                        }
                    },
                    "page_size": {
                        "type": "integer",
                        "description": "Number of aggregated results per page (1-1000)",
                        "default": 1000
                    },
                    "filters": {
                        "type": "object",
                        "description": "Optional filters to apply before aggregation",
                        "properties": {
                            "queries": {
                                "type": "array",
                                "description": "Array of query groups",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "queries": {
                                            "type": "array",
                                            "description": "Array of individual queries within this group",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "conditions": {
                                                        "type": "array",
                                                        "description": "Array of filter conditions",
                                                        "items": {
                                                            "type": "object",
                                                            "properties": {
                                                                "operator": {
                                                                    "type": "string",
                                                                    "description": "Filter operator to apply",
                                                                    "enum": [
                                                                        "CONTAINS",
                                                                        "NOT_IN", 
                                                                        "EQ",
                                                                        "NEQ",
                                                                        "EMPTY",
                                                                        "NON_EMPTY",
                                                                        "STARTS_WITH",
                                                                        "BETWEEN",
                                                                        "GT",
                                                                        "LT",
                                                                        "GTE",
                                                                        "LTE"
                                                                    ]
                                                                },
                                                                "filterKeyType": {
                                                                    "type": "string",
                                                                    "description": "Type of field being filtered",
                                                                    "enum": ["STANDARD", "CUSTOM"]
                                                                },
                                                                "key": {
                                                                    "type": "string",
                                                                    "description": "Field key to filter on. For STANDARD type: use $submissionId, $owner, $status, $createdAt, $lastUpdatedAt, $state. For CUSTOM type: use your app's field names",
                                                                },
                                                                "value": {
                                                                    "type": "string",
                                                                    "description": "Value to filter by. Leave empty for EMPTY/NON_EMPTY operators"
                                                                }
                                                            },
                                                            "required": ["operator", "filterKeyType", "key", "value"],
                                                            "additionalProperties": False
                                                        }
                                                    },
                                                    "operator": {
                                                        "type": "string",
                                                        "description": "Logical operator to combine conditions",
                                                        "enum": ["AND", "OR"],
                                                        "default": "AND"
                                                    }
                                                },
                                                "required": ["conditions"],
                                                "additionalProperties": False
                                            }
                                        }
                                    },
                                    "required": ["queries"],
                                    "additionalProperties": False
                                }
                            }
                        },
                        "required": ["queries"],
                        "additionalProperties": False
                    }
                },
                "required": ["app_id", "requesting_user_email_address"],
                "additionalProperties": False
            },
            annotations={
                "title": "Get Submissions Aggregation",
                "readOnlyHint": True,
                "openWorldHint": True,
                "idempotentHint": True
            }
        ),
        types.Tool(
            name="get_clappia_app_definition",
            description="Fetches complete definition of a Clappia application including forms, fields, sections, and metadata. Retrieves structure and configuration of a Clappia app to understand available fields, validation rules, and workflow logic before creating charts, filtering submissions, or planning integrations.",
            inputSchema={
                "type": "object",
                "properties": {
                    "app_id": {"type": "string", "description": "Unique application identifier in uppercase letters and numbers format (e.g., QGU236634). Use this to specify which Clappia app definition to retrieve."},
                    "requesting_user_email_address": {"type": "string", "description": "Email of the requesting user"},
                    "language": {"type": "string", "default": "en", "description": "Language code for field labels and translations. Available options: 'en' (English, default), 'es' (Spanish), 'fr' (French), 'de' (German). Use 'es' for Spanish reports or 'fr' for French localization."},
                    "strip_html": {"type": "boolean", "default": True, "description": "Whether to remove HTML formatting from text fields. True (default) removes HTML tags for clean text, False preserves HTML formatting for display purposes."},
                    "include_tags": {"type": "boolean", "default": True, "description": "Whether to include metadata tags in response. True (default) includes full metadata tags, False returns basic structure only for lightweight responses."}
                },
                "required": ["app_id", "requesting_user_email_address"]
            },
            annotations={
                "title": "Get App Definition",
                "readOnlyHint": True,
                "openWorldHint": True
            }
        ),
        
        types.Tool(
            name="create_clappia_app_submission",
            description="Create a new submission in a Clappia app. Fetch app definition first to see the fields in the app.",
            inputSchema={
                "type": "object",
                "properties": {
                    "app_id": {"type": "string", "description": "The Clappia app ID"},
                    "data": {"type": "object", "description": "Submission data as key-value pairs"},
                    "requesting_user_email_address": {"type": "string", "description": "Email of the requesting user"}
                },
                "required": ["app_id", "data", "requesting_user_email_address"]
            },
            annotations={
                "title": "Create Submission",
                "readOnlyHint": False,
                "destructiveHint": False,
                "openWorldHint": True
            }
        ),
        
        types.Tool(
            name="edit_clappia_submission",
            description="Edit an existing submission in a Clappia app. Fetch app definition first to see the fields in the app.",
            inputSchema={
                "type": "object",
                "properties": {
                    "app_id": {"type": "string", "description": "The Clappia app ID"},
                    "submission_id": {"type": "string", "description": "The submission ID to edit"},
                    "data": {"type": "object", "description": "Updated submission data"},
                    "requesting_user_email_address": {"type": "string", "description": "Email of the requesting user"}
                },
                "required": ["app_id", "submission_id", "data", "requesting_user_email_address"]
            },
            annotations={
                "title": "Edit Submission",
                "readOnlyHint": False,
                "destructiveHint": True,
                "openWorldHint": True
            }
        ),
        
        types.Tool(
            name="update_clappia_submission_status",
            description="Update the status of a Clappia submission. Fetch app definition first to see and verify the statuses in the app.",
            inputSchema={
                "type": "object",
                "properties": {
                    "app_id": {"type": "string", "description": "The Clappia app ID"},
                    "submission_id": {"type": "string", "description": "The submission ID"},
                    "status_name": {"type": "string", "description": "New status name"},
                    "requesting_user_email_address": {"type": "string", "description": "Email of the requesting user"},
                    "comments": {"type": "string", "description": "Optional comments"}
                },
                "required": ["app_id", "submission_id", "status_name", "requesting_user_email_address"]
            },
            annotations={
                "title": "Update Submission Status",
                "readOnlyHint": False,
                "destructiveHint": False,
                "openWorldHint": True
            }
        ),
        
        types.Tool(
            name="update_clappia_submission_owners",
            description="Update the owners of a Clappia submission",
            inputSchema={
                "type": "object",
                "properties": {
                    "app_id": {"type": "string", "description": "The Clappia app ID"},
                    "submission_id": {"type": "string", "description": "The submission ID"},
                    "email_ids": {"type": "array", "items": {"type": "string"}, "description": "List of email addresses"},
                    "requesting_user_email_address": {"type": "string", "description": "Email of the requesting user"}
                },
                "required": ["app_id", "submission_id", "email_ids", "requesting_user_email_address"]
            },
            annotations={
                "title": "Update Submission Owners",
                "readOnlyHint": False,
                "destructiveHint": False,
                "openWorldHint": True
            }
        ),
        
        # App Definition Tools
       types.Tool(
            name="create_clappia_app",
            description="Create a new Clappia app with specified sections and fields",
            inputSchema={
                "type": "object",
                "properties": {
                    "app_name": {
                        "type": "string",
                        "description": "Name of the app to create",
                        "minLength": 3
                    },
                    "requesting_user_email_address": {
                        "type": "string",
                        "description": "Email of the requesting user",
                        "format": "email",
                        "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
                    },
                    "sections": {
                        "type": "array",
                        "description": "Array of sections with fields",
                        "minItems": 1,
                        "items": {
                            "type": "object",
                            "properties": {
                                "sectionName": {
                                    "type": "string",
                                    "description": "Name of the section",
                                    "minLength": 1
                                },
                                "fields": {
                                    "type": "array",
                                    "description": "Array of fields in this section",
                                    "minItems": 1,
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "fieldType": {
                                                "type": "string",
                                                "description": "Type of field",
                                                "enum": [
                                                    "singleLineText",
                                                    "multiLineText", 
                                                    "singleSelector",
                                                    "multiSelector",
                                                    "dropDown",
                                                    "dateSelector",
                                                    "timeSelector",
                                                    "phoneNumber"
                                                ]
                                            },
                                            "label": {
                                                "type": "string",
                                                "description": "Label for the field",
                                                "minLength": 1
                                            },
                                            "options": {
                                                "type": "array",
                                                "description": "Options for selector/dropdown fields (required for singleSelector, multiSelector, dropDown)",
                                                "items": {
                                                    "type": "string"
                                                }
                                            }
                                        },
                                        "required": ["fieldType", "label"],
                                        "additionalProperties": False
                                    }
                                }
                            },
                            "required": ["sectionName", "fields"],
                            "additionalProperties": False
                        }
                    }
                },
                "required": ["app_name", "requesting_user_email_address", "sections"],
                "additionalProperties": False
            },
            annotations={
                "title": "Create Clappia App",
                "readOnlyHint": False,
                "destructiveHint": False,
                "openWorldHint": True,
                "idempotentHint": False
            }
        ),
        
        types.Tool(
            name="add_field_to_clappia_app",
            description="Add a new field to an existing Clappia application at a specific position. Supports 21 different field types including text, selectors, files, GPS, calculations, and more.",
            inputSchema={
                "type": "object",
                "properties": {
                    "app_id": {"type": "string", "description": "Application ID (e.g., 'MFX093412'). Must be in uppercase letters and numbers format."},
                    "requesting_user_email_address": {"type": "string", "description": "Email address of the user adding the field. Must be a valid email format."},
                    "section_index": {"type": "integer", "description": "Index of the section to add the field to (starts from 0)."},
                    "field_index": {"type": "integer", "description": "Position within the section for the new field (starts from 0)."},
                    "field_type": {"type": "string", "description": "Type of field. Supported types: singleLineText, multiLineText, singleSelector, multiSelector, dropDown, dateSelector, timeSelector, phoneNumber, uniqueNumbering, file, gpsLocation, html, calculationsAndLogic, codeScanner, counter, slider, signature, validation, liveTracking, nfcReader, address."},
                    "label": {"type": "string", "description": "Display label for the field."},
                    "description": {"type": "string", "description": "Field description or help text."},
                    "required": {"type": "boolean", "description": "Whether the field is required."},
                    "block_width_percentage_desktop": {"type": "integer", "description": "Width percentage on desktop (1-100). Allowed values: 25, 50, 75, 100"},
                    "block_width_percentage_mobile": {"type": "integer", "description": "Width percentage on mobile (1-100). Allowed values: 50, 100"},
                    "display_condition": {"type": "string", "description": "Condition for when to show the field."},
                    "retain_values": {"type": "boolean", "description": "Whether to retain values when field is hidden."},
                    "is_editable": {"type": "boolean", "description": "Whether the field can be edited."},
                    "editability_condition": {"type": "string", "description": "Condition for when field is editable."},
                    "validation": {"type": "string", "description": "Validation type."},
                    "default_value": {"type": "string", "description": "Default value for the field (applicable only for singleLineText)."},
                    "options": {"type": "array", "items": {"type": "string"}, "description": "List of options for selector fields (applicable for singleSelector/multiSelector/dropDown)."},
                    "style": {"type": "string", "description": "Style for selector fields - 'Standard' or 'Chips' (applicable for singleSelector/multiSelector)."},
                    "number_of_cols": {"type": "integer", "description": "Number of columns for selector fields (applicable for singleSelector/multiSelector)."},
                    "allowed_file_types": {"type": "array", "items": {"type": "string"}, "description": "List of allowed file types (applicable for file fields). Valid values: 'images_camera_upload', 'images_gallery_upload', 'videos', 'documents'."},
                    "max_file_allowed": {"type": "integer", "description": "Maximum files allowed, between 1-10 (applicable for file fields)."},
                    "image_quality": {"type": "string", "description": "Image quality - 'low', 'medium', 'high' (applicable for file fields)."},
                    "image_text": {"type": "string", "description": "Text overlay for image fields (applicable for file fields)."},
                    "file_name_prefix": {"type": "string", "description": "Prefix for uploaded file names (applicable for file fields)."},
                    "formula": {"type": "string", "description": "Formula for calculation fields (applicable for calculationsAndLogic fields). Formula is a string that contains the formula for the field in format, Example: {sales} - {costs}, where {sales} and {costs} are the field names in the app. IMPORTANT: Try fetching the app definition and see the fields in the app, then use the field names in the formula."},
                    "hidden": {"type": "boolean", "description": "Whether the field is hidden (applicable for formula fields)."}
                },
                "required": ["app_id", "requesting_user_email_address", "section_index", "field_index", "field_type"]
            },
            annotations={
                "title": "Add Field to App",
                "readOnlyHint": False,
                "destructiveHint": False,
                "openWorldHint": True
            }
        ),
        
        types.Tool(
            name="update_field_in_clappia_app",
            description="Updates an existing field in a Clappia application with new configuration. Modifies the properties of an existing field in a Clappia app, enabling dynamic form updates, A/B testing, and iterative improvements without recreating the entire app.",
            inputSchema={
                "type": "object",
                "properties": {
                    "app_id": {"type": "string", "description": "Application ID in uppercase letters and numbers format (e.g., 'MFX093412')."},
                    "requesting_user_email_address": {"type": "string", "description": "Email address of the user updating the field. This user must have permission to modify the app. Must be a valid email format."},
                    "field_name": {"type": "string", "description": "Variable name of the existing field to update (e.g., 'employeeName', 'department')."},
                    "label": {"type": "string", "description": "New display label for the field."},
                    "description": {"type": "string", "description": "New field description/help text."},
                    "required": {"type": "boolean", "description": "Whether the field is mandatory."},
                    "block_width_percentage_desktop": {"type": "integer", "description": "Width percentage on desktop (1-100). Allowed values: 25, 50, 75, 100"},
                    "block_width_percentage_mobile": {"type": "integer", "description": "Width percentage on mobile (1-100). Allowed values: 50, 100"},
                    "display_condition": {"type": "string", "description": "Condition for when to show the field."},
                    "retain_values": {"type": "boolean", "description": "Whether to retain values when field is hidden."},
                    "is_editable": {"type": "boolean", "description": "Whether the field can be edited."},
                    "editability_condition": {"type": "string", "description": "Condition for when field is editable."},
                    "validation": {"type": "string", "description": "Validation type - 'none', 'number', 'email', 'url', 'custom'."},
                    "default_value": {"type": "string", "description": "Default value for the field (applicable only for singleLineText)."},
                    "options": {"type": "array", "items": {"type": "string"}, "description": "List of options for selector fields (applicable for singleSelector/multiSelector/dropDown)."},
                    "style": {"type": "string", "description": "Style for selector fields - 'Standard' or 'Chips' (applicable for singleSelector/multiSelector)."},
                    "number_of_cols": {"type": "integer", "description": "Number of columns for selector fields (applicable for singleSelector/multiSelector)."},
                    "allowed_file_types": {"type": "array", "items": {"type": "string"}, "description": "List of allowed file types (applicable for file fields). Valid values: 'images_camera_upload', 'images_gallery_upload', 'videos', 'documents'."},
                    "max_file_allowed": {"type": "integer", "description": "Maximum files allowed, between 1-10 (applicable for file fields)."},
                    "image_quality": {"type": "string", "description": "Image quality - 'low', 'medium', 'high' (applicable for file fields)."},
                    "image_text": {"type": "string", "description": "Text overlay for image fields (applicable for file fields)."},
                    "file_name_prefix": {"type": "string", "description": "Prefix for uploaded file names (applicable for file fields)."},
                    "formula": {"type": "string", "description": "Formula for calculation fields (applicable for calculationsAndLogic fields). Formula is a string that contains the formula for the field in format. Example: {sales} - {costs}, where {sales} and {costs} are the field names in the app. IMPORTANT: Try fetching the app definition and see the fields in the app, then use the field names in the formula."},
                    "hidden": {"type": "boolean", "description": "Whether the field is hidden (applicable for formula fields)."}
                },
                "required": ["app_id", "requesting_user_email_address", "field_name"]
            },
            annotations={
                "title": "Update App Field",
                "readOnlyHint": False,
                "destructiveHint": True,
                "openWorldHint": True
            }
        )
    ]

@app.call_tool()
async def call_tool(
    name: str,
    arguments: dict
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool calls for all Clappia operations."""
    
    try:
        # Submission Management Tools
        if name == "get_clappia_submissions":
            result = submission_client.get_submissions(
                arguments["app_id"],
                arguments["requesting_user_email_address"],
                arguments.get("page_size", 10),
                arguments.get("forward", True),
                arguments.get("filters")
            )
            return [types.TextContent(type="text", text=str(result))]
            
        elif name == "get_clappia_submissions_aggregation":
            result = submission_client.get_submissions_aggregation(
                arguments["app_id"],
                arguments["requesting_user_email_address"],
                arguments.get("dimensions"),
                arguments.get("aggregation_dimensions"),
                arguments.get("x_axis_labels"),
                arguments.get("forward", True),
                arguments.get("page_size", 1000),
                arguments.get("filters")
            )
            return [types.TextContent(type="text", text=str(result))]
            
        elif name == "get_clappia_app_definition":
            result = app_definition_client.get_definition(
                arguments["app_id"],
                arguments.get("language", "en"),
                arguments.get("strip_html", True),
                arguments.get("include_tags", True)
            )
            return [types.TextContent(type="text", text=str(result))]
            
        elif name == "create_clappia_app_submission":
            result = submission_client.create_submission(
                arguments["app_id"],
                arguments["data"],
                arguments["requesting_user_email_address"]
            )
            return [types.TextContent(type="text", text=str(result))]
            
        elif name == "edit_clappia_submission":
            result = submission_client.edit_submission(
                arguments["app_id"],
                arguments["submission_id"],
                arguments["data"],
                arguments["requesting_user_email_address"]
            )
            return [types.TextContent(type="text", text=str(result))]
            
        elif name == "update_clappia_submission_status":
            result = submission_client.update_status(
                arguments["app_id"],
                arguments["submission_id"],
                arguments["requesting_user_email_address"],
                arguments["status_name"],
                arguments.get("comments")
            )
            return [types.TextContent(type="text", text=str(result))]
            
        elif name == "update_clappia_submission_owners":
            result = submission_client.update_owners(
                arguments["app_id"],
                arguments["submission_id"],
                arguments["requesting_user_email_address"],
                arguments["email_ids"]
            )
            return [types.TextContent(type="text", text=str(result))]
            
        # App Definition Tools
        elif name == "create_clappia_app":
            result = app_definition_client.create_app(
                arguments["app_name"],
                arguments["requesting_user_email_address"],
                arguments["sections"]
            )
            return [types.TextContent(type="text", text=str(result))]
            
        elif name == "add_field_to_clappia_app":
            result = app_definition_client.add_field(
                app_id=arguments["app_id"],
                requesting_user_email_address=arguments["requesting_user_email_address"],
                section_index=arguments["section_index"],
                field_index=arguments["field_index"],
                field_type=arguments["field_type"],
                label=arguments.get("label"),
                description=arguments.get("description"),
                required=arguments.get("required"),
                block_width_percentage_desktop=arguments.get("block_width_percentage_desktop"),
                block_width_percentage_mobile=arguments.get("block_width_percentage_mobile"),
                display_condition=arguments.get("display_condition"),
                retain_values=arguments.get("retain_values"),
                is_editable=arguments.get("is_editable"),
                editability_condition=arguments.get("editability_condition"),
                validation=arguments.get("validation"),
                default_value=arguments.get("default_value"),
                options=arguments.get("options"),
                style=arguments.get("style"),
                number_of_cols=arguments.get("number_of_cols"),
                allowed_file_types=arguments.get("allowed_file_types"),
                max_file_allowed=arguments.get("max_file_allowed"),
                image_quality=arguments.get("image_quality"),
                image_text=arguments.get("image_text"),
                file_name_prefix=arguments.get("file_name_prefix"),
                formula=arguments.get("formula"),
                hidden=arguments.get("hidden")
            )
            return [types.TextContent(type="text", text=str(result))]
            
        elif name == "update_field_in_clappia_app":
            result = app_definition_client.update_field(
                app_id=arguments["app_id"],
                requesting_user_email_address=arguments["requesting_user_email_address"],
                field_name=arguments["field_name"],
                label=arguments.get("label"),
                description=arguments.get("description"),
                required=arguments.get("required"),
                block_width_percentage_desktop=arguments.get("block_width_percentage_desktop"),
                block_width_percentage_mobile=arguments.get("block_width_percentage_mobile"),
                display_condition=arguments.get("display_condition"),
                retain_values=arguments.get("retain_values"),
                is_editable=arguments.get("is_editable"),
                editability_condition=arguments.get("editability_condition"),
                validation=arguments.get("validation"),
                default_value=arguments.get("default_value"),
                options=arguments.get("options"),
                style=arguments.get("style"),
                number_of_cols=arguments.get("number_of_cols"),
                allowed_file_types=arguments.get("allowed_file_types"),
                max_file_allowed=arguments.get("max_file_allowed"),
                image_quality=arguments.get("image_quality"),
                image_text=arguments.get("image_text"),
                file_name_prefix=arguments.get("file_name_prefix"),
                formula=arguments.get("formula"),
                hidden=arguments.get("hidden")
            )
            return [types.TextContent(type="text", text=str(result))]
            
        else:
            raise ValueError(f"Tool not found: {name}")
            
    except Exception as e:
        logger.error(f"Error in tool {name}: {str(e)}")
        return [types.TextContent(type="text", text=f"Error executing {name}: {str(e)}")]

async def main():
    """Start Clappia MCP server with error handling."""
    try:
        logger.info("Starting Clappia MCP server")
        logger.info("IMPORTANT: All tools require requesting_user_email_address to be explicitly provided")
        logger.info("Do not use default values for this parameter")
        logger.info("requesting_user_email_address must be a valid email format")
        logger.info("CLAPPIA_API_KEY and CLAPPIA_WORKPLACE_ID must be set as environment variables")
        
        async with stdio_server() as (read_stream, write_stream):
            await app.run(read_stream, write_stream, app.create_initialization_options())
    except KeyboardInterrupt:
        logger.info("Server shutdown requested by user")
    except Exception as e:
        logger.error(f"Server startup failed: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        sys.exit(1)
    finally:
        logger.info("MCP server shutdown complete")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())