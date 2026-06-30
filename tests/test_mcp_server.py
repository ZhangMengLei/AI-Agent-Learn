import importlib.util
import sys
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "implementations" / "06-mcp-server" / "main.py"
SPEC = importlib.util.spec_from_file_location("mcp_server", MODULE_PATH)
mcp_server = importlib.util.module_from_spec(SPEC)
sys.modules["mcp_server"] = mcp_server
assert SPEC.loader is not None
SPEC.loader.exec_module(mcp_server)


class MCPServerTest(unittest.TestCase):
    def setUp(self):
        self.server = mcp_server.MiniMCPServer()

    def test_tools_list_returns_metadata(self):
        response = self.server.handle({"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}})
        self.assertEqual("2.0", response["jsonrpc"])
        names = [tool["name"] for tool in response["result"]["tools"]]
        self.assertIn("search_notes", names)

    def test_search_notes_finds_mcp_note(self):
        response = self.server.handle({"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "search_notes", "arguments": {"query": "mcp"}}})
        results = response["result"]["content"]
        self.assertEqual("note-003", results[0]["id"])

    def test_read_mcp_resource_returns_markdown(self):
        response = self.server.handle({"jsonrpc": "2.0", "id": 3, "method": "resources/read", "params": {"uri": "docs://mcp-basic"}})
        self.assertEqual("text/markdown", response["result"]["mimeType"])
        self.assertIn("MCP", response["result"]["text"])

    def test_unknown_method_returns_json_rpc_error(self):
        response = self.server.handle({"jsonrpc": "2.0", "id": 4, "method": "missing", "params": {}})
        self.assertEqual("2.0", response["jsonrpc"])
        self.assertEqual(4, response["id"])
        self.assertEqual(-32601, response["error"]["code"])

    def test_missing_query_returns_clear_error(self):
        response = self.server.handle({"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "search_notes", "arguments": {}}})
        self.assertEqual(-32602, response["error"]["code"])
        self.assertIn("query", response["error"]["message"])


if __name__ == "__main__":
    unittest.main()
