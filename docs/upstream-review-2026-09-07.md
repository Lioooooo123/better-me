# 上游审阅与优化：2026-09-07

先与首次导入的原始快照比较上游，再与当前定制版本比较；选择性合入，不执行上游安装脚本。当前 Hub 管理 26 个技能，不修改其他新装技能、系统技能、插件缓存、CLI 或认证。

## 核验版本

| 上游 | 固定审阅版本 |
|---|---|
| [KevinYoung-Kw/vibe-resume-skill](https://github.com/KevinYoung-Kw/vibe-resume-skill) | [650588e7c7c5](https://github.com/KevinYoung-Kw/vibe-resume-skill/tree/650588e7c7c5d90cbacfb1cd806d35acff036519) |
| [larksuite/cli](https://github.com/larksuite/cli) | [7fd6ef3c0718](https://github.com/larksuite/cli/tree/7fd6ef3c07182257ce776cdc5a614e122d5bd4b3) |
| [mattpocock/skills](https://github.com/mattpocock/skills) | [3cca18b368ae](https://github.com/mattpocock/skills/tree/3cca18b368ae95cdbdebbff572ccafa662551015) |
| [tw93/Waza](https://github.com/tw93/Waza) | [2ae9e487a97b](https://github.com/tw93/Waza/tree/2ae9e487a97bc101ca23b7f5a8fd3389c1ecffe2) |
| [wondelai/skills](https://github.com/wondelai/skills) | [eade5d170b3a](https://github.com/wondelai/skills/tree/eade5d170b3a593c5b6ebcaca898102134aee108) |

23 个目录核验成功，保存完整 commit、tree OID 和入口 SHA-256。obsidian-vault 当前未找到匹配目录，不能由此推断应该删除；asu-skills 和 Hub 自身继续本地维护。larksuite/cli 与 wondelai/skills 的 MIT 许可已补存。

## 合入的变化

| 范围 | 具体变化 |
|---|---|
| think | 判断是否值得做时先看需求、依赖与长期维护成本，避免自动扩成工程计划。 |
| codebase-design、domain-modeling | 补接口的错误/顺序/性能契约，检验抽象是否集中复杂度；ADR 根据实际取舍记录，沿用项目格式。 |
| to-tickets | 跨仓机械重构允许兼容层、分批迁移、最后收紧；依赖和最终验证必须明确。 |
| hunt、ui | 原生冻结用问题发生时的线程栈和日志取证；截图比较保持状态与宽度一致。 |
| learn、write | 针对知识缺口补证据；长文精简保留作者立场与情绪，不把单次经验推广成通用要求。 |
| read | 修正直连抓取的注释：不使用第三方提取服务，不等于 URL 不离开本机。 |
| html-resume-builder | 选择性加入 --template 校验与 12 套模板标记；解析实际 HTML 属性，注释和脚本文字不能冒充标记。允许自定义模板，未指定时不增加限制。身份一致不代表样式或内容验收。 |
| lark-calendar | 修正实例与例外不能按正数 ID 后缀区分的问题；增加本机可用参与人查询，完整说明共同忙闲覆盖。 |
| lark-im | 说明文件夹与单文件不同，自动下载不递归；新版一层展开/截断说明保留版本边界。 |
| health | 可调用只读上游检查器，仓库变化不冒充具体技能更新。 |

## 保留本地选择

check、health 的广泛触发/强制输出未整体导入；本地已有的证据优先与按风险判断继续保留。tdd 不恢复每次测试边界重复批准或禁止局部重构。setup-pre-commit 不附带自动 commit；handoff 保留显式调用。ios-hig-design 上游主要扩充入口，11 份参考没有变化，未重新引入统一评分或扩大平台审查范围。

简历上游要求只能使用 12 套官方模板、固定留白和工程术语禁令，这些不适合定制工作，未采纳。没有以模板标记替代真实视觉检查。

飞书本机仍为 1.0.92。当前 help 不支持 calendar +delete、+list-attendees、+update --apply-to、多人 common_free 等新接口，因此没有直接导入。附件输出继续服从本机 relative-only 限制。没有升级 CLI 或操作真实日程、消息和附件。

## 验证

- 16 项 unittest 通过，包含真实 Git 仓库的 unchanged/changed/missing-branch 检查；上游检查器实际联网核对 5 个仓库成功。
- 26 个技能的清单、元数据、引用、依赖和上游指纹检查通过；官方 quick_validate 另行核对。
- basic-a4 使用 --template basic-a4 --strict-final 实际导出，15 项检查通过；临时输入是 QA 替换材料，不是用户简历。12 套模板标记与各自 manifest 一致。
- 独立 Agent 仅得到 to-tickets 技能及跨 3 包 CustomerId 重构请求，产出了兼容层、典型调用链、批量迁移、内部收紧和外部退出条件，未创建外部 issue。该项为规划场景试用，不是实现执行或总体成功率评测。
- 其余原有行为场景仍为 not_run，不宣称完成了模型 A/B 对照。

本机原有符号链接直接读取此次源码改动，安装状态 pending_actions=0；不需重装或迁移备份。
