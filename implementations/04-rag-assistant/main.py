"""Local Markdown RAG teaching demo using only the Python standard library.

The module intentionally avoids embedding APIs and real LLM calls. Retrieval is
keyword based, and answer generation is a deterministic mock summary assembled
from retrieved chunks.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import argparse
import math
import re
import sys
from typing import Iterable, Sequence


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DOCS_DIR = REPO_ROOT / "data" / "docs"

# A compact stop-word list keeps keyword scoring focused while staying easy to
# inspect for learners. Chinese terms are handled as substring keywords below.
STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "be",
    "by",
    "for",
    "from",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "the",
    "to",
    "with",
    "什么",
    "是什么",
    "怎么",
    "如何",
    "以及",
    "一个",
    "这个",
    "那个",
}


@dataclass(frozen=True)
class Document:
    """A Markdown document loaded from disk."""

    path: Path
    title: str
    text: str


@dataclass(frozen=True)
class Chunk:
    """A retrievable text chunk with source metadata."""

    id: str
    text: str
    metadata: dict[str, str | int]

    def citation(self) -> str:
        """Return a compact citation string for display."""

        section = self.metadata.get("section") or "未命名章节"
        return f"[{self.id}] {self.metadata['source']} > {section}"


@dataclass(frozen=True)
class SearchResult:
    """A scored chunk returned by retrieval."""

    chunk: Chunk
    score: float
    matched_terms: tuple[str, ...]


def load_documents(docs_dir: Path = DEFAULT_DOCS_DIR) -> list[Document]:
    """Load all Markdown documents from a directory in deterministic order."""

    if not docs_dir.exists():
        return []

    documents: list[Document] = []
    for path in sorted(docs_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8").strip()
        if not text:
            continue
        title = extract_title(text) or path.stem
        documents.append(Document(path=path, title=title, text=text))
    return documents


def extract_title(markdown: str) -> str:
    """Extract the first level-1 Markdown heading, if present."""

    for line in markdown.splitlines():
        match = re.match(r"^#\s+(.+?)\s*$", line)
        if match:
            return match.group(1)
    return ""


def chunk_documents(documents: Sequence[Document]) -> list[Chunk]:
    """Split Markdown documents by heading, then by paragraph.

    Each chunk carries metadata that makes citations explainable: source file,
    document title, section heading, paragraph index, and character offsets.
    """

    chunks: list[Chunk] = []
    next_id = 1
    for document in documents:
        sections = split_markdown_sections(document.text)
        for section_title, section_body, start_offset in sections:
            paragraphs = split_paragraphs(section_body)
            for paragraph_index, paragraph in enumerate(paragraphs, start=1):
                text = paragraph.strip()
                if not text:
                    continue
                chunk = Chunk(
                    id=f"C{next_id}",
                    text=text,
                    metadata={
                        "source": document.path.name,
                        "path": str(document.path),
                        "title": document.title,
                        "section": section_title or document.title,
                        "paragraph": paragraph_index,
                        "start": start_offset + section_body.find(paragraph),
                        "end": start_offset + section_body.find(paragraph) + len(paragraph),
                    },
                )
                chunks.append(chunk)
                next_id += 1
    return chunks


def split_markdown_sections(markdown: str) -> list[tuple[str, str, int]]:
    """Split Markdown into sections using headings as boundaries."""

    heading_pattern = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
    matches = list(heading_pattern.finditer(markdown))
    if not matches:
        return [("全文", markdown, 0)]

    sections: list[tuple[str, str, int]] = []
    for index, match in enumerate(matches):
        title = match.group(2).strip()
        body_start = match.end()
        body_end = matches[index + 1].start() if index + 1 < len(matches) else len(markdown)
        body = markdown[body_start:body_end].strip()
        if body:
            sections.append((title, body, body_start))
    return sections


def split_paragraphs(text: str) -> list[str]:
    """Split text into paragraphs and normalize whitespace inside each one."""

    raw_paragraphs = re.split(r"\n\s*\n", text.strip())
    return [normalize_whitespace(paragraph) for paragraph in raw_paragraphs if paragraph.strip()]


def normalize_whitespace(text: str) -> str:
    """Collapse line breaks and repeated spaces for easier display."""

    return re.sub(r"\s+", " ", text).strip()


def tokenize(text: str) -> list[str]:
    """Extract simple retrieval keywords from English and Chinese text.

    English words are separated by word boundaries. Chinese spans are captured
    as character bigrams/trigrams plus the full short phrase, which is enough for
    this teaching demo without external tokenizers.
    """

    lowered = text.lower()
    terms: list[str] = []

    for word in re.findall(r"[a-z0-9]+", lowered):
        if len(word) > 1 and word not in STOP_WORDS:
            terms.append(word)

    for span in re.findall(r"[一-鿿]+", text):
        if span not in STOP_WORDS and len(span) <= 6:
            terms.append(span)
        for size in (2, 3):
            for index in range(0, max(0, len(span) - size + 1)):
                term = span[index : index + size]
                if term not in STOP_WORDS:
                    terms.append(term)

    return deduplicate(terms)


def deduplicate(items: Iterable[str]) -> list[str]:
    """Return items in first-seen order without duplicates."""

    seen: set[str] = set()
    unique: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            unique.append(item)
    return unique


def search(query: str, chunks: Sequence[Chunk], top_k: int = 3) -> list[SearchResult]:
    """Retrieve chunks by keyword overlap and simple term-frequency scoring."""

    query_terms = tokenize(query)
    if not query_terms:
        return []

    results: list[SearchResult] = []
    for chunk in chunks:
        searchable_text = " ".join(
            [
                chunk.text,
                str(chunk.metadata.get("title", "")),
                str(chunk.metadata.get("section", "")),
                str(chunk.metadata.get("source", "")),
            ]
        ).lower()
        matched_terms = tuple(term for term in query_terms if term.lower() in searchable_text)
        if not matched_terms:
            continue
        score = score_match(matched_terms, query_terms, chunk)
        results.append(SearchResult(chunk=chunk, score=score, matched_terms=matched_terms))

    return sorted(results, key=lambda result: (-result.score, result.chunk.id))[:top_k]


def score_match(matched_terms: Sequence[str], query_terms: Sequence[str], chunk: Chunk) -> float:
    """Score a chunk using coverage, frequency, title hits, and length penalty."""

    searchable_text = chunk.text.lower()
    section_text = str(chunk.metadata.get("section", "")).lower()
    title_text = str(chunk.metadata.get("title", "")).lower()

    coverage = len(set(matched_terms)) / max(1, len(set(query_terms)))
    frequency = sum(searchable_text.count(term.lower()) for term in matched_terms)
    heading_bonus = sum(1 for term in matched_terms if term.lower() in section_text or term.lower() in title_text)
    length_penalty = math.log(max(20, len(chunk.text)), 10)

    return round((coverage * 3.0) + frequency + (heading_bonus * 0.5) - (length_penalty * 0.1), 4)


def generate_mock_answer(query: str, results: Sequence[SearchResult]) -> str:
    """Build a deterministic answer from retrieved chunks and citations."""

    if not results:
        return (
            f"问题：{query}\n\n"
            "未在本地 Markdown 知识库中检索到足够相关的内容。"
            "可以补充 data/docs/*.md 后重试。"
        )

    lines = [f"问题：{query}", "", "基于本地文档检索到的片段，回答如下："]
    for index, result in enumerate(results, start=1):
        summary = shorten(result.chunk.text, max_chars=180)
        lines.append(f"{index}. {summary} {result.chunk.citation()}")

    lines.extend(["", "引用："])
    for result in results:
        terms = ", ".join(result.matched_terms)
        lines.append(f"- {result.chunk.citation()}（score={result.score}, matched={terms}）")
    return "\n".join(lines)


def shorten(text: str, max_chars: int) -> str:
    """Trim long snippets without cutting too aggressively."""

    clean = normalize_whitespace(text)
    if len(clean) <= max_chars:
        return clean
    return clean[: max_chars - 1].rstrip() + "…"


def answer_question(query: str, docs_dir: Path = DEFAULT_DOCS_DIR, top_k: int = 3) -> str:
    """Run the full local RAG flow: load, chunk, retrieve, mock-generate."""

    documents = load_documents(docs_dir)
    chunks = chunk_documents(documents)
    results = search(query, chunks, top_k=top_k)
    return generate_mock_answer(query, results)


def build_arg_parser() -> argparse.ArgumentParser:
    """Create the command-line parser."""

    parser = argparse.ArgumentParser(description="本地 Markdown RAG 教学 Demo（无外部依赖）")
    parser.add_argument("query", help="用户问题，例如：Agent 和 Chatbot 区别是什么")
    parser.add_argument(
        "--docs-dir",
        type=Path,
        default=DEFAULT_DOCS_DIR,
        help=f"Markdown 文档目录，默认：{DEFAULT_DOCS_DIR}",
    )
    parser.add_argument("--top-k", type=int, default=3, help="返回的检索片段数量")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point."""

    parser = build_arg_parser()
    args = parser.parse_args(argv)
    print(answer_question(args.query, docs_dir=args.docs_dir, top_k=args.top_k))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
