# 查询日程参与人

本机 `lark-cli 1.0.92` 没有上游新版的 `calendar +list-attendees`；使用已支持的原生只读命令：

```bash
lark-cli calendar event.attendees list --as user \
  --calendar-id '<calendar_id>' --event-id '<event_id>' --page-size 100

# has_more=true 时使用返回游标续页
lark-cli calendar event.attendees list --as user \
  --calendar-id '<calendar_id>' --event-id '<event_id>' \
  --page-size 100 --page-token '<page_token>'
```

使用已知日历 ID；不要把其他日历的事件默认放到主日历查询。参与人类型包括 `user`、`resource`（会议室）、`chat` 和 `third_party`。按返回类型筛选；原生命令没有 shortcut 的 `--type` 参数。

群参与人缺少 `rsvp_status` 不代表所有群成员已接受或拒绝；需要个人状态时另查相应成员数据。完整名单需处理全部分页，不能把第一页或筛选后为空当作无参与人。

若将来安装版本的 `calendar --help` 已列出 `+list-attendees`，再按其 `--help` 使用 `--type` 等新参数。
