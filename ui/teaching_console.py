"""Generate the local AI-Agent-Learn teaching console.

The console is a static HTML file. It reads the existing course materials and
demo modules, then embeds a deterministic teaching dataset for browser-side
exploration. No network calls or real model calls are made.
"""

from __future__ import annotations

import argparse
import html
import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = PROJECT_ROOT / "ui" / "dist" / "teaching-console.html"
DEFAULT_PROGRESS = PROJECT_ROOT / "data" / "notes" / "learning-progress.example.json"
DEFAULT_PROMPT_INPUT = "我想做一个可以回答公司文档问题的 RAG 助手。"
DEFAULT_RAG_QUERY = "Agent 和 Chatbot 区别是什么"
DEFAULT_AGENT_TOPIC = "Agent 如何完成研究任务"
READING_SPEED_CHARS_PER_MINUTE = 520
LEARNING_DOC_PREFIXES = (
    "README.md",
    "labs/",
    "lessons/",
    "checkpoints/",
    "solutions/",
    "implementations/",
    "data/docs/",
    "ui/README.md",
)

COLLECTION_TITLES = {
    "overview": "总览与使用指南",
    "labs": "Labs 学习支持",
    "checkpoints": "阶段自查清单",
    "solutions": "参考答案讲解",
    "implementations": "可运行实现说明",
    "knowledge": "样例知识库文档",
    "ui": "本地教学 GUI 指南",
}


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    if spec.loader is None:
        raise ImportError(f"Cannot load module from {path}")
    spec.loader.exec_module(module)
    return module


def first_paragraph(markdown: str) -> str:
    for block in markdown.split("\n\n"):
        clean = " ".join(line.strip() for line in block.splitlines() if line.strip() and not line.startswith("#"))
        if clean:
            return clean[:180]
    return ""


def is_learning_markdown(path: Path) -> bool:
    relative = path.relative_to(PROJECT_ROOT).as_posix()
    if relative.startswith("ui/dist/"):
        return False
    return any(relative == prefix or relative.startswith(prefix) for prefix in LEARNING_DOC_PREFIXES)


def collection_for(path: Path, lesson_stage_titles: dict[str, str]) -> tuple[str, str]:
    relative = path.relative_to(PROJECT_ROOT).as_posix()
    if relative.startswith("lessons/"):
        stage_slug = relative.split("/", 2)[1]
        return stage_slug, lesson_stage_titles.get(stage_slug, stage_slug)
    if relative == "README.md":
        return "overview", COLLECTION_TITLES["overview"]
    if relative.startswith("data/docs/"):
        return "knowledge", COLLECTION_TITLES["knowledge"]
    top_level = relative.split("/", 1)[0]
    return top_level, COLLECTION_TITLES.get(top_level, top_level)


def item_label(path: Path, collection_slug: str) -> str:
    relative = path.relative_to(PROJECT_ROOT).as_posix()
    if collection_slug in {"overview", "knowledge", "ui"}:
        return path.stem if path.name != "README.md" else "README.md"
    parts = relative.split("/")
    if collection_slug in {"labs", "checkpoints"}:
        return parts[-1]
    if collection_slug in {"solutions", "implementations"} and len(parts) > 2:
        return "/".join(parts[1:])
    if collection_slug.startswith(tuple(str(index).zfill(2) for index in range(9))) and relative.startswith("lessons/"):
        return "/".join(parts[2:])
    return "/".join(parts[1:])


def document_sort_key(document: dict[str, Any]) -> tuple[int, str, str]:
    order = {
        "overview": 0,
        "labs": 1,
        "00-ai-foundation": 2,
        "01-prompt": 3,
        "02-llm-api": 4,
        "03-tool-use": 5,
        "04-rag": 6,
        "05-agent": 7,
        "06-mcp": 8,
        "07-claude-code": 9,
        "08-eval-security": 10,
        "checkpoints": 11,
        "solutions": 12,
        "implementations": 13,
        "knowledge": 14,
        "ui": 15,
    }
    return (order.get(document["collectionSlug"], 99), document["collectionSlug"], document["path"])


def solution_path_for(lesson_path: str) -> str | None:
    if not lesson_path.startswith("lessons/"):
        return None

    parts = lesson_path.split("/")
    if len(parts) < 3:
        return None

    stage_slug = parts[1]
    relative_item = "/".join(parts[2:])
    solution_map = {
        "03-exercises.md": "03-exercises.md",
        "04-exercises-lab/README.md": "04-exercises-lab.md",
        "05-project.md": "05-project.md",
        "06-project-lab/README.md": "06-project-lab.md",
    }
    mapped_item = solution_map.get(relative_item)
    if mapped_item is None:
        return None

    candidate = PROJECT_ROOT / "solutions" / stage_slug / mapped_item
    if not candidate.exists():
        return None
    return candidate.relative_to(PROJECT_ROOT).as_posix()


def build_lesson_documents(learning_status: ModuleType, statuses: list[Any]) -> list[dict[str, Any]]:
    stage_titles = {status.stage.slug: status.stage.title for status in statuses}
    documents: list[dict[str, Any]] = []
    for path in sorted(PROJECT_ROOT.rglob("*.md")):
        if not is_learning_markdown(path):
            continue
        content = path.read_text(encoding="utf-8")
        relative_path = path.relative_to(PROJECT_ROOT).as_posix()
        collection_slug, collection_title = collection_for(path, stage_titles)
        solution_path = solution_path_for(relative_path)
        documents.append(
            {
                "id": relative_path,
                "stageSlug": collection_slug,
                "stageTitle": collection_title,
                "collectionSlug": collection_slug,
                "collectionTitle": collection_title,
                "item": item_label(path, collection_slug),
                "title": learning_status.extract_title(path) or path.name,
                "path": relative_path,
                "content": content,
                "excerpt": first_paragraph(content),
                "estimatedMinutes": max(2, round(len(content) / READING_SPEED_CHARS_PER_MINUTE)),
                "solutionPath": solution_path,
            }
        )
    documents_by_path = {document["path"]: document for document in documents}
    for document in documents:
        solution_path = document.get("solutionPath")
        solution = documents_by_path.get(solution_path) if solution_path else None
        document["solution"] = (
            {
                "id": solution["id"],
                "title": solution["title"],
                "path": solution["path"],
                "item": solution["item"],
            }
            if solution
            else None
        )
    return sorted(documents, key=document_sort_key)


