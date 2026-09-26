# 权限治理

适用于明确资源、资源列表、Drive文件夹或Wiki容器的权限读取与已授权变更。单资源问题直接读取目标设置；容器递归仅在要求容器覆盖时执行。只有需要活跃度时读访问日志，不强制固定状态机、JSON清单或确认模板。

常用命令与参数见 [命令参考](lark-drive-workflow-permission-governance-commands.md)；业务表达见 [权限含义](lark-drive-workflow-permission-governance-outputs.md)。身份/授权沿用 [shared](../../lark-shared/MODULE.md)，已明确授权的同一动作不再确认。

目标 token/type 不明时用 [inspect](lark-drive-inspect.md)；明确folder URL可直接提取。当前 inspect 支持folder，不沿用旧“不支持folder”的分支。Wiki space URL 是容器标识，直接解析space_id，不当单文档。

读取设置不授权缩权或通知owner；有明确执行要求时完成字段/范围核对后继续。协作者直接列表与成员操作使用对应原子命令，不冒充完整继承链、DLP、历史审计或AI索引检查。

## Discovery Rules

容器范围只能先做只读发现和覆盖摘要，不能在发现阶段执行权限申请、权限 patch 或密级更新。

通用规则：

1. "所有文档"只表示当前身份在确认范围内可枚举到的文档。不可见、无权限、API 不返回或工具预算不足的部分必须进入 `discovery_blockers` 或 `unsupported_checks`。
2. 发现阶段必须生成稳定 `path`。不要只保存 title；同名文档必须能通过 path 或 token 区分。
3. 权限设置读取使用 `drive +permission-get-setting`，目标类型包括 `doc`、`sheet`、`file`、`wiki`、`bitable`、`docx`、`mindnote`、`minutes`、`slides`、`folder`、`apps`；未来新增类型以 shortcut 和 OpenAPI 元数据为准。
4. `minutes` 只能作为 `partial_public_permission` 目标：可读取 / 修改公开权限和 owner 转移能力以运行时 schema 为准，但 `drive metas batch_query` 当前不支持 `minutes`，URL、owner、密级等 metadata 可能进入 `unsupported_checks`。
5. `folder` 作为递归容器时先枚举子资源；如用户明确要查询文件夹自身权限设置，可对该文件夹单独执行 `drive +permission-get-setting --token <folder_token> --type folder`。不要执行 raw `permission.public patch type=folder`，除非 schema 和需求都明确支持。`shortcut`、`catalog` 或缺少 stable token/type 的条目必须记录为 unsupported，除非后续 API 明确解析出支持目标。
6. 对大范围目标输出进度时，只展示已扫描容器数、已发现目标数、已审计目标数、剩余队列或 blocker；不要默认展示内部 page token / cursor。

Wiki space / node 发现：

1. `/wiki/space/<space_id>` 直接解析为 `target_scope=wiki_space`。不要因为 `drive +inspect` 对该 URL 返回 not found 就停止。
2. 用 `wiki +node-list --space-id <space_id>` 读取根节点；当节点 `has_child=true` 时，用该节点的 `node_token` 继续递归读取子节点。
3. Wiki 节点必须同时保留 `node_token`、`obj_token` 和 `obj_type`。权限读取优先用 `type=wiki` + `node_token` 表达 Wiki 节点权限；元数据补充可使用 `obj_type` + `obj_token`。
4. 如果节点只有 `obj_token` / `obj_type`，但无法确认 Wiki 节点权限 token，保留该目标为 partial，并在 `unsupported_checks` 中说明只能读取底层对象或无法完整判断 Wiki 节点权限。

Drive folder 发现：

1. `/drive/folder/<folder_token>` 解析为 `target_scope=drive_folder`。默认继续枚举其子文档；只有用户明确要求文件夹自身权限设置时，才额外调用 `drive +permission-get-setting --token <folder_token> --type folder` 读取该文件夹自身设置。
2. 按 [`lark-drive-files-list.md`](lark-drive-files-list.md) 递归处理 `data.files`、`has_more` 和 `next_page_token`。不要把第一页数量当作完整范围。
3. 只对返回项中的 `folder` 继续递归；对子文档按 `type + token` 归一化为 `discovered_targets`。
4. 如果某个目录分页失败、无 continuation token、权限不足或 API 报错，只阻断该目录分支，并在 `discovery_blockers` 中记录；继续处理其他可枚举分支。

## Fact Read Rules

1. `drive metas batch_query` 单次最多 200 个 `request_docs`；当 `targets` 或 `discovered_targets` 超过 200 个时，必须分批读取并合并结果。
2. `drive +permission-get-setting` 没有批量读取接口；对支持目标逐个读取。单个目标失败时记录 `unsupported_checks` 或 `partial`，不要阻断其他目标。
3. 对 Wiki 发现目标，公开权限读取优先使用 `type=wiki` + `node_token`；metadata 可使用 `obj_type` + `obj_token` 补充 title、owner、URL 和 `sec_label_name`。
4. 当 intent 是 `list_permission_settings` 时，只输出权限设置清单和覆盖限制，不主动生成修复计划。
5. 单目标、多目标明确列表和容器发现目标都必须复用同一套逐目标事实读取与语义归一逻辑；差异只体现在目标来源、coverage summary 和输出聚合。
6. `permission_public` 用户可见含义是“目标公共访问和协作权限设置”，语义以官方 OpenAPI 字段说明为准，同时兼容当前 CLI schema 返回的字段：优先使用 `external_access_entity`，缺失时才用 `external_access` boolean 映射为 `open` / `closed`；`manage_collaborator_entity`、`copy_entity`、`lock_switch` 等字段缺失时标记为 unknown，不要伪造；未识别字段保留在 raw evidence / partial note 中。
7. `drive file.statistics get` 和 `drive file.view_records list` 只在用户要求最近访问、活跃度、闲置暴露、访问复核，或用户提供的 policy 明确依赖活跃度时执行；不要为普通权限审计默认读取访问记录。
8. 访问统计 / 访问记录当前只对 `doc`、`docx`、`sheet`、`bitable`、`mindnote`、`wiki`、`file` 作为支持类型处理。其他类型必须进入 `unsupported_checks`，不能推断活跃度。
9. `view_records` 是访问证据，不是权限列表。没有返回访问记录只能表述为“未获得最近访问证据”或“低活跃候选”，不能表述为“无人有权限”。

