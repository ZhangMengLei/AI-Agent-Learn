from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import tempfile
import textwrap
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "implementations" / "04-rag-assistant" / "main.py"

spec = importlib.util.spec_from_file_location("rag_assistant", MODULE_PATH)
rag_assistant = importlib.util.module_from_spec(spec)
sys.modules["rag_assistant"] = rag_assistant
assert spec.loader is not None
spec.loader.exec_module(rag_assistant)


class RagAssistantTest(unittest.TestCase):
    def write_doc(self, docs_dir: Path, name: str, content: str) -> Path:
        path = docs_dir / name
        path.write_text(textwrap.dedent(content).strip(), encoding="utf-8")
        return path

    def test_load_documents_reads_markdown_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            docs_dir = Path(tmp_dir)
            self.write_doc(
                docs_dir,
                "agent.md",
                """
                # Agent 基础

                Agent 会根据目标调用工具并观察结果。
                """,
            )
            (docs_dir / "notes.txt").write_text("should be ignored", encoding="utf-8")

            documents = rag_assistant.load_documents(docs_dir)

            self.assertEqual(len(documents), 1)
            self.assertEqual(documents[0].title, "Agent 基础")
            self.assertEqual(documents[0].path.name, "agent.md")
            self.assertIn("调用工具", documents[0].text)

    def test_chunk_metadata_contains_source_section_and_paragraph(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            docs_dir = Path(tmp_dir)
            self.write_doc(
                docs_dir,
                "rag.md",
                """
                # RAG 入门

                ## 检索

                RAG 先检索相关 chunk。

                第二段用于测试段落序号。
                """,
            )

            chunks = rag_assistant.chunk_documents(rag_assistant.load_documents(docs_dir))

            self.assertEqual(len(chunks), 2)
            self.assertEqual(chunks[0].metadata["source"], "rag.md")
            self.assertEqual(chunks[0].metadata["title"], "RAG 入门")
            self.assertEqual(chunks[0].metadata["section"], "检索")
            self.assertEqual(chunks[0].metadata["paragraph"], 1)
            self.assertEqual(chunks[1].metadata["paragraph"], 2)
            self.assertIsInstance(chunks[0].metadata["start"], int)
            self.assertIsInstance(chunks[0].metadata["end"], int)

    def test_search_returns_relevant_chunk_first(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            docs_dir = Path(tmp_dir)
            self.write_doc(
                docs_dir,
                "agent.md",
                """
                # Agent 和 Chatbot

                ## 核心区别

                Chatbot 偏向回答问题，Agent 偏向拆解目标、调用工具、观察结果并完成任务。
                """,
            )
            self.write_doc(
                docs_dir,
                "rag.md",
                """
                # RAG

                ## 引用

                RAG 回答应该带有来源引用。
                """,
            )
            chunks = rag_assistant.chunk_documents(rag_assistant.load_documents(docs_dir))

            results = rag_assistant.search("Agent 和 Chatbot 区别是什么", chunks, top_k=1)

            self.assertEqual(len(results), 1)
            self.assertEqual(results[0].chunk.metadata["source"], "agent.md")
            self.assertIn("agent", results[0].matched_terms)
            self.assertGreater(results[0].score, 0)

    def test_mock_answer_includes_citation_format(self) -> None:
        chunk = rag_assistant.Chunk(
            id="C7",
            text="Chatbot 偏向回答问题，Agent 偏向完成任务。",
            metadata={
                "source": "agent.md",
                "path": "/tmp/agent.md",
                "title": "Agent 和 Chatbot",
                "section": "核心区别",
                "paragraph": 1,
                "start": 0,
                "end": 24,
            },
        )
        result = rag_assistant.SearchResult(chunk=chunk, score=3.2, matched_terms=("Agent", "Chatbot"))

        answer = rag_assistant.generate_mock_answer("Agent 和 Chatbot 区别是什么", [result])

        self.assertIn("[C7] agent.md > 核心区别", answer)
        self.assertIn("引用：", answer)
        self.assertIn("score=3.2", answer)
        self.assertIn("matched=Agent, Chatbot", answer)


if __name__ == "__main__":
    unittest.main()
