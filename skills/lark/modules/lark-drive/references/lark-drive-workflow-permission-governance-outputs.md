# 权限含义与结果表达

单目标回答结论、依据和检查范围；多目标按用户需要列出可定位对象与覆盖缺口，大列表可用文件或分页。没有固定模板、Top N或风险编号格式要求；需要后续选择时保持稳定URL/ID。

未提供组织policy时，允许对外分享、低活跃、无密级标签是待复核事实，不直接等同于违规、泄露或已被AI索引。只读检查不自动创建整改任务或发送owner通知。写入有具体会话授权即可推进，不要求每种命令分别再确认。

## Semantic Rendering

面向用户的主结论优先渲染 实际返回字段的语义状态，并使用用户当前语言；底层字段名只在 raw evidence、排障或完整清单中保留。下表给出字段值到业务表达的标准映射；其他语言应表达同等业务含义。

字段来源边界：下表同时覆盖官方 OpenAPI 语义和当前 / 未来 CLI schema。只有实际响应或当前 schema 返回的字段和值，才可渲染为确定状态；当前 installed CLI 未返回的字段（例如 `copy_entity`、`manage_collaborator_entity`、`external_access_entity`）或未出现的枚举值，只能在 raw response / schema 实际出现时使用，缺失时必须按 unknown / unsupported 处理，不要臆造。

| Raw field / value | Semantic State | 中文说法 | English phrasing |
|-------------------|----------------|----------|------------------|
| `link_share_entity=anyone_readable` | `link_access=public_readable` | 互联网上获得链接的任何人可阅读 | Anyone on the internet with the link can read |
| `link_share_entity=anyone_editable` | `link_access=public_editable` | 互联网上获得链接的任何人可编辑 | Anyone on the internet with the link can edit |
| `link_share_entity=partner_tenant_readable` | `link_access=partner_readable` | 关联组织内知道链接可读 | People in partner tenants with the link can read |
| `link_share_entity=partner_tenant_editable` | `link_access=partner_editable` | 关联组织内知道链接可编辑 | People in partner tenants with the link can edit |
| `link_share_entity=tenant_readable` | `link_access=tenant_readable` | 公司内知道链接可读 | People in the tenant with the link can read |
| `link_share_entity=tenant_editable` | `link_access=tenant_editable` | 公司内知道链接可编辑 | People in the tenant with the link can edit |
| link sharing explicitly disabled | `link_access=closed` | 未开启链接分享 | Link sharing is disabled |
| `external_access_entity=open` or `external_access=true` | `external_sharing=open` | 允许分享到组织外；不等于已经存在外部协作者 | External sharing is open; this does not mean external collaborators already exist |
| `external_access_entity=allow_share_partner_tenant` | `external_sharing=partner_only` | 仅允许分享到关联组织 | Sharing is allowed only with partner tenants |
| `external_access_entity=closed` or `external_access=false` | `external_sharing=closed` | 当前不允许分享到组织外 | External sharing is disabled |
| `invite_external=true` | `external_invitation=enabled` | 当前允许邀请外部用户 | Inviting external users is enabled |
| `invite_external=false` | `external_invitation=disabled` | 当前不允许邀请外部用户 | Inviting external users is disabled |
| `share_entity=anyone` | `collaborator_org_scope=all_viewers_or_editors` | 所有可阅读或可编辑者可查看、添加、移除协作者 | All viewers or editors can view, add, and remove collaborators |
| `share_entity=same_tenant` | `collaborator_org_scope=tenant_viewers_or_editors` | 组织内可阅读或可编辑者可查看、添加、移除协作者 | Tenant viewers or editors can view, add, and remove collaborators |
| `manage_collaborator_entity=collaborator_can_view` | `collaborator_permission_scope=viewer` | 拥有可阅读权限的协作者可查看、添加、移除协作者 | Collaborators with view permission can view, add, and remove collaborators |
| `manage_collaborator_entity=collaborator_can_edit` | `collaborator_permission_scope=editor` | 拥有可编辑权限的协作者可查看、添加、移除协作者 | Collaborators with edit permission can view, add, and remove collaborators |
| `manage_collaborator_entity=collaborator_full_access` | `collaborator_permission_scope=full_access` | 拥有可管理权限的协作者可查看、添加、移除协作者 | Collaborators with full-access permission can view, add, and remove collaborators |
| `copy_entity=anyone_can_view` | `copy_scope=viewer` | 拥有可阅读权限的用户可复制内容 | Users with view permission can copy content |
| `copy_entity=anyone_can_edit` | `copy_scope=editor` | 拥有可编辑权限的用户可复制内容 | Users with edit permission can copy content |
| `copy_entity=only_full_access` | `copy_scope=full_access` | 仅拥有可管理权限的协作者可复制内容 | Only collaborators with full-access permission can copy content |
| `security_entity=anyone_can_view` | `security_scope=viewer` | 拥有可阅读权限的用户可创建副本、打印、下载 | Users with view permission can create copies, print, and download |
| `security_entity=anyone_can_edit` | `security_scope=editor` | 拥有可编辑权限的用户可创建副本、打印、下载 | Users with edit permission can create copies, print, and download |
| `security_entity=only_full_access` | `security_scope=full_access` | 仅拥有可管理权限的用户可创建副本、打印、下载 | Only users with full-access permission can create copies, print, and download |
| `comment_entity=anyone_can_view` | `comment_scope=viewer` | 拥有可阅读权限的用户可评论 | Users with view permission can comment |
| `comment_entity=anyone_can_edit` | `comment_scope=editor` | 拥有可编辑权限的用户可评论 | Users with edit permission can comment |
| `lock_switch=true` | `lock_state=locked_not_inheriting` | 已限制权限，不再继承父级页面权限 | The node is locked and no longer inherits parent-page permissions |
| `lock_switch=false` | `lock_state=not_locked_or_inheriting` | 未限制权限，可能继承父级页面权限 | The node is not locked and may inherit parent-page permissions |
| field absent / unsupported | `<state>=unknown` | 当前 schema 未返回，无法判断 | The current schema did not return this field, so it is unknown |
| `check_scope=current_public_permission_only` | `check_scope=current_public_permission_only` | 本次判断的是当前目标公共访问和协作权限设置，不是协作者名单或历史权限变更审计 | This check covers the target's current public access and collaboration settings, not collaborator-list or historical permission-change auditing |
| 已成功读取且明确无密级标签 | `sec_label=missing` | 未设置密级标签 | No security label is set |


需要形成变更计划时记录目标、当前值、期望值、字段差异及所选动作；只保留帮助用户判断的信息。范围或状态实质改变时更新计划，不复用过时快照。最终区分已改、已受理/待审批、失败和未覆盖部分。
