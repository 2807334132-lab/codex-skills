# /competitor-setup-cron — 竞品跟踪定时任务设置

安装竞品跟踪技能后，需要设置两个 Cron 定时任务才能实现全自动运行。

## 任务 1：每周一 08:00 — 周度情报采集

在 Claude Code 中逐字输入（不要省略任何部分）：

```
CronCreate cron:"0 8 * * 1" recurring:true durable:true prompt:"执行竞品周跟踪：对所有 P0 核心竞品执行 check，输出摘要"
```

## 任务 2：每月 1 日 09:00 — 月度全景报告

```
CronCreate cron:"0 9 1 * *" recurring:true durable:true prompt:"生成上月的竞品全景快照（月报），输出 HTML 报告并发送到飞书 Miss Claudian"
```

## 验证

设置后运行 `CronList` 确认两个任务已注册。
