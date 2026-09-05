# 按主题收集资料

用于搜索指定主题并归档到明确 Drive/Wiki 目标。按现有会话完成搜索、验证、计划与已授权移动，不设置独立状态机或多轮确认仪式。

| 需要解决的问题 | 按需参考 |
|---|---|
| 主题、范围、目标位置 | [输入与目标](lark-drive-workflow-topic-move-collector-setup.md) |
| 搜索、扩词、分页与去重 | [召回](lark-drive-workflow-topic-move-collector-recall.md) |
| 资源身份、移动权限与内容证据 | [解析和验证](lark-drive-workflow-topic-move-collector-resolve-verify.md) |
| 分类与具体移动参数 | [移动计划](lark-drive-workflow-topic-move-collector-review-plan.md) |
| 创建、移动、异步结果与恢复 | [执行](lark-drive-workflow-topic-move-collector-execute.md) |

只搜索时不要求先提供归档目标；需要移动时再补齐目标。已有明确主题/范围可立即只读查询。默认个人归档先搜索本人 owner 的资源（`--mine`）并说明范围；用户要求所有可见资源时移除此限制，不要求额外确认同一范围。

题名/内容强命中且可移动的资源可以形成默认计划；弱相关或权限未知项保留为例外，不擅自移动。无法读取不意味着无内容，无访问权限不自动授权向 owner 申请访问。保持资源 ID、原/目标位置、证据、写入结果与必要恢复记录，不强制 JSON 格式。
