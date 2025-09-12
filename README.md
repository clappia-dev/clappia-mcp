# Clappia MCP

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)

MCP server for Clappia platform integration. Manage applications, submissions, workflows, and analytics through Claude Desktop.

[Clappia](https://www.clappia.com) is a no-code platform for building custom business applications.

## Table of Contents

-  [Features](#features)
-  [Prerequisites](#prerequisites)
-  [Steps to Setup MCP Server](#steps-to-setup-mcp-server)
-  [Project Structure](#project-structure)
-  [Troubleshooting](#troubleshooting)
-  [Support](#support)
-  [License](#license)

## Features

### App Management

-  Create new Clappia applications
-  Get app definitions and metadata
-  Update app metadata and versions
-  Manage app sections and page breaks

### Field Management

-  Add and update fields (30+ field types supported)
-  Reorder sections and fields
-  Configure field properties and validation

### Submission Management

-  Create and edit submissions
-  Update submission status and owners
-  Get submissions with filtering and pagination
-  Export submissions to Excel
-  Get submission aggregations for analytics

### Workflow Management

-  Get app workflow configurations
-  Add, update, and reorder workflow steps
-  Support for various workflow step types

### Analytics

-  Add, update, and reorder charts
-  Get app charts for analytics dashboard

### Workplace Management

-  Add users to workplace
-  Update user details, attributes, roles, and groups
-  Add users to specific apps
-  Get workplace apps and users

## Prerequisites

-  **Python 3.10+**
-  **Clappia API Key** and Workplace ID
-  **Claude for Desktop**

## Steps to Setup MCP Server

### 1. Install Prerequisites

**Download and install:**

-  Python 3.10+: `https://www.python.org/downloads/`
-  Claude Desktop: `https://claude.ai/download`
-  uv: `https://docs.astral.sh/uv/getting-started/installation/`
-  Git: `https://git-scm.com/downloads`
-  VS Code: `https://code.visualstudio.com/download`
-  Cursor: `https://cursor.com/downloads`

### 2. Clone and Setup

```bash
# Clone repository to desktop
git clone https://github.com/clappia-dev/clappia-mcp
cd clappia-mcp

# Setup Python environment
uv venv
uv sync

# Activate virtual environment
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows
```

### 3. Get Clappia API Key

```bash
# Visit your Clappia workplace
open https://<your_workplace>.clappia.com

# Go to: Workplace Settings → Preferences → API Keys
# Copy your API key
```

**Direct links:**

-  Clappia Platform: `https://www.clappia.com`
-  Your Workplace: `https://<your_workplace>.clappia.com`

### 4. Configure Claude Desktop

```json
// Open Claude → Settings → Developer → Edit Config
// Add this to claude_desktop_config.json:
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
      },
      "clappia-workflows": {
         "command": "uv",
         "args": [
            "--directory",
            "/path/to/clappia-mcp",
            "run",
            "workflows_server.py"
         ],
         "env": {
            "CLAPPIA_API_KEY": "your_api_key_here"
         }
      },
      "clappia-analytics": {
         "command": "uv",
         "args": [
            "--directory",
            "/path/to/clappia-mcp",
            "run",
            "analytics_server.py"
         ],
         "env": {
            "CLAPPIA_API_KEY": "your_api_key_here"
         }
      },
      "clappia-workplace": {
         "command": "uv",
         "args": [
            "--directory",
            "/path/to/clappia-mcp",
            "run",
            "workplace_server.py"
         ],
         "env": {
            "CLAPPIA_API_KEY": "your_api_key_here"
         }
      }
   }
}
```

**Enable/Disable Servers:**

-  To enable/disable a server:Use Claude Desktop's interface after server is running
-  To enable/disable tools: Use Claude Desktop's interface after server is running

### 5. Start Using

```bash
# Restart Claude Desktop
# Look for tools icon (🔧) in input box
# Start managing your Clappia apps!
```

## 📁 Project Structure

```
clappia-mcp/
├── main_server.py         # 🎯 Main MCP server with module selection
├── submissions_server.py  # 📝 Submissions-focused MCP server
├── definitions_server.py  # 📱 App definitions-focused MCP server
├── workflows_server.py    # 🔄 Workflows-focused MCP server
├── analytics_server.py    # 📊 Analytics-focused MCP server
├── workplace_server.py    # 👥 Workplace management-focused MCP server
├── tools/                 # 🛠️ Core functionality modules
│   ├── submissions.py     # Submission management tools
│   ├── definitions.py     # App definition and field management tools
│   ├── workflows.py       # Workflow step management tools
│   ├── analytics.py       # Analytics and chart generation tools
│   └── workplace.py       # Workplace user management tools
├── utils/                 # 🔧 Utility modules
│   ├── __init__.py        # Package initialization
│   ├── clients.py         # API client configurations and setup
│   └── logging_utils.py   # Logging utilities and configuration
├── pyproject.toml         # 📦 Project metadata and dependencies
├── uv.lock               # 🔒 Dependency lock file
└── README.md             # 📖 This documentation
```

### Server Architecture

-  **`main_server.py`**: Primary server that can run all modules or specific subsets
-  **Specialized Servers**: Focused servers for specific use cases (submissions, definitions, etc.)
-  **`tools/`**: Modular tool implementations using Pydantic models
-  **`utils/`**: Shared utilities for logging, API clients, and common functionality

## Troubleshooting

| Issue                       | Symptoms                        | Solution                                                                             |
| --------------------------- | ------------------------------- | ------------------------------------------------------------------------------------ |
| **Server Not Starting**     | No tools icon in Claude Desktop | Check Python 3.10+, verify uv installation, reinstall dependencies, check file paths |
| **API Connection Issues**   | Authentication errors           | Verify API key, check workplace permissions, test network connectivity               |
| **Tool Execution Failures** | Tools return errors             | Check input parameters, validate data types, verify app ID format                    |
| **Configuration Issues**    | Tools don't work as expected    | Verify environment variables, check JSON syntax, restart Claude Desktop              |
| **Performance Issues**      | Slow response times             | Check API status, reduce page size, optimize filters                                 |

### Quick Fixes

-  **Python version**: `python --version` (need 3.10+)
-  **Reinstall dependencies**: `rm -rf .venv uv.lock && uv sync`
-  **Check logs**: Look in Claude Desktop console for errors
-  **Verify API key**: Ensure it's correct and has proper permissions

## 📞 Support

### Getting Help

-  📖 **Documentation**: Check this README and inline code documentation
-  🐛 **Issues**: Search existing issues or create a new one
-  💬 **Discussions**: Use GitHub Discussions for questions and ideas
-  📧 **Contact**: Reach out to the maintainers for urgent issues

### Reporting Issues

When reporting issues, please include:

-  Python version (`python --version`)
-  uv version (`uv --version`)
-  Operating system
-  Steps to reproduce the issue
-  Expected vs actual behavior
-  Error messages (without sensitive information)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

-  **Clappia Team**: For providing the excellent no-code platform and API
-  **Anthropic**: For creating the Model Context Protocol
-  **Contributors**: Thank you to all contributors who help improve this project
