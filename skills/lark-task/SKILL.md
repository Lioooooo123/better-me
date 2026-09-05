---
name: lark-task
description: 查询、创建和更新飞书任务、清单、负责人及截止时间。仅用于飞书任务；Codex 任务管理使用宿主工具，计划拆解可用 to-tickets。
metadata:
  cli-baseline: "1.0.92"
---

# 飞书任务

个人任务显式 `--as user`。操作使用任务 GUID 或 applink 的 guid 参数，不使用客户端展示编号（如 t104121）。已有任务或清单 ID 直接复用，仅有名称才搜索。

| 操作 | 参考 |
|---|---|
| 我的任务、相关任务 | [get-my-tasks](references/lark-task-get-my-tasks.md)、[get-related-tasks](references/lark-task-get-related-tasks.md) |
| 搜索、定位清单 | [search](references/lark-task-search.md)、[tasklist-search](references/lark-task-tasklist-search.md) |
| 创建、更新 | [create](references/lark-task-create.md)、[update](references/lark-task-update.md) |
| 完成或重开 | [complete](references/lark-task-complete.md)、[reopen](references/lark-task-reopen.md) |
| 指派与关注 | [assign](references/lark-task-assign.md)、[followers](references/lark-task-followers.md) |
| 清单 | [tasklist-create](references/lark-task-tasklist-create.md)、[tasklist-task-add](references/lark-task-tasklist-task-add.md) |
| 评论、附件 | [comment](references/lark-task-comment.md)、[upload-attachment](references/lark-task-upload-attachment.md) |

创建和指派需要明确目标与会话授权；把研究结论提取成候选任务不等于自动向他人分配工作。截止时间按用户时区显示，缺失截止时间不自行补造。

更新返回的 confirmed/updated_fields 或完成状态已覆盖目标时，直接使用，不例行再查一次相同字段。结果不确定时先定位任务，避免重复创建。

联动：用户明确要把计划变任务时使用 `to-tickets` 的已确认清单；综合安排时与 `lark-calendar` 组合。认证问题才读 `lark-shared`，不为了列表展示过度查询全部成员信息。
