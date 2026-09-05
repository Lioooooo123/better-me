# 身份与权限

## 认证任务速查

| 用户意图 | 首选命令 / 回答 |
|---|---|
| 获取全部权限 | `lark-cli auth login --domain all --no-wait --json` |
| 按业务域授权 | `lark-cli auth login --domain docs --domain drive --no-wait --json`；`--domain` 可重复，也可用逗号分隔 |
| 指定单个 scope 授权 | `lark-cli auth login --scope "<scope>" --no-wait --json` |
| 检查当前登录态、是谁登录、token 是否有效 | `lark-cli auth status --json --verify`；回答时引用 `identity`、`verified`、`identities.user.status`、`identities.user.userName`、`identities.user.openId`（用户 open id）、`identities.user.tokenStatus`、`identities.user.scope` |
| 快速查看当前身份状态 | `lark-cli whoami`；实际生效的那一个身份 |
| 退出当前机器的用户登录态 | `lark-cli auth logout --json`；`loggedOut:true` 表示注销成功 |
| bot 缺少权限 | 不要执行 `auth login`；引导用户在开发者后台开通 bot scope，优先复用错误里的 `console_url` |
| 取消用户对应用的全部服务端授权 | `auth logout` 只清本机登录态；服务端授权需用户在飞书授权管理页取消 |
| 只取消一个 scope | CLI 不支持单独撤销一个已授予 scope；可重新走最小 scope 授权，或让用户在授权管理页处理 |

机器读取 JSON 时，为减少 `_notice` 干扰，可在命令前加：

```bash
LARKSUITE_CLI_NO_UPDATE_NOTIFIER=1 LARKSUITE_CLI_NO_SKILLS_NOTIFIER=1 lark-cli auth status --json --verify
```

## 身份类型

两种身份类型，通过 `--as` 切换：

| 身份 | 标识 | 获取方式 | 适用场景 |
|------|------|---------|---------|
| user 用户身份 | `--as user` | `lark-cli auth login` 等 | 访问用户自己的资源（日历、云空间/云盘/云存储等） |
| bot 应用身份 | `--as bot` | 自动，只需 appId + appSecret | 应用级操作,访问bot自己的资源 |

## 身份选择原则

输出的 `[identity: bot/user]` 代表当前身份。bot 与 user 表现差异很大，需确认身份符合目标需求：

- **Bot 与用户是不同操作者**：bot 默认不会列出用户私有资源；明确授予bot的资源是否可访问以服务权限和实际响应为准。例如 `--as bot` 查主日历访问的是bot自己的日历
- **Bot 无法代表用户操作**：发消息以应用名义发送，创建文档归属 bot
- **Bot 权限**：只需在飞书开发者后台开通 scope，无需 `auth login`
- **User 权限**：后台开通 scope + 用户通过 `auth login` 授权，两层都要满足

## 身份延续
- CLI命令执行时，身份选择优先级为：显式 `--as` 优先；省略时由 CLI 根据当前配置和可用凭证自动选择(可通过 `lark-cli whoami` 查看 `identity` 和选择逻辑)。
- 因此，盲目省略 `--as` 是不可控的，在明确需要保持某一身份时，建议全程显式选择。

## 权限不足处理

遇到权限相关错误时，**根据当前身份类型采取不同解决方案**。

错误响应中包含关键信息：
- `missing_scopes`：列出缺失的 scope (N选1)
- `console_url`：飞书开发者后台的权限配置链接
- `hint`：建议的修复命令

### Bot 身份（`--as bot`）

将错误中的 `console_url` 原样提供给用户，引导去后台开通 scope。**禁止**对 bot 执行 `auth login`。

### User 身份（`--as user`）

```bash
lark-cli auth login --domain <domain> --no-wait --json          # 按业务域发起授权
lark-cli auth login --scope "<missing_scope>" --no-wait --json  # 按具体 scope 发起授权（推荐，符合最小权限原则）
```

**规则**：auth login 必须指定范围（`--scope`、`--domain` 或 `--recommend`）。多次 login 的 scope 会累积（增量授权）。


### 发起与完成认证

只在用户要求认证管理或当前命令确实未登录/缺scope时发起；正常业务不预跑登录或扩大授权。

```bash
# 立即返回 device_code 与 verification_url
lark-cli auth login --scope "<required_scope>" --no-wait --json
# 用户完成授权后，用本次返回的 device_code 继续
lark-cli auth login --device-code <device_code>
```

将 verification_url 原样作为可点击链接显示，不编解码或改写query。需要扫码时可用 `lark-cli auth qrcode <verification_url> --output ./auth.png`；二维码不是每次登录的必经步骤。

先让用户看到链接，再等待授权状态；避免一个阻塞调用遮住授权提示。使用运行时支持的非阻塞会话或在需要用户操作时交还控制权，不要求固定“先结束一轮，再回复已完成”的仪式。等待期间可继续无依赖工作。

认证成功后恢复原业务命令。device_code只用于本次登录，不输出到报告或提交仓库；过期时沿用原scope/domain/recommend/exclude重新发起，不扩大权限、不复用过期链接。
