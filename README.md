# Clappia MCP (Model Context Protocol)

A Python-based MCP server that provides a comprehensive interface for interacting with the Clappia platform. This server enables programmatic management of Clappia applications, forms, submissions, and more.

Clappia is a no-code platform that allows businesses, operations teams, and non-developers to create custom apps—like inspection forms, approval workflows, field data collection tools, internal dashboards, and more—without writing a single line of code. It's used across industries for automating manual processes, digitizing paperwork, and improving operational efficiency. [Click here](https://www.clappia.com) to learn more.

## Features

-  **App Management**
   -  Create new Clappia apps with customizable sections and fields (via MCP tools)
   -  Retrieve detailed app definitions with field metadata
-  **Submission Management**
   -  Create new submissions with field data
   -  Edit existing submissions with validation
   -  Update submission status with optional comments
   -  Manage submission owners with email-based assignments
   -  Retrieve submissions with advanced filtering and pagination
   -  Get submission aggregations for analytics with customizable dimensions
-  **Field Management**
   -  Add new fields with comprehensive configuration options
   -  Update field properties including validation, display conditions, and layout

## Prerequisites

-  Python 3.10 or higher
-  [uv](https://github.com/astral-sh/uv) python package manager
-  Access to Clappia API Key and Workplace ID
-  Claude for Desktop (or any other MCP Clients)

## Installation

1. **Set up Clappia API Access**:
   -  Visit your Workplace in Clappia (https://<your_workplace>.clappia.com), you need to have Workplace Manager Access to this Workplace.
   -  Visit Workplace Settings. Note your Workplace ID.
   -  Visit Workplace Settings -> Preferences -> API Keys. Note your API Key, generate one if it is not yet generated.
2. **Set up Claude for Desktop**:

   -  Download Claude for Desktop for [macOS](https://claude.ai/download) or [Windows](https://claude.ai/download)
   -  Install and launch Claude for Desktop
   -  Open Claude menu → Settings → Developer → Edit Config
   -  Add the following configuration to `claude_desktop_config.json`:
      ```json
      {
         "mcpServers": {
            "clappia-mcp": {
               "command": "uv",
               "args": [
                  "--directory",
                  "/Users/<YOUR_DIRECTORY>/Desktop/clappia-mcp",
                  "run",
                  "clappia-mcp.py"
               ],
               "env": {
                  "CLAPPIA_API_KEY": "<ENTER_YOUR_WORKPLACE_API_KEY_HERE>",
                  "CLAPPIA_WORKPLACE_ID": "<ENTER_YOUR_WORKPLACE_ID_HERE>"
               }
            }
         }
      }
      ```
   -  Restart Claude for Desktop
   -  Verify the MCP server is running by checking for the tools icon in the input box

3. **Clone the repository**:

   ```bash
   git clone https://github.com/clappia-dev/clappia-mcp.git
   cd clappia-mcp
   ```

4. **Set up Python Environment**:

   ```bash
   # Install uv if not already installed
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Install dependencies
   uv sync
   ```

## Project Structure

```
clappia-mcp/
├── clappia-mcp.py          # Main MCP server implementation and tool definitions
├── tools/                  # Core functionality modules
│   ├── get_submissions.py  # Submission retrieval logic
│   └── get_submissions_aggregation.py # Analytics functionality
├── pyproject.toml         # Project metadata and dependencies
├── uv.lock                # Dependency lock file (if using uv)
└── .env                   # Environment variables
```

All main tool logic is exposed via `clappia-mcp.py`, which uses the `clappia_api_tools` package for Clappia API operations. The `tools/` directory contains helper modules for submissions and analytics.

### Usage

-  The server will automatically start when Claude Desktop launches
-  Access tools through the Claude Desktop interface
-  All tool invocations are handled via the MCP protocol and do not require direct Python imports

### Troubleshooting

1. **Server Not Starting**:
   -  Check Claude Desktop logs for errors
   -  Verify Python environment is activated
   -  Ensure all dependencies are installed
   -  Check environment variables are set correctly
2. **API Connection Issues**:
   -  Verify API credentials in `claude_desktop_config.json` file
   -  Check network connectivity
   -  Review API rate limits
3. **Tool Execution Failures**:
   -  Check server logs for detailed error messages
   -  Verify input parameters match API requirements
   -  Ensure proper permissions for API operations

### Example Tool Usage

All tool usage is via the MCP server interface (e.g., Claude Desktop). Here are the main tools exposed:

-  **get_clappia_submissions**: Retrieve Clappia form submissions with optional filtering.
-  **get_clappia_submissions_aggregation**: Aggregate Clappia submission data for analytics.
-  **get_clappia_app_definition**: Retrieve the definition of a Clappia app.
-  **create_clappia_app_submission**: Create a new submission for a Clappia app.
-  **edit_clappia_submission**: Edit an existing submission.
-  **update_clappia_submission_status**: Update the status of a submission.
-  **update_clappia_submission_owners**: Update the owners of a submission.
-  **create_clappia_app**: Create a new Clappia app.
-  **add_field_to_clappia_app**: Add a field to a Clappia app.
-  **update_field_in_clappia_app**: Update a field in a Clappia app.

**Parameters and expected formats for each tool are documented in the code (`clappia-mcp.py`).**

#### Example: Retrieve Submissions (via MCP tool)

You can use the `get_clappia_submissions` tool with parameters like:

```
app_id: "APP123"
requesting_user_email_address: "user@company.com"
page_size: 10
filters: { ... }  # Optional filtering conditions
```

#### Example: Create a Submission (via MCP tool)

```
app_id: "APP123"
data: {"employeeName": "John Doe", "employeeId": "12345"}
requesting_user_email_address: "user@company.com"
```

## API Documentation

### Field Types

-  **Text Fields**
   -  `singleLineText`: Single line text input
   -  `multiLineText`: Multi-line text input
   -  `richTextEditor`: Rich text editor with formatting
-  **Selector Fields**
   -  `singleSelector`: Single choice selection
   -  `multiSelector`: Multiple choice selection
   -  `dropDown`: Dropdown selection
-  **Date/Time Fields**
   -  `dateSelector`: Date selection
   -  `timeSelector`: Time selection
   -  `dateTime`: Combined date and time selection
-  **File Fields**
   -  `file`: File upload with configurable types
   -  `camera`: Direct camera capture
   -  `signature`: Digital signature capture
-  **Advanced Fields**
   -  `calculationsAndLogic`: Formula-based calculations
   -  `gpsLocation`: Location tracking
   -  `codeScanner`: Barcode/QR code scanning
   -  `nfcReader`: NFC tag reading
   -  `liveTracking`: Real-time location tracking
   -  `address`: Address input with validation

### Validation Types

-  `none`: No validation
-  `number`: Numeric validation
-  `email`: Email format validation
-  `url`: URL format validation
-  `custom`: Custom validation rules

### Field Properties

-  **Layout**
   -  `block_width_percentage_desktop`: Width on desktop (25, 50, 75, 100)
   -  `block_width_percentage_mobile`: Width on mobile (50, 100)
   -  `number_of_cols`: Number of columns for selector fields
-  **Behavior**
   -  `required`: Whether field is mandatory
   -  `is_editable`: Whether field can be edited
   -  `hidden`: Whether field is hidden
   -  `retain_values`: Whether to retain values when hidden
-  **Conditions**
   -  `display_condition`: Condition for field visibility
   -  `editability_condition`: Condition for field editability
-  **File Settings**
   -  `allowed_file_types`: List of allowed file types
   -  `max_file_allowed`: Maximum files allowed (1-10)
   -  `image_quality`: Image quality (low, medium, high)
   -  `file_name_prefix`: Prefix for uploaded files

## Error Handling

The server implements comprehensive error handling for:

-  Invalid API credentials
-  Network connectivity issues
-  Invalid input parameters
-  API rate limiting
-  Server errors

All errors are logged with appropriate context for debugging.

## Security

-  API keys are stored in environment variables
-  All API calls are made over HTTPS
-  Input validation is implemented for all parameters
-  Rate limiting is supported
-  Error messages are sanitized

## Performance Considerations

-  Connection pooling for API requests
-  Efficient payload construction
-  Proper resource cleanup
-  Logging optimization
-  Error handling optimization

## Support

For support, please:

1. Check the documentation
2. Review existing issues
3. Create a new issue if needed

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## API Integration

### Clappia Public API

The MCP server integrates with Clappia's public API to provide the following capabilities:

1. **Authentication**:
   -  API key-based authentication
   -  Secure credential management
   -  Rate limiting support
2. **Endpoints**:
   -  Application management
   -  Form submissions
   -  Field operations
   -  User management
   -  Analytics and reporting
3. **API Documentation**:
   -  Visit [Clappia Developer Portal](https://developer.clappia.com/) for:
      -  API reference
      -  Authentication guide
      -  Rate limits
      -  Best practices
      -  Example implementations
4. **API Versioning**:
   -  Current stable version: v1
   -  Backward compatibility maintained
   -  Deprecation notices provided
