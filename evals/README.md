# 路由场景与实跑记录

`scenarios.json` 是待验证的任务输入，不是通过记录。`relevant_skills` 只写本仓库默认安装的顶层入口；`expected_modules` 与 `forbidden_modules` 写按需模块。`acceptance` 描述实际结果，`execution_status: not_run` 不能因为 `make check` 通过而改为通过。

修改入口描述、模块路由或安装清单时，至少检查受影响场景的正例和相邻领域的反例。`make check` 只验证名称、父入口、链接和脚本行为。要验证模型选择，在相同模型、工具、权限和输入材料下开启新任务，记录实际加载的入口与模块、关键动作、输出及未满足的验收项。与旧版比较时保留旧版快照；有外部写入的场景使用隔离资源，不能在真实群聊或文档上重放测试发送。

把实跑证据保存在 `evals/results/`，注明日期、版本、运行条件和对应场景 ID。只有观察到的结果才更新状态；无法取得完整轨迹时记录缺口，不按预期推断已读取哪些模块。优先挑选 `small-edit`、`lark-doc-progressive`、`ordinary-react-review` 和 `ui-polish-progressive`，分别检查总入口误触发、飞书路由、React 模块误读和 UI 模块选择。
