---
name: ios-hig-design
description: 设计或审查 iOS/iPadOS 的原生体验、导航、safe area、Dynamic Type、VoiceOver 和自适应布局。用于明确平台体验工作；纯 Swift 逻辑问题不触发。
license: MIT
metadata:
  author: wondelai
---

# iOS 平台体验

先看现有界面、设计 token、同类组件、支持的系统版本与设备。保留真实接口字段、产品语义和既有导航，不为美观添加虚构数据或重复入口。

检查受影响的 safe area、系统手势、语义颜色、文字样式、原生控件及熟悉的返回/关闭/键盘行为。Dynamic Type 的大字号不应裁切关键操作；有意义的控件提供合适 VoiceOver 标签、值和顺序，装饰元素避免多余朗读。

按任务覆盖窄宽布局、明暗模式、加载/空/错误状态、文本扩展与 Reduce Motion。尺寸、组件可用性和数值要求可能随版本变化，需要准确数值时核对当前 Apple 官方文档。

只读取相关参考：

- [导航](references/navigation.md)、[控件](references/components.md)、[无障碍](references/accessibility.md)
- [字体](references/typography.md)、[颜色与材质](references/colors-depth.md)、[手势](references/gestures.md)
- [键盘](references/keyboard-input.md)、[权限提示](references/privacy-permissions.md)
- [系统集成](references/system-integration.md)、[组件与扩展](references/widgets-extensions.md)、[图标](references/app-icons.md)

参考中的旧示例不是当前系统行为的替代证据。当前 Apple 文档、项目支持版本和实测结果优先；不强制打分或完整 HIG 清单。

只读审查给具体问题及影响，已要求实现则复用项目 SwiftUI/UIKit 架构完成修改。分别报告源码检查、构建/测试、渲染验收和真机行为。

联动：产品布局用 `ui`，SwiftUI 实现和模拟器能力用已安装 build-ios-apps 插件；只有真正涉及 Figma 设计转换才进入 Figma 工作流。
