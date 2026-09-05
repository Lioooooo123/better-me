# 整理范围与盘点

## 定位范围

复用已有 URL、token、唯一目标名称与身份；只有范围实际歧义时澄清，不对准确链接重复确认。

| 用户目标 | 解析方式 |
|---|---|
| `/drive/folder/<token>` | `folder_token`；普通文件夹树 |
| 明确 Drive 根目录 | 首层省略或传空 `folder_token`，随后按子文件夹 token 遍历 |
| Wiki URL | [wiki +node-get](../../lark-wiki/references/lark-wiki-node-get.md)，保留 node_token、obj_token、obj_type、space_id |
| Wiki 空间名称 | 查真实 space_id，多候选才消歧 |
| 我的文档库 / 个人知识库 / my_library | Wiki personal library；写空间根时解析真实 space_id，不当 Drive root 或 `--mine` 搜索 |
| 明确关键词/过滤范围 | [drive +search](lark-drive-search.md)；没有关键词时使用过滤条件，不把“最近”当 query |

“我的云盘”不能自动等同于仅本人 owner 的文件。已有单资源链接不授权扩到整个知识库；存在多个环境/profile时沿用已指定环境，无法确定才问。

## 分页与遍历

- Drive 按 [files list](lark-drive-files-list.md) 手动读取 `data.files`、`has_more`、`next_page_token`；下页将返回的 `next_page_token` 放入 `--params` 的 `page_token`。不将 `--page-all` 多段输出当单个 JSON。
- Drive 根目录首层不支持分页且不返回根级 shortcut；子文件夹仍按普通分页遍历，子文件夹返回的 shortcut 纳入盘点。披露根级快捷方式的覆盖限制。
- Wiki 按 [node list](../../lark-wiki/references/lark-wiki-node-list.md) 分页；`--page-all` 只翻当前层，`has_child=true` 的节点仍需递归。
- 搜索目标沿用原 query、过滤条件及返回游标，完整盘点时继续到 `has_more=false`。内部批次不是用户确认点，也不是完整覆盖的证明。
- 大范围保留未处理容器、路径、游标、已访问页与去重键。无效或缺失游标有限恢复后仍失败时，记录受影响分支，继续其它独立分支；结果标明未覆盖部分。

## 身份与去重

记录标题、真实类型、URL、源父级、树路径及必要 token。路径来自父子遍历，不能用标题冒充。

- Wiki 按 `space_id + node_token` 去重，不能只按 `obj_token`：同一文档可在多个节点/快捷方式出现。
- Drive 按 `type + token` 去重；搜索与树结果只按明确相同身份合并。
- Wiki shortcut 保留 node_token 与 origin_node_token；无法解析时保留条目并标明不确定，不能丢弃或猜测。
- 需要 owner、时间或 URL 时才补 `drive metas batch_query`。

概览报实际扫描数量、目录结构和缺口。未完成的分页或权限分支不能宣称全覆盖。此阶段只读；不自动申请可能通知 owner 的权限。
