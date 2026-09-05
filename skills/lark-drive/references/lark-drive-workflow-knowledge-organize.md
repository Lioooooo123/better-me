# 知识整理

用于盘点并整理已指定 Drive 文件夹、Wiki 节点/空间、个人文档库或明确搜索范围。沿用用户已有分类和命名；没有既有分类时从实际内容推导，不强加固定目录层数或“待人工确认”文件夹。

按需要读取：

- [范围与盘点](lark-drive-workflow-knowledge-organize-discovery.md)：真实身份、分页、树与节点去重。
- [内容分析](lark-drive-workflow-knowledge-organize-analysis.md)：证据不足时的补读与分类。
- [生成计划](lark-drive-workflow-knowledge-organize-planning.md)：源/目标、父子顺序、授权范围。
- [执行与验证](lark-drive-workflow-knowledge-organize-execution.md)：真实 token、异步结果、局部失败。
- [恢复](lark-drive-workflow-knowledge-organize-rollback.md)：仅恢复请求或失败处理需要时读取。

已知目标可以直接只读盘点并形成可检查计划。用户已授权明确范围的整理时继续执行；“只给方案”则交付计划。分类未定项默认保留原位置并说明，除非用户已指定临时归档位置。不要为了让目录显得整洁而自动移动空目录、改名、删除或修改权限。

常用操作是 `drive +create-folder`、`drive +move`、`wiki +node-create`、`wiki +move --node-token`。跨 Drive/Wiki 容器迁移按 [主题收集执行](lark-drive-workflow-topic-move-collector-execute.md) 的移动语义处理，不把 Wiki 对象 token 当节点 token。重命名等额外目标有明确授权时使用对应原子命令，无需另走审批式工作流。

权限申请可能通知 owner，不因读取失败自动申请。使用 [组合任务规则](lark-drive-workflow.md) 和会话已有授权，不额外要求“范围确认→思路确认→计划确认→执行确认”四轮交互。
