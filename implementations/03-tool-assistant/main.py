#!/usr/bin/env python3
"""A tiny Tool Use / Function Calling teaching demo.

This file intentionally uses only Python standard library modules and a mock
model. It demonstrates the core engineering pieces behind tool use without
calling any real LLM API.
"""

from __future__ import annotations

import argparse
import ast
import operator
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable


class PermissionLevel(str, Enum):
    """Simple permission levels for tools."""

    PUBLIC = "public"  # Safe, no confirmation needed.
    READ = "read"  # Reads local/mock data.
    WRITE = "write"  # Changes local/mock data, should ask user first.


@dataclass(frozen=True)
class ToolCall:
    """The model's structured request to call a tool."""

    name: str
    arguments: dict[str, Any]


@dataclass
class ToolResult:
    """Normalized result returned by every tool execution."""

    ok: bool
    content: Any = None
    error: str | None = None


@dataclass(frozen=True)
class ParameterSpec:
    """Minimal parameter schema for beginner-friendly validation."""

    type: type
    required: bool = True
    description: str = ""


@dataclass(frozen=True)
class ToolSpec:
    """Metadata and callable for one registered tool."""

    name: str
    description: str
    permission: PermissionLevel
    parameters: dict[str, ParameterSpec]
    handler: Callable[..., Any]


@dataclass
class ToolLogEntry:
    """One audit entry for a tool invocation."""

    tool_name: str
    arguments: dict[str, Any]
    permission: str
    status: str
    message: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))


class ToolRegistry:
    """Registers tools, validates arguments, checks permission, and logs calls."""

    def __init__(self) -> None:
        self._tools: dict[str, ToolSpec] = {}
        self.log: list[ToolLogEntry] = []

    def register(self, spec: ToolSpec) -> None:
        if spec.name in self._tools:
            raise ValueError(f"Tool already registered: {spec.name}")
        self._tools[spec.name] = spec

    def get(self, name: str) -> ToolSpec | None:
        return self._tools.get(name)

    def execute(
        self,
        call: ToolCall,
        confirm_permission: Callable[[ToolSpec, dict[str, Any]], bool] | None = None,
    ) -> ToolResult:
        spec = self.get(call.name)
        if spec is None:
            self._append_log(call.name, call.arguments, "unknown", "error", "unknown tool")
            return ToolResult(ok=False, error=f"Unknown tool: {call.name}")

        validation_error = self._validate_arguments(spec, call.arguments)
        if validation_error:
            self._append_log(spec.name, call.arguments, spec.permission.value, "error", validation_error)
            return ToolResult(ok=False, error=validation_error)

        if spec.permission == PermissionLevel.WRITE:
            allowed = confirm_permission(spec, call.arguments) if confirm_permission else False
            if not allowed:
                self._append_log(spec.name, call.arguments, spec.permission.value, "denied", "permission denied")
                return ToolResult(ok=False, error=f"Permission denied for tool: {spec.name}")

        try:
            content = spec.handler(**call.arguments)
        except Exception as exc:  # Teaching demo: keep errors visible and normalized.
            self._append_log(spec.name, call.arguments, spec.permission.value, "error", str(exc))
            return ToolResult(ok=False, error=str(exc))

        self._append_log(spec.name, call.arguments, spec.permission.value, "success", "ok")
        return ToolResult(ok=True, content=content)

    def _validate_arguments(self, spec: ToolSpec, arguments: dict[str, Any]) -> str | None:
        for name, param in spec.parameters.items():
            if param.required and name not in arguments:
                return f"Missing required argument: {name}"
            if name in arguments and not isinstance(arguments[name], param.type):
                expected = param.type.__name__
                actual = type(arguments[name]).__name__
                return f"Invalid type for {name}: expected {expected}, got {actual}"

        allowed_names = set(spec.parameters)
        for name in arguments:
            if name not in allowed_names:
                return f"Unknown argument for {spec.name}: {name}"
        return None

    def _append_log(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        permission: str,
        status: str,
        message: str,
    ) -> None:
        self.log.append(
            ToolLogEntry(
                tool_name=tool_name,
                arguments=dict(arguments),
                permission=permission,
                status=status,
                message=message,
            )
        )


