# **Tuba Workflow MCP Server**

This project is a Model Context Protocol (MCP) server that acts as a bridge to the [Tuba.ai](https://tuba.ai/) platform.

Tuba is an all-in-one AI vision workflow builder that streamlines the entire lifecycle of computer vision tasks. This server exposes your Tuba project's workflow as a set of callable tools, allowing other applications (like AI assistants, scripts, or services like Claude Desktop) to programmatically control and interact with your AI vision pipelines.

## **Table of Contents**

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Configuration](#configuration)
  - [Local Development & Testing](#local-development--testing)
  - [Claude Desktop Configuration](#claude-desktop-configuration)
- [Available Tools](#available-tools)
- [Usage Examples](#usage-examples)
- [Contributing](#contributing)
- [License](#license)
- [Security](#security)

## **Features**

This MCP server provides the following tools to interact with the Tuba Workflow API:

| Tool                              | Description                                                         |
| --------------------------------- | ------------------------------------------------------------------- |
| **run()**                         | Executes the workflow for your project                              |
| **status()**                      | Retrieves the current workflow execution status                     |
| **result()**                      | Fetches workflow results (downloads as `result.zip` if file output) |
| **get_workflow_blocks()**         | Retrieves the current configuration of all workflow blocks          |
| **update_workflow_blocks_data()** | Updates parameters and uploads files to workflow blocks             |

## **Getting Started**

### **Prerequisites**

- **Python 3.10 or higher** - Required for modern type hints and async features
- **[uv](https://github.com/astral-sh/uv)** - Fast Python package installer and environment manager
- **A Tuba.ai account** with an active project
- **TUBA_WORKFLOW_ACCESS_TOKEN** - Your project's API access token

### **Installation**

1. **Clone the repository:**

   ```bash
   git clone <this_repo>
   cd <this_repo>
   ```

2. **Install uv:**

   - **macOS/Linux:**

     ```bash
     curl -LsSf https://astral.sh/uv/install.sh | sh
     ```

   - **Windows:**
     ```powershell
     powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
     ```

3. **Create a virtual environment and install dependencies:**
   ```bash
   uv venv
   uv pip install -r requirements-lock.txt
   ```

## **Configuration**

### **Local Development & Testing**

For local development, the server loads your access token from an environment file using `python-dotenv`.

1. **Create a `.env` file** in the project root:

   ```bash
   touch .env
   ```

2. **Add your access token:**

   ```env
   TUBA_WORKFLOW_ACCESS_TOKEN="your_secret_token_goes_here"
   ```

   > **Note:** The `.gitignore` file ensures this file is never committed to version control.

3. **Test the server:**

   ```bash
   uv run python tuba_workflow_mcp_server.py
   ```

4. **Verify it's working:**
   The server should start without errors. You can test it by connecting an MCP client or using the tools through Claude Desktop.

### **Claude Desktop Configuration**

To use this server with Claude Desktop, add the following configuration to your `claude_desktop_config.json` file:

**macOS/Linux Location:**

```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows Location:**

```
%APPDATA%\Claude\claude_desktop_config.json
```

**Configuration:**

```json
{
  "mcpServers": {
    "TubaWorkflow": {
      "command": "<home_path>/.local/bin/uv",
      "args": [
        "run",
        "--directory",
        "<absolute_path_to_tuba_workflow_mcp_server_folder>",
        "python",
        "tuba_workflow_mcp_server.py"
      ],
      "env": {
        "TUBA_WORKFLOW_ACCESS_TOKEN": "<your_access_token>"
      }
    }
  }
}
```

**Replace the placeholders:**

- `<home_path>` - Your home directory path (e.g., `/Users/yourname` or `C:\Users\yourname`)
- `<absolute_path_to_tuba_workflow_mcp_server_folder>` - Full path to this project folder
- `<your_access_token>` - Your Tuba.ai workflow access token

**Example (macOS):**

```json
{
  "mcpServers": {
    "TubaWorkflow": {
      "command": "/Users/john/.local/bin/uv",
      "args": [
        "run",
        "--directory",
        "/Users/john/projects/tuba-workflow-mcp-server",
        "python",
        "tuba_workflow_mcp_server.py"
      ],
      "env": {
        "TUBA_WORKFLOW_ACCESS_TOKEN": "<your_access_token>"
      }
    }
  }
}
```

After configuration, restart Claude Desktop to load the MCP server.

## **Available Tools**

### **run()**

Executes the workflow for your authenticated project.

---

### **status()**

Retrieves the current status of the workflow execution.

---

### **result()**

Fetches the results of the workflow execution. If the result is a file (e.g., processed images, videos), it will be automatically saved as `result.zip` in your current working directory.

---

### **get_workflow_blocks()**

Retrieves the current configuration of all workflow blocks in your project. Use this to discover available block IDs and their current parameter values.

---

### **update_workflow_blocks_data()**

Updates parameters and uploads files to workflow blocks. Supports three file upload methods:

- **Local files** - Upload from file paths on your system
- **Remote URLs** - Fetch and upload files from web URLs
- **Base64 data** - Upload files encoded as base64 strings

**File Field Naming Convention:**
File field names should follow this format: `<block_id>_<param_name>`

## **Usage Examples**

Once configured with Claude Desktop (or another MCP client), you can interact with your Tuba workflow using natural language. The AI assistant will handle all the technical details like finding block IDs, formatting JSON correctly, handling file paths, and monitoring workflow progress.

**Example conversations:**

- "Can you check the status of my Tuba workflow?"
- "Start my workflow and let me know when it's done"
- "Update the confidence threshold to 0.8 for my object detector"
- "Process this image with my workflow: /path/to/image.jpg"
- "Upload these three images from URLs and run the workflow"
- "Show me my workflow configuration"

## **Contributing**

We welcome contributions! Please see our [Code of Conduct](CODE_OF_CONDUCT.md) for community guidelines.

**Before contributing:**

1. Check existing issues and pull requests
2. Follow the existing code style
3. Add tests for new features
4. Update documentation as needed

For major changes, please open an issue first to discuss what you would like to change.

## **License**

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## **Security**

Security is a top priority. If you discover a vulnerability, please report it responsibly.

**Do not open public GitHub issues for security vulnerabilities.**

Instead, use GitHub's private vulnerability reporting feature:

1. Navigate to the **Security** tab
2. Click **Report a Vulnerability**
3. Provide detailed information about the issue

See [SECURITY.md](SECURITY.md) for more information.

---

## **Resources**

- [Tuba.ai Platform](https://tuba.ai/)
- [Model Context Protocol (MCP) Specification](https://modelcontextprotocol.io/)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)

## **Support**

For questions, issues, or feedback:

- **Tuba.ai Support:** support@tuba.ai
- **Join Discord Community** https://discord.com/invite/gDSZr6N5rC
- **GitHub Issues:** Use for bug reports and feature requests
- **Discussions:** Use GitHub Discussions for questions and community interaction

---

**Copyright © 2025 DevisionX. All rights reserved.**