def build_console_data(progress_path: Path | None = DEFAULT_PROGRESS) -> dict[str, Any]:
    learning_status = load_module("ui_learning_status", PROJECT_ROOT / "labs" / "learning_status.py")
    prompt_lab = load_module("ui_prompt_lab", PROJECT_ROOT / "implementations" / "01-prompt-lab" / "main.py")
    rag = load_module("ui_rag_assistant", PROJECT_ROOT / "implementations" / "04-rag-assistant" / "main.py")
    research_agent = load_module("ui_research_agent", PROJECT_ROOT / "implementations" / "05-research-agent" / "research_agent.py")
    eval_lab = load_module("ui_eval_lab", PROJECT_ROOT / "implementations" / "08-eval-lab" / "eval_lab.py")

    progress = learning_status.load_progress(progress_path if progress_path and progress_path.exists() else None)
    stages = learning_status.discover_stages(PROJECT_ROOT)
    statuses = learning_status.summarize_statuses(stages, progress)
    next_status = learning_status.choose_next_status(statuses)
    lesson_documents = build_lesson_documents(learning_status, statuses)

    library = prompt_lab.PromptLibrary()
    checker = prompt_lab.PromptQualityChecker()
    prompt_templates = []
    for name in library.list_templates():
        template = library.get_template(name)
        rendered = template.render(DEFAULT_PROMPT_INPUT)
        prompt_templates.append(
            {
                "name": template.name,
                "description": template.description,
                "role": template.role,
                "task": template.task,
                "context": template.context,
                "constraints": template.constraints,
                "outputFormat": template.output_format,
                "acceptanceCriteria": template.acceptance_criteria,
                "samplePrompt": rendered,
                "sampleScore": checker.check(rendered),
                "sampleOutput": prompt_lab.MockPromptRunner().run(name, DEFAULT_PROMPT_INPUT),
            }
        )

    documents = rag.load_documents()
    chunks = rag.chunk_documents(documents)
    rag_results = rag.search(DEFAULT_RAG_QUERY, chunks, top_k=4)

    agent = research_agent.ResearchAgent(registry=research_agent.build_default_registry(), max_iterations=4)
    agent_result = agent.run(DEFAULT_AGENT_TOPIC)

    cases = eval_lab.load_golden_cases()
    eval_results = eval_lab.run_eval(cases)
    eval_summary = eval_lab.summarize_results(eval_results)

    return {
        "meta": {
            "title": "AI-Agent-Learn Teaching Console",
            "generatedFrom": str(PROJECT_ROOT),
            "progressFile": str(progress_path.relative_to(PROJECT_ROOT)) if progress_path and progress_path.exists() else "",
        },
        "dashboard": {
            "stages": [
                {
                    "slug": status.stage.slug,
                    "title": status.stage.title,
                    "completed": status.completed_count,
                    "total": status.total_count,
                    "percent": status.percent,
                    "nextItem": status.next_item,
                    "note": status.note,
                    "demoCommand": learning_status.DEMO_COMMANDS.get(status.stage.slug, ""),
                    "lessonPath": f"lessons/{status.stage.slug}",
                }
                for status in statuses
            ],
            "next": {
                "slug": next_status.stage.slug,
                "title": next_status.stage.title,
                "actions": learning_status.next_actions(next_status),
            }
            if next_status
            else None,
        },
        "reader": {
            "documents": lesson_documents,
            "defaultDocumentId": lesson_documents[0]["id"] if lesson_documents else "",
            "collections": [
                {"slug": slug, "title": title, "count": sum(1 for document in lesson_documents if document["collectionSlug"] == slug)}
                for slug, title in dict((document["collectionSlug"], document["collectionTitle"]) for document in lesson_documents).items()
            ],
        },
        "prompt": {
            "defaultInput": DEFAULT_PROMPT_INPUT,
            "templates": prompt_templates,
            "qualityMarkers": prompt_lab.PromptQualityChecker.markers,
        },
        "rag": {
            "defaultQuery": DEFAULT_RAG_QUERY,
            "documents": [{"title": document.title, "path": str(document.path.relative_to(PROJECT_ROOT))} for document in documents],
            "chunks": [
                {
                    "id": chunk.id,
                    "text": chunk.text,
                    "source": chunk.metadata["source"],
                    "title": chunk.metadata["title"],
                    "section": chunk.metadata["section"],
                    "paragraph": chunk.metadata["paragraph"],
                }
                for chunk in chunks
            ],
            "sampleResults": [
                {
                    "id": result.chunk.id,
                    "score": result.score,
                    "matchedTerms": result.matched_terms,
                    "text": result.chunk.text,
                    "citation": result.chunk.citation(),
                }
                for result in rag_results
            ],
        },
        "agent": {
            "topic": agent_result.topic,
            "plan": agent_result.plan,
            "toolLog": [
                {
                    "iteration": call.iteration,
                    "toolName": call.tool_name,
                    "toolInput": call.tool_input,
                    "observation": call.observation,
                }
                for call in agent_result.tool_log
            ],
            "stoppedByLimit": agent_result.stopped_by_limit,
        },
        "eval": {
            "summary": {
                "total": eval_summary["total"],
                "averageScore": eval_summary["average_score"],
                "accuracy": eval_summary["accuracy"],
                "hallucinationRate": eval_summary["hallucination_rate"],
                "averageLatencyMs": eval_summary["average_latency_ms"],
                "totalTokens": eval_summary["total_tokens"],
            },
            "results": [
                {
                    "caseId": result.case_id,
                    "category": result.category,
                    "riskLevel": result.risk_level,
                    "question": result.question,
                    "answer": result.answer,
                    "score": result.score,
                    "passed": result.passed,
                    "hallucination": result.hallucination,
                }
                for result in eval_results
            ],
        },
    }


