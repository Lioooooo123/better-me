---
name: lark-calendar
description: 查询和安排飞书日程、忙闲、参会人与会议室。用于明确时间安排；会议逐字稿不属于此技能，普通 Codex 提醒使用宿主调度工具。
metadata:
  cli-baseline: "1.0.92"
---

# 飞书日历

按资源归属选身份：个人日程默认 `--as user`，明确 bot 日历才用 `--as bot`。用户说“你帮我创建”仍是个人委托，不改变身份。

查询日程可用 `calendar +agenda`，关键字查询用 `+search-event`，单项详情用 `+get`。先使用已有 calendar_id/event_id；未知参数读取对应 `--help`。时间输出按用户时区并明确日期，避免把全天日程当零点会议。

| 操作 | 参考 |
|---|---|
| 预约、改时间、会议室 | [schedule-meeting](references/lark-calendar-schedule-meeting.md) |
| 创建日程 | [create](references/lark-calendar-create.md) |
| 改字段、增减参与者 | [update](references/lark-calendar-update.md) |
| 可用时段或会议室 | [suggestion](references/lark-calendar-suggestion.md)、[room-find](references/lark-calendar-room-find.md) |
| 查询参与人、会议室名单 | [list-attendees](references/lark-calendar-list-attendees.md) |
| 重复日程 | [recurring](references/lark-calendar-recurring.md) |
| 接受/拒绝、分享加入 | [rsvp](references/lark-calendar-rsvp.md)、[join-event](references/lark-calendar-join-event.md) |

日期、时区、参与者和重复事件的修改范围应在执行前明确；已经确认的内容复用，不能把改一次扩成整系列。会议室需要实际可用时间，不凭名称假定预订成功。

按请求查询必要时间窗并处理分页。冲突检测使用时间区间相交，维护当前活动区间或冲突组最大结束时间，不能只比较相邻两个日程；已拒绝的事件不计入忙碌，接壤不算重叠。

联动：用户要“今日安排和待办”时组合 `lark-task`；只问会议就只查日历。会议信息或妙记属于可选服务，见 `lark-shared` 的 [按需能力](../lark-shared/references/optional-services.md)。
