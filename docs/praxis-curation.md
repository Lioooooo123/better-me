# Praxis · 知行：命名与补充

日期：2026-09-07。Praxis 表示将理解与方法付诸实践；它是技能库的名字，不是新的总入口技能。

## 选择

| 候选 | 决定 | 理由 |
|---|---|---|
| openai/skills 的 gh-fix-ci | 纳入并适配 | 现有 hunt 不专门覆盖 PR 检查、run/job 日志、旧 SHA 与新运行的区别。 |
| mattpocock/skills 的 resolving-merge-conflicts | 纳入并适配 | 补正在进行的 merge/rebase 冲突、三阶段内容、双方意图和合并验证。 |
| anthropics/skills 的 webapp-testing | 暂不纳入 | 与当前浏览器/UI 能力重叠；其统一 Python Playwright 与 networkidle 流程不适合直接引入当前宿主。 |
| 官方 Figma、Cloudflare、PDF、Notebook、安全类候选 | 暂不纳入 | 已有对应插件，或用户已明确移除；不重复安装。 |
| 更多框架专用技能 | 暂缓 | 当前没有指定采用该框架的任务，避免增加常驻发现负担。 |

## 定制

gh-fix-ci 复用当前认证，仅遇到错误再诊断身份；修复授权沿用会话，明确区分旧提交失败、运行中、取消和业务失败，不自动重跑部署工作流。

冲突技能保留原上游的双方意图分析；移除“永不 abort”和“stage everything”的绝对规则，支持用户取消，保护无关暂存和未跟踪内容。

## 验证与维护

新入口通过官方格式验证；库内检查覆盖 25 个技能的元数据、依赖、引用和来源。独立 Agent 在隔离仓库中实际完成一个 merge 冲突：合并双方不同配置变化，两个父提交，无未合并项，无关文件哈希和未跟踪状态保持不变。未声称测试了所有 rebase 形态或实际失败 CI 修复。

维护命令改为 scripts/manage.py；已有迁移状态与备份目录保留 ~/.codex/skill-hub/ 以兼容恢复。GitHub 仓库和本机源码目录使用 praxis，个人安装链接和锁文件随迁移同步。没有新增自动更新任务或重新启用已移除插件。