def render_html(data: dict[str, Any]) -> str:
    encoded_data = json.dumps(data, ensure_ascii=False, indent=2).replace("</", "<\\/")
    title = html.escape(data["meta"]["title"])
    template = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>__TITLE__</title>
  <style>
    :root {{
      --paper: #f7f4ec;
      --ink: #20201d;
      --muted: #6b695f;
      --line: #d8d1c1;
      --panel: #fffcf4;
      --field: #f1eadc;
      --green: #1f7a5a;
      --green-soft: #dff0e7;
      --blue: #2458a7;
      --blue-soft: #dce8f8;
      --red: #b43d32;
      --red-soft: #f5dfdc;
      --gold: #b7791f;
      --shadow: 0 16px 36px rgba(32, 32, 29, 0.12);
    }}

    * {{
      box-sizing: border-box;
    }}

    body {{
      margin: 0;
      background:
        linear-gradient(90deg, rgba(32, 32, 29, 0.035) 1px, transparent 1px),
        linear-gradient(0deg, rgba(32, 32, 29, 0.035) 1px, transparent 1px),
        var(--paper);
      background-size: 28px 28px;
      color: var(--ink);
      font-family: "Avenir Next", "Trebuchet MS", "PingFang SC", sans-serif;
    }}

    button, input, textarea, select {{
      font: inherit;
    }}

    .shell {{
      min-height: 100vh;
      display: grid;
      grid-template-columns: 300px minmax(0, 1fr);
    }}

    .rail {{
      border-right: 1px solid var(--line);
      background: rgba(255, 252, 244, 0.86);
      backdrop-filter: blur(10px);
      padding: 24px;
      position: sticky;
      top: 0;
      height: 100vh;
      overflow: auto;
    }}

    .brand {{
      display: grid;
      gap: 8px;
      margin-bottom: 28px;
    }}

    .brand-mark {{
      width: 52px;
      height: 52px;
      display: grid;
      place-items: center;
      border: 2px solid var(--ink);
      background: var(--green-soft);
      box-shadow: 5px 5px 0 var(--ink);
      font-family: Georgia, "Times New Roman", serif;
      font-size: 25px;
      font-weight: 700;
    }}

    h1, h2, h3 {{
      margin: 0;
      font-family: Georgia, "Times New Roman", "Songti SC", serif;
      letter-spacing: 0;
    }}

    h1 {{
      font-size: 28px;
      line-height: 1.08;
    }}

    h2 {{
      font-size: 30px;
      line-height: 1.1;
    }}

    h3 {{
      font-size: 18px;
    }}

    p {{
      margin: 0;
      line-height: 1.65;
      color: var(--muted);
    }}

    .tabs {{
      display: grid;
      gap: 8px;
    }}

    .tab-button {{
      min-height: 44px;
      border: 1px solid var(--line);
      background: transparent;
      color: var(--ink);
      text-align: left;
      padding: 10px 12px;
      border-radius: 6px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 10px;
      transition: transform 150ms ease, background 150ms ease, border-color 150ms ease;
    }}

    .tab-button:hover {{
      transform: translateX(2px);
      border-color: var(--ink);
    }}

    .tab-button[aria-selected="true"] {{
      background: var(--ink);
      color: var(--paper);
      border-color: var(--ink);
    }}

    .tab-icon {{
      width: 24px;
      text-align: center;
      font-weight: 700;
    }}

    .main {{
      padding: 28px;
      max-width: 1280px;
      width: 100%;
    }}

    .topbar {{
      display: flex;
      justify-content: space-between;
      gap: 16px;
      align-items: flex-start;
      margin-bottom: 24px;
    }}

    .stamp {{
      border: 1px solid var(--line);
      background: var(--panel);
      border-radius: 6px;
      padding: 10px 12px;
      color: var(--muted);
      font-size: 13px;
      max-width: 460px;
    }}

    .view {{
      display: none;
      animation: rise 260ms ease both;
    }}

    .view.active {{
      display: block;
    }}

    @keyframes rise {{
      from {{ opacity: 0; transform: translateY(8px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}

    .summary-grid {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
      margin: 22px 0;
    }}

    .metric, .panel, .stage-card, .chunk-card, .trace-row, .eval-row {{
      border: 1px solid var(--line);
      background: var(--panel);
      border-radius: 8px;
      box-shadow: 0 1px 0 rgba(32, 32, 29, 0.04);
    }}

    .metric {{
      padding: 16px;
      min-height: 94px;
    }}

    .metric strong {{
      display: block;
      font-size: 28px;
      line-height: 1.1;
      margin-top: 8px;
    }}

    .grid-2 {{
      display: grid;
      grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.1fr);
      gap: 16px;
      align-items: start;
    }}

    .grid-3 {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 12px;
    }}

    .reader-layout {{
      display: grid;
      grid-template-columns: 320px minmax(0, 1fr);
      gap: 16px;
      align-items: start;
    }}

    .reader-tools {{
      display: grid;
      gap: 12px;
      position: sticky;
      top: 24px;
    }}

    .doc-list {{
      display: grid;
      gap: 8px;
      max-height: 360px;
      overflow: auto;
      padding-right: 4px;
    }}

    .doc-button {{
      width: 100%;
      border: 1px solid var(--line);
      background: #fffdf8;
      color: var(--ink);
      border-radius: 6px;
      padding: 10px;
      text-align: left;
      cursor: pointer;
      display: grid;
      gap: 4px;
    }}

    .doc-button:hover, .doc-button.active {{
      border-color: var(--green);
      background: var(--green-soft);
    }}

    .doc-button.done {{
      box-shadow: inset 4px 0 0 var(--green);
    }}

    .article {{
      display: grid;
      gap: 18px;
    }}

    .solution-panel {{
      border: 1px solid var(--line);
      background: var(--blue-soft);
      border-radius: 8px;
      padding: 14px;
      display: none;
      gap: 10px;
    }}

    .solution-panel.visible {{
      display: grid;
    }}

    .route-pill {{
      display: block;
      width: 100%;
      border: 1px dashed var(--blue);
      background: rgba(255, 255, 255, 0.55);
      color: var(--blue);
      border-radius: 6px;
      padding: 8px 10px;
      font-size: 12px;
      word-break: break-all;
    }}

    .article-body {{
      border: 1px solid var(--line);
      background: var(--panel);
      border-radius: 8px;
      padding: 28px;
      line-height: 1.78;
    }}

    .article-body h1, .article-body h2, .article-body h3 {{
      margin-top: 20px;
      margin-bottom: 10px;
    }}

    .article-body h1:first-child, .article-body h2:first-child, .article-body h3:first-child {{
      margin-top: 0;
    }}

    .article-body p, .article-body li {{
      color: var(--ink);
    }}

    .article-body code {{
      background: var(--field);
      border: 1px solid var(--line);
      border-radius: 4px;
      padding: 1px 5px;
    }}

    .article-body table {{
      width: 100%;
      border-collapse: collapse;
      margin: 14px 0;
      font-size: 14px;
    }}

    .article-body th, .article-body td {{
      border: 1px solid var(--line);
      padding: 8px 10px;
      vertical-align: top;
      text-align: left;
    }}

    .article-body th {{
      background: var(--field);
    }}

    .article-body pre code {{
      background: transparent;
      border: 0;
      padding: 0;
    }}

    .note-area {{
      min-height: 160px;
    }}

    .panel {{
      padding: 18px;
    }}

    .section-title {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 14px;
    }}

    .tag {{
      display: inline-flex;
      align-items: center;
      min-height: 24px;
      padding: 2px 8px;
      border-radius: 999px;
      border: 1px solid var(--line);
      background: var(--field);
      color: var(--muted);
      font-size: 12px;
      white-space: nowrap;
    }}

    .stage-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 12px;
      margin-top: 16px;
    }}

    .stage-card {{
      padding: 14px;
      min-height: 170px;
      display: grid;
      gap: 12px;
    }}

    .stage-card.current {{
      border-color: var(--green);
      box-shadow: inset 4px 0 0 var(--green);
    }}

    .bar {{
      height: 10px;
      background: var(--field);
      border-radius: 999px;
      overflow: hidden;
      border: 1px solid var(--line);
    }}

    .bar span {{
      display: block;
      height: 100%;
      background: linear-gradient(90deg, var(--green), var(--blue));
      width: var(--value);
    }}

    .action-list {{
      display: grid;
      gap: 10px;
      padding: 0;
      margin: 0;
      list-style: none;
    }}

    .action-list li {{
      padding: 10px 12px;
      border-left: 4px solid var(--green);
      background: var(--green-soft);
      border-radius: 6px;
    }}

    .control-row {{
      display: flex;
      gap: 10px;
      align-items: center;
      flex-wrap: wrap;
      margin-bottom: 12px;
    }}

    select, input, textarea {{
      width: 100%;
      border: 1px solid var(--line);
      background: #fffdf8;
      color: var(--ink);
      border-radius: 6px;
      padding: 10px 12px;
      outline: none;
    }}

    select:focus, input:focus, textarea:focus {{
      border-color: var(--blue);
      box-shadow: 0 0 0 3px var(--blue-soft);
    }}

    textarea {{
      min-height: 120px;
      resize: vertical;
    }}

    .button {{
      border: 1px solid var(--ink);
      background: var(--ink);
      color: var(--paper);
      border-radius: 6px;
      min-height: 40px;
      padding: 9px 12px;
      cursor: pointer;
    }}

    .button.secondary {{
      background: transparent;
      color: var(--ink);
    }}

    .score-ring {{
      width: 96px;
      height: 96px;
      border-radius: 50%;
      display: grid;
      place-items: center;
      background: conic-gradient(var(--green) calc(var(--score) * 1%), var(--field) 0);
      border: 1px solid var(--line);
      margin: 0 auto 12px;
      position: relative;
    }}

    .score-ring::after {{
      content: "";
      position: absolute;
      inset: 10px;
      background: var(--panel);
      border-radius: 50%;
    }}

    .score-ring strong {{
      position: relative;
      z-index: 1;
      font-size: 22px;
    }}

    pre {{
      margin: 0;
      white-space: pre-wrap;
      word-break: break-word;
      background: #24231f;
      color: #f9f1df;
      border-radius: 8px;
      padding: 16px;
      line-height: 1.58;
      overflow: auto;
      max-height: 460px;
    }}

    .chunk-list, .trace-list, .eval-list {{
      display: grid;
      gap: 10px;
    }}

    .chunk-card {{
      padding: 14px;
      display: grid;
      gap: 8px;
    }}

    .chunk-meta {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      align-items: center;
    }}

    .trace-row {{
      display: grid;
      grid-template-columns: 92px minmax(0, 1fr);
      gap: 12px;
      padding: 14px;
      align-items: start;
    }}

    .trace-index {{
      font-weight: 700;
      color: var(--blue);
    }}

    .eval-row {{
      display: grid;
      grid-template-columns: 90px 110px 80px minmax(0, 1fr);
      gap: 12px;
      padding: 12px;
      align-items: start;
    }}

    .pass {{
      color: var(--green);
      font-weight: 700;
    }}

    .fail {{
      color: var(--red);
      font-weight: 700;
    }}

    .mini-map {{
      display: grid;
      grid-template-columns: repeat(9, 1fr);
      gap: 6px;
      margin-top: 14px;
    }}

    .mini-map span {{
      aspect-ratio: 1;
      border: 1px solid var(--line);
      border-radius: 4px;
      background: var(--field);
      position: relative;
    }}

    .mini-map span::after {{
      content: "";
      position: absolute;
      inset: auto 0 0;
      height: var(--value);
      background: var(--green);
      border-radius: 0 0 3px 3px;
    }}

    @media (max-width: 920px) {{
      .shell {{
        grid-template-columns: 1fr;
      }}

      .rail {{
        position: static;
        height: auto;
        border-right: 0;
        border-bottom: 1px solid var(--line);
      }}

      .tabs {{
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }}

      .topbar, .grid-2, .grid-3, .summary-grid, .reader-layout {{
        grid-template-columns: 1fr;
        display: grid;
      }}

      .reader-tools {{
        position: static;
      }}

      .eval-row, .trace-row {{
        grid-template-columns: 1fr;
      }}
    }}
  </style>
