# better-me 维护约定

本仓库是个人 Codex 技能的源码；`catalog/skills.json` 决定默认安装集合，`catalog/modules.json` 记录按需读取的专用模块，`catalog/migration-baseline.json` 记录首次迁移范围。系统技能和插件缓存由上游维护。

维护流程见 `CONTRIBUTING.md`。统一检查用 `make check`（虚拟环境可传 `PYTHON=.venv/bin/python`）；技能目录级上游比较用 `make upstream`，结果只供审阅，不自动更新源码或基线。

- 修改技能时保留实际领域约束，删除无关仪式、重复全局规则和无条件流程。各技能可独立工作，按需要调用伙伴技能；不用固定流水线。
- 顶层入口用 `SKILL.md` 放共同约束与模块路由；专用模块用 `MODULE.md`，细节再放参考中，按当前任务读取。调整模块时不恢复独立安装入口，除非该能力确需独立触发。
- 引用是指令的一部分。更改入口时同时检查其引用中的冲突和失效路径；不要把旧问题简单藏进 reference。
- 保留已有显式调用策略；安装程序不得修改无关技能、全局权限或认证配置。迁移先预览、备份，再安装；用临时 home 验证安装与恢复。
- `python3 scripts/validate.py` 检查目录、元数据、引用与技能依赖；`python3 -m unittest discover -s tests -v` 验证安装/恢复和实际脚本行为。YAML 检查依赖 PyYAML，见 `requirements-dev.txt`。
- 修改脚本时验证真实输入输出与错误路径。行为案例在 `evals/scenarios.json`；静态通过不等于模型实跑通过，未执行的案例保持未执行。
- 本地备份和用户实际工作材料留在 `.local/` 或用户指定位置，不进入技能模板。来源与上游许可见 `catalog/`。