## Risk Classification

风险标签只能作为 evidence labels。除非用户提供明确 policy，否则不要表述为绝对违规、已泄露或已外部访问。

默认优先级面向用户决策，而不是制造告警感：

- `P0`：`link_share_entity=anyone_readable/anyone_editable`，互联网公开链接候选风险。
- `P1`：`external_access_entity=open` / `external_access=true`、关联组织访问、公司内链接可编辑，或外部分享且缺少 / 低于 policy 密级标签。
- `P2`：公司内知道链接可读、协作者管理范围较宽。
- `PolicyReview`：复制、创建副本、打印、下载、评论等依赖 policy 的设置；没有明确 policy 时不要称为高风险。
- `Unknown`：读取失败、已删除、无权限、API 不支持、协作者名单 / 继承链 / DLP / AI 索引 / 审计日志未覆盖。

对每个目标按实际字段判断；必要时按 [`lark-drive-workflow-permission-governance-outputs.md`](lark-drive-workflow-permission-governance-outputs.md) 的 `Semantic Rendering` 渲染。`public_exposure_check` 只是 `target_count=1` 的轻量渲染模式；它和多目标、容器诊断复用同一套语义字段与风险分类。该判断只覆盖当前目标公共访问和协作权限设置，不审计协作者名单、历史权限变更、完整继承链或审计日志。

`AI 检索暴露候选风险` 只是基于权限和标签的代理标签。除非另有工具明确返回索引状态，否则不要声称某个文档已经被 Agent、Copilot 或 RAG 索引。

## 写入规则

- 目标公共访问和协作权限设置修改（`drive permission.public patch`）属于高风险写入。授权范围尚不明确时，先展示 target title、token、current setting、desired setting 和准确 field changes。
- 如果 `manage_public_auth.auth_result=false`，禁止 patch。告诉用户需要具备 manage-public 权限的用户，或由 owner 操作。
- 权限设置读取使用 `drive +permission-get-setting`；裸 token 必须传 `--type`，URL 可以自动推断。写入仍使用 `drive permission.public patch`，只 patch 已解析且 schema 明确支持的类型和字段，不要把读取支持的 `folder` 自动外推为可写入。
- 不要 patch 已解析类型不支持的字段。对于 wiki 目标，必须省略 schema 明确标注为 wiki 不支持的字段。
- 密级标签更新和权限设置是不同动作，计划中分别说明；已有会话同时授权两者时可连续执行。
- `drive +apply-permission` 默认不批量执行；每次调用都会向 owner 发送通知。
- `permission_request_candidates` 可以来自用户直接提供的目标、明确列表或容器发现目标；只要能构造 token、type、权限类型和申请理由，就可以进入候选。不要因为目标不在 `discovered_targets` 中而拒绝单目标 / 小列表权限申请。
- 容器范围内的"统一申请权限"必须先产出 `permission_request_candidates`。未展示候选目标、数量、权限类型和 owner 通知影响前，禁止调用 `drive +apply-permission`。
- 用户显式确认批量权限申请后，也必须逐个目标顺序调用 `drive +apply-permission`，并在结果中区分已发起申请、失败、无法构造申请请求和未发现目标。
- `drive permission.members transfer_owner` 属于 owner 转移高风险写入。执行前核对目标、当前 owner、新 owner 的 `member_id` / `member_type`、`need_notification`、`remove_old_owner`、`old_owner_perm`、`stay_put`、执行顺序和验证方式；不能只凭姓名猜测新 owner。
- owner 转移没有 `permission.members auth` 的等价 precheck。执行前只能用 schema 和当前 metadata 做计划，执行后必须用 `drive metas batch_query` fresh read 验证 owner；metadata 不支持的类型必须把验证标记为 partial。
- 批量 owner 转移必须逐个顺序执行；失败项进入结果清单，不要重复执行已成功目标。`remove_old_owner=true` 或 `old_owner_perm` 降权必须单独在确认中高亮。
- 用户要求“生成整改方案 / dry-run / 先看看会改什么”时，只生成 `remediation_plan`，不执行任何写命令。dry-run 必须包含 target count、field changes、跳过原因、验证方式和有限回滚范围。
- 用户基于完整风险清单选择对象时，按稳定ID、URL或清单中明确的选择解析具体目标。无法唯一匹配的选择先核对清单，仍歧义时再问。
- 针对 `selected_risk_items` 生成 dry-run 前，必须重新读取所选目标的 `drive +permission-get-setting`；如果当前设置和清单快照不同，标记为 `changed_since_report` 并跳过或要求用户确认更新后的计划。
- 执行 `drive permission.public patch` 前，必须把当前 `public_permission_facts` 中会被改动的字段保存为 `public_permission_snapshots`。该快照只用于目标公共访问和协作权限设置字段的有限回滚说明，不覆盖协作者、owner、继承权限或密级标签。
- 如果用户要求批量收紧权限，必须按风险分层和目标顺序逐个执行；失败项进入结果清单，不要因为单个失败而重复执行已成功目标。
- 遇到 secure-label downgrade error `1063013` 时，停止重试，并告诉用户需要在文档 UI 中完成审批。
