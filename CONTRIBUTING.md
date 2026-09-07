# 维护 Praxis

技能源码在 `skills/<name>/`，安装集合与依赖在 `catalog/skills.json`，上游审阅版本在 `catalog/upstream-state.json`。安装链接直接读取源码；合入前检查改动会影响哪些实际任务。

## 新增或调整技能

先写出真实使用场景与预期结果。查现有技能和已安装插件能否覆盖；只补规则时优先修改现有技能，有独立触发条件和交付物时才新增入口。

入口使用 `SKILL.md`，YAML 中包含 `name` 和具体的 `description`。详细规则放在直接链接的 `references/`，可重复操作放在 `scripts/`。规则应说明适用条件、原因和可核对的例子；不为很短的技能强制拆文件或生成大篇汇编。

新增入口同步更新清单、上游映射、README 与来源许可。仅显式调用的技能同步 `agents/openai.yaml`。不得把个人改写标记为上游原版；新增原创技能时先扩展来源模型与校验，不能伪造上游记录。

## 更新上游

运行 `make upstream`，只审查 `skill_changed` 对应的目录差异；`path_missing` 需要确认移动或删除，`error` 需要重试或检查来源。未解决的来源保持未解决。

读取旧审阅 commit 与本次 commit 下的技能正文及引用，记录采纳、跳过和本地保留的规则。完成实际审阅后才更新对应 commit、目录树与入口指纹，并同步清单中的来源信息。仓库分支变化不能直接批量推进所有技能的审阅版本。

## 验证与交付

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
make check PYTHON=.venv/bin/python
make status
```

本地和 CI 使用同一个 `make check`。它检查元数据、引用和依赖，并执行脚本回归。安装/恢复改动使用临时 home 验证；行为改动更新 `evals/scenarios.json` 的相关案例，实跑证据放 `evals/results/`，未实跑明确记录。

提交说明写清触发问题、行为变化及已执行验证。来源审阅记录放 `docs/`，临时下载在系统临时目录或 `.local/` 并在结束后清理。发布、推送和安装遵循会话已有授权；不要把它们混入只读检查命令。
