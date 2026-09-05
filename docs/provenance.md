# 来源与许可

本仓库是个人私有维护集合，不为所有来源套用统一开源许可。入口按个人工作范围重写；复用的参考、脚本与模板仍遵守各自来源约束。

| 来源 | 处理与许可 |
|---|---|
| [tw93/Waza](https://github.com/tw93/Waza) | 重写入口；保留 read 抓取与 write 标点助手。MIT，原许可在 catalog/upstream。 |
| [mattpocock/skills](https://github.com/mattpocock/skills) | 重写专业方法入口；保留 handoff/to-tickets 的显式调用策略。MIT，原许可在 catalog/upstream。 |
| [KevinYoung-Kw/vibe-resume-skill](https://github.com/KevinYoung-Kw/vibe-resume-skill) | 保留并修改简历脚本、模板和预览，移除演示/推广素材。作者 KevinYoung-Kw（水的离子积），CC BY-NC 4.0；商业使用按原许可取得授权。修改包括拒绝覆盖、缺工具不算通过、取消统一留白与普通工程词禁令。 |
| 飞书 CLI 配套技能 | 从本机快照导入保留的 7 项参考与助手，简化编排规则。具体来源字段见 catalog/skills.json；未确认统一再授权许可，维持私有使用。实测 CLI 基线 1.0.92，参数以当前 help 为准。 |
| ios-hig-design | 本机技能标注作者 wondelai、MIT，保留署名与领域参考，重写入口并修正失效引用；未根据作者名猜测仓库。 |
| asu-skills、skill-hub | 本地写作与组合规则；原 asu-skills 未在安装锁登记来源。 |

简历[完整许可条款](https://creativecommons.org/licenses/by-nc/4.0/legalcode)。licenses.json 中 NOASSERTION 是 GitHub 的识别结果，保存的许可文件明确写明 CC BY-NC 4.0，应以实际条款为准。

`original_folder_hash` 是原安装器目录哈希，不是上游 commit。迁移基线的 SHA-256 是本机快照指纹，不代表上游最新版本。来源缺口保持明确，不伪造版本、作者或授权。
