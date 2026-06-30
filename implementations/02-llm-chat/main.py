from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from typing import Iterable, List, Optional


@dataclass(frozen=True)
class Message:
    role: str
    content: str


@dataclass(frozen=True)
class LLMResponse:
    content: str
    input_tokens: int
    output_tokens: int
    latency_ms: int
    model: str


class MockLLMClient:
    def complete(
        self,
        messages: List[Message],
        model: str = "mock-basic",
        temperature: float = 0.3,
        max_tokens: int = 400,
    ) -> LLMResponse:
        prompt = messages[-1].content if messages else ""
        content = self._answer(prompt, max_tokens)
        return LLMResponse(
            content=content,
            input_tokens=estimate_tokens("\n".join(message.content for message in messages)),
            output_tokens=estimate_tokens(content),
            latency_ms=12,
            model=model,
        )

    def stream(self, messages: List[Message], **kwargs: object) -> Iterable[str]:
        response = self.complete(messages, **kwargs)
        words = response.content.split()
        for word in words:
            yield word + " "

    def _answer(self, prompt: str, max_tokens: int) -> str:
        lowered = prompt.lower()
        if "stream" in lowered or "流式" in prompt:
            answer = "Streaming 会把模型输出拆成片段逐步返回，改善首字响应，但通常不减少总 token 成本。"
        elif "temperature" in lowered:
            answer = "temperature 控制输出随机性。值越低越稳定，值越高越发散，教学和结构化任务通常建议较低。"
        elif "上下文" in prompt or "history" in lowered:
            answer = "多轮上下文需要把必要历史放进 messages，但要定期裁剪或摘要，避免成本过高。"
        else:
            answer = "这是一个 mock LLM 回答，用来演示 messages、参数、token 和日志结构。"
        return " ".join(answer.split()[:max_tokens])


class Conversation:
    def __init__(self, system_prompt: str, max_turns: int = 3) -> None:
        self.system_prompt = system_prompt
        self.max_turns = max_turns
        self.history: List[Message] = []

    def add_user(self, content: str) -> None:
        self.history.append(Message("user", content))
        self._trim()

    def add_assistant(self, content: str) -> None:
        self.history.append(Message("assistant", content))
        self._trim()

    def messages(self) -> List[Message]:
        return [Message("system", self.system_prompt), *self.history]

    def _trim(self) -> None:
        keep = self.max_turns * 2
        if len(self.history) > keep:
            self.history = self.history[-keep:]


class CallLogger:
    def __init__(self) -> None:
        self.entries: List[dict] = []

    def record(
        self,
        messages: List[Message],
        response: LLMResponse,
        temperature: float,
        max_tokens: int,
        success: bool = True,
        error: Optional[str] = None,
    ) -> dict:
        entry = {
            "model": response.model,
            "message_count": len(messages),
            "input_tokens": response.input_tokens,
            "output_tokens": response.output_tokens,
            "latency_ms": response.latency_ms,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "success": success,
            "error": error,
        }
        self.entries.append(entry)
        return entry


def estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4) if text else 0


def run_single(prompt: str, stream: bool, show_log: bool) -> str:
    client = MockLLMClient()
    logger = CallLogger()
    conversation = Conversation("你是中文 AI 学习助手，用简洁语言解释 LLM API 概念。")
    conversation.add_user(prompt)
    messages = conversation.messages()
    response = client.complete(messages)
    logger.record(messages, response, temperature=0.3, max_tokens=400)
    lines = ["请求 messages：", json.dumps([asdict(m) for m in messages], ensure_ascii=False, indent=2), ""]
    if stream:
        chunks = list(client.stream(messages))
        lines.extend(["Streaming chunks：", "|".join(chunks), "", "拼接结果：", "".join(chunks).strip()])
    else:
        lines.extend(["完整响应：", response.content])
    if show_log:
        lines.extend(["", "调用日志：", json.dumps(logger.entries, ensure_ascii=False, indent=2)])
    return "\n".join(lines)


def run_multi_turn(show_log: bool) -> str:
    client = MockLLMClient()
    logger = CallLogger()
    conversation = Conversation("你是中文 AI 学习助手，回答要短。", max_turns=2)
    for prompt in ["什么是 Prompt？", "那多轮上下文怎么处理？"]:
        conversation.add_user(prompt)
        messages = conversation.messages()
        response = client.complete(messages)
        conversation.add_assistant(response.content)
        logger.record(messages, response, temperature=0.3, max_tokens=400)
    lines = ["多轮 messages：", json.dumps([asdict(m) for m in conversation.messages()], ensure_ascii=False, indent=2)]
    if show_log:
        lines.extend(["", "调用日志：", json.dumps(logger.entries, ensure_ascii=False, indent=2)])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Mock LLM API / Chat / Streaming 教学 Demo")
    parser.add_argument("prompt", nargs="?", default="解释 temperature 是什么")
    parser.add_argument("--stream", action="store_true")
    parser.add_argument("--multi-turn", action="store_true")
    parser.add_argument("--show-log", action="store_true")
    args = parser.parse_args()
    if args.multi_turn:
        print(run_multi_turn(args.show_log))
    else:
        print(run_single(args.prompt, args.stream, args.show_log))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
