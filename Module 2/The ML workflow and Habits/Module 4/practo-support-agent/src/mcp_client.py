from src.mcp_server import MCPServer

class MCPClient:
    """Model Context Protocol (MCP) Client invoking remote server tools."""
    
    def __init__(self, server: MCPServer):
        self.server = server

    def execute_remote_tool(self, tool_name: str, arguments: dict):
        return self.server.call_tool(tool_name, arguments)