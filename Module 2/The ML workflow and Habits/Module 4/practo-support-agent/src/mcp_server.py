from src.tools import AgentTools

class MCPServer:
    """Model Context Protocol (MCP) Server exposing agent tools."""
    
    def __init__(self):
        self.registered_tools = {
            "lookup_appointment": AgentTools.lookup_appointment_status,
            "calculate_escalation": AgentTools.calculate_escalation_score
        }

    def list_tools(self):
        return list(self.registered_tools.keys())

    def call_tool(self, tool_name: str, arguments: dict):
        if tool_name not in self.registered_tools:
            return {"error": f"Tool '{tool_name}' not found on MCP Server."}
        return self.registered_tools[tool_name](**arguments)