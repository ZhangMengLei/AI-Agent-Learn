.PHONY: help install list demo lint test clean

PYTHON ?= python
PIP ?= $(PYTHON) -m pip
STAGE ?= 01-prompt
LAB ?= 04-exercises-lab
LESSON_DIR := lessons/$(STAGE)/$(LAB)

help:
	@printf '%s\n' 'AI-Agent-Learn 常用命令'
	@printf '%s\n' ''
	@printf '%s\n' 'make install                         安装 Python 依赖'
	@printf '%s\n' 'make list                            查看课程、数据和自查清单'
	@printf '%s\n' 'make demo STAGE=01-prompt LAB=04-exercises-lab'
	@printf '%s\n' '                                     检查并运行某个 demo 目录'
	@printf '%s\n' 'make lint                            编译检查 Python 文件'
	@printf '%s\n' 'make test                            运行 unittest 测试'
	@printf '%s\n' 'make clean                           清理缓存和输出目录'

install:
	$(PIP) install -r requirements.txt

list:
	@printf '%s\n' '课程阶段：'
	@find lessons -maxdepth 2 -name README.md | sort
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

clean:
	@find . -type d \( -name '__pycache__' -o -name '.pytest_cache' -o -name '.ruff_cache' -o -name '.mypy_cache' \) -prune -exec rm -rf {} +
	@rm -rf outputs artifacts tmp
	@printf '%s\n' '已清理缓存和本地输出目录。'
