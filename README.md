# better-me

把方法用于实际工作。个人编码与工作技能源码。当前维护 28 个技能，均来自本机 `~/.agents/skills/`；按实际任务组合，共享已有材料、决定与验证结果。小任务直接完成，不必跑固定流水线。

| 工作 | 技能 |
|---|---|
| 编码与设计 | think、hunt、check、tdd、codebase-design、domain-modeling、ui、better-ui、improve-react、ios-hig-design |
| 研究与表达 | read、learn、write、show-me、obsidian-vault |
| 求职交付 | html-resume-builder |
| 维护与交接 | health、handoff、to-tickets、gh-fix-ci、resolving-merge-conflicts |
| 飞书 | lark-shared、lark-doc、lark-drive、lark-wiki、lark-im、lark-calendar、lark-task |

`handoff` 和 `to-tickets` 继续保持仅显式调用。其余按描述触发，不会自动安装缺失插件。模型和推理参数由 Codex 配置管理。

## 使用示例

- “定位崩溃并修好”：`hunt`；确实需要模块调整才加入 `codebase-design`。
- “比较三篇文章，把结论存进笔记库”：`read → learn → obsidian-vault`，复用来源和正文。
- “根据已有经历制作岗位简历 PDF”：`write → html-resume-builder`，传递真实事实和既有删减授权。
- “找到飞书文档并整理内容”：`lark-drive → lark-doc`；实际调整知识库节点时才加入 `lark-wiki`。
- “审查 React 代码的可维护性”：`improve-react`；拿到诊断结果后，按实际缺陷决定是否修改。
- “把当前流程画清楚”：`show-me`；界面实现和视觉打磨分别使用 `ui`、`better-ui`。

箭头是可选阶段衔接；只执行目标所需部分。发送消息、发布和外部任务创建按用户已授权的具体范围执行。

## 安装与恢复

仓库应留在固定位置。安装后的个人技能是指向本仓库的符号链接，修改源码即可更新；已加载的 Codex 任务可能需要新建任务才能读取新版本。

```sh
python3 scripts/manage.py install          # 预览
python3 scripts/manage.py install --apply  # 备份后安装
python3 scripts/manage.py status
python3 scripts/manage.py rollback         # 预览恢复
python3 scripts/manage.py rollback --apply
```

默认安装到 `~/.agents/skills/`，备份与迁移日志在 `~/.codex/skill-hub/`。可用 `--home <directory>` 隔离验证。首次迁移只替换已记录且整棵目录指纹一致的原技能；后续新增技能也须与现有目录指纹一致，才能接管为仓库链接。遇到未知或已修改内容就停止。系统技能和插件缓存不在范围内。锁文件只更新本仓库管理的条目；恢复前检查冲突，并保留无关条目的后续修改。

原 24 个飞书技能保留 7 个，另 17 个退出默认安装。少用服务的显式需求优先查询已有 CLI，见[扩展服务说明](skills/lark-shared/references/optional-services.md)，不会自动恢复整套技能。

## 维护与验证

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
make check PYTHON=.venv/bin/python
```

[清单](catalog/skills.json)记录依赖、可选伙伴和来源；[场景用例](evals/scenarios.json)记录行为验收标准。静态检查和脚本回归不等于模型实跑；未执行模型对照，不宣称速度、token 或任务成功率改善。

首次迁移时，原 42 个技能入口合计 503,356 字节，新 26 个合计 43,584 字节，减少 91.3%。这包含移除技能的贡献；是入口体积变化，不是上下文或性能测量。

- [设计依据](docs/design.md)
- [来源与许可](docs/provenance.md)
- [验证记录](docs/verification.md)
- [首次审计](audits/2026-09-05/skill-audit.md)与[原始清单](audits/2026-09-05/skill-inventory.json)保留为修改前快照。

## 上游更新

```sh
make upstream
```

只读检查 8 个上游仓库，并按技能目录树指纹区分 `unchanged`、`skill_changed`、`path_missing` 和 `error`。`repository_changed` 仅表示分支有变化，不代表技能更新。查询失败或响应被截断会返回错误，不能当成没有更新。基础分支检查仍可用 `python3 scripts/check_upstream.py`。

检查固定到本次解析的 commit，不安装、覆盖技能或推进[审阅基线](catalog/upstream-state.json)。本地有改写，发现更新后仍需选择性合入并验证；该文件不是本地等同于上游的安装锁。

26 个技能已核实上游路径；`obsidian-vault` 暂未在其登记来源的当前快照中找到，`show-me` 的本机来源记录缺失，均保留本地版本。官方系统和插件缓存仍由上游安装机制管理。

[2026-09-26 更新记录](docs/upstream-review-2026-09-26.md)列出本次采纳、暂缓和实际验证；[2026-09-07 更新记录](docs/upstream-review-2026-09-07.md)保留历史审阅。

此前已移除 skill-hub、setup-pre-commit、asu-skills 三个入口；历史审计保留当时范围。仓库与本机源码目录现为 better-me；历史备份继续使用 `~/.codex/skill-hub/`，保持恢复记录可用。

[命名与候选筛选记录](docs/praxis-curation.md)记录新增原因、暂不纳入的候选及验证范围。

维护流程见 [CONTRIBUTING.md](CONTRIBUTING.md)；与 Vercel 的对照及取舍见[维护设计](docs/maintenance.md)。
