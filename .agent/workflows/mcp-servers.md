---
description: Setup and verify MCP servers for the Groundswell project, specifically for Database and Filesystem access.
---

# Groundswell MCP Server Setup

This workflow guides you through setting up the Model Context Protocol (MCP) servers required for the Groundswell execution intelligence platform.

## Prerequisites
- Node.js & npm installed
- Python & `uv` installed
- Supabase project credentials

## 1. Filesystem Server
Most MCP clients come with a filesystem server built-in or pre-configured.
- [ ] Verify you have read/write access to the `groundswell` directory.
- [ ] Ensure `.env` files are accessible but `node_modules` are excluded if possible to reduce noise.

## 2. PostgreSQL Server (for Supabase)
We use the PostgreSQL MCP server to interact with the Supabase database directly from the agent context.

### Configuration
Add the following to your MCP client configuration (e.g., `claude_config.json`):

```json
{
  "mcpServers": {
    "postgres": {
      "command": "uvx",
      "args": [
        "mcp-server-postgres",
        "--connection-string",
        "postgresql://postgres:[YOUR_PASSWORD]@db.[YOUR_PROJECT_REF].supabase.co:5432/postgres"
      ]
    }
  }
}
```

### Verification
// turbo
1. Test the connection by listing tables in the database (once configured).
   - Use a tool/command like: `list_tables` (if available via the MCP server) or simply query the existence of tables.

## 3. Brave Search Server (Optional)
For gathering market signals and competitor analysis.

```json
{
  "mcpServers": {
    "brave-search": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-brave-search"
      ],
      "env": {
        "BRAVE_API_KEY": "[YOUR_API_KEY]"
      }
    }
  }
}
```

## 4. Verification Step
Run a quick check to ensure environment variables are loaded.

```bash
echo "Checking for .env file..."
ls -la backend/.env
```
