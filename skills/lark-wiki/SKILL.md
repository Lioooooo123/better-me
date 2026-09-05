---
name: lark-wiki
description: 管理飞书知识空间和节点的查找、创建、移动、复制及成员。用于 Wiki 结构工作；正文用 lark-doc，文件搜索和上传用 lark-drive。
metadata:
  cli-baseline: "1.0.92"
---

# 飞书知识库

个人空间显式 `--as user`；解析节点和后续操作保持同一身份。`space_id`、`node_token`、底层 `obj_token` 是不同对象，不能用 URL 或名称替代 ID。

| 操作 | 参考 |
|---|---|
| 找空间、节点 | [space-list](references/lark-wiki-space-list.md)、[node-get](references/lark-wiki-node-get.md)、[node-list](references/lark-wiki-node-list.md) |
| 新建空间或节点 | [space-create](references/lark-wiki-space-create.md)、[node-create](references/lark-wiki-node-create.md) |
| 移动、复制 | [move](references/lark-wiki-move.md)、[node-copy](references/lark-wiki-node-copy.md) |
| 移到云空间 | [move-to-drive](references/lark-wiki-move-to-drive.md) |
| 删除节点或空间 | [node-delete](references/lark-wiki-node-delete.md)、[delete-space](references/lark-wiki-delete-space.md) |
| 成员 | [member-list](references/lark-wiki-member-list.md)、[member-add](references/lark-wiki-member-add.md)、[member-remove](references/lark-wiki-member-remove.md) |

按名称定位需覆盖必要分页并处理重名，不因首个精确匹配就认定唯一。删除前必须把目标解析到具体 ID 并确认已有授权对应该对象，保留原权限与归属影响的说明。

“我的文档库/个人知识库”是 Wiki personal library，不自动降级为 Drive 根目录。重命名使用现有 update-title 路径保持节点 ID，不复制节点替代改名。

用户、群、部门和应用成员使用各自正确的 ID/type。bot 添加部门成员是已知不可用路径，不靠写请求试错或静默换身份；实际参数读取 reference/help。

联动：跨容器找文件用 `lark-drive`，节点正文用 `lark-doc`。只做一次必要的资源解析，后续复用得到的 ID 和身份；认证异常用 `lark-shared`。
