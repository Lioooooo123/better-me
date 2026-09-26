# task +followers

> For unresolved authentication, permission, or global-argument questions, consult [lark-shared](../../lark-shared/MODULE.md). Reuse verified session context.

Manage task followers. Add or remove followers from an existing task.

## Recommended Commands

```bash
# Add a follower
lark-cli task +followers --task-id "<task_guid>" --add "ou_aaa"

# Add an app follower
lark-cli task +followers --task-id "<task_guid>" --add "cli_xxx"

# Remove a follower
lark-cli task +followers --task-id "<task_guid>" --remove "ou_aaa"
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--task-id <guid>` | Yes | The task GUID to modify. For Feishu task applinks, use the `guid` query parameter, not the `suite_entity_num` / display task ID like `t104121`. |
| `--add <ids>` | No | Comma-separated follower IDs. Use user `open_id`s like `ou_xxx` for people, or app IDs like `cli_xxx` for apps. |
| `--remove <ids>` | No | Comma-separated follower IDs. Use user `open_id`s like `ou_xxx` for people, or app IDs like `cli_xxx` for apps. |

## Workflow

1. Confirm the task and followers to add/remove.
2. Execute the command.
3. Report success.

> [!CAUTION]
> Write only within the user’s explicit authorization for this target and operation. Reuse authorization already given in this task; ask only if the target, content, or requested action is unresolved.