class SafeCalculator:
    """Evaluates arithmetic expressions with a small AST allowlist."""

    _operators: dict[type[ast.AST], Callable[[Any, Any], Any]] = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
    }
    _unary_operators: dict[type[ast.AST], Callable[[Any], Any]] = {
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    def calculate(self, expression: str) -> str:
        tree = ast.parse(expression, mode="eval")
        value = self._eval_node(tree.body)
        return f"{expression} = {value}"

    def _eval_node(self, node: ast.AST) -> int | float:
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in self._operators:
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            return self._operators[type(node.op)](left, right)
        if isinstance(node, ast.UnaryOp) and type(node.op) in self._unary_operators:
            return self._unary_operators[type(node.op)](self._eval_node(node.operand))
        raise ValueError("Calculator only supports numbers and + - * / // % ** parentheses")


class MockNotes:
    """In-memory notes tool. It demonstrates WRITE permission confirmation."""

    def __init__(self) -> None:
        self._notes: list[str] = []

    def add(self, text: str) -> str:
        self._notes.append(text)
        return f"已记录笔记：{text}"

    def list_notes(self) -> str:
        if not self._notes:
            return "当前没有笔记。"
        return "\n".join(f"{index}. {note}" for index, note in enumerate(self._notes, start=1))


def mock_weather(city: str) -> str:
    """Returns deterministic mock weather, not real network data."""

    weather_by_city = {
        "北京": "晴，26°C，北风 2 级",
        "上海": "多云，28°C，东南风 3 级",
        "广州": "小雨，30°C，湿度较高",
        "深圳": "阵雨，29°C，注意带伞",
    }
    weather = weather_by_city.get(city, "多云，25°C（示例数据）")
    return f"{city}天气：{weather}。"


class MockModel:
    """Rule-based mock model that chooses tools from user input."""

    _known_cities = ("北京", "上海", "广州", "深圳", "杭州", "成都", "南京", "武汉")

    def plan(self, user_input: str) -> ToolCall | None:
        text = user_input.strip()
        lowered = text.lower()

        if "unknown_tool" in lowered:
            return ToolCall(name="unknown_tool", arguments={})

        if "天气" in text or "weather" in lowered:
            return ToolCall(name="mock_weather", arguments={"city": self._extract_city(text)})

        if self._looks_like_calculation(text):
            return ToolCall(name="calculator", arguments={"expression": self._extract_expression(text)})

        if any(keyword in text for keyword in ("记录", "记下", "添加笔记")) or "add note" in lowered:
            note_text = self._extract_note_text(text)
            return ToolCall(name="mock_notes", arguments={"text": note_text})

        if "笔记" in text or "notes" in lowered:
            return ToolCall(name="list_notes", arguments={})

        return None

    def _extract_city(self, text: str) -> str:
        for city in self._known_cities:
            if city in text:
                return city
        match = re.search(r"([一-龥]{2,4})天气", text)
        if match:
            return match.group(1)
        return "北京"

    def _looks_like_calculation(self, text: str) -> bool:
        if any(keyword in text for keyword in ("计算", "算一下", "等于多少")):
            return True
        return bool(re.fullmatch(r"[\d\s+\-*/().%]+", text))

    def _extract_expression(self, text: str) -> str:
        replacements = {
            "加": "+",
            "减": "-",
            "乘以": "*",
            "乘": "*",
            "除以": "/",
            "除": "/",
            "计算": "",
            "算一下": "",
            "等于多少": "",
            "？": "",
            "?": "",
        }
        expression = text
        for old, new in replacements.items():
            expression = expression.replace(old, new)
        match = re.search(r"[\d\s+\-*/().%]+", expression)
        if not match:
            raise ValueError("No arithmetic expression found")
        return match.group(0).strip()

    def _extract_note_text(self, text: str) -> str:
        for prefix in ("记录", "记下", "添加笔记", "add note"):
            text = text.replace(prefix, "", 1)
        return text.strip(" ：:，,") or "空笔记"


class ToolAssistant:
    """Orchestrates mock model planning, registry execution, and final answer."""

    def __init__(self, registry: ToolRegistry | None = None, model: MockModel | None = None) -> None:
        self.registry = registry or build_default_registry()
        self.model = model or MockModel()

    def handle(
        self,
        user_input: str,
        confirm_permission: Callable[[ToolSpec, dict[str, Any]], bool] | None = None,
    ) -> str:
        call = self.model.plan(user_input)
        if call is None:
            return "我没有选择工具。你可以问天气、让我计算，或让我记录/查看笔记。"

        result = self.registry.execute(call, confirm_permission=confirm_permission)
        if result.ok:
            return f"工具 {call.name} 返回：{result.content}"
        return f"工具 {call.name} 调用失败：{result.error}"


def build_default_registry() -> ToolRegistry:
    calculator = SafeCalculator()
    notes = MockNotes()
    registry = ToolRegistry()
    registry.register(
        ToolSpec(
            name="calculator",
            description="Evaluate a safe arithmetic expression.",
            permission=PermissionLevel.PUBLIC,
            parameters={"expression": ParameterSpec(str, description="Arithmetic expression, e.g. 1 + 2 * 3")},
            handler=calculator.calculate,
        )
    )
    registry.register(
        ToolSpec(
            name="mock_weather",
            description="Return deterministic mock weather for a city.",
            permission=PermissionLevel.READ,
            parameters={"city": ParameterSpec(str, description="City name, e.g. 北京")},
            handler=mock_weather,
        )
    )
    registry.register(
        ToolSpec(
            name="mock_notes",
            description="Add an in-memory note. Requires WRITE confirmation.",
            permission=PermissionLevel.WRITE,
            parameters={"text": ParameterSpec(str, description="Note content")},
            handler=notes.add,
        )
    )
    registry.register(
        ToolSpec(
            name="list_notes",
            description="List in-memory notes.",
            permission=PermissionLevel.READ,
            parameters={},
            handler=notes.list_notes,
        )
    )
    return registry


def cli_confirm_permission(auto_yes: bool) -> Callable[[ToolSpec, dict[str, Any]], bool]:
    def confirm(spec: ToolSpec, arguments: dict[str, Any]) -> bool:
        if auto_yes:
            return True
        answer = input(f"工具 {spec.name} 需要 {spec.permission.value} 权限，参数 {arguments}。是否允许？[y/N] ")
        return answer.strip().lower() in {"y", "yes"}

    return confirm


def run_once(user_input: str, auto_yes: bool = False) -> str:
    assistant = ToolAssistant()
    return assistant.handle(user_input, confirm_permission=cli_confirm_permission(auto_yes))


def run_repl(auto_yes: bool = False) -> None:
    assistant = ToolAssistant()
    confirm = cli_confirm_permission(auto_yes)
    print("Tool Assistant Demo。输入 exit 退出。")
    while True:
        try:
            user_input = input("> ").strip()
        except EOFError:
            break
        if user_input.lower() in {"exit", "quit"}:
            break
        if not user_input:
            continue
        print(assistant.handle(user_input, confirm_permission=confirm))


def main() -> None:
    parser = argparse.ArgumentParser(description="Mock Tool Use teaching demo")
    parser.add_argument("message", nargs="?", help="User message, e.g. 北京天气怎么样")
    parser.add_argument("--yes", action="store_true", help="Automatically approve WRITE tools")
    args = parser.parse_args()

    if args.message:
        print(run_once(args.message, auto_yes=args.yes))
    else:
        run_repl(auto_yes=args.yes)


if __name__ == "__main__":
    main()
