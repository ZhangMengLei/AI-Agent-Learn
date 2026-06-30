import importlib.util
import sys
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "implementations" / "02-llm-chat" / "main.py"
SPEC = importlib.util.spec_from_file_location("llm_chat", MODULE_PATH)
llm_chat = importlib.util.module_from_spec(SPEC)
sys.modules["llm_chat"] = llm_chat
assert SPEC.loader is not None
SPEC.loader.exec_module(llm_chat)


class LLMChatTest(unittest.TestCase):
    def test_complete_returns_deterministic_response(self):
        client = llm_chat.MockLLMClient()
        response = client.complete([llm_chat.Message("user", "解释 temperature 是什么")])
        self.assertIn("temperature", response.content)
        self.assertGreater(response.input_tokens, 0)
        self.assertGreater(response.output_tokens, 0)

    def test_stream_reconstructs_complete_response(self):
        client = llm_chat.MockLLMClient()
        messages = [llm_chat.Message("user", "什么是 streaming")]
        complete = client.complete(messages).content
        streamed = "".join(client.stream(messages)).strip()
        self.assertEqual(complete, streamed)

    def test_conversation_keeps_system_message(self):
        conversation = llm_chat.Conversation("系统提示", max_turns=1)
        conversation.add_user("第一轮")
        conversation.add_assistant("回答")
        conversation.add_user("第二轮")
        messages = conversation.messages()
        self.assertEqual("system", messages[0].role)
        self.assertEqual("系统提示", messages[0].content)
        self.assertLessEqual(len(messages), 3)

    def test_call_log_has_no_api_key(self):
        client = llm_chat.MockLLMClient()
        messages = [llm_chat.Message("user", "hello")]
        response = client.complete(messages)
        entry = llm_chat.CallLogger().record(messages, response, temperature=0.3, max_tokens=100)
        self.assertIn("model", entry)
        self.assertNotIn("api_key", entry)


if __name__ == "__main__":
    unittest.main()
