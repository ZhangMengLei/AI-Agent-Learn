# 08 Eval Lab

这是一个面向初学者的最小评测实验工程，只使用 Python 标准库，不调用真实模型。

## 你会看到什么

- `data/eval/golden.jsonl`：固定评测集。
- `mock_answer()`：模拟模型回答，保证课堂演示和 CI 可重复。
- `score_answer()`：用规则命中 expected_points，并处理高风险样例。
- `reports/run-001-report.md`：生成 Markdown 报告。

## 运行方式

在仓库根目录执行：

```bash
python implementations/08-eval-lab/eval_lab.py
```

运行后会生成或覆盖：

```text
implementations/08-eval-lab/reports/run-001-report.md
```

## 学习建议

1. 先新增一条 golden case，观察报告指标变化。
2. 修改 `mock_answer()`，模拟模型变好或变差。
3. 修改 `score_answer()`，理解规则评分的优点和局限。
4. 把这个脚本接入 CI，就能在改 Prompt 后快速发现回归。
