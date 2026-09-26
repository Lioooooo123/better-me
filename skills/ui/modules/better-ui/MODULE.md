---
name: better-ui
description: 精修已有产品界面的表面、图标、对齐与动效；从 ui 按需读取，不用于普通界面实现。
---

# UI 细节模块

保留项目的组件、设计 token、信息密度和动效语言。先指出真实界面的具体差异，再选择相关配方；上游给出的数值是示例，不覆盖产品已有规范或用户要求。

| 当前问题 | 只读相关参考 |
|---|---|
| 嵌套圆角、边框、阴影、图片轮廓 | [surfaces](surfaces.md) |
| 图标尺寸、字重、状态与 RTL | [icons](icons.md) |
| 图标切换动效 | [icon transitions](icon-transitions.md) |
| 入场、退场和错峰 | [enter/exit](enter-exit.md) |
| 按压、主题切换和交互动效 | [animations](animations.md) |
| 动效卡顿与 `will-change` | [performance](performance.md) |

几何居中看着偏时才做光学校正。动效不能是状态变化的唯一提示；减少动态效果、键盘、焦点和命中区域沿用产品现有无障碍要求。不要为了细节打磨引入新的图标库、动效依赖或全局 CSS 规则。

按同一状态与宽度比较修改前后，检查受影响的交互状态；无法运行界面时只报告源码证据和未验证部分。
