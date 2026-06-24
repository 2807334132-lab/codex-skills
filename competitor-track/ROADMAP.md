# 竞品跟踪 Skill — 迭代路线图

> 当前版本：v1.0.0（2026-06-22）
> 状态：已部署到本地，可分发给其他同事

---

## 立即做（今天/明天）

### 1. 发版仓库
- [ ] 把 `competitor-track-skill/` 推到 Git 仓库（公司 Git / GitHub 私有仓库）
- [ ] 其他同事 clone 后运行 `bash install.sh` 即可安装

### 2. 设置定时任务
在 Claude Code 中执行：
```
/competitor-setup-cron
```
按提示完成 CronCreate 设置：
- 每周一 08:00 → `/competitor weekly`
- 每月 1 日 09:00 → `/competitor report`

### 3. 补完天工的评分
```
/competitor check 天工
```
给 P0 竞品做首次正式评分，启动优先级自动分配机制。

---

## 短期迭代（v1.1 — 1~2 周内）

### 产品功能矩阵（🚩 最高优先级）
当前 `report` 全景报告中的 L1-L6 产品对比矩阵还是手动填充的。
**目标**：创建一个静态的 `昆仑元_竞品定位.md`，维护昆仑元及各竞品在 6 层能力中的位置，report 时自动读取。

### PDF/DOCX 自动解析落盘测试
`init` 理论上支持 doc-parse 解析 PDF，但需要实测验证：
- [ ] 准备一份 PDF 竞品报告
- [ ] `/competitor init` 扫描，看能否正确提取竞品实体
- [ ] 如遇到问题，在 `knowledge-discovery.md` 中加入降级逻辑

### `/competitor report` 端到端验证
- [ ] 手动跑一次 `/competitor report` 生成完整的全景快照
- [ ] 检查 HTML 报告渲染效果
- [ ] 检查 Feishu 推送是否正常

### 独立安装包可用性测试
- [ ] 让一位市场部同事按 README 独立安装
- [ ] 观察他们在哪一步卡住，完善文档

---

## 中期迭代（v1.2 — 1 个月内）

### 知识图谱化
当前竞品信息是"文件化"的（Markdown 日志），查询效率依赖文件名匹配。
考虑：
- 建立一个轻量索引 `竞品索引.json`，记录每个竞品的元数据（别名、评分、优先级、最近跟踪时间、跟踪日志列表）
- init / track / check 时自动更新索引
- list / threat 直接从索引读取，不用每次 Glob 扫描文件名

### 多渠道情报接入
当前只有 WebSearch/WebFetch 做情报采集。后续可接入：
- **微信公众号自动采集**：通过第三方 RSS/API 接入公众号更新
- **IT 桔子/Crunchbase**：自动获取融资动态
- **GitHub Watch**：竞品仓库的 Release / Issue / PR 自动通知

### 自定义评分模板
当前评分模型（6维度加权）是写死在 `threat-scoring.md` 中的。
目标：允许用户通过 YAML 配置自定义评分维度/权重：

```yaml
scoring:
  dimensions:
    - name: 产品重叠度
      weight: 0.25
      description: 功能匹配度 + 目标客户重合度
    - name: 市场影响力
      weight: 0.20
```

---

## 长期规划（v2.0 — 3 个月内）

### 多团队共享数据
当前跟踪数据在 `WorkBuddy/Claw/竞品跟踪/`（本地目录）。
目标：支持通过飞书文档/飞书 Base 共享竞品数据，多个 team member 可同时读写。

### 竞争预警
当 check 发现重大信号时（如竞品融资、关键版本发布、重要客户流失），自动生成预警通知推送到飞书群。规则可配置：

```yaml
alerts:
  - trigger: release_major
    action: feishu_message
    target: "竞争情报群"
  - trigger: score_change > 10
    action: feishu_message + daily_summary
```

### 市场化仪表板
将竞品全景报告做成一个可交互的 HTML 仪表板（非静态生成），包含：
- 威胁评分雷达图
- 时间序列趋势图
- 竞品对比热力图
- 昆仑元定位偏移可视化

### 与其他技能联动
- 与 `a-stock-data` 联动：自动获取上市竞品的股价/财报数据
- 与 `lark-doc` 联动：将月报自动写入飞书文档版本管理

---

## 运营流程建议

### 日常
| 频次 | 动作 | 谁做 |
|------|------|------|
| 每周一自动 | `/competitor weekly`（Cron） | 系统自动 |
| 每月1日自动 | `/competitor report`（Cron） | 系统自动 |
| 看到新闻 | `/competitor check <竞品名>` | 所有人 |
| 拿到新资料 | `/competitor init <目录>` | 市场部 |

### 团队分工建议
| 角色 | 职责 | 使用命令 |
|------|------|---------|
| 市场分析师 | 竞品跟踪的日常维护 | init / check |
| 产品经理 | 深度对比分析 | compare / threat |
| 市场部负责人 | 月报输出和决策 | report / threat |
| 所有员工 | 随手丢资料 | init |

### 知识沉淀
每次 `check` 后的跟踪日志就是知识沉淀 —— 不需要专门写"竞品分析报告"。
每个月 `report` 生成的 HTML 报告就是正式交付物。
发版本时，`竞品跟踪/` 目录一起 commit，历史可回溯。
