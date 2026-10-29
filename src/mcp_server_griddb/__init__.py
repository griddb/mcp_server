from . import server
import asyncio
import argparse


def main():
    """Main entry point for the package."""
    parser = argparse.ArgumentParser(description='GridDB MCP Server')
    parser.add_argument('--url', 
                       default="jdbc:gs://127.0.0.1:20001/myCluster",
                       help='Url for JDBC Connection')
    parser.add_argument('--user', 
                       default="admin",
                       help='Username for JDBC Connection')
    parser.add_argument('--password', 
                       default="admin",
                       help='Password for JDBC Connection')

    args = parser.parse_args()
    asyncio.run(server.main(args.url, args.user, args.password))


# Optionally expose other important items at package level
__all__ = ["main", "server"]
