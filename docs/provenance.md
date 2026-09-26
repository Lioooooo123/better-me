# 来源与许可

本仓库是个人私有维护集合，不为所有来源套用统一开源许可。入口按个人工作范围重写；复用的参考、脚本与模板仍遵守各自来源约束。

| 来源 | 处理与许可 |
|---|---|
| [tw93/Waza](https://github.com/tw93/Waza) | 重写入口；保留 read 抓取与 write 标点助手。MIT，原许可在 catalog/upstream。 |
| [mattpocock/skills](https://github.com/mattpocock/skills) | 重写专业方法入口；保留 handoff/to-tickets 的显式调用策略。MIT，原许可在 catalog/upstream。 |
| [KevinYoung-Kw/vibe-resume-skill](https://github.com/KevinYoung-Kw/vibe-resume-skill) | 保留并修改简历脚本、模板和预览，移除演示/推广素材。作者 KevinYoung-Kw（水的离子积），CC BY-NC 4.0；商业使用按原许可取得授权。修改包括拒绝覆盖、缺工具不算通过、取消统一留白与普通工程词禁令。 |
| 飞书 CLI 配套技能 | 从本机快照导入保留的 7 项参考与助手，简化编排规则。2026-09-07 已核对官方 larksuite/cli 仓库、目录与 MIT 许可，并保存原许可；具体来源与审阅版本见 catalog/upstream-state.json。实测 CLI 基线 1.0.92，参数以当前 help 为准。 |
| ios-hig-design | 本机技能标注作者 wondelai、MIT，保留署名与领域参考，重写入口并修正失效引用；2026-09-07 已核对 wondelai/skills/ios-hig-design，原 11 份参考与上游一致，补存 MIT 许可与版本。 |
| [jakubkrehel/skills](https://github.com/jakubkrehel/skills) | 原导入的 `better-ui` 8 个文件与 2026-09-26 审阅版本一致；当前入口已精简为 `ui` 的按需模块，配方文件保留。MIT 许可保存在 `catalog/upstream/`。 |
| [millionco/react-doctor](https://github.com/millionco/react-doctor) | `improve-react` 保留本机已调整的审查方法，现作为 `check` 模块按类别拆分；去除强制委派和拒绝修复的要求。原版为 Modified MIT，许可保存在 `catalog/upstream/`，包含模型训练/评测数据及托管产品用途限制。 |
| show-me | 本机独立技能，原安装记录没有来源地址；不推断作者或上游许可。 |
| asu-skills、skill-hub | 本地写作与组合规则；原 asu-skills 未在安装锁登记来源。 |

简历[完整许可条款](https://creativecommons.org/licenses/by-nc/4.0/legalcode)。licenses.json 中 NOASSERTION 是 GitHub 的识别结果，保存的许可文件明确写明 CC BY-NC 4.0，应以实际条款为准。

`original_folder_hash` 是原安装器目录哈希，不是上游 commit。迁移基线的 SHA-256 是本机快照指纹，不代表上游最新版本。来源缺口保持明确，不伪造版本、作者或授权。

上游追踪补充：`catalog/upstream-state.json` 记录 8 个仓库 commit、26 个已核实技能目录和树指纹，不表示本地内容与上游逐字相同。7 个飞书来源、`better-ui`、`ios-hig-design` 和 `improve-react` 现在保留为父技能的按需模块，来源数据在 `catalog/modules.json`；新建的 `lark` 路由为本地整理。`obsidian-vault` 在标注来源的当前快照中未找到；`show-me` 来源不明，两者继续保留本地版本。旧入口 asu-skills 与 skill-hub 已退出默认安装。

此前扩充的 `gh-fix-ci` 参考 openai/skills，保留 Apache-2.0 原许可，重写入口并复用现有 gh CLI，未导入额外检查脚本；`resolving-merge-conflicts` 参考 mattpocock/skills（MIT），保留冲突意图分析并调整暂存、取消和提交边界。准确路径与审阅 commit 见 `catalog/upstream-state.json`。
