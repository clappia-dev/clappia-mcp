# Clappia MCP (Model Context Protocol)

A Python-based MCP server that provides a comprehensive interface for interacting with the Clappia platform. This server enables programmatic management of Clappia applications, forms, submissions, and more.

## Features

-  **Application Management**

   -  Create new Clappia applications with customizable sections and fields
   -  Add new fields to existing applications with advanced configuration options
   -  Update field properties and configurations
   -  Retrieve detailed application definitions with field metadata

-  **Submission Management**

   -  Create new form submissions with field data
   -  Edit existing submissions with validation
   -  Update submission status with optional comments
   -  Manage submission owners with email-based assignments
   -  Retrieve submissions with advanced filtering and pagination
   -  Get submission aggregations for analytics with customizable dimensions

-  **Field Management**
   -  Add new fields with comprehensive configuration options
   -  Update field properties including validation, display conditions, and layout
   -  Configure field validations (number, email, URL, custom)
   -  Set up conditional logic for field display and editability
   -  Manage field layouts with responsive design options

## Prerequisites

-  Python 3.8 or higher
-  uv python package manager
-  Access to Clappia API credentials
-  Claude for Desktop (for local development and testing)
-  Node.js (for running MCP servers)

## Installation

1. **Set up Claude for Desktop**:

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
                  "/Users/rishabhverma/Desktop/clappia-mcp",
                  "run",
                  "clappia-mcp.py"
               ]
            }
         }
      }
      ```
   -  Restart Claude for Desktop
   -  Verify the MCP server is running by checking for the tools icon in the input box

2. **Set up Clappia API Access**:

   -  Visit [Clappia Developer Portal](https://developer.clappia.com/)
   -  Create an account or sign in
   -  Generate API credentials
   -  Note your API key and base URL

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

5. **Set up environment variables**:
   Create a `.env` file in the root directory with the following variables:
   ```
   DEV_API_KEY=your_api_key_here
   CLAPPIA_EXTERNAL_API_BASE_URL=your_api_base_url_here
   ```

## Project Structure

```
clappia-mcp/
├── clappia-mcp.py          # Main MCP server implementation
├── tools/                  # Core functionality modules
│   ├── add_field.py        # Field addition functionality
│   ├── create_app.py       # App creation functionality
│   ├── create_submission.py # Submission creation
│   ├── edit_submission.py  # Submission editing
│   ├── get_definition.py   # App definition retrieval
│   ├── get_submissions.py  # Submission retrieval
│   ├── get_submissions_aggregation.py # Analytics functionality
│   ├── update_field.py     # Field update functionality
│   ├── update_submission_owners.py # Owner management
│   └── update_submission_status.py # Status management
├── pyproject.toml         # Project metadata and dependencies
├── uv.lock               # Dependency lock file (if using uv)
└── .env                  # Environment variables
```

### Usage

-  The server will automatically start when Claude Desktop launches
-  Access tools through the Claude Desktop interface

### Troubleshooting

1. **Server Not Starting**:

   -  Check Claude Desktop logs for errors
   -  Verify Python environment is activated
   -  Ensure all dependencies are installed
   -  Check environment variables are set correctly

2. **API Connection Issues**:

   -  Verify API credentials in `.env` file
   -  Check network connectivity
   -  Validate API base URL format
   -  Review API rate limits

3. **Tool Execution Failures**:
   -  Check server logs for detailed error messages
   -  Verify input parameters match API requirements
   -  Ensure proper permissions for API operations

### Example API Calls

1. **Create a New Application**

   ```python
   from tools.create_app import create_app, Section, Field

   result = create_app(
       workplace_id="ON83542",
       app_name="Employee Survey",
       requesting_user_email_address="user@company.com",
       sections=[
           Section(
               sectionName="Personal Information",
               fields=[
                   Field(
                       fieldType="singleLineText",
                       label="Full Name",
                       required=True
                   )
               ]
           )
       ]
   )
   ```

2. **Add a Field to an Application**

   ```python
   from tools.add_field import add_field_to_app

   result = add_field_to_app(
       app_id="APP123",
       workplace_id="ON83542",
       requesting_user_email_address="user@company.com",
       section_index=0,
       field_index=1,
       field_type="singleLineText",
       label="Employee ID",
       required=True,
       validation="number",
       block_width_percentage_desktop=50,
       block_width_percentage_mobile=100
   )
   ```

3. **Update a Field**

   ```python
   from tools.update_field import update_field_in_app

   result = update_field_in_app(
       app_id="APP123",
       workplace_id="ON83542",
       requesting_user_email_address="user@company.com",
       field_name="employeeName",
       label="Full Employee Name",
       required=True,
       validation="none",
       display_condition="status == 'active'"
   )
   ```

4. **Create a Submission**

   ```python
   from tools.create_submission import create_app_submission

   result = create_app_submission(
       app_id="APP123",
       workplace_id="ON83542",
       data={"employeeName": "John Doe", "employeeId": "12345"},
       email="user@company.com"
   )
   ```

5. **Get Submissions with Filtering**

   ```python
   from tools.get_submissions import get_app_submissions, Filters, QueryGroup, Query, Condition

   filters = Filters(queries=[
       QueryGroup(queries=[
           Query(
               conditions=[
                   Condition(
                       operator="EQ",
                       filterKeyType="STANDARD",
                       key="status",
                       value="active"
                   )
               ],
               operator="AND"
           )
       ])
   ])

   result = get_app_submissions(
       workplace_id="ON83542",
       app_id="APP123",
       requesting_user_email_address="user@company.com",
       page_size=10,
       filters=filters
   )
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
