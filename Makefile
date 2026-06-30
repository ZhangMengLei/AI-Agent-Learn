.PHONY: help install list demo demo-prompt demo-llm demo-tool demo-rag demo-agent demo-mcp demo-claude-code demo-eval demo-all lint test check-secrets check clean

PYTHON ?= python3
PIP ?= $(PYTHON) -m pip
STAGE ?= 01-prompt
LAB ?= 04-exercises-lab
QUERY ?= Agent 和 Chatbot 区别是什么
LESSON_DIR := lessons/$(STAGE)/$(LAB)

help:
	@printf '%s\n' 'AI-Agent-Learn 常用命令'
	@printf '%s\n' ''
	@printf '%s\n' 'make install                         安装 Python 依赖'
	@printf '%s\n' 'make list                            查看课程、数据、自查清单和可运行实现'
	@printf '%s\n' 'make demo STAGE=01-prompt LAB=04-exercises-lab'
	@printf '%s\n' '                                     检查并运行某个 lesson demo 目录'
	@printf '%s\n' 'make demo-prompt                     运行 Prompt 模板与质量检查 Demo'
	@printf '%s\n' 'make demo-llm                        运行 LLM API 生命周期 Mock Demo'
	@printf '%s\n' 'make demo-tool                       运行 Tool Use 教学 Demo'
	@printf '%s\n' 'make demo-rag QUERY="Agent 和 Chatbot 区别是什么"'
	@printf '%s\n' '                                     运行本地 Markdown RAG Demo'
	@printf '%s\n' 'make demo-agent                      运行研究 Agent Demo（会覆盖报告文件）'
	@printf '%s\n' 'make demo-mcp                        运行 MCP / JSON-RPC Mock Server Demo'
	@printf '%s\n' 'make demo-claude-code                运行 Claude Code 工作流模拟 Demo'
	@printf '%s\n' 'make demo-eval                       运行 Eval Lab Demo（会覆盖报告文件）'
	@printf '%s\n' 'make demo-all                        顺序运行 01-08 全阶段 Demo'
	@printf '%s\n' 'make lint                            编译检查 Python 文件'
	@printf '%s\n' 'make test                            运行 unittest 测试'
	@printf '%s\n' 'make check-secrets                   检查误提交的 .env 和明显密钥字面量'
	@printf '%s\n' 'make check                           运行 lint、test 和 check-secrets'
	@printf '%s\n' 'make clean                           清理缓存和输出目录'

install:
	$(PIP) install -r requirements.txt

list:
	@printf '%s\n' '课程阶段：'
	@find lessons -maxdepth 2 -name README.md | sort
	@printf '%s\n' ''
	@printf '%s\n' '可运行实现：'
	@find implementations -maxdepth 2 -name README.md | sort 2>/dev/null || true
	@printf '%s\n' ''
	@printf '%s\n' '答案讲解：'
	@find solutions -maxdepth 2 -name README.md | sort 2>/dev/null || true
	@printf '%s\n' ''
	@printf '%s\n' '样例数据：'
	@find data -type f | sort 2>/dev/null || true
	@printf '%s\n' ''
	@printf '%s\n' '自查清单：'
	@find checkpoints -type f -name '*.md' | sort 2>/dev/null || true

demo:
	@if [ ! -d "$(LESSON_DIR)" ]; then \
		printf '%s\n' "未找到目录：$(LESSON_DIR)"; \
		exit 1; \
	fi
	@printf '%s\n' "目标 demo 目录：$(LESSON_DIR)"
	@if [ -f "$(LESSON_DIR)/main.py" ]; then \
		$(PYTHON) "$(LESSON_DIR)/main.py"; \
	elif [ -f "$(LESSON_DIR)/app.py" ]; then \
		$(PYTHON) "$(LESSON_DIR)/app.py"; \
	elif [ -f "$(LESSON_DIR)/README.md" ]; then \
		printf '%s\n' '该目录当前以说明文档为主，请阅读 README.md 后按步骤完成练习。'; \
	else \
		printf '%s\n' '未发现 main.py、app.py 或 README.md，请检查该阶段是否已补充 demo。'; \
	fi

demo-prompt:
	$(PYTHON) implementations/01-prompt-lab/main.py --template summarize --input "Prompt 是人与大模型协作时的任务说明书。" --compare

demo-llm:
	$(PYTHON) implementations/02-llm-chat/main.py "解释 streaming 和多轮上下文" --stream --show-log

demo-tool:
	$(PYTHON) implementations/03-tool-assistant/main.py "计算 1 + 2 * 3"

demo-rag:
	$(PYTHON) implementations/04-rag-assistant/main.py "$(QUERY)"

demo-agent:
	$(PYTHON) implementations/05-research-agent/research_agent.py

demo-mcp:
	$(PYTHON) implementations/06-mcp-server/main.py --demo

demo-claude-code:
	$(PYTHON) implementations/07-claude-code-workflow/main.py --scenario bugfix --show-policy

demo-eval:
	$(PYTHON) implementations/08-eval-lab/eval_lab.py

demo-all: demo-prompt demo-llm demo-tool demo-rag demo-agent demo-mcp demo-claude-code demo-eval

lint:
	@if find implementations tests -name '*.py' -print -quit 2>/dev/null | grep -q .; then \
		$(PYTHON) -m compileall -q implementations tests; \
	else \
		printf '%s\n' '未发现 Python 文件，跳过编译检查。'; \
	fi

test:
	@if [ -d tests ]; then \
		$(PYTHON) -m unittest discover -s tests; \
	else \
		printf '%s\n' '未发现 tests 目录，跳过 unittest。'; \
	fi

check-secrets:
	@if find . \( -path './.git' -o -path './.claude' \) -prune -o \( -name .env -o -name '.env.*' \) ! -name '.env.example' -print | grep -q .; then \
		printf '%s\n' 'Do not commit real .env files. Keep only .env.example.'; \
		exit 1; \
	fi
	@if grep -RInE '(^|[^A-Za-z0-9_-])sk-[A-Za-z0-9_-]{20,}|api[_-]?key[[:space:]]*=[[:space:]]*["'"'"'][^"'"'"']+["'"'"']' . --exclude-dir=.git --exclude-dir=.claude; then \
		printf '%s\n' 'Potential secret literal found.'; \
		exit 1; \
	fi

check: lint test check-secrets

clean:
	@find . -type d \( -name '__pycache__' -o -name '.pytest_cache' -o -name '.ruff_cache' -o -name '.mypy_cache' \) -prune -exec rm -rf {} +
	@rm -rf outputs artifacts tmp
	@printf '%s\n' '已清理缓存和本地输出目录。'
