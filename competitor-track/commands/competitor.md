# /competitor — 竞品跟踪（Competitive Tracking）

昆仑元竞品跟踪系统 — 全维竞品分析、情报采集、威胁评估、报告生成。

## 用法

| 命令 | 说明 |
|------|------|
| `/competitor init <dir>` | 扫描目录，自动发现竞品并导入跟踪基线 |
| `/competitor check <name>` | 查询竞品最新动态 |
| `/competitor report` | 生成本月竞品全景报告（支持 `--month YYYYMM`） |
| `/competitor track <name>` | 手动新增竞品跟踪基线 |
| `/competitor compare <a> <b>` | 竞品头对头对比分析 |
| `/competitor threat` | 威胁评估总览 |
| `/competitor list` | 列出所有跟踪竞品 |
| `/competitor weekly` | 触发周度情报采集 |

## 示例

```
/competitor init WorkBuddy/Claw/竞品跟踪/inputs
/competitor check GPUStack
/competitor report
/competitor compare GPUStack 天工
/competitor list
```

## 数据目录

所有跟踪日志和报告存储在 `WorkBuddy/Claw/竞品跟踪/`。

## 定时任务

首次安装后运行 `/competitor-setup-cron` 设置周报和月报定时任务。
