# 主题与目标位置

从当前会话解析主题、排除词、目标位置、身份及明确的类型/时间/owner范围。沿用已知值，只有关键缺失或多候选时问；不要要求用户重新确认已给链接后才开始只读搜索。

默认使用 `--as user`。个人归档默认 `--mine` 指本人 owner，不等于所有可见；用户说“不限 owner/包含共享给我/所有可见”时不加 `--mine`。没有用户范围要求时不强加 folder/space 限制。

| 目标 | 需要保留 |
|---|---|
| Drive 文件夹 | 真实 folder_token，必要时 [inspect](lark-drive-inspect.md) 解析 |
| Wiki 节点 | [node get](../../lark-wiki/references/lark-wiki-node-get.md) 返回的 node_token 与 space_id；obj_token用于内容，不用于节点移动 |
| Wiki 空间根 | 真实 space_id 与明确根标识 |
| 待创建容器 | 已解析父级、名称、类型；写入授权范围内才创建 |

Drive root 与 Wiki personal library/my_library 是不同目标。若已有目标不可解析，报告缺口并继续与目标无关的只读搜索；不猜目标、不换身份、不创建替代对象。

移动方向：Drive→Drive 用 `drive +move`；文档→Wiki 用 `wiki +move` docs-to-wiki；Wiki→Wiki 用 `wiki +move --node-token`；Wiki→Drive 用 `wiki +move-to-drive`。具体支持类型、权限与参数见 [移动计划](lark-drive-workflow-topic-move-collector-review-plan.md)。
