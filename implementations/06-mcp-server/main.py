from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[2]
NOTES_PATH = ROOT / "data" / "notes" / "ai-agent-notes.json"
DOCS_DIR = ROOT / "data" / "docs"


@dataclass(frozen=True)
class JsonRpcResponse:
    id: Any
    result: Optional[dict] = None
    error: Optional[dict] = None

    def to_dict(self) -> dict:
        data = {"jsonrpc": "2.0", "id": self.id}
        if self.error is not None:
            data["error"] = self.error
        else:
            data["result"] = self.result or {}
        return data


class MiniMCPServer:
    def __init__(self, root: Path = ROOT) -> None:
        self.root = root
        self.notes_path = root / "data" / "notes" / "ai-agent-notes.json"
        self.docs_dir = root / "data" / "docs"

    def handle(self, request: Dict[str, Any]) -> dict:
        request_id = request.get("id")
        method = request.get("method")
        params = request.get("params") or {}
        try:
            if method == "initialize":
                result = self.initialize()
            elif method == "tools/list":
                result = {"tools": self.list_tools()}
            elif method == "tools/call":
                result = self.call_tool(params)
            elif method == "resources/list":
                result = {"resources": self.list_resources()}
            elif method == "resources/read":
                result = self.read_resource(params)
            elif method == "prompts/list":
                result = {"prompts": self.list_prompts()}
            elif method == "prompts/get":
                result = self.get_prompt(params)
            else:
                return JsonRpcResponse(request_id, error={"code": -32601, "message": f"method not found: {method}"}).to_dict()
            return JsonRpcResponse(request_id, result=result).to_dict()
        except ValueError as exc:
            return JsonRpcResponse(request_id, error={"code": -32602, "message": str(exc)}).to_dict()

    def initialize(self) -> dict:
        return {"serverInfo": {"name": "learning-notes-mcp", "version": "0.1.0"}, "capabilities": {"tools": True, "resources": True, "prompts": True}}

    def list_tools(self) -> List[dict]:
        return [
            {"name": "search_notes", "description": "按关键词搜索学习笔记", "input_schema": {"required": ["query"]}},
            {"name": "list_lessons", "description": "列出课程阶段", "input_schema": {"required": []}},
            {"name": "summarize_doc", "description": "读取样例文档并返回摘要", "input_schema": {"required": ["doc"]}},
        ]

    def call_tool(self, params: Dict[str, Any]) -> dict:
        name = params.get("name")
        arguments = params.get("arguments") or {}
        if name == "search_notes":
            query = str(arguments.get("query", "")).strip()
            if not query:
                raise ValueError("search_notes requires query")
            return {"content": self.search_notes(query)}
        if name == "list_lessons":
            lessons = sorted(path.name for path in (self.root / "lessons").iterdir() if path.is_dir())
            return {"content": lessons}
        if name == "summarize_doc":
            doc = str(arguments.get("doc", "")).strip()
            if not doc:
                raise ValueError("summarize_doc requires doc")
            path = self.docs_dir / doc
            if not path.exists():
                raise ValueError(f"unknown doc: {doc}")
            text = path.read_text(encoding="utf-8")
            return {"content": {"doc": doc, "summary": first_non_heading_line(text)}}
        raise ValueError(f"unknown tool: {name}")

    def search_notes(self, query: str) -> List[dict]:
        notes = json.loads(self.notes_path.read_text(encoding="utf-8"))
        query_lower = query.lower()
        results = []
        for note in notes:
            haystack = " ".join([note["topic"], note["title"], note["summary"], " ".join(note["tags"])]).lower()
            if query_lower in haystack:
                results.append(note)
        return results

    def list_resources(self) -> List[dict]:
        return [
            {"uri": "notes://ai-agent", "name": "AI Agent 学习笔记", "mimeType": "application/json"},
            {"uri": "docs://prompt-basic", "name": "Prompt 基础", "mimeType": "text/markdown"},
            {"uri": "docs://mcp-basic", "name": "MCP 基础", "mimeType": "text/markdown"},
        ]

    def read_resource(self, params: Dict[str, Any]) -> dict:
        uri = params.get("uri")
        if uri == "notes://ai-agent":
            return {"uri": uri, "mimeType": "application/json", "text": self.notes_path.read_text(encoding="utf-8")}
        mapping = {"docs://prompt-basic": "prompt-basic.md", "docs://mcp-basic": "mcp-basic.md"}
        if uri in mapping:
            return {"uri": uri, "mimeType": "text/markdown", "text": (self.docs_dir / mapping[uri]).read_text(encoding="utf-8")}
        raise ValueError(f"unknown resource: {uri}")

    def list_prompts(self) -> List[dict]:
        return [
            {"name": "explain_mcp_tool", "description": "解释某个 MCP Tool 的用途"},
            {"name": "design_mcp_server", "description": "设计一个最小 MCP Server"},
        ]

    def get_prompt(self, params: Dict[str, Any]) -> dict:
        name = params.get("name")
        arguments = params.get("arguments") or {}
        topic = arguments.get("topic", "MCP")
        if name == "explain_mcp_tool":
            return {"messages": [{"role": "user", "content": f"请面向初学者解释 {topic} 这个 MCP Tool 的用途、输入和风险。"}]}
        if name == "design_mcp_server":
            return {"messages": [{"role": "user", "content": f"请设计一个围绕 {topic} 的最小 MCP Server，包含 tools、resources 和 prompts。"}]}
        raise ValueError(f"unknown prompt: {name}")


def first_non_heading_line(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            return stripped
    return ""


def demo_requests() -> List[dict]:
    return [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
        {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "search_notes", "arguments": {"query": "mcp"}}},
        {"jsonrpc": "2.0", "id": 4, "method": "resources/read", "params": {"uri": "docs://mcp-basic"}},
        {"jsonrpc": "2.0", "id": 5, "method": "prompts/get", "params": {"name": "design_mcp_server", "arguments": {"topic": "学习笔记"}}},
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="最小 MCP / JSON-RPC 教学 Demo")
    parser.add_argument("--demo", action="store_true")
    parser.add_argument("--request-json")
    args = parser.parse_args()
    server = MiniMCPServer()
    requests = demo_requests() if args.demo or not args.request_json else [json.loads(args.request_json)]
    for request in requests:
        print(json.dumps(server.handle(request), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
