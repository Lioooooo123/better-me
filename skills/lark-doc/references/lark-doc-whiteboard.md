# 文档画板

图示确有助于理解时使用，不设图片数量或复杂度配额。主Agent可直接完成；只有运行时允许且存在独立、具体、值得并行的任务才委派，不强制子Agent。

## 插入新图

按图形表达能力选择Mermaid、SVG或PlantUML；CLI读取本地文件时使用CWD内相对路径。

```xml
<whiteboard type="mermaid">graph LR; A --> B</whiteboard>
<whiteboard type="mermaid" path="@./diagram.mmd"></whiteboard>
<whiteboard type="svg" path="@./diagram.svg"></whiteboard>
<whiteboard type="plantuml" path="@./sequence.puml"></whiteboard>
```

SVG需完整svg根与viewBox，不引用外部脚本/图片。文字使用text，不转path；留足宽度应对CJK约1em、Latin约0.6em重排。设计服从原内容和用户风格，不因文字较少擅自补事实。

###### 画板怎么处理 SVG

画板的 svg-parser 把可识别元素转成可编辑节点, 其余降级为内嵌图片(渲染没问题, 虽然不可编辑, 但是可以正常显示)；但非阴影用途的
`<filter>` / `<pattern>` / `<clipPath>` / `<mask>` 等装饰特性画板不支持（见下方⚠️）
**不需要所有元素都可编辑, 但必须避免使用不支持的装饰特性, 且要兼顾可编辑和美观漂亮**

**可识别的元素**

- 形状：`<rect>` / `<circle>` / `<ellipse>` / `<polygon>`
- 连线：`<line>` / `<polyline>` / `<path>`(自动识别为直线 / 折线 / 曲线)
- 文本：`<text>` / `<tspan>` 画板硬编码 Noto Sans SC **文字必须用 `<text>`**
- 分组：`<g>` / `<a>` / `<use>` 引用 `<symbol>`
- 变换：`translate` / `rotate` / `scale` 正常；`skewX` / `skewY` / `matrix(...)` 降级
- 阴影：`<filter>` 里放 `<feDropShadow>` 或标准 drop/inner primitive 链 (`<feGaussianBlur in="SourceAlpha">` + `<feOffset>` + `<feFlood>` + `<feComposite>` + `<feMerge>`), 会被识别成节点阴影, drop 至多 1 个, inner 至多 1 个; 其余 filter 效果不识别
- 渐变：`<linearGradient>` / `<radialGradient>` 在 `<defs>` 中定义, 通过 `fill="url(#id)"` 引用 (载体限 `<rect>` / `<circle>` / `<ellipse>` / `<polygon>` / `<path>`), 需要至少 2 个 `<stop>`, `gradientUnits` 只支持默认的 `objectBoundingBox` (不写即可)

> [!IMPORTANT]
> ⚠️ **不支持的装饰特性**

- `<pattern>` / `<clipPath>` / `<mask>` / 非阴影用途的 `<filter>` (blur / hue-rotate / 复合合成 / `flood-color=url(...)` / 多个 `<feDropShadow>` 等) → 画板不支持，**请避免使用，否则会导致画板渲染问题**
- 渐变边界：`gradientUnits="userSpaceOnUse"` / `spreadMethod="reflect|repeat"` / stops 少于 2 个 / 复杂 `gradientTransform` 会变成不可编辑图片, 视觉正确但失去可编辑性, 若无必要请沿用默认 `objectBoundingBox`


## 编辑与验证

已有画板先从 [docs fetch](lark-doc-fetch.md) 取得真实board_token，复用同一画板。复杂度不要求隔离到另一个Agent；按 [可选画板服务](../../lark-shared/references/optional-services.md) 发现当前更新/导出命令，再读取精确help。

更新不通过删除再插入实现，除非用户已明确要求重建并理解其影响。整板overwrite、SVG有损转换等语义按当前命令说明核对。

```bash
lark-cli whiteboard +export --whiteboard-token <board_token> --output-type preview --output ./preview.png --as user
```

需要视觉检查时导出并查看实际预览；Mermaid/SVG内容完整、无空占位，检查文字与关系。使用返回的真实文件路径与token，不猜输出名。
