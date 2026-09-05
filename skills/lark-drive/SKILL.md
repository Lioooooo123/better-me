---
name: lark-drive
description: 查找和管理飞书云空间文件、文件夹、导入导出、权限与评论。用于云盘文件操作；正文编辑用 lark-doc，Wiki 节点结构用 lark-wiki。
metadata:
  cli-baseline: "1.0.92"
---

# 飞书云空间

已有 URL/token 直接解析使用；仅有名称时搜索并消歧。个人资源默认 `--as user`。Wiki token 不能直接当底层 file token；不明确资源类型时先 inspect。

| 操作 | 参考 |
|---|---|
| 搜索、识别、列目录 | [search](references/lark-drive-search.md)、[inspect](references/lark-drive-inspect.md)、[files-list](references/lark-drive-files-list.md) |
| 创建文件夹、移动、复制 | [create-folder](references/lark-drive-create-folder.md)、[move](references/lark-drive-move.md)、[copy](references/lark-drive-copy.md) |
| 导入、上传 | [import](references/lark-drive-import.md)、[upload](references/lark-drive-upload.md) |
| 导出、下载 | [export](references/lark-drive-export.md)、[download](references/lark-drive-download.md) |
| 改标题、删除 | [update-title](references/lark-drive-update-title.md)、[delete](references/lark-drive-delete.md) |
| 评论 | [list-comments](references/lark-drive-list-comments.md)、[add-comment](references/lark-drive-add-comment.md) |
| 权限设置 | [permission-get-setting](references/lark-drive-permission-get-setting.md)、[permission-guide](references/lark-drive-permission-guide.md) |
| 整理/治理复杂集合 | [workflow](references/lark-drive-workflow.md)，只进入对应范围 |

在线复制用 copy，不用导出再导入或重建正文代替。上传到 Wiki 仍可走 Drive；已有 Wiki 节点移到 Drive 使用 `lark-wiki` 的 move-to-drive。在线文档导出和文件下载不同，遵循相应资源类型。

导入同一目标位置时串行执行并确认异步结果。权限、not-found 或格式错误不重复同参重试；网络/限流按提示做有界重试。

修改范围与授权沿用会话。批量删除、权限公开、转移所有权等先定位具体对象、影响与参数；没有这一级明确授权时先给可审阅计划。已有准确授权不因跨轮丢失，确认 flag 按 `lark-shared` 契约处理。

联动：`lark-doc` 提供正文，`lark-wiki` 提供节点结构；原生 Markdown、表格等可按 [按需能力](../lark-shared/references/optional-services.md) 使用当前 CLI，不自动安装已移除技能。
