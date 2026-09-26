# task +tasklist-create

> For unresolved authentication, permission, or global-argument questions, consult [lark-shared](../../lark-shared/SKILL.md). Reuse verified session context.

Create a new tasklist, and optionally batch create tasks within it.

## Recommended Commands

```bash
# Create an empty tasklist
lark-cli task +tasklist-create --name "Q1 Goals"

# Create a tasklist and add members
lark-cli task +tasklist-create --name "Project A" --member "ou_xxx,ou_yyy"

# Create a tasklist and batch create tasks within it
lark-cli task +tasklist-create --name "Launch Checklist" --data '[{"summary": "Code Review", "assignee": "ou_aaa"}, {"summary": "Deploy", "assignee": "ou_bbb"}]'
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--name <text>` | Yes | The name of the tasklist. |
| `--member <ids>` | No | Comma-separated list of user `open_id`s to add as editors. |
| `--data <json>` | No | JSON array of task definitions to create and add to the tasklist automatically. |

## Workflow

1. Confirm the tasklist name, members, and tasks (if any).
2. Execute the command `lark-cli task +tasklist-create ...`.
3. Report success, including the new tasklist ID and the result of the batch task creation.

> [!CAUTION]
> Write only within the user’s explicit authorization for this target and operation. Reuse authorization already given in this task; ask only if the target, content, or requested action is unresolved.
