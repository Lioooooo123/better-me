# 实施验证记录

2026-09-05，macOS 本机。

- 26 个入口通过系统 skill-creator 的 quick_validate.py。
- 本仓库验证器检查清单、YAML、显式调用策略、资源引用和必需依赖图；全部通过。代码样例中的占位链接不当作文件路径。
- 13 项 unittest 通过：迁移预览、幂等、恢复、冲突、符号链接目录保护、中途失败恢复、备份变更、锁文件无关条目保留，以及简历缺工具/真实失败区分、默认工程词、拒绝覆盖和模板路径约束。
- 12 套模板 manifest 有效，实际 create_workspace 逐套成功；没有将此结果当作 12 套视觉验收。
- basic-a4 实际 Chrome 导出与 Poppler 检查：原模板因示例联系方式等残留返回失败；替换为 QA 专用内容后 14 项通过，导出一页 A4 并查看截图，无明显重叠或裁切。这是脚本和样式冒烟检查，不是用户简历交付。
- read/fetch.sh 对本地 HTTP 正文实际提取成功；默认流程未请求外部代理。
- CLI 基线：lark-cli 1.0.92；本次没有写入飞书服务、发送消息或重新登录。

14 个行为场景记录在 evals/scenarios.json，execution_status 均为 not_run。尚未做优化前后的模型实跑对照，不能据此宣称任务成功率或速度改善。CI 配置已加入，远端执行结果另行核对。

本机迁移已完成：26 个有效链接、17 个飞书技能已退出安装、2 个个人技能从旧 Codex 路径集中迁移；无关锁文件条目逐项一致。安装状态 pending_actions=0。恢复入口：python3 scripts/hub.py rollback --apply，备份保存在 ~/.codex/skill-hub/backups/。
