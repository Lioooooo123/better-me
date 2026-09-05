# 搜索与召回

按 [drive search](lark-drive-search.md) 使用用户原关键词与已定范围。保留命中 query、真实 URL/token、类型和足够相关性片段。

- 用户提供短语时先保留短语，明确排除词保持；只有过滤条件时用空 query 搭配条件。
- 扩词按覆盖缺口进行，可用真实别名、`intitle:`、`--only-title`、`--only-comment`、类型分拆或 OR；无须每次强制先基础再增强两阶段。扩展保持同一 owner/时间/文件夹范围，不引入不相关类别。
- 完整收集请求需处理剩余分页；`has_more=true` 时保存并继续返回游标。五页之类的内部批次不是结束理由，也不需用户逐批确认。
- 只需定位或摘要时按需求停止，不把所有搜索自动升级为全库穷举。没有更多新证据的扩词可以结束，不能把未读完的已知页面称为完整覆盖。
- 分页错误有限恢复，仍失败则保留游标、已得结果与缺口，继续独立查询；说明部分覆盖，不无限重试。

去重使用稳定身份：Drive `type+token`；Wiki 保留节点身份，同一 obj_token 的多个 node 不合并。token缺失时URL仅作暂时键，无法确定则保留条目并标注。合并重复项时保留各查询证据。

解析与内容验证可以逐批穿插进行，见 [解析和验证](lark-drive-workflow-topic-move-collector-resolve-verify.md)，不要求生成固定 CandidateItem / QueryRecallState JSON。
