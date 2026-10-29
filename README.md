# GridDB MCP Server

## Overview
A Model Context Protocol (MCP) server implementation that provides database interaction through GridDB. This server enables running SQL queries.

This software is based on MCP Python SDK v1.  
It has been created based on [SQLite MCP Server](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/sqlite),
which is a sample code of MCP Server.

## Operating environment

Program execution are checked in the environment below.

    OS: Windows, Linux
        (Windows) PowerShell
        (Linux) WSL on Windows, Docker CE
    Python 3.12, uv, OpenJDK 21
    MCP Python SDK v1
    GridDB JDBC Driver: V5.9 CE(Community Edition)
    GridDB Server: V5.9 CE, V6.0 EE(Enterprise Edition)

## Components

### Tools
The server offers three read-only tools.
- read_query
- list_tables
- describe_table

If you use optional tools (write_query, create_table), replace the server.py file in the src/mcp_server_griddb folder with optional/server.py.

#### Query Tools
- `read_query`
   - Execute SELECT queries to read data from the database
   - Input:
     - `query` (string): The SELECT SQL query to execute
   - Returns: Query results as array of objects

- `write_query` (optional)
   - Execute INSERT, UPDATE, or DELETE queries
   - Input:
     - `query` (string): The SQL modification query
   - Returns: `{ affected_rows: number }`

- `create_table` (optional)
   - Create new tables in the database
   - Input:
     - `query` (string): CREATE TABLE SQL statement
   - Returns: Confirmation of table creation

#### Schema Tools
- `list_tables`
   - Get a list of all tables in the database
   - No input required
   - Returns: Array of table names

- `describe_table`
   - View schema information for a specific table
   - Input:
     - `table_name` (string): Name of table to describe
   - Returns: Array of column definitions with names and types


## Usage with VS Code

There are two ways to run the MCP server:  
(A) Use uv to run the MCP server on Windows.  
(B) Use WSL and Docker CE to run the MCP server on Linux.

#### (A) uv

1. Install Python, uv and OpenJDK.
2. Place the source code of this MCP server in your user profile folder. ex. "C:/Users/user1"
3. Add the following JSON block to `mcp.json` file for VS Code. You can do this by pressing `Ctrl + Shift + P` and typing `MCP: Open User Configuration`.

```json
{
  "servers": {
    "griddb": {
      "command": "uv",
      "args": [
        "run",
        "mcp-server-griddb",
        "--url",
        "(GridDB Server connection URL for the GridDB JDBC driver)",
        "--user",
        "(GridDB username)",
        "--password",
        "(password for GridDB username)"
      ],
      "cwd":"(Path to the source code of this MCP server)"
    }
  }
}
```

Example:
```json
{
  "servers": {
    "griddb": {
      "command": "uv",
      "args": [
        "run",
        "mcp-server-griddb",
        "--url",
        "jdbc:gs://192.0.2.0:20001/myCluster",
        "--user",
        "admin",
        "--password",
        "admin"
      ],
      "cwd":"C:/Users/user1/mcp_server"
    }
  }
}

```

4. Start PowerShell, navigate to the folder above (ex. "C:/Users/user1/mcp_server"), and run the following commands:

```
uv sync --frozen --no-install-project --no-dev --no-editable

uv sync --frozen --no-dev --no-editable

curl.exe -L "https://repo1.maven.org/maven2/com/github/griddb/gridstore-jdbc/5.9.0/gridstore-jdbc-5.9.0.jar" -o gridstore-jdbc.jar
```

#### (B) Docker

1. Install WSL and Docker CE.
2. Add the following JSON block to `mcp.json` file for VS Code. You can do this by pressing `Ctrl + Shift + P` and typing `MCP: Open User Configuration`.

```json
{
  "servers": {
    "griddb": {
      "command": "wsl",
      "args": [
        "docker",
        "run",
        "-i",
        "--rm",
        "--network=host",
        "-v",
        "mcp-griddb:/mcp",
        "mcp/griddb",
        "--url",
        "(GridDB Server connection URL for the GridDB JDBC driver)",
        "--user",
        "(GridDB username)",
        "--password",
        "(password for GridDB username)"
      ]
    }
  }
}
```
        
Example:
```json
{
  "servers": {
    "griddb": {
      "command": "wsl",
      "args": [
        "docker",
        "run",
        "-i",
        "--rm",
        "--network=host",
        "-v",
        "mcp-griddb:/mcp",
        "mcp/griddb",
        "--url",
        "jdbc:gs://127.0.0.1:20001/myCluster",
        "--user",
        "admin",
        "--password",
        "admin"
      ]
    }
  }
}
```

3. Place the source code of this MCP server in a folder on WSL. ex. "\\wsl.localhost\Ubuntu\home\user1"
4. Start WSL, navigate to the folder above (ex. /home/user1/mcp_server), and build the Docker image by running the following command:

```bash
docker build -t mcp/griddb .
```

Note: To disable the MCP server configuration in VS Code, delete the JSON block you added to the mcp.json file.

## Community
  * Issues  
    Use the GitHub issue function if you have any requests, questions, or bug reports. 
  * PullRequest  
    Use the GitHub pull request function if you want to contribute code.
    You'll need to agree GridDB Contributor License Agreement(CLA_rev1.1.pdf).
    By using the GitHub pull request function, you shall be deemed to have agreed to GridDB Contributor License Agreement.

## License

This MCP server is licensed under the MIT License. This means you are free to use, modify, and distribute the software, subject to the terms and conditions of the MIT License. For more details, please see the LICENSE file in the project repository.

# Trademarks

All other company names or product names may be trademarks of their respective companies.
