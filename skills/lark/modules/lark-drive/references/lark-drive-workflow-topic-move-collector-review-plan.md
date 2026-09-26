# 主题收集的移动计划

主题短语、多个主题词的有效上下文、真实单元格或用户给出的项目别名命中可作为强证据；单词或弱摘要匹配作为待判定。默认计划纳入强相关且执行条件成立的对象；弱相关、不可读、权限未知或不支持方向的资源列出原因，不默认移动。

计划可用简洁表格：资源稳定 ID/URL、标题、原位置、目标位置、动作、依据和例外。分组仅服务用户选择，不需要固定分组数或确认菜单。用户调整后修订相关项及依赖，保留其它原请求，避免执行旧目标。

## 移动参数

| 命令 | 需要的坐标 |
|---|---|
| `drive +move` | file_token、type、folder_token；Drive root 明确记录为根，命令省略目标folder |
| `wiki +move` 节点 | node_token，以及target_space_id或target_parent_token；可选source_space_id，不能换成obj_token |
| `wiki +move` docs-to-wiki | obj_type、obj_token、target_space_id、可选target_parent_token；直接迁入使用apply=false，不能自动转为申请模式 |
| `wiki +move-to-drive` | node_token、folder_token；Drive root 明确根语义 |
| `drive +create-folder` | name、父folder_token；根创建省略父级 |
| `wiki +node-create` | space_id、title、obj_type、可选parent_node_token |

具体flag和类型以 [Drive move](lark-drive-move.md)、[Wiki move](../../lark-wiki/references/lark-wiki-move.md)、[Wiki→Drive](../../lark-wiki/references/lark-wiki-move-to-drive.md) 为准。

先比较原/目标父级的类型、token与space_id；都明确相同才标记已在目标位置，不能将未知空值当相等。新目标用创建结果填依赖，不重搜同名目标。

写前保留原位置/类型/节点与对象token；跨容器权限模型不能承诺自动无损恢复，原父级未知也需注明。说明实际新增影响，已有会话的准确授权继续有效，不要求用户说特定“包括不可恢复项”口令。
