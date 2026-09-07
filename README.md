# Personal Codex Skill Hub

个人编码与工作技能源码。26 个技能按实际任务组合，共享已有材料、决定与验证结果；小任务直接完成，不必跑固定流水线。

| 工作 | 技能 |
|---|---|
| 编码与设计 | think、hunt、check、tdd、codebase-design、domain-modeling、setup-pre-commit、ui、ios-hig-design |
| 研究与表达 | read、learn、write、obsidian-vault |
| 求职交付 | asu-skills、html-resume-builder |
| 维护与交接 | health、handoff、to-tickets |
| 飞书 | lark-shared、lark-doc、lark-drive、lark-wiki、lark-im、lark-calendar、lark-task |
| 跨阶段组合 | skill-hub |

`handoff` 和 `to-tickets` 继续保持仅显式调用。其余按描述触发；Hub 不要求每次对话先加载，也不会自动安装缺失插件。模型和推理参数由 Codex 配置管理。

## 使用示例

- “定位崩溃并修好”：`hunt`；确实需要模块调整才加入 `codebase-design`。
- “比较三篇文章，把结论存进笔记库”：`read → learn → obsidian-vault`，复用来源和正文。
- “根据已有经历制作岗位简历 PDF”：`asu-skills → write → html-resume-builder`，传递真实事实和既有删减授权。
- “找到飞书文档并整理内容”：`lark-drive → lark-doc`；实际调整知识库节点时才加入 `lark-wiki`。

箭头是可选阶段衔接；只执行目标所需部分。发送消息、发布和外部任务创建按用户已授权的具体范围执行。

## 安装与恢复

仓库应留在固定位置。安装后的个人技能是指向本仓库的符号链接，修改源码即可更新；已加载的 Codex 任务可能需要新建任务才能读取新版本。

```sh
python3 scripts/hub.py install          # 预览
python3 scripts/hub.py install --apply  # 备份后安装
python3 scripts/hub.py status
python3 scripts/hub.py rollback         # 预览恢复
python3 scripts/hub.py rollback --apply
```

默认安装到 `~/.agents/skills/`，备份与迁移日志在 `~/.codex/skill-hub/`。可用 `--home <directory>` 隔离验证。首次迁移只替换已记录且整棵目录指纹一致的原技能，遇到未知或已修改内容就停止。系统技能和插件缓存不在范围内。锁文件只更新本仓库管理的条目；恢复前检查冲突，并保留无关条目的后续修改。

原 24 个飞书技能保留 7 个，另 17 个退出默认安装。少用服务的显式需求优先查询已有 CLI，见[扩展服务说明](skills/lark-shared/references/optional-services.md)，不会自动恢复整套技能。

## 维护与验证

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python scripts/validate.py
.venv/bin/python -m unittest discover -s tests -v
```

[清单](catalog/skills.json)记录依赖、可选伙伴和来源；[场景用例](evals/scenarios.json)记录行为验收标准。静态检查和脚本回归不等于模型实跑；未执行模型对照，不宣称速度、token 或任务成功率改善。

首次迁移时，原 42 个技能入口合计 503,356 字节，新 26 个合计 43,584 字节，减少 91.3%。这包含移除技能的贡献；是入口体积变化，不是上下文或性能测量。

- [设计依据](docs/design.md)
- [来源与许可](docs/provenance.md)
- [验证记录](docs/verification.md)
- [首次审计](audits/2026-09-05/skill-audit.md)与[原始清单](audits/2026-09-05/skill-inventory.json)保留为修改前快照。

## 上游更新

```sh
python3 scripts/check_upstream.py
```

只读检查 5 个上游分支是否相对审阅版本变化，不安装或覆盖技能。`repository_changed` 仅代表仓库有变化；下一步按 [上游状态](catalog/upstream-state.json) 中的目录、commit 与树指纹比对，再选择性合入并验证。此文件是审阅基线，不是声称本地完全等于上游的安装锁。

23 个技能已核实上游路径；`obsidian-vault` 暂未在其登记来源的当前快照中找到，保留本地版本。`asu-skills` 与 `skill-hub` 为本地维护。官方系统和插件缓存仍由上游安装机制管理。

[2026-09-07 更新记录](docs/upstream-review-2026-09-07.md)列出本次采纳、跳过和实际验证。
