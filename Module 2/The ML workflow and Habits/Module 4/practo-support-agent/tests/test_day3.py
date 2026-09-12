import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.mcp_server import MCPServer
from src.mcp_client import MCPClient
from src.checkpointing import SQLiteCheckpointSaver
from src.timeouts import execute_with_timeout

def test_day3_pipeline():
    # 1. Test MCP Protocol (Server/Client decoupler)
    mcp_server = MCPServer()
    mcp_client = MCPClient(mcp_server)
    
    mcp_res = mcp_client.execute_remote_tool("lookup_appointment", {"appointment_id": "APP-1001"})
    assert mcp_res["found"] is True
    
    # 2. Test SQLite Checkpointing Persistence
    saver = SQLiteCheckpointSaver()
    test_state = {"thread_id": "session_001", "status": "completed"}
    saver.save_checkpoint("session_001", test_state)
    loaded = saver.load_checkpoint("session_001")
    assert loaded["status"] == "completed"
    
    # 3. Test Timeout & Retry Wrapper
    def dummy_task():
        return "success"
    
    result = execute_with_timeout(dummy_task, timeout_sec=2.0)
    assert result == "success"
    
    print("\n🎉 Day 3 Production Requirements PASSED successfully!")

if __name__ == "__main__":
    test_day3_pipeline()