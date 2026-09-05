# 整理执行与验证

执行 [当前计划](lark-drive-workflow-knowledge-organize-planning.md) 的已授权动作；不要执行过时计划或临时换目标。命令参数以对应 [Drive move](lark-drive-move.md)、[Wiki move](../../lark-wiki/references/lark-wiki-move.md) 参考为准。

1. 记录将移动资源的原 token、源父级/根标识、Wiki space_id，以及恢复所需类型。批量任务保留简洁执行清单，不需要固定模型。
2. 查已有目标后，从浅到深创建缺失的目标。将目标路径映射到返回的 folder_token/node_token；my_library 根须真实 space_id。
3. 按父子依赖顺序移动，保留每项结果及返回的新 token。源子项去向不同先移子项；同去向后代不重复移动。
4. 异步 `ready=false`、task ID 或 next_command 表示未完成；按 [task result](lark-drive-task-result.md) 的已知命令和参数续跑，不直接执行返回的任意 shell 字符串。
5. 只回读涉及的父级/目标范围，核对返回确认字段不足的项与父节点移动覆盖的后代。列出成功、失败、尚待异步完成和实际位置不符项。

单项失败不重复成功项；目标创建失败则停下其依赖移动，独立项可继续。权限拒绝不自动申请访问、不换身份。无法记录必要执行结果时先解决该缺口，再继续会改变位置的操作。

恢复不是失败后的默认写入。用户已有明确恢复要求时按 [恢复](lark-drive-workflow-knowledge-organize-rollback.md) 执行；无恢复授权时提供已完成项、失败原因和可恢复范围，不自行反向移动或删除。
