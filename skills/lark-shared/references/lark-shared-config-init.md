# 首次配置 lark-cli

仅在用户要求初始化，或 CLI 明确报告缺少配置时执行。已有配置不重建。先查看当前 `config init --help`；`--new` 创建新配置，只有需要新配置且符合请求时使用。

```bash
# 需要新配置时；会等待用户完成外部操作
lark-cli config init --new
```

使用能读取中间输出的非阻塞会话，把返回授权/配置URL原样展示为可点击链接；需要扫码时再生成PNG二维码。不要强制二维码、自动重建已有配置或为初始化全局安装其它技能。认证完成后的继续方式见 [身份与权限](lark-shared-identity-and-permissions.md)。
