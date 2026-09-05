# 恢复整理前的位置

仅恢复请求或失败后的恢复决策需要时读取。使用写前位置记录与实际成功日志，不根据标题猜测源位置。

- 仅将已成功、位置已知、支持恢复的移动逆序执行；失败、pending、外部状态已变化和来源未知项先核对。
- 使用最新返回 token 作为当前源，原父级/根标识作为目标。Drive root、Wiki space root 都有效，不将空父级和未知位置混同。
- 跨 Drive/Wiki 迁移可能改变权限模型，不能宣称简单反移能无损恢复。没有对应支持时保留当前对象并报告限制。
- 具体恢复范围已有明确授权时无需再次确认；新增删除或新的不可逆影响不由“恢复位置”自动授权。

命令形态如下，身份与门禁 flag 按当前 help 和 [会话授权](../../lark-shared/references/lark-shared-high-risk-approval.md) 处理：

```bash
# Drive 回到原文件夹；回根目录省略 --folder-token
lark-cli drive +move --file-token <current_token> --type <type> --folder-token <original_parent_token> --as user
# Wiki 回到原节点；回空间根目录改传 --target-space-id
lark-cli wiki +move --node-token <current_node_token> --target-parent-token <original_parent_token> --as user
lark-cli wiki +move --node-token <current_node_token> --target-space-id <original_space_id> --as user
```

异步任务按 [task result](lark-drive-task-result.md) 跟踪。恢复后只核对涉及父级与资源身份，报告未恢复项；不能把 pending 算恢复成功。

## 新建容器清理

清理必须在用户已授权范围内，只考虑日志证明由本次整理创建的容器。先验证其不包含原有、未知、恢复失败或他人新增资源；不确定时保留。

- Drive 文件夹必须确认空或仅含本次已纳入清理的空子容器，先子后父。命令见 [Drive delete](lark-drive-delete.md)。
- Wiki 节点不能仅凭“无子节点”认定为空，还需确认节点自身没有需要保留内容。命令见 [Wiki node delete](../../lark-wiki/references/lark-wiki-node-delete.md)。保留子节点时 `--include-children=false` 会将其提升到父级，属于位置变化，必须在授权范围内。
- 不删除知识空间，不以删除容器替代恢复其内部用户资源。

清理后验证目标删除状态，分别报告已删除、失败和仍在处理；不为正常成功任务主动加载这份恢复指南。
