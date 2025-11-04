# Clappia MCP Server

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)

MCP server for managing [Clappia](https://www.clappia.com) applications through Claude Desktop. Build apps, manage data, configure workflows, and analyze submissions using natural language.

## Features

**App Management** - Create and configure applications, manage 30+ field types, organize sections and layouts

**Submissions** - Create, update, and query submissions with filtering, pagination, and Excel export

**Workflows** - Configure multi-step workflows with automated actions and notifications

**Analytics** - Build dashboards with multiple chart types for data visualization

**User Management** - Manage workplace users, roles, groups, and app-level permissions

**Authentication** - Secure API key authentication with token management

## Prerequisites

- **macOS**: Homebrew and MCP Proxy (`brew install mcp-proxy`)
- **Windows**: Node.js 20+ ([download](https://nodejs.org/))
- **All Platforms**: Claude Desktop ([download](https://claude.ai/download)) and Clappia API key

> A paid Claude account is recommended for production use due to higher token consumption.

## Setup

### 1. Install Prerequisites

**macOS:**
```bash
brew install mcp-proxy
```

**Windows:**
Download and install Node.js 20+ from [nodejs.org](https://nodejs.org/)

### 2. Get API Key

1. Navigate to `https://<your_workplace>.clappia.com`
2. Go to **Workplace Settings** → **Preferences** → **API Keys**
3. Copy your API key

### 3. Configure Claude Desktop

1. Open Claude Desktop → **Settings** → **Developer** → **Edit Config**
2. Add the configuration below
3. Replace `your_api_key` with your actual key
4. Save and completely restart Claude Desktop

**macOS Configuration:**
```json
{
  "mcpServers": {
    "clappia-mcp": {
      "command": "mcp-proxy",
      "args": [
        "--headers",
        "X-API-Key",
        "your_api_key",
        "https://mcp.clappia.com/sse"
      ]
    }
  }
}
```

**Windows Configuration:**
```json
{
  "mcpServers": {
    "clappia-mcp": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.clappia.com/sse",
        "--header",
        "X-API-Key:your_api_key"
      ]
    }
  }
}
```

### 4. Enable Tools

After restarting Claude Desktop, go to **Search & Tools** and enable Clappia MCP tools.

## Usage

Example prompts:

```
Create an Employee Management app for hr@company.com with Name, Department, and Joining Date fields

[APP_ID] Add a Number field for employee ID with validation

[APP_ID] Create a workflow to send email notifications on new submissions
```

> When working with existing apps, prefix requests with the App ID (found in the app URL or Clappia's right panel).

## Project Structure

```
clappia-mcp/
├── http_server.py          # HTTP/SSE server (JWT auth, OAuth2)
├── mcp_server.py           # MCP server (stdio transport)
├── Dockerfile.http         # HTTP server container
├── Dockerfile.mcp          # MCP server container
├── pyproject.toml          # Dependencies
└── src/
    ├── tools/              # Tool implementations
    │   ├── submissions.py
    │   ├── definitions.py
    │   ├── workflows.py
    │   ├── analytics.py
    │   ├── workplace.py
    │   └── auth.py
    └── utils/              # Utilities
        ├── constants.py
        ├── context.py
        ├── jwt_utils.py
        └── logging_utils.py
```

## Troubleshooting

**Tools not appearing**
- Verify MCP Proxy (macOS) or Node.js 20+ (Windows) is installed
- Check API key is correct with no extra spaces
- Completely quit and restart Claude Desktop (may need to do twice)

**Connection errors**
- Verify API key validity and permissions
- Check network connectivity
- Review JSON configuration syntax

**Tool execution failures**
- Verify all required parameters
- Ensure correct App ID format
- Check error messages for specific guidance

**Slow performance**
- Reduce pagination page sizes
- Optimize data filters
- Consider upgrading Claude account

For detailed troubleshooting, see the [official setup guide](https://www.clappia.com/help/clappia-mcp-setup).

## Development

```bash
# Clone repository
git clone https://github.com/clappia/clappia-mcp.git
cd clappia-mcp

# Install dependencies
uv sync

# Run servers
python mcp_server.py    # MCP server
python http_server.py   # HTTP/SSE server
```

## Support

- [Documentation](https://www.clappia.com/help/clappia-mcp-setup)
- [GitHub Issues](https://github.com/clappia/clappia-mcp/issues)
- [API Reference](https://www.clappia.com/help/api-reference)

## License

MIT License - see [LICENSE](LICENSE) file for details.