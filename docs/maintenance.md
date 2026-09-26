# 借鉴 Vercel 的维护方式

审阅日期：2026-09-07。此次只借鉴维护机制，未复制第三方规则或安装新技能。

## 对照来源

- [vercel-labs/skills](https://github.com/vercel-labs/skills/tree/1682051d48c34f5eb135e6475c1a965dce05e820) 是安装与发现 CLI；其 `AGENTS.md` 描述用技能文件夹树 SHA 判断更新，代码与测试分别维护。
- [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills/tree/063bee94c3f4df8453406c830b0a7df0f2860278) 是技能集合；其 `AGENTS.md` 规定标准入口、按需引用和脚本约定。
- [React 技能维护说明](https://github.com/vercel-labs/agent-skills/blob/063bee94c3f4df8453406c830b0a7df0f2860278/skills/react-best-practices/README.md) 将规则分文件编写，附正确和错误示例，再构建汇编与测试素材。对应 CI 执行 validate 和 build。
- [发现索引工作流](https://github.com/vercel-labs/agent-skills/blob/063bee94c3f4df8453406c830b0a7df0f2860278/.github/workflows/agent-skills-discovery.yml) 校验索引，并在 push 后发布 release 附件。

## better-me 的落实

| 机制 | better-me 做法 |
|---|---|
| 内容与工具分工 | 保留 `skills/` 与 `scripts/`，19 个顶层入口和 10 个按需模块暂不拆仓库 |
| 技能级更新判断 | `make upstream` 查询固定 commit 的目录树，与已审阅树指纹比较；错误不伪装成未变化 |
| 明确维护方法 | `CONTRIBUTING.md` 说明新增、更新、许可、验证和交付；PR 模板收集本次变化的证据 |
| 本地与 CI 一致 | `make check` 统一元数据检查和脚本测试；网络上游检查单独运行 |
| 规则按需加载 | 延续短入口与直接引用；复杂规则才拆分，并补适用条件和示例 |
| 安装可恢复 | 继续用已有安装预览、备份和恢复，不用通用 update 覆盖个人改写 |

审阅时还是私人源码库，因此未增加 npm 发布、公开发现索引、自动 release 或定时通知。当时也没有因为借鉴维护方式而安装 `find-skills` 或恢复已移除的总入口技能。

仓库现已公开；上段是 2026-09-07 的原始取舍记录。公开可读不等于已经建立插件发布渠道，仍不自动增加 release 或发现索引。

GitHub 树 API 使用匿名只读请求，受公共速率限制；失败会返回 `error` 和非零退出码。`path_missing` 表示本次完整目录树中找不到登记路径，不代表已确定该技能永久删除。上游状态仍是审阅基线，检查不会自动修改它。

## 2026-09-26：广覆盖与按需加载

[Anthropic Skills](https://github.com/anthropics/skills)在一个仓库展示多个领域，技能内部再按具体任务读取参考；[OpenAI Plugins](https://github.com/openai/plugins)以插件分组技能；[Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills)即使覆盖多个科学领域，也保留专用技能入口。这些是目录和分发方式的参考，不要求 better-me 复制它们的数量或流程。[Agent Skills 规范](https://agentskills.io/specification)将描述、入口正文与按需资源分层；[Codex 技能文档](https://developers.openai.com/codex/skills)说明描述决定隐式匹配，过多描述还可能在初始列表中被缩短或省略。

better-me 继续用 19 个有独立触发条件的入口与 10 个模块，不增加“任何任务都触发”的总 skill。飞书的 `lark-shared` 是条件性参考，不是所有飞书模块的必读依赖。新增领域先判断现有入口能否按需路由；只有任务边界或交付物确实独立时再增加入口。

维护验收同时看误触发和漏触发：`evals/scenarios.json` 指明应选入口、应读与不应读的模块；校验器检查引用仍在目录中。模型实际读取和任务结果需要另行在同一运行条件下记录，静态通过不能代替它。
