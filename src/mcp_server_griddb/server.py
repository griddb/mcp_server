import os
import sys
import logging
from contextlib import closing
from typing import Any

from mcp.server import InitializationOptions
from mcp.server.lowlevel import Server, NotificationOptions
from mcp.server.stdio import stdio_server
import mcp.types as types

import jpype
import jpype.dbapi2

# reconfigure UnicodeEncodeError prone default (i.e. windows-1252) to utf-8
if sys.platform == "win32" and os.environ.get('PYTHONIOENCODING') is None:
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

logger = logging.getLogger('mcp_griddb_server')
logger.info("Starting MCP GridDB Server")

class GridDBDatabase:
    def __init__(self, url: str, user: str, password: str):
        self.url = url
        self.user = user
        self.password = password
        self._init_database()

    def _init_database(self):
        """Initialize connection to the GridDB database"""
        logger.debug("Initializing database connection")
        jpype.startJVM(classpath=["./gridstore-jdbc.jar"])

    def _execute_query(self, query: str, is_description: bool = False) -> list[list]:
        """Execute a SQL query and return results as a list of dictionaries"""
        logger.debug(f"Executing query: {query}")
        try:
            with closing(
                    jpype.dbapi2.connect(
                        self.url,
                        driver="com.toshiba.mwcloud.gs.sql.Driver",
                        driver_args={"user": self.user, "password": self.password}
                    )
                ) as conn:
                with closing(conn.cursor()) as cursor:
                    cursor.execute(query)

                    if is_description:
                        results = cursor.description
                    else:
                        results = cursor.fetchall()
                    logger.debug(f"Read query returned {len(results)} rows")
                    return results
        except Exception as e:
            logger.error(f"Database error executing query: {e}")
            raise

async def main(url: str, user: str, password: str):
    logger.info(f"Starting GridDB MCP Server")

    db = GridDBDatabase(url, user, password)
    server = Server("griddb-manager")

    # Register handlers
    logger.debug("Registering handlers")

    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        """List available tools"""
        return [
            types.Tool(
                name="read_query",
                description="Execute a SELECT query on the GridDB database",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "SELECT SQL query to execute"},
                    },
                    "required": ["query"],
                },
            ),
            types.Tool(
                name="list_tables",
                description="List all tables in the GridDB database",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            ),
            types.Tool(
                name="describe_table",
                description="Get the schema information for a specific table",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "table_name": {"type": "string", "description": "Name of the table to describe"},
                    },
                    "required": ["table_name"],
                },
            ),
        ]

    @server.call_tool()
    async def handle_call_tool(
        name: str, arguments: dict[str, Any] | None
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        """Handle tool execution requests"""
        try:
            if name == "list_tables":
                results = db._execute_query(
                    'SELECT table_name FROM "#tables"'
                )
                return [types.TextContent(type="text", text=str(results))]

            elif name == "describe_table":
                if not arguments or "table_name" not in arguments:
                    raise ValueError("Missing table_name argument")
                sql = "SELECT * FROM " + arguments['table_name'] + " limit 1"
                results = db._execute_query(sql, True)
                return [types.TextContent(type="text", text=str(results))]

            if not arguments:
                raise ValueError("Missing arguments")

            if name == "read_query":
                if not arguments["query"].strip().upper().startswith("SELECT"):
                    raise ValueError("Only SELECT queries are allowed for read_query")
                results = db._execute_query(arguments["query"])
                return [types.TextContent(type="text", text=str(results))]

            else:
                raise ValueError(f"Unknown tool: {name}")

        except Exception as e:
            return [types.TextContent(type="text", text=f"Error: {str(e)}")]

    async with stdio_server() as (read_stream, write_stream):
        logger.info("Server running with stdio transport")
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="griddb",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

class ServerWrapper():
    """A wrapper to compat with mcp[cli]"""
    def run(self):
        import asyncio
        asyncio.run(main("jdbc:gs://127.0.0.1:20001/myCluster", "admin", "admin"))


wrapper = ServerWrapper()
