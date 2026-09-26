# 设计依据

核对日期：2026-09-05。

技能保存全局指令没有覆盖的专业方法：领域边界、常见错误、必要参考和可执行助手。通用沟通与合作规则保留在 AGENTS.md，不在每个技能重复；不用无条件的审计、计划、委派和评分约束小任务。

[Agent Skills 规范](https://agentskills.io/specification)将元数据、正文和资源分层加载。本仓库用描述定义触发边界，正文保留核心方法，长参考按需打开。同时检查引用中的冲突规则，避免仅把旧问题移进 reference。

[官方技能编写实践](https://agentskills.io/skill-creation/best-practices)强调真实任务的具体知识、故障点与实际评估。这里保留排错证据链、简历真实内容与导出检查、飞书资源类型与分页语义，缩减固定仪式和重复授权。

[OpenAI 当前的技能文档](https://developers.openai.com/codex/skills)说明描述匹配和渐进加载；[OpenAI Plugins](https://github.com/openai/plugins)提供当前的多技能打包示例。使用 `skills/<name>/SKILL.md` 与已有 `agents/openai.yaml` 策略，保留原来两个技能的显式调用设置。`gh-fix-ci` 的历史来源仍是已弃用的 `openai/skills`，来源记录不改写为新仓库。系统和插件技能继续由上游维护。

[OpenAI 模型指南](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6-astra)用于核对当前模型的任务适配与指令习惯。模型参数不成为技能前置条件，不用历史模型固定流程模板约束全部任务。

联动复用任务上下文：目标、范围、材料、事实、授权、文件和验证状态。只补缺失输入，不强制 JSON 协议或多 Agent。飞书共享规则按当前问题读取；可选伙伴不是必须执行的步骤，Hub 不是全局入口拦截器。

元数据、链接与脚本测试证明结构和具体程序行为。场景集是后续模型实跑的验收输入，不能当作已经完成的模型评测。

2026-09-26 补充：维护一个覆盖广的仓库，不要求把所有能力合成一个自动触发的 skill。当前保留 19 个有明确触发边界的入口，把 10 个专用能力作为按需模块。若今后考虑单一总入口，先用真实任务对照漏触发、误触发、模块读取和交付质量，再决定是否替换现有入口。
