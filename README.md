# Clappia MCP (Model Context Protocol)

A Python-based MCP server that provides a comprehensive interface for interacting with the Clappia platform. This server enables programmatic management of Clappia applications, forms, submissions, and more.

Clappia is a no-code platform that allows businesses, operations teams, and non-developers to create custom apps—like inspection forms, approval workflows, field data collection tools, internal dashboards, and more—without writing a single line of code. It's used across industries for automating manual processes, digitizing paperwork, and improving operational efficiency. [Click here](https://www.clappia.com) to learn more.

## Features

-  **App Management**

   -  Create new Clappia apps with customizable sections and fields

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
   -  Configure field validations (number, email, URL, custom)
   -  Set up conditional logic for field display and editability
   -  Manage field layouts with responsive design options

## Prerequisites

-  Python 3.8 or higher
-  uv python package manager
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
                  "/Users/<YOUR_DIECTORY>/<PATH_OF_THE_MCP_FOLDER>",
                  "run",
                  "server.py"
               ],
               "env": {
                  "CLAPPIA_API_KEY": "<ENTER_YOUR_WORKPLACE_API_KEY_HERE>"
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
├── server.py              # Legacy main MCP server (all tools)
├── main_server.py         # New main server with module selection
├── submissions_server.py  # Submissions-focused MCP server
├── definitions_server.py  # App definitions-focused MCP server
├── workflows_server.py    # Workflows-focused MCP server
├── analytics_server.py    # Analytics-focused MCP server
├── workplace_server.py    # Workplace management-focused MCP server
├── test_servers.py        # Test script for all servers
├── tools/                 # Core functionality modules
│   ├── submissions.py     # Submission management tools
│   ├── definitions.py     # App definition tools
│   ├── workflows.py       # Workflow management tools
│   ├── analytics.py       # Analytics and chart tools
│   └── workplace.py       # Workplace user management tools
├── utils/                 # Utility modules
│   ├── clients.py         # API client configurations
│   └── logging_utils.py   # Logging utilities
├── pyproject.toml         # Project metadata and dependencies
├── uv.lock               # Dependency lock file (if using uv)
└── .env                  # Environment variables
```

## Running Different MCP Servers

You can now run different MCP servers based on your specific needs:

### 1. All-in-One Server (Legacy)

```bash
# Run all tools in one server
uv run server.py
```

### 2. Main Server with Module Selection

```bash
# Run all modules
uv run main_server.py

# Run specific modules only
uv run main_server.py --modules submissions definitions

# List available tools
uv run main_server.py --list-tools
```

### 3. Specialized Servers

```bash
# Submissions-focused server
uv run submissions_server.py

# App definitions-focused server
uv run definitions_server.py

# Workflows-focused server
uv run workflows_server.py

# Analytics-focused server
uv run analytics_server.py

# Workplace management-focused server
uv run workplace_server.py
```

### Claude Desktop Configuration

Update your `claude_desktop_config.json` to use any of these servers:

```json
{
   "mcpServers": {
      "clappia-submissions": {
         "command": "uv",
         "args": [
            "--directory",
            "/path/to/clappia-mcp",
            "run",
            "submissions_server.py"
         ],
         "env": {
            "CLAPPIA_API_KEY": "your_api_key_here"
         }
      },
      "clappia-definitions": {
         "command": "uv",
         "args": [
            "--directory",
            "/path/to/clappia-mcp",
            "run",
            "definitions_server.py"
         ],
         "env": {
            "CLAPPIA_API_KEY": "your_api_key_here"
         }
      }
   }
}
```

### Testing Servers

You can test all servers to ensure they're working correctly:

```bash
# Test all servers
uv run test_servers.py

# Or run directly
./test_servers.py
```

This will verify that each server can be imported and tools can be registered successfully.

### Usage

-  The server will automatically start when Claude Desktop launches
-  Access tools through the Claude Desktop interface
-  Each specialized server provides focused functionality for specific use cases

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

### Example API Calls

1. **Create a New Application**

   ```python
   from tools.create_app import create_app, Section, Field

   result = create_app(
       name="Employee Survey",
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
       app_id="APP123",
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
