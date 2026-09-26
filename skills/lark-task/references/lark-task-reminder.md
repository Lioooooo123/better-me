# task +reminder

> For unresolved authentication, permission, or global-argument questions, consult [lark-shared](../../lark-shared/SKILL.md). Reuse verified session context.
> **Priority:** For creating or modifying task reminder times, prioritize using this `+reminder` shortcut over other task update methods. It provides a more reliable and direct way to manage reminders.

Manage task reminders. Set new reminders or remove existing ones. Note that setting a task reminder requires a due date.

## Recommended Commands

```bash
# Set a reminder (e.g., 30 minutes before due)
lark-cli task +reminder --task-id "<task_guid>" --set "30"

# Set a reminder (e.g., 1 hour before due)
lark-cli task +reminder --task-id "<task_guid>" --set "1h"

# Remove all reminders
lark-cli task +reminder --task-id "<task_guid>" --remove "true"
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--task-id <guid>` | Yes | The task GUID to modify. For Feishu task applinks, use the `guid` query parameter, not the `suite_entity_num` / display task ID like `t104121`. |
| `--set <val>` | No | Relative fire minutes before the due time. Supports numbers (e.g., `30`) or units (e.g., `15m`, `1h`, `1d`). |
| `--remove <bool>` | No | If set to `true`, removes all existing reminders from the task. |

## Workflow

1. Confirm the task and reminder action.
2. Execute the command.
3. Report success.

> [!CAUTION]
> Write only within the user’s explicit authorization for this target and operation. Reuse authorization already given in this task; ask only if the target, content, or requested action is unresolved.
