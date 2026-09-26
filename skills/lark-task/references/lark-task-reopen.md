# task +reopen

> For unresolved authentication, permission, or global-argument questions, consult [lark-shared](../../lark-shared/SKILL.md). Reuse verified session context.

Reopen a previously completed task.

## Recommended Commands

```bash
# Reopen a task
lark-cli task +reopen --task-id "<task_guid>"
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--task-id <guid>` | Yes | The task GUID to reopen. For Feishu task applinks, use the `guid` query parameter, not the `suite_entity_num` / display task ID like `t104121`. |

## Workflow

1. Confirm the task to reopen.
2. Execute the command.
3. Report success.

> [!CAUTION]
> Write only within the user’s explicit authorization for this target and operation. Reuse authorization already given in this task; ask only if the target, content, or requested action is unresolved.
