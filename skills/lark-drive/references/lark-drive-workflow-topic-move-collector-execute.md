# 主题收集执行与恢复

按当前计划与会话授权执行。只要求方案或只读搜索时不写；具体目标、参数和影响已获授权时不要再添加一轮确认。

1. 保存源位置、token/type、目标及必要恢复依据。
2. 需要新目标时先用 [create folder](lark-drive-create-folder.md) 或 [node create](../../lark-wiki/references/lark-wiki-node-create.md) 创建，保存真实返回 token；失败只阻断该目标的依赖。
3. 按 [移动计划](lark-drive-workflow-topic-move-collector-review-plan.md) 执行相应方向命令，不在运行中替换源/目标。父子节点共享目标时避免重复移动。
4. 记录每项请求结果及返回 token/task ID，权限失败不自动申请或重发；独立项可继续。
5. 异步按 [task result](lark-drive-task-result.md) 跟踪到终态；仅查询所改目标范围验证身份与位置，报告失败或尚在处理项。

源→目标映射：Drive→Drive `drive +move`；文档→Wiki `wiki +move` 的 docs-to-wiki；Wiki→Wiki `wiki +move --node-token`；Wiki→Drive `wiki +move-to-drive`。不可用方向不通过复制重建冒充移动。

## 恢复

恢复按 [恢复位置](lark-drive-workflow-knowledge-organize-rollback.md) 使用原位置记录与成功日志；只处理本次实际移动的对象。跨Drive/Wiki迁移或来源未知不能保证无损恢复，不自行反向移动或删除迁入文档。

用户明确要求恢复位置时可执行同范围受支持反移；清理新建目标涉及删除时需有相应授权，不把删除自动并入恢复。Wiki删除 `--include-children=false` 会保留并提升子节点到父级，此变化必须符合用户要求；Drive目标须先确认不会删掉用户资源。只清理由日志证明确属本次创建的容器。

交付实际完成项、验证结果和剩余缺口，不强制用户再选“结束流程”，也不为成功任务追加恢复建议。
