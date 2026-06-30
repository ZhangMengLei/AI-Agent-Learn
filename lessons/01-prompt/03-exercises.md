# Prompt 练习

## 练习 1：文章总结 Prompt

请写一个 Prompt，要求 AI 总结一篇文章，并按下面格式输出：

```text
一句话总结：
核心要点：
适合谁看：
我的建议：
```

要求：

- 用中文回答
- 不要编造文章中没有的信息
- 面向初学者

## 练习 2：代码解释 Prompt

请写一个 Prompt，要求 AI 给新手解释一段代码。

必须包含：

- 整体作用
- 关键逻辑
- 易错点
- 简化版本

## 练习 3：JSON 信息提取 Prompt

请写一个 Prompt，从用户输入中提取下面字段：

```json
{
  "name": "",
  "job": "",
  "goal": "",
  "keywords": []
}
```

要求：

- 严格输出 JSON
- 不要输出解释
- 缺失字段用 null
- keywords 必须是数组

## 练习 4：对比实验

针对同一个任务，分别写 3 个 Prompt：

1. 简单 Prompt
2. 带角色和任务的 Prompt
3. 带角色、任务、约束和输出格式的 Prompt

比较三次输出的差异。

记录：

```text
任务：
Prompt 1 效果：
Prompt 2 效果：
Prompt 3 效果：
我的结论：
```
