# Clappia MCP

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)
[![smithery badge](https://smithery.ai/badge/@clappia-dev/simitry-clappia-mcp)](https://smithery.ai/server/@clappia-dev/simitry-clappia-mcp)

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

-  **Docker Desktop** (with Docker CLI)
-  **Clappia API Key** and Workplace ID
-  **Claude for Desktop**

## Steps to Setup MCP Server

### Installing via Smithery

To install Clappia automatically via [Smithery](https://smithery.ai/server/@clappia-dev/simitry-clappia-mcp):

```bash
npx -y @smithery/cli install @clappia-dev/simitry-clappia-mcp
```

### 1. Install Prerequisites

**Install Homebrew (if not already installed):**
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Install Docker CLI:**
```bash
brew install docker
```

**Download and install:**
-  Docker Desktop: `https://www.docker.com/products/docker-desktop/`
-  Claude Desktop: `https://claude.ai/download`

**Configure Docker Desktop:**
-  Install Docker Desktop and configure it to run in the background
-  Ensure Docker is running before proceeding

### 2. Get Clappia API Key

```bash
# Visit your Clappia workplace
open https://<your_workplace>.clappia.com

# Go to: Workplace Settings → Preferences → API Keys
# Copy your API key
```

**Direct links:**

-  Clappia Platform: `https://www.clappia.com`
-  Your Workplace: `https://<your_workplace>.clappia.com`

### 3. Configure Claude Desktop

**Open Claude Desktop:**
1.  Open Claude Desktop
2.  Go to Settings
3.  Select Developer option → Edit Config → Click on Edit
4.  Replace the content with the configuration below

```json
{
  "mcpServers": {
    "clappia-app-form-mcp": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "-e", "CLAPPIA_API_KEY=your_api_key",
        "okaru413/clappia-mcp-form:1.0.0"
      ]
    },
    "clappia-app-workflow-mcp": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "-e", "CLAPPIA_API_KEY=your_api_key",
        "okaru413/clappia-mcp-workflow:1.0.0"
      ]
    },
    "clappia-app-charts-mcp": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "-e", "CLAPPIA_API_KEY=your_api_key",
        "okaru413/clappia-mcp-charts:1.0.0"
      ]
    },
    "clappia-app-submission-mcp": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "-e", "CLAPPIA_API_KEY=your_api_key",
        "okaru413/clappia-mcp-submission:1.0.0"
      ]
    },
    "clappia-workplace-mcp": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "-e", "CLAPPIA_API_KEY=your_api_key",
        "okaru413/clappia-mcp-workplace:1.0.0"
      ]
    }
  }
}
```

**Important:** 
-  Replace `your_api_key` with your actual Clappia API key
-  After making changes, **close Claude Desktop completely** and reopen it
-  If servers don't appear, close and reopen Claude Desktop again

### 4. Start Using

```bash
# Look for tools icon (🔧) in Claude Desktop input box
# Start managing your Clappia apps with Docker containers!
```

## 📁 Project Structure

```
clappia-mcp/
├── main_server.py         # 🎯 Main MCP server with module selection
├── server/                # 🖥️ Specialized MCP servers
│   ├── submissions_server.py  # 📝 Submissions-focused MCP server
│   ├── definitions_server.py  # 📱 App definitions-focused MCP server
│   ├── workflows_server.py    # 🔄 Workflows-focused MCP server
│   ├── analytics_server.py   # 📊 Analytics-focused MCP server
│   └── workplace_server.py    # 👥 Workplace management-focused MCP server
├── docker/                # 🐳 Docker configuration files
│   ├── Dockerfile.form        # Form server Docker configuration
│   ├── Dockerfile.workflow    # Workflow server Docker configuration
│   ├── Dockerfile.submission  # Submission server Docker configuration
│   ├── Dockerfile.workplace   # Workplace server Docker configuration
│   └── Dockerfile.charts      # Charts server Docker configuration
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
| **Server Not Starting**     | No tools icon in Claude Desktop | Check Docker Desktop is running, verify Docker CLI installation, restart Claude Desktop |
| **Docker Issues**          | Docker command not found        | Install Docker CLI via Homebrew, ensure Docker Desktop is running                    |
| **API Connection Issues**   | Authentication errors           | Verify API key, check workplace permissions, test network connectivity               |
| **Tool Execution Failures** | Tools return errors             | Check input parameters, validate data types, verify app ID format                    |
| **Configuration Issues**    | Tools don't work as expected    | Verify JSON syntax, restart Claude Desktop completely, check Docker container logs   |
| **Performance Issues**      | Slow response times             | Check API status, reduce page size, optimize filters                                 |

### Quick Fixes

-  **Docker status**: `docker --version` and `docker ps` (ensure Docker is running)
-  **Restart Docker**: Restart Docker Desktop if containers fail to start
-  **Check logs**: Look in Claude Desktop console for errors
-  **Verify API key**: Ensure it's correct and has proper permissions
-  **Restart Claude**: Close Claude Desktop completely and reopen after configuration changes

## 📞 Support

### Getting Help

-  📖 **Documentation**: Check this README and inline code documentation
-  🐛 **Issues**: Search existing issues or create a new one
-  💬 **Discussions**: Use GitHub Discussions for questions and ideas
-  📧 **Contact**: Reach out to the maintainers for urgent issues

### Reporting Issues

When reporting issues, please include:

-  Docker version (`docker --version`)
-  Docker Desktop version and status
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
