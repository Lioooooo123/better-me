# task +set-ancestor

> For unresolved authentication, permission, or global-argument questions, consult [lark-shared](../../lark-shared/MODULE.md). Reuse verified session context.

Set a parent task for a task, or clear the parent to make it independent.

## Recommended Commands

```bash
# Set a parent task
lark-cli task +set-ancestor --task-id "guid_1" --ancestor-id "guid_2"

# Clear the parent task
lark-cli task +set-ancestor --task-id "guid_1"
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--task-id <guid>` | Yes | The task GUID to update. |
| `--ancestor-id <guid>` | No | The parent task GUID. Omit it to clear the ancestor. |

## Workflow

1. Confirm the child task and, if applicable, the ancestor task.
2. Execute `lark-cli task +set-ancestor ...`
3. Report the updated task GUID and whether the ancestor was set or cleared.

> [!CAUTION]
> Write only within the user’s explicit authorization for this target and operation. Reuse authorization already given in this task; ask only if the target, content, or requested action is unresolved.
