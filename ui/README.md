# 本地教学 GUI

`ui/` 提供一个离线静态教学控制台，用来把课程路线、课程阅读、Prompt 实验、RAG 检索、Agent 执行轨迹和 Eval 结果放到同一个可视化界面中。

目标是让学习者可以主要在 UI 上完成学习，而不是频繁回到文件目录。

## 生成方式

```bash
make ui
```

默认会生成：

```text
ui/dist/teaching-console.html
```

直接用浏览器打开这个 HTML 文件即可。它不需要 Node.js、不需要后端服务、不调用真实模型，也不会访问网络。

如果你已经维护自己的学习进度 JSON，可以传入：

```bash
make ui PROGRESS=data/notes/learning-progress.example.json
```

## 页面包含什么

- 学习路线：展示 00-08 阶段完成度、下一项和推荐行动。
- 课程阅读：在浏览器里直接阅读根 README、Labs、全部课程阶段、checkpoints、solutions、implementations 说明和 `data/docs` 样例知识库。
- 内部链接：课程 Markdown 里的相对链接会尽量在 UI 内打开对应文档，适合连续阅读。
- 对应答案：练习、练习 Lab、项目、项目 Lab 文档会在正文上方显示“对应答案”，点击即可打开 `solutions/...` 中的答案讲解。
- 路由打开：阅读器支持 `#/reader/<文档路径>`，例如 `#/reader/solutions%2F01-prompt%2F03-exercises.md` 可以直接打开某个答案。
- Prompt Lab：选择模板、输入任务，比较结构化 Prompt 和随口 Prompt 的评分。
- RAG 检索：对本地 `data/docs/*.md` 切分后的 chunk 做浏览器端检索，展示命中词和来源。
- Agent Trace：展示研究 Agent 的计划、工具调用和 observation。
- Eval 面板：展示 golden dataset 的通过率、平均分、高风险样例和明细。

## 在 UI 里直接学习

1. 打开“学习路线”，点击某个阶段卡片里的“在 UI 中学习”。
2. 在“课程阅读”里选择资料集合和文档，也可以用搜索框查找关键词。
3. 点击正文里的课程链接，UI 会打开对应内嵌文档。
4. 做练习或项目时，使用“对应答案”按钮打开答案讲解；答案页也会提供返回章节的入口。
5. 阅读右侧正文，完成后点击“标记已读”。
6. 在“学习笔记”里记录卡点、复述和下一步实验。
7. 点击“导出进度”，得到 `ai-agent-learn-progress.json`，可以作为个人进度备份。

阅读状态和笔记默认保存在浏览器 `localStorage` 中，不会写回仓库。如果换浏览器或清理浏览器数据，需要重新导入或重新记录。

## 设计边界

- 这是教学 GUI，不是产品后台。
- 不保存真实 API Key、cookie、token 或生产数据。
- 已读状态和笔记只保存在当前浏览器本地。
- UI 会内嵌学习 Markdown；如果新增或修改课程内容，需要重新运行 `make ui`。
- 所有模型回答都是 mock 或规则生成，适合解释工程结构。

## 适合课堂怎么用

1. 先打开“学习路线”，让学习者知道当前阶段和下一步。
2. 进入“课程阅读”，读完一个文档后立刻做已读标记和笔记。
3. 用 “Prompt Lab” 演示为什么结构化任务说明更稳定。
4. 用 “RAG 检索” 展示检索不是魔法，而是 chunk、命中词、引用来源。
5. 用 “Agent Trace” 解释计划、工具调用、观察结果的循环。
6. 用 “Eval 面板” 强调 AI 应用上线前需要固定测试集和安全样例。