</head>
<body>
  <div class="shell">
    <aside class="rail">
      <div class="brand">
        <div class="brand-mark">AI</div>
        <h1>Teaching Console</h1>
        <p>本地教学控制台：把路线、实验、检索、Agent 轨迹和评测放到一个可观察界面。</p>
      </div>
      <nav class="tabs" aria-label="教学控制台视图">
        <button class="tab-button" data-view="dashboard" aria-selected="true"><span class="tab-icon">01</span>学习路线</button>
        <button class="tab-button" data-view="reader"><span class="tab-icon">02</span>课程阅读</button>
        <button class="tab-button" data-view="prompt"><span class="tab-icon">03</span>Prompt Lab</button>
        <button class="tab-button" data-view="rag"><span class="tab-icon">04</span>RAG 检索</button>
        <button class="tab-button" data-view="agent"><span class="tab-icon">05</span>Agent Trace</button>
        <button class="tab-button" data-view="eval"><span class="tab-icon">06</span>Eval 面板</button>
      </nav>
    </aside>
    <main class="main">
      <div class="topbar">
        <div>
          <h2>AI-Agent-Learn 本地教学 GUI</h2>
          <p>面向学习者的离线控制台。先看路线，再进入 Prompt、RAG、Agent、Eval 的可视化实验。</p>
        </div>
        <div class="stamp" id="sourceStamp"></div>
      </div>

      <section id="dashboard" class="view active"></section>
      <section id="reader" class="view"></section>
      <section id="prompt" class="view"></section>
      <section id="rag" class="view"></section>
      <section id="agent" class="view"></section>
      <section id="eval" class="view"></section>
    </main>
  </div>

  <script id="console-data" type="application/json">__CONSOLE_DATA__</script>
  <script>
    const data = JSON.parse(document.getElementById("console-data").textContent);
    const $ = (selector, root = document) => root.querySelector(selector);
    const escapeHtml = (value) => String(value)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");

    document.getElementById("sourceStamp").innerHTML =
      `<strong>Source</strong><br>${escapeHtml(data.meta.generatedFrom)}<br>` +
      `${data.meta.progressFile ? `Progress: ${escapeHtml(data.meta.progressFile)}` : "Progress: default empty state"}`;

    const storageKey = "ai-agent-learn-console-state";
    let learningState = loadLearningState();

    function loadLearningState() {{
      try {{
        return JSON.parse(localStorage.getItem(storageKey)) || {{ completedDocs: {{}}, notes: {{}} }};
      }} catch (error) {{
        return {{ completedDocs: {{}}, notes: {{}} }};
      }}
    }}

    function saveLearningState() {{
      localStorage.setItem(storageKey, JSON.stringify(learningState));
    }}

    function showView(viewId, updateHash = true) {{
      document.querySelectorAll(".tab-button").forEach((item) => item.setAttribute("aria-selected", item.dataset.view === viewId ? "true" : "false"));
      document.querySelectorAll(".view").forEach((view) => view.classList.toggle("active", view.id === viewId));
      if (updateHash) {{
        setRoute(`/${viewId}`);
      }}
    }}

    function routeForDocument(documentId) {{
      return `#/reader/${encodeURIComponent(documentId)}`;
    }}

    function setRoute(route) {{
      const nextHash = route.startsWith("#") ? route : `#${route}`;
      if (location.hash !== nextHash) {{
        history.pushState(null, "", nextHash);
      }}
    }}

    function applyRoute() {{
      const hash = location.hash || "#/dashboard";
      const parts = hash.replace(/^#\\/?/, "").split("/");
      const view = parts[0] || "dashboard";
      if (view === "reader" && parts[1]) {{
        openReaderDocument(decodeURIComponent(parts.slice(1).join("/")), false);
        return;
      }}
      const knownViews = new Set(["dashboard", "reader", "prompt", "rag", "agent", "eval"]);
      showView(knownViews.has(view) ? view : "dashboard", false);
    }}

    document.querySelectorAll(".tab-button").forEach((button) => {{
      button.addEventListener("click", () => {{
        if (button.dataset.view === "reader") {{
          const currentDoc = $("#readerDoc")?.value || data.reader.defaultDocumentId;
          setRoute(`/reader/${encodeURIComponent(currentDoc)}`);
          applyRoute();
        }} else {{
          showView(button.dataset.view);
        }}
      }});
    }});
    window.addEventListener("hashchange", applyRoute);

    function renderDashboard() {{
      const stages = data.dashboard.stages;
      const completed = stages.filter((stage) => stage.percent === 100).length;
      const average = Math.round(stages.reduce((sum, stage) => sum + stage.percent, 0) / stages.length);
      const next = data.dashboard.next;
      document.getElementById("dashboard").innerHTML = `
        <div class="summary-grid">
          <div class="metric"><span class="tag">Stages</span><strong>${stages.length}</strong><p>课程阶段</p></div>
          <div class="metric"><span class="tag">Done</span><strong>${completed}</strong><p>已完成阶段</p></div>
          <div class="metric"><span class="tag">Progress</span><strong>${average}%</strong><p>平均完成度</p></div>
          <div class="metric"><span class="tag">Next</span><strong>${escapeHtml(next ? next.slug.slice(0, 2) : "--")}</strong><p>${escapeHtml(next ? next.title : "暂无")}</p></div>
        </div>
        <div class="grid-2">
          <div class="panel">
            <div class="section-title"><h3>推荐下一步</h3><span class="tag">${escapeHtml(next ? next.slug : "complete")}</span></div>
            <ul class="action-list">${(next ? next.actions : ["所有阶段已完成，进入复盘。"]).map((action) => `<li>${escapeHtml(action)}</li>`).join("")}</ul>
          </div>
          <div class="panel">
            <div class="section-title"><h3>阶段热力图</h3><span class="tag">completion</span></div>
            <div class="mini-map">${stages.map((stage) => `<span title="${escapeHtml(stage.slug)} ${stage.percent}%" style="--value:${stage.percent}%"></span>`).join("")}</div>
            <p style="margin-top:14px">每个小格代表一个阶段，填充高度代表完成度。它刻意简单，方便课堂上解释“先完成闭环，再追求扩展”。</p>
          </div>
        </div>
        <div class="stage-grid">
          ${stages.map((stage) => `
            <article class="stage-card ${next && next.slug === stage.slug ? "current" : ""}">
              <div class="section-title"><h3>${escapeHtml(stage.title)}</h3><span class="tag">${stage.percent}%</span></div>
              <div class="bar" aria-label="${escapeHtml(stage.slug)} progress"><span style="--value:${stage.percent}%"></span></div>
              <p>下一项：${escapeHtml(stage.nextItem)}</p>
              <p>${escapeHtml(stage.demoCommand || stage.lessonPath)}</p>
              <button class="button secondary" data-open-stage="${escapeHtml(stage.slug)}">在 UI 中学习</button>
            </article>
          `).join("")}
        </div>
      `;
      document.querySelectorAll("[data-open-stage]").forEach((button) => {{
        button.addEventListener("click", () => {{
          $("#readerStage").value = button.dataset.openStage;
          updateReaderStage();
          const currentDoc = $("#readerDoc").value;
          setRoute(`/reader/${encodeURIComponent(currentDoc)}`);
          showView("reader", false);
        }});
      }});
    }}

    function renderReader() {{
      const documents = data.reader.documents;
      const collections = data.reader.collections;
      document.getElementById("reader").innerHTML = `
        <div class="reader-layout">
          <aside class="reader-tools">
            <div class="panel">
              <div class="section-title"><h3>课程阅读器</h3><span class="tag">${documents.length} docs</span></div>
              <label>资料集合</label>
              <select id="readerStage">${collections.map((collection) => `<option value="${escapeHtml(collection.slug)}">${escapeHtml(collection.title)} (${collection.count})</option>`).join("")}</select>
              <label style="display:block;margin-top:12px">文档</label>
              <select id="readerDoc"></select>
              <label style="display:block;margin-top:12px">搜索</label>
              <input id="readerSearch" placeholder="搜索标题、路径或正文关键词">
              <div class="control-row" style="margin-top:12px">
                <button class="button" id="completeDocButton">标记已读</button>
                <button class="button secondary" id="exportProgressButton">导出进度</button>
              </div>
            </div>
            <div class="panel">
              <div class="section-title"><h3>阶段文档</h3><span class="tag" id="readerStageCount">0/0</span></div>
              <div class="doc-list" id="readerDocList"></div>
            </div>
            <div class="panel">
              <div class="section-title"><h3>学习笔记</h3><span class="tag">local</span></div>
              <textarea id="readerNote" class="note-area" placeholder="写下卡点、复述、下一步实验。"></textarea>
            </div>
          </aside>
          <article class="article">
            <div class="panel">
              <div class="section-title">
                <h3 id="readerTitle">课程文档</h3>
                <span class="tag" id="readerMeta"></span>
              </div>
              <p id="readerExcerpt"></p>
            </div>
            <div class="solution-panel" id="readerSolutionPanel"></div>
            <div class="article-body" id="readerBody"></div>
          </article>
        </div>
      `;
      $("#readerStage").addEventListener("change", updateReaderStage);
      $("#readerDoc").addEventListener("change", updateReaderDocument);
      $("#readerSearch").addEventListener("input", updateReaderStage);
      $("#completeDocButton").addEventListener("click", toggleCurrentDocumentDone);
      $("#exportProgressButton").addEventListener("click", exportProgress);
      $("#readerNote").addEventListener("input", () => {{
        const documentId = $("#readerDoc").value;
        learningState.notes[documentId] = $("#readerNote").value;
        saveLearningState();
      }});
      const nextSlug = data.dashboard.next ? data.dashboard.next.slug : collections[0].slug;
      $("#readerStage").value = nextSlug;
      updateReaderStage();
    }}

    function docsForStage(stageSlug) {{
      const query = ($("#readerSearch")?.value || "").trim().toLowerCase();
      return data.reader.documents.filter((doc) => {{
        const inCollection = doc.collectionSlug === stageSlug;
        if (!inCollection) return false;
        if (!query) return true;
        return `${doc.title} ${doc.path} ${doc.excerpt} ${doc.content}`.toLowerCase().includes(query);
      }});
    }}

    function updateReaderStage() {{
      const stageSlug = $("#readerStage").value;
      const documents = docsForStage(stageSlug);
      $("#readerDoc").innerHTML = documents.map((doc) => `<option value="${escapeHtml(doc.id)}">${escapeHtml(doc.item)} - ${escapeHtml(doc.title)}</option>`).join("");
      $("#readerDoc").value = documents[0] ? documents[0].id : "";
      updateReaderDocument();
    }}

    function openReaderDocument(documentId, updateHash = true) {{
      const doc = data.reader.documents.find((item) => item.id === documentId);
      if (!doc) return;
      showView("reader", false);
      $("#readerStage").value = doc.collectionSlug;
      $("#readerSearch").value = "";
      const documents = docsForStage(doc.collectionSlug);
      $("#readerDoc").innerHTML = documents.map((item) => `<option value="${escapeHtml(item.id)}">${escapeHtml(item.item)} - ${escapeHtml(item.title)}</option>`).join("");
      $("#readerDoc").value = doc.id;
      updateReaderDocument();
      if (updateHash) setRoute(`/reader/${encodeURIComponent(doc.id)}`);
    }}

    function updateReaderDocument() {{
      const documentId = $("#readerDoc").value;
      const doc = data.reader.documents.find((item) => item.id === documentId);
      if (!doc) {{
        $("#readerTitle").textContent = "没有匹配文档";
        $("#readerMeta").textContent = "";
        $("#readerExcerpt").textContent = "换一个资料集合或清空搜索关键词。";
        $("#readerBody").innerHTML = "";
        $("#readerDocList").innerHTML = "";
        return;
      }}
      const stageDocs = docsForStage(doc.collectionSlug);
      const doneCount = stageDocs.filter((item) => learningState.completedDocs[item.id]).length;
      $("#readerStageCount").textContent = `${doneCount}/${stageDocs.length}`;
      $("#readerTitle").textContent = doc.title;
      $("#readerMeta").textContent = `${doc.path} · ${doc.estimatedMinutes} min`;
      $("#readerExcerpt").textContent = doc.excerpt;
      updateSolutionPanel(doc);
      $("#readerBody").innerHTML = renderMarkdown(doc.content, doc);
      $("#readerNote").value = learningState.notes[doc.id] || "";
      $("#completeDocButton").textContent = learningState.completedDocs[doc.id] ? "取消已读" : "标记已读";
      $("#readerDocList").innerHTML = stageDocs.map((item) => `
        <button class="doc-button ${item.id === doc.id ? "active" : ""} ${learningState.completedDocs[item.id] ? "done" : ""}" data-doc-id="${escapeHtml(item.id)}">
          <strong>${escapeHtml(item.item)} · ${escapeHtml(item.title)}</strong>
          <span>${escapeHtml(item.path)} · ${item.estimatedMinutes} min</span>
        </button>
      `).join("");
      document.querySelectorAll("[data-doc-id]").forEach((button) => {{
        button.addEventListener("click", () => {{
          $("#readerDoc").value = button.dataset.docId;
          updateReaderDocument();
          setRoute(`/reader/${encodeURIComponent(button.dataset.docId)}`);
        }});
      }});
      document.querySelectorAll("[data-doc-link]").forEach((link) => {{
        link.addEventListener("click", (event) => {{
          event.preventDefault();
          openReaderDocument(link.dataset.docLink);
        }});
      }});
    }}

    function updateSolutionPanel(doc) {{
      const panel = $("#readerSolutionPanel");
      const sourceDoc = data.reader.documents.find((item) => item.solutionPath === doc.path);
      if (doc.solution) {{
        const route = routeForDocument(doc.solution.id);
        panel.classList.add("visible");
        panel.innerHTML = `
          <div class="section-title"><h3>对应答案</h3><span class="tag">solution route</span></div>
          <p>${escapeHtml(doc.solution.title)} · ${escapeHtml(doc.solution.path)}</p>
          <code class="route-pill">${escapeHtml(route)}</code>
          <div class="control-row">
            <button class="button" id="openSolutionButton">打开答案</button>
          </div>
        `;
        $("#openSolutionButton").addEventListener("click", () => openReaderDocument(doc.solution.id));
        return;
      }}
      if (sourceDoc) {{
        const route = routeForDocument(sourceDoc.id);
        panel.classList.add("visible");
        panel.innerHTML = `
          <div class="section-title"><h3>对应章节</h3><span class="tag">lesson route</span></div>
          <p>${escapeHtml(sourceDoc.title)} · ${escapeHtml(sourceDoc.path)}</p>
          <code class="route-pill">${escapeHtml(route)}</code>
          <div class="control-row">
            <button class="button secondary" id="openSourceLessonButton">返回章节</button>
          </div>
        `;
        $("#openSourceLessonButton").addEventListener("click", () => openReaderDocument(sourceDoc.id));
        return;
      }}
      panel.classList.remove("visible");
      panel.innerHTML = "";
    }}

    function toggleCurrentDocumentDone() {{
      const documentId = $("#readerDoc").value;
      learningState.completedDocs[documentId] = !learningState.completedDocs[documentId];
      if (!learningState.completedDocs[documentId]) delete learningState.completedDocs[documentId];
      saveLearningState();
      updateReaderDocument();
      renderDashboard();
    }}

    function exportProgress() {{
      const completedByStage = {{}};
      data.reader.documents.forEach((doc) => {{
        if (!learningState.completedDocs[doc.id]) return;
        if (!completedByStage[doc.stageSlug]) completedByStage[doc.stageSlug] = {{ completed: [], note: "" }};
        completedByStage[doc.stageSlug].completed.push(doc.item);
      }});
      const notes = Object.entries(learningState.notes)
        .filter(([, note]) => note.trim())
        .map(([documentId, note]) => ({{ documentId, note }}));
      const payload = {{
        exportedFrom: "AI-Agent-Learn Teaching Console",
        stages: completedByStage,
        notes,
      }};
      const blob = new Blob([JSON.stringify(payload, null, 2)], {{ type: "application/json" }});
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = "ai-agent-learn-progress.json";
      link.click();
      URL.revokeObjectURL(url);
    }}

    function renderMarkdown(markdown, currentDoc) {{
      const lines = markdown.replaceAll("\\r\\n", "\\n").split("\\n");
      const htmlParts = [];
      let inCode = false;
      let listOpen = false;
      let orderedListOpen = false;
      let tableRows = [];
      let paragraph = [];

      const flushParagraph = () => {{
        if (!paragraph.length) return;
        htmlParts.push(`<p>${inlineMarkdown(paragraph.join(" "), currentDoc)}</p>`);
        paragraph = [];
      }};
      const closeList = () => {{
        if (!listOpen) return;
        htmlParts.push("</ul>");
        listOpen = false;
      }};
      const closeOrderedList = () => {{
        if (!orderedListOpen) return;
        htmlParts.push("</ol>");
        orderedListOpen = false;
      }};
      const closeLists = () => {{
        closeList();
        closeOrderedList();
      }};
      const flushTable = () => {{
        if (!tableRows.length) return;
        const rows = tableRows
          .map((line) => line.trim().replace(/^\\|/, "").replace(/\\|$/, "").split("|").map((cell) => cell.trim()))
          .filter((cells) => !cells.every((cell) => /^:?-{{3,}}:?$/.test(cell)));
        if (rows.length) {{
          const [header, ...bodyRows] = rows;
          htmlParts.push("<table><thead><tr>" + header.map((cell) => `<th>${inlineMarkdown(cell, currentDoc)}</th>`).join("") + "</tr></thead><tbody>");
          bodyRows.forEach((row) => {{
            htmlParts.push("<tr>" + row.map((cell) => `<td>${inlineMarkdown(cell, currentDoc)}</td>`).join("") + "</tr>");
          }});
          htmlParts.push("</tbody></table>");
        }}
        tableRows = [];
      }};

      for (const line of lines) {{
        if (line.startsWith("```")) {{
          flushParagraph();
          closeLists();
          flushTable();
          if (inCode) {{
            htmlParts.push("</code></pre>");
            inCode = false;
          }} else {{
            htmlParts.push("<pre><code>");
            inCode = true;
          }}
          continue;
        }}
        if (inCode) {{
          htmlParts.push(escapeHtml(line) + "\\n");
          continue;
        }}
        if (!line.trim()) {{
          flushParagraph();
          closeLists();
          flushTable();
          continue;
        }}
        if (line.trim().startsWith("|") && line.includes("|")) {{
          flushParagraph();
          closeLists();
          tableRows.push(line);
          continue;
        }}
        flushTable();
        const heading = line.match(/^(#{1,4})\\s+(.+)$/);
        if (heading) {{
          flushParagraph();
          closeLists();
          const level = Math.min(heading[1].length, 3);
          htmlParts.push(`<h${level}>${inlineMarkdown(heading[2], currentDoc)}</h${level}>`);
          continue;
        }}
        const bullet = line.match(/^[-*]\\s+(.+)$/);
        if (bullet) {{
          flushParagraph();
          closeOrderedList();
          if (!listOpen) {{
            htmlParts.push("<ul>");
            listOpen = true;
          }}
          htmlParts.push(`<li>${inlineMarkdown(bullet[1], currentDoc)}</li>`);
          continue;
        }}
        const numbered = line.match(/^\\d+\\.\\s+(.+)$/);
        if (numbered) {{
          flushParagraph();
          closeList();
          if (!orderedListOpen) {{
            htmlParts.push("<ol>");
            orderedListOpen = true;
          }}
          htmlParts.push(`<li>${inlineMarkdown(numbered[1], currentDoc)}</li>`);
          continue;
        }}
        paragraph.push(line.trim());
      }}
      flushParagraph();
      closeLists();
      flushTable();
      if (inCode) htmlParts.push("</code></pre>");
      return htmlParts.join("");
    }}

    function inlineMarkdown(text, currentDoc) {{
      return escapeHtml(text)
        .replace(/`([^`]+)`/g, "<code>$1</code>")
        .replace(/\\*\\*([^*]+)\\*\\*/g, "<strong>$1</strong>")
        .replace(/\\[([^\\]]+)\\]\\(([^)]+)\\)/g, (_match, label, href) => buildMarkdownLink(label, href, currentDoc));
    }}

    function buildMarkdownLink(label, href, currentDoc) {{
      const target = resolveDocumentLink(href, currentDoc);
      if (target) {{
        return `<a href="${escapeHtml(routeForDocument(target.id))}" data-doc-link="${escapeHtml(target.id)}" title="${escapeHtml(target.path)}">${label}</a>`;
      }}
      return `<a href="${escapeHtml(href)}">${label}</a>`;
    }}

    function resolveDocumentLink(href, currentDoc) {{
      if (!href || href.startsWith("#") || href.startsWith("http://") || href.startsWith("https://") || href.startsWith("mailto:")) return null;
      const withoutAnchor = href.split("#")[0];
      if (!withoutAnchor) return null;
      const baseParts = currentDoc.path.split("/").slice(0, -1);
      const rawParts = (withoutAnchor.startsWith("/") ? withoutAnchor.slice(1) : [...baseParts, withoutAnchor].join("/")).split("/");
      const normalized = [];
      rawParts.forEach((part) => {{
        if (!part || part === ".") return;
        if (part === "..") normalized.pop();
        else normalized.push(part);
      }});
      const candidate = normalized.join("/");
      const candidates = [
        candidate,
        candidate.endsWith("/") ? `${candidate}README.md` : `${candidate}/README.md`,
        candidate.endsWith(".md") ? candidate : `${candidate}.md`,
      ];
      return data.reader.documents.find((doc) => candidates.includes(doc.id)) || null;
    }}

    function renderPrompt() {{
      const templates = data.prompt.templates;
      document.getElementById("prompt").innerHTML = `
        <div class="grid-2">
          <div class="panel">
            <div class="section-title"><h3>Prompt 结构实验</h3><span class="tag">offline</span></div>
            <label>模板</label>
            <select id="promptTemplate">${templates.map((template) => `<option value="${escapeHtml(template.name)}">${escapeHtml(template.name)} - ${escapeHtml(template.description)}</option>`).join("")}</select>
            <label style="display:block;margin-top:12px">输入</label>
            <textarea id="promptInput">${escapeHtml(data.prompt.defaultInput)}</textarea>
            <div class="control-row" style="margin-top:12px">
              <button class="button" id="renderPromptButton">生成结构化 Prompt</button>
              <button class="button secondary" id="resetPromptButton">恢复示例</button>
            </div>
            <div class="grid-3" id="promptScorePanel"></div>
          </div>
          <div class="panel">
            <div class="section-title"><h3>生成结果</h3><span class="tag">structured vs naive</span></div>
            <pre id="promptOutput"></pre>
          </div>
        </div>
      `;
      $("#renderPromptButton").addEventListener("click", updatePrompt);
      $("#resetPromptButton").addEventListener("click", () => {{
        $("#promptInput").value = data.prompt.defaultInput;
        updatePrompt();
      }});
      $("#promptTemplate").addEventListener("change", updatePrompt);
      updatePrompt();
    }}

    function buildPrompt(template, userInput) {{
      const bullets = (items) => items.map((item) => `- ${item}`).join("\\n");
      return `角色：${template.role}
任务：${template.task}
上下文：${template.context}

输入：
${userInput.trim()}

约束：
${bullets(template.constraints)}

输出格式：
${template.outputFormat}

验收标准：
${bullets(template.acceptanceCriteria)}`;
    }}

    function scorePrompt(prompt) {{
      const markers = data.prompt.qualityMarkers;
      const passed = Object.entries(markers).filter(([, marker]) => prompt.includes(marker)).map(([name]) => name);
      const score = Math.round((passed.length / Object.keys(markers).length) * 100);
      return {{ score, passed, missing: Object.keys(markers).filter((name) => !passed.includes(name)) }};
    }}

    function updatePrompt() {{
      const template = data.prompt.templates.find((item) => item.name === $("#promptTemplate").value);
      const input = $("#promptInput").value || data.prompt.defaultInput;
      const structured = buildPrompt(template, input);
      const naive = `帮我处理一下：${input}`;
      const structuredScore = scorePrompt(structured);
      const naiveScore = scorePrompt(naive);
      $("#promptScorePanel").innerHTML = `
        <div class="metric"><div class="score-ring" style="--score:${structuredScore.score}"><strong>${structuredScore.score}</strong></div><p>结构化 Prompt 得分</p></div>
        <div class="metric"><div class="score-ring" style="--score:${naiveScore.score}"><strong>${naiveScore.score}</strong></div><p>随口 Prompt 得分</p></div>
        <div class="metric"><span class="tag">Missing</span><strong>${naiveScore.missing.length}</strong><p>随口 Prompt 缺失结构项</p></div>
      `;
      $("#promptOutput").textContent = `${structured}\\n\\n--- Mock 输出 ---\\n${template.sampleOutput}`;
    }}

    function renderRag() {{
      document.getElementById("rag").innerHTML = `
        <div class="grid-2">
          <div class="panel">
            <div class="section-title"><h3>RAG 检索可视化</h3><span class="tag">${data.rag.documents.length} docs / ${data.rag.chunks.length} chunks</span></div>
            <label>问题</label>
            <input id="ragQuery" value="${escapeHtml(data.rag.defaultQuery)}">
            <div class="control-row" style="margin-top:12px">
              <button class="button" id="searchRagButton">检索本地知识库</button>
              <button class="button secondary" data-query="RAG 为什么需要引用">RAG 引用</button>
              <button class="button secondary" data-query="MCP 解决什么问题">MCP</button>
            </div>
            <div class="panel" style="box-shadow:none;background:var(--field);margin-top:12px">
              <h3>文档来源</h3>
              <p>${data.rag.documents.map((doc) => `${escapeHtml(doc.title)}（${escapeHtml(doc.path)}）`).join("；")}</p>
            </div>
          </div>
          <div class="panel">
            <div class="section-title"><h3>检索结果</h3><span class="tag">top 4</span></div>
            <div class="chunk-list" id="ragResults"></div>
          </div>
        </div>
      `;
      $("#searchRagButton").addEventListener("click", updateRag);
      document.querySelectorAll("[data-query]").forEach((button) => {{
        button.addEventListener("click", () => {{
          $("#ragQuery").value = button.dataset.query;
          updateRag();
        }});
      }});
      updateRag();
    }}

    function tokenize(text) {{
      const lowered = text.toLowerCase();
      const terms = [];
      for (const match of lowered.matchAll(/[a-z0-9]+/g)) {{
        if (match[0].length > 1) terms.push(match[0]);
      }}
      for (const match of text.matchAll(/[\\u4e00-\\u9fff]+/g)) {{
        const span = match[0];
        if (span.length <= 6) terms.push(span);
        for (const size of [2, 3]) {{
          for (let index = 0; index <= span.length - size; index += 1) {{
            terms.push(span.slice(index, index + size));
          }}
        }}
      }}
      return [...new Set(terms.filter((term) => !["什么", "是什么", "怎么", "如何", "以及", "一个"].includes(term)))];
    }}

    function updateRag() {{
      const query = $("#ragQuery").value;
      const terms = tokenize(query);
      const results = data.rag.chunks
        .map((chunk) => {{
          const haystack = `${chunk.text} ${chunk.title} ${chunk.section} ${chunk.source}`.toLowerCase();
          const matched = terms.filter((term) => haystack.includes(term.toLowerCase()));
          const score = matched.length ? matched.length * 2 + (matched.some((term) => chunk.section.includes(term)) ? 1 : 0) : 0;
          return {{ chunk, matched, score }};
        }})
        .filter((result) => result.score > 0)
        .sort((a, b) => b.score - a.score || a.chunk.id.localeCompare(b.chunk.id))
        .slice(0, 4);
      $("#ragResults").innerHTML = results.length ? results.map((result, index) => `
        <article class="chunk-card">
          <div class="chunk-meta">
            <span class="tag">#${index + 1}</span>
            <span class="tag">${escapeHtml(result.chunk.id)}</span>
            <span class="tag">score ${result.score}</span>
            <span class="tag">${escapeHtml(result.chunk.source)} > ${escapeHtml(result.chunk.section)}</span>
          </div>
          <p>${escapeHtml(result.chunk.text)}</p>
          <p>命中词：${escapeHtml(result.matched.join(", ") || "-")}</p>
        </article>
      `).join("") : `<p>没有检索到相关 chunk。可以换一个问题，或补充 data/docs。</p>`;
    }}

    function renderAgent() {{
      const toolLog = data.agent.toolLog;
      document.getElementById("agent").innerHTML = `
        <div class="grid-2">
          <div class="panel">
            <div class="section-title"><h3>研究计划</h3><span class="tag">${escapeHtml(data.agent.topic)}</span></div>
            <ul class="action-list">${data.agent.plan.map((step) => `<li>${escapeHtml(step)}</li>`).join("")}</ul>
          </div>
          <div class="panel">
            <div class="section-title"><h3>执行轨迹</h3><span class="tag">${toolLog.length} tool calls</span></div>
            <div class="trace-list">${toolLog.map((call) => `
              <article class="trace-row">
                <div class="trace-index">Step ${call.iteration}</div>
                <div>
                  <h3>${escapeHtml(call.toolName)}(${escapeHtml(call.toolInput)})</h3>
                  <p>${escapeHtml(call.observation)}</p>
                </div>
              </article>
            `).join("")}</div>
          </div>
        </div>
      `;
    }}

    function renderEval() {{
      const summary = data.eval.summary;
      const results = data.eval.results;
      document.getElementById("eval").innerHTML = `
        <div class="summary-grid">
          <div class="metric"><span class="tag">Cases</span><strong>${summary.total}</strong><p>测试用例</p></div>
          <div class="metric"><span class="tag">Score</span><strong>${summary.averageScore}</strong><p>平均分</p></div>
          <div class="metric"><span class="tag">Accuracy</span><strong>${Math.round(summary.accuracy * 100)}%</strong><p>通过率</p></div>
          <div class="metric"><span class="tag">Risk</span><strong>${results.filter((item) => item.riskLevel === "high").length}</strong><p>高风险样例</p></div>
        </div>
        <div class="panel">
          <div class="section-title"><h3>评测明细</h3><span class="tag">${summary.totalTokens} estimated tokens</span></div>
          <div class="eval-list">${results.map((result) => `
            <article class="eval-row">
              <div><span class="tag">${escapeHtml(result.caseId)}</span></div>
              <div>${escapeHtml(result.category)}<br><span class="tag">${escapeHtml(result.riskLevel)}</span></div>
              <div class="${result.passed ? "pass" : "fail"}">${result.passed ? "通过" : "失败"}<br>${result.score}/5</div>
              <div><h3>${escapeHtml(result.question)}</h3><p>${escapeHtml(result.answer)}</p></div>
            </article>
          `).join("")}</div>
        </div>
      `;
    }}

    renderDashboard();
    renderReader();
    renderPrompt();
    renderRag();
    renderAgent();
    renderEval();
    applyRoute();
  </script>
</body>
</html>
"""
    return template.replace("__TITLE__", title).replace("__CONSOLE_DATA__", encoded_data).replace("{{", "{").replace("}}", "}")


def write_console(output_path: Path = DEFAULT_OUTPUT, progress_path: Path | None = DEFAULT_PROGRESS) -> Path:
    data = build_console_data(progress_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_html(data), encoding="utf-8")
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="生成 AI-Agent-Learn 本地教学 GUI。")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help=f"输出 HTML 路径，默认：{DEFAULT_OUTPUT}")
    parser.add_argument("--progress", type=Path, default=DEFAULT_PROGRESS, help="可选学习进度 JSON。")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_path = write_console(args.output, args.progress)
    print(f"教学控制台已生成：{output_path}")
    print("可以直接用浏览器打开该 HTML 文件。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
