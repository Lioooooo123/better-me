# 设计依据

核对日期：2026-09-05。

技能保存全局指令没有覆盖的专业方法：领域边界、常见错误、必要参考和可执行助手。通用沟通与合作规则保留在 AGENTS.md，不在每个技能重复；不用无条件的审计、计划、委派和评分约束小任务。

[Agent Skills 规范](https://agentskills.io/specification)将元数据、正文和资源分层加载。本仓库用描述定义触发边界，正文保留核心方法，长参考按需打开。同时检查引用中的冲突规则，避免仅把旧问题移进 reference。

[官方技能编写实践](https://agentskills.io/skill-creation/best-practices)强调真实任务的具体知识、故障点与实际评估。这里保留排错证据链、简历真实内容与导出检查、飞书资源类型与分页语义，缩减固定仪式和重复授权。

[OpenAI skills](https://github.com/openai/skills)提供目录和资源组织参考。使用 `skills/<name>/SKILL.md` 与已有 `agents/openai.yaml` 策略，保留原来两个技能的显式调用设置。系统和插件技能继续由上游维护。

[OpenAI 模型指南](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6-astra)用于核对当前模型的任务适配与指令习惯。模型参数不成为技能前置条件，不用历史模型固定流程模板约束全部任务。

联动复用任务上下文：目标、范围、材料、事实、授权、文件和验证状态。只补缺失输入，不强制 JSON 协议或多 Agent。必需依赖仅用于飞书共享规则；可选伙伴不是必须执行的步骤，Hub 不是全局入口拦截器。

元数据、链接与脚本测试证明结构和具体程序行为。场景集是后续模型实跑的验收输入，不能当作已经完成的模型评测。
