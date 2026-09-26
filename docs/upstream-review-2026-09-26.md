# 上游审阅与本机技能纳入：2026-09-26

本次把 `~/.agents/skills/` 的 28 个技能全部纳入 `better-me`。原有 25 个继续由仓库维护，已存在的本机链接保留；新增 `better-ui`、`improve-react`、`show-me`。安装器只在新技能的本机目录与仓库目录指纹一致时接管，原目录和锁记录保存在既有恢复日志中。`show-me` 的原安装记录没有上游地址，按本地技能登记。

## 审阅快照

| 来源 | 本次固定 commit | 结果 |
|---|---|---|
| [jakubkrehel/skills](https://github.com/jakubkrehel/skills) | `267330e1adfc66a718fb65fa6918c1f06d0a689e` | `better-ui` 的 8 个文件与本机原目录一致；保存 MIT 许可。 |
| [millionco/react-doctor](https://github.com/millionco/react-doctor) | `d741d58e7831e37c9f6a5528340c103059bd1ccf` | `improve-react` 使用本机已调整版本，保留 3 个文件与 Modified MIT 许可。 |
| [larksuite/cli](https://github.com/larksuite/cli) | `a079fd7a0f2e5f91ef2a45017175ac9b7435ee97` | 7 个保留技能的目录差异已审阅；选择性合入 Wiki token 路由，其余见下文。 |
| [tw93/Waza](https://github.com/tw93/Waza) | `c3b74dd5845b39a80a79c36bb82b028947674a05` | 7 个技能的上游变化已审阅，本地缩减范围和授权语义保留。 |
| [wondelai/skills](https://github.com/wondelai/skills) | `c172996495bed0fcd26896a9416b2093fd7073f0` | `ios-hig-design` 上游仅更新版本并删除推广链接，本地此前已无该链接。 |
| [mattpocock/skills](https://github.com/mattpocock/skills) | `c55ee46073ed923f86ce59a5eb3b6d895095d1b7` | 仓库分支前进，已核对已追踪技能目录树未变；`obsidian-vault` 路径仍未找到。 |
| [KevinYoung-Kw/vibe-resume-skill](https://github.com/KevinYoung-Kw/vibe-resume-skill) | `650588e7c7c5d90cbacfb1cd806d35acff036519` | 无新目录变化。 |
| [openai/skills](https://github.com/openai/skills) | `49f948faa9258a0c61caceaf225e179651397431` | 无新目录变化。 |

`catalog/upstream-state.json` 的 commit 和目录树是审阅基线，并不表示本仓库技能逐字等同上游。本机原始目录指纹保留在 `catalog/skills.json` 的 `original_folder_hash`，此次审阅没有改写它。

## 采纳与暂缓

- 飞书 Wiki token 路由改用 `wiki +node-get --node-token`，按返回的 `data.obj_type`、`data.obj_token`、`data.node_token` 和 `data.space_id` 取值；本机 `lark-cli 1.0.92` 的 help 确认该 shortcut 和参数可用。`lark-task` 的上游变化仅为跨目录 `lark-shared` 链接路径修正，本地链接原本已正确。
- 飞书上游还加入了会议/视频会议关联、`--concise` 消息输出、文档草稿契约、Wiki 节点解析和 Drive 文件夹同步完成的说明。上游 CLI 包为 `1.0.96`，本机仍为 `1.0.92`；至少 `--concise` 与相关会议命令在当前 help 不可用。这些新行为没有写入本地可执行指引；继续按现有 CLI 的 help 和本地参考执行。Drive 文件夹移动仍依据返回的 `ready`、`next_command` 处理。
- Waza 本次涉及审查授权跨轮持续、故障诊断、深度健康审计、研究与 UI 规则。跨轮授权与按实际任务裁剪已由当前全局指令和本地技能覆盖；强制探针、委派、统一输出格式及过宽触发范围没有引入。没有把上游一般规则视为本机必须执行的命令。
- `improve-react` 的本机修改保留用户已授权修复与当前 Agent 直接完成任务的语义。`show-me` 不虚构上游来源或许可。

## 验证边界

`make check PYTHON=.venv/bin/python` 通过：目录/元数据/引用/依赖检查与 22 项脚本测试均成功。新增 3 个技能分别通过 `quick_validate.py`；本机 28 个安装路径均指向仓库，安装日志与锁中有 28 个条目，原 3 个目录仍在备份。更新基线后重跑 `make upstream`：8 个仓库和 26 个已追踪技能均为 `unchanged`；`obsidian-vault` 为 `path_not_found`，`show-me` 为 `local`。

本次没有调用真实飞书数据或做模型行为对照。首次迁移和 2026-09-07 的实验数字仍是历史快照，不代表 28 个技能的性能。
