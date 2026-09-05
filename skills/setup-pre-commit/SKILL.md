---
name: setup-pre-commit
description: 为现有仓库配置或修复提交前的格式化、类型及其他已要求的检查。用于明确 pre-commit、Husky 或 lint-staged 请求；不默认提交代码或运行全部测试。
---

# 提交前检查

检查 Git 工作区与暂存状态，读取项目已有 hooks、scripts、格式化工具和包管理器。以 `packageManager`、当前锁文件（包括 bun.lock）和项目约定为准。

为用户要求的检查选择现有工具。已有 Biome、Ruff 或原生 hook 时先复用，不无条件引入 Prettier、Husky 或新的测试栈。新工具的版本和命令以当前官方文档核对。

合并已有 prepare、pre-commit 与 lint-staged 配置，保留原有行为；调用对应包管理器的 exec/run，不固定使用 npx。对文件路径采用参数数组或工具自带处理，考虑空格与非 ASCII 路径。

格式化可限定暂存文件；类型检查和测试按真实工具能力与用户需求选择，不把整个测试套件普遍放进每次提交。

在隔离 fixture 或不会触碰用户暂存内容的受控方式中验证 hook 的失败/成功路径。实际执行 lint-staged 可能暂存或重写文件，先明确影响，不能把它当纯只读探针。

设置完成不自动执行 git add 或 commit。只有会话明确授权提交时，才选择性暂存本次文件并提交，保留其他 WIP 和已有暂存项。

联动：错误由 `hunt` 定位；`check` 可以复核配置差异，已有验证结果直接复用。
