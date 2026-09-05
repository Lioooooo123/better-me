# 资源解析、移动权限与内容证据

解析与验证可以在一次读取中完成，复用可靠现有结果，不为满足状态机重复执行。每项需要真实类型、URL/token、源父级/根标识、Wiki space_id（适用时）、相关性依据及执行缺口。

- Drive token/类型不确定时用 [inspect](lark-drive-inspect.md)；Wiki用 [node get](../../lark-wiki/references/lark-wiki-node-get.md)，同时保留 node_token、obj_token、obj_type。
- 文件夹不是普通文档内容；快捷方式保留自身身份及解析出的源，不静默替换用户指定对象。
- 源父级未知时记录未知与恢复限制，不按展示路径编 token。
- 需要 owner/title/URL 才补 `drive metas batch_query`；权限状态从实际响应判断。

## 移动权限边界

读取权限、资源 owner、节点权限和目标写权限是不同事实：

| 移动方式 | 所需证据 |
|---|---|
| Drive→Drive | 源资源可管理、源位置可编辑、目标可写 |
| 文档→Wiki | 源文档可直接迁入及目标节点/空间可写；owner元数据不足以证明全部条件 |
| Wiki→Wiki | 源节点/空间可移动、目标可写；底层文档owner不能证明节点可移动 |
| Wiki→Drive | 源Wiki节点可移出、目标Drive位置可写 |

`drive permission.members auth` 不提供 `full_access` 或 move action，不能用 view/edit/share/manage_public 结果推断全部移动条件。待创建目标看其父级创建/写权限。已知 denied 不执行；无法确认的权限如不能由当前命令的只读预览核实则标注例外，不能伪装为可移动或改变身份绕过。

## 内容证据

[docs fetch](../../lark-doc/references/lark-doc-fetch.md) 可读大纲/相关段，标题已精确且足够强时可复用并注明依据。表格、Base、slides、预览等按 [可选服务](../../lark-shared/references/optional-services.md) 当前 help 选择，不使用臆造的 `sheets +read/+find`。

无权限或格式不支持时保留可见元数据和未验证原因；不自动申请访问。主题相关性与可执行性分别记录，不能因为无移动权限就否认内容相关，也不能因为内容相关就推断可移动。
