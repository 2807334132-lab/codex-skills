---
name: competitor-track
description: 昆仑元竞品跟踪系统 — 全维竞品分析、情报采集、威胁评估、报告生成。支持从任意目录自动发现竞品、建立跟踪基线、生成全景报告。
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
  - WebSearch
  - Write
  - CronCreate
---

# 竞品跟踪技能 — /competitor

## 命令速查

| 命令 | 作用 | 使用场景 |
|------|------|---------|
| `/competitor init <dir>` | **扫描目录，自动发现竞品并导入基线** | 🏁 拿到一批新资料，快速建立跟踪 |
| `/competitor check <name>` | 查询竞品最新动态 | 日常监控，获取更新摘要 |
| `/competitor report` | 生成竞品全景月报 | 月度/季度全景分析 |
| `/competitor track <name>` | 手动新增竞品跟踪基线 | 已知竞品直接录入 |
| `/competitor compare <a> <b>` | 头对头对比两个竞品 | 需要深度了解差异时 |
| `/competitor threat` | 展示当前威胁评估总览 | 快速定位最大威胁 |
| `/competitor list` | 列出所有跟踪竞品 | 了解跟踪范围 |
| `/competitor weekly` | 执行周度情报采集 | 配合 Cron 定时任务 |

**数据目录**：`WorkBuddy/Claw/竞品跟踪/`（所有跟踪日志和报告写在此处）


## 重要：本技能只有一个注册入口

本技能只有当前这个 `SKILL.md` 被 Claude Code 注册。`modules/` 下的文件是通过 `Read` 加载的参考文档，**不注册**，不会与其他 skill 冲突。


## 工作流定义

### 1. /competitor init <dir> — 知识发现与基线导入

**适用场景**：市场部或其他部门有一批竞品资料（MD/PDF/DOCX/TXT/HTML），需要自动扫描并建立跟踪基线。

**前置准备**：
1. Read `modules/knowledge-discovery.md`（知识发现引擎规程）
2. Read `modules/competitor-analysis.md`（通用分析框架）
3. Read `templates/init-report-template.md`（发现报告模板）
4. Read `templates/tracking-log-template.md`（跟踪日志模板）

**Phase 1: 目录扫描**
1. Glob 递归扫描 `<dir>` 下所有 `.md` / `.pdf` / `.docx` / `.txt` / `.html`
2. 统计文件类型分布和总容量
3. 排除 `node_modules/`、`.git/`、`dist/`、`build/`、`__pycache__/`、隐藏文件和二进制文件
4. 输出扫描清单给用户确认

**Phase 2: 内容解析（并行 ≤5 并发）**
- `.md` / `.txt` → 直接 Read
- `.pdf` / `.docx` → 如 doc-parse skill 可用，调用 MinerU 转为 Markdown 后 Read；如不可用，标注"需人工解析"
- `.html` → 用 bash htmlq/pandoc 或 Read 后提取正文（去掉 CSS/JS/标签）
- 所有结果暂存（source_file → source_type → content）

**Phase 3: AI 识别 + 差异分析**
1. 汇总所有解析文本
2. 用 WebSearch 辅助识别不明确的竞品实体（如仅提了简称/昵称）
3. 识别以下实体：
   - 竞品名称（公司名/产品名/平台名）
   - 产品/技术描述
   - 客户/合作伙伴提及
   - 融资/估值信息
   - 市场定位关键词
   - 对昆仑元的潜在威胁/机会信号
4. 对比已有基线：grep `WorkBuddy/Claw/竞品跟踪/` 下所有 `*_跟踪日志_*.md`
5. 分类输出：
   - ✅ 新发现（可导入）— 名称清晰，有足够信息
   - 🔍 模糊匹配（需确认）— 名称模糊/可能有歧义
   - ⏭ 已在跟踪中（自动跳过）
   - 💡 低置信度（仅记录不导入）
6. 写入 `竞品发现报告_{YYYYMMDD}.md`（参考 init-report-template.md）

**Phase 4: 导入确认（交互式）**
1. 展示新发现竞品摘要表（每个竞品：名称、主要发现、来源文件、置信度）
2. 等待用户确认要导入哪些
3. 对确认的竞品，逐个：
   a. 填充 tracking-log-template.md
   b. 头部嵌入来源元数据（来源文件路径、发现时间戳、发现方式）
   c. 写入 `{竞品名}_跟踪日志_{YYYYMMDD}.md`
4. 输出导入摘要（"从 xxx 资料中发现了 N 个竞品，已导入 M 个"）
5. 记录到 `MEMORY.md`（竞品跟踪 > 新增基线）

**异常处理**：
- 目录不存在 → 提示并退出
- doc-parse 不可用 → PDF/DOCX 标红"需人工解析"，继续处理其他文件
- 空目录 → 提示并退出
- 所有文件都是已知跟踪竞品 → 输出"无新发现"并给出已有基线的快速 check


### 2. /competitor check <name> — 竞品实时查询

**前置准备**：
1. Read `modules/competitor-analysis.md`
2. Read `modules/threat-scoring.md`

**Phase 1: 加载基线**
1. 查找 `WorkBuddy/Claw/竞品跟踪/` 下最近的 `{name}_跟踪日志_*.md`
   - 精确匹配优先（如 "GPUStack"）
   - 模糊匹配后备（如 "天工" → "天工" 或 "昆仑万维天工"）
2. 如果找不到，提示"未跟踪此竞品"并建议使用 `track` 或 `init`
3. 从日志中提取：当前版本号、上次跟踪时间、已知维度、上次威胁评分

**Phase 2: 情报采集（并行 3 路）**
- Route A: WebFetch GitHub 仓库（如有）tags/releases API，检查新版本
- Route B: WebSearch 近 30 天新闻（"{竞品名}" + "${行业关键词}"）
- Route C: WebSearch 技术评测/社区讨论（"{竞品名}" + "评测"/"更新"/"发布"）

**Phase 3: 差异分析 + 日志追加**
1. 对比"上次状态" vs "本次发现"：
   - 列出变化项（新产品/新功能/新定价/新合作/新叙事）
   - 调用 competitor-analysis.md 框架做增量分析
   - 调用 threat-scoring.md 框架重新评估威胁评分
2. 输出变化摘要（含置信度标注）
3. 追加到 `{name}_跟踪日志_{YYYYMMDD}.md`（如果今天已存在日志，追加今日条目）
4. 如果威胁评分有变化（±5 分以上），输出提示并说明驱动因素

**输出格式**：
```
## GPUStack — 检查结果（{YYYY-MM-DD}）

### 变化摘要
- v2.2 发布（相比上次 v2.1），叙事从 GPU 调度转向 Token 工厂
- 新增功能：GPU 实例服务、Helm Chart、Multi-LoRA
- 社区活跃度：近 30 天 +200 Stars

### 威胁评分变化
- 当前评分：65/100（上月 55）↑+10
- 主要驱动：叙事重构（10 → 25），产品重叠度提升（20 → 30）

### 推荐关注
- [ ] 关注其企业版演进信号
- [ ] 更新定价对比表
```
（信息标注置信度标签：✅ 已验证 / 📄 来源单一 / 🔍 需核实 / 💡 推测 / ⏳ 过期）


### 3. /competitor report — 竞品全景月报

**前置准备**：
1. Read `modules/competitor-analysis.md`
2. Read `modules/threat-scoring.md`
3. Read `modules/report-synthesis.md`
4. Read `templates/report-template.html`

**Phase 1: 准备**
1. 确定报告时间区间（默认当前自然月，支持 `--month YYYYMM` 指定）
2. Glob `WorkBuddy/Claw/竞品跟踪/` 下所有 `*_跟踪日志_*.md`
3. 从每个跟踪日志读取：竞品名、当前评分、优先级
4. 按优先级自动排序：P0 → P1 → P2 → P3
5. 如果存在上期报告（`竞品全景快照_{上月}.md`），加载作为对比基准
6. 输出"竞品清单"给用户确认（含上次跟踪时间标注）

**Phase 2: 综合分析**
1. 按优先级对 P0/P1 竞品执行 check 刷新（调用 check 逻辑，采集情报）
2. 对 P2/P3 竞品执行轻量 check（仅 WebSearch，不深入分析）
3. 综合判断：
   - 逐个竞品当前态势（上升/稳定/下降）
   - 关键事件时间线（所有竞品合并排序）
   - 竞品间交叉影响分析（"A 和 B 合作了，对昆仑元意味着什么"）
   - 本月最大的 3 个竞争信号
   - 昆仑元定位校准建议
4. 评分：按 threat-scoring.md 框架计算全量评分（所有竞品统一评估）
5. 按 report-synthesis.md 结构填充月度全景报告内容
6. 生成数据摘要（含评分变化趋势）

**Phase 3: 发布**
1. 写入 Markdown 版：`竞品全景快照_{YYYYMM}.md`
2. 渲染 HTML 版：
   a. Read `templates/report-template.html`
   b. 用合成数据填充模板中的占位符
   c. 写入 `竞品全景报告_{YYYYMM}.html`
3. 如 lark-im skill 可用，通过飞书发送报告到 Miss Claudian
4. 更新 `MEMORY.md` 中竞品跟踪状态
5. 输出报告摘要给用户

**月报内容**（参考 report-synthesis.md 中 9 个 Section 的定义）：
1. 执行摘要（3-5 条关键发现）
2. 竞争定位评分矩阵（含月度变化）
3. 产品功能矩阵（L1-L6 能力对比）
4. 技术与能力差距
5. 市场叙事对比
6. 商业模式分析
7. 逐竞品威胁评估
8. 历史跟踪日志
9. 推荐行动（🔴🟡🟢）


### 4. /competitor track <name> — 新增跟踪基线

**适用场景**：已知一个竞品名称，需要直接建立跟踪基线。

**前置准备**：
1. Read `modules/competitor-analysis.md`
2. Read `templates/tracking-log-template.md`

**Phase 1: 前置检查**
1. 检查 `WorkBuddy/Claw/竞品跟踪/` 下是否已有该竞品的跟踪日志
2. 如果已有，提示已有基线 + 询问是否要执行 check 更新

**Phase 2: 基线采集（顺序）**
1. WebSearch 搜索竞品基本信息：
   - 公司全称、成立时间、总部地点
   - 核心产品、定位
   - 融资轮次、金额、估值、关键投资人
2. WebFetch 竞品 GitHub 主页（如有）：
   - Stars / Forks / Contributors
   - License / 最近 Release
   - 语言 / 技术栈
3. WebFetch 竞品官网核心页面：
   - 产品定位 / 核心卖点
   - 功能列表（Feature list）
   - 定价信息
   - 目标客户 / 案例
4. WebSearch 新闻/评测初步扫描

**Phase 3: 分析 + 写入**
1. 调用 competitor-analysis.md 框架做初步分析
2. 填充 tracking-log-template.md
3. 写入 `{竞品名}_跟踪日志_{YYYYMMDD}.md`
4. 输出基线摘要（含置信度标注）
5. 如需记录到 `MEMORY.md`，追加一条

**输出格式**：
```
✅ 跟踪基线已建立：{竞品名}

### 基础信息
- 产品类型：{SaaS/开源/一体机/AI模型}
- 最新版本：{vX.X}
- GitHub Stars：{N}
- 商业模式：{免费/订阅/买断}
- 目标用户：{描述}

### 初始评估
- 初步威胁评分：{N}/100（待后续 check 校准）
- 初始优先级：P3 背景（信息待补充）
- 初判产品重叠度：{高/中/低}

### 待补充信息
- [ ] 详细产品功能对比
- [ ] 技术架构评估
- [ ] 定价模型详细分析
```

### 5. /competitor compare <a> <b> — 竞品头对头对比

**前置准备**：
1. Read `modules/competitor-analysis.md`
2. Read `modules/report-synthesis.md`（对比报告结构）

**Phase 1: 数据加载**
1. 查找 A、B 的最近跟踪日志
2. 如果某一方未跟踪，提示并用 WebSearch 即时采集
3. 加载产品矩阵（如有）

**Phase 2: 对比分析**
1. 按 competitor-analysis.md 的 8 个维度做逐项对比
2. 构建对比表格（产品/技术/市场/商业模式/威胁）
3. 标注昆仑元视角（"对昆仑元的影响"）
4. 按 report-synthesis.md 的对比报告结构输出
5. 写入 `竞品对比_{A}_{B}_{YYYYMMDD}.md`
6. 输出对比报告摘要


### 6. /competitor threat — 威胁评估总览

1. 读取所有跟踪日志
2. 按威胁评分降序排列
3. 输出威胁总览表（竞品 / 评分 / 优先级 / 主要威胁向量 / 最近变化 / 关注等级）
4. 标注本月评分上升/下降最多的竞品
5. 输出最高威胁 3 个竞品的快速摘要


### 7. /competitor list — 列出所有跟踪竞品

1. Glob `WorkBuddy/Claw/竞品跟踪/` 下所有 `*_跟踪日志_*.md`
2. 从文件名去重提取竞品名集合
3. 输出跟踪一览表：

```
当前跟踪竞品（共 N 个）：

| 优先级 | 竞品 | 最近跟踪 | 威胁评分 | 跟踪日志数 |
|--------|------|---------|---------|-----------|
| P0 核心 | GPUStack | 2026-06-22 | 65 | 1 |
| P0 核心 | 天工 | 2026-06-22 | 72 | 1 |
| P1 重要 | MiniMax | (尚未跟踪) | - | 0 |
...
```

4. 标注 P0 和 P1 竞品的上次跟踪时间，如果超过跟踪频率阈值则标红


### 8. /competitor weekly — 周度情报采集

**适用场景**：配合 Cron 定时任务，每周一早 08:00 自动执行。

**执行流程**：
1. 读取所有跟踪日志
2. 自动识别 P0 竞品（当前跟踪中威胁评分 Top 2）
3. 对每个 P0 竞品执行 `check`（仅 Phase 2 情报采集，不输出日志到终端）
4. 如发现重大信号（版本更新、融资、关键人员变动），输出提醒
5. 汇总周度摘要（"本周 P0 竞品更新：{正常/有变化}"）
6. 更新 `MEMORY.md` 跟踪活动记录


## Cron 定时任务设置

安装后需要手动设置两个 Cron 定时任务方可实现全自动运行。

### 任务 1：每周一 08:00 — 周度情报采集

执行 `/competitor weekly`。使用 CronCreate 设置：

- cron: `0 8 * * 1`（每周一 08:00）
- prompt: 执行竞品周跟踪：对所有 P0 核心竞品执行 check，输出摘要
- recurring: true
- durable: true

### 任务 2：每月 1 日 09:00 — 月度全景报告

执行 `/competitor report`。使用 CronCreate 设置：

- cron: `0 9 1 * *`（每月 1 日 09:00）
- prompt: 生成上月的竞品全景快照（月报），输出 HTML 报告并发送到飞书 Miss Claudian
- recurring: true
- durable: true

### 为什么 Cron 任务需要单独设置

CronCreate 是用户侧操作，不能在 SKILL.md 中自动执行。
安装后请在 Claude Code 中输入以下命令完成设置：

```
/competitor-setup-cron
```


## 通用规则

### 数据目录约定
- 所有跟踪日志命名：`{竞品名}_跟踪日志_{YYYYMMDD}.md`
- 所有报告命名：`竞品全景快照_{YYYYMM}.md` / `竞品全景报告_{YYYYMM}.html`
- 所有对比命名：`竞品对比_{A}_{B}_{YYYYMMDD}.md`
- 发现报告命名：`竞品发现报告_{YYYYMMDD}.md`

### 信息可信度标注
- ✅ 已验证：从官方来源或一手信息确认
- 📄 来源单一：仅有一个可靠来源
- 🔍 需核实：二手渠道或推理
- 💡 推测：基于趋势的合理推测
- ⏳ 过期：信息超过 30 天

### 优先级校准时注意
- 竞品优先级不需要每次都调整
- 在 `report` 或 `check` 评分变化超过 ±10 分时才自动重新分配优先级
- 手工覆盖：使用 `/competitor priority <name> <P0/P1/P2/P3>`（仅限当前会话）

### 来源引用
- 所有输出中，关键信息附带来源（URL 或本地文件路径）
- WebSearch 结果标注来源网站
- 从文件 `init` 导入的标注文件路径

### 并行限制
- Phase 2 中的并行采集使用 WebFetch/WebSearch，限制 ≤3 路并发
- Knowledge Discovery 中的 doc-parse 解析限制 ≤5 路并发
- 以上为硬限制，不可超过

### 异常处理
- 网络错误（WebFetch/WebSearch 失败）：重试 1 次，仍失败则跳过该路采集，标注"采集失败"
- 竞品名称模糊匹配失败：提示"未找到竞品，请检查名称"，列出相似名称候选
- doc-parse 不可用：PDF/DOCX 文件标红跳过，不阻塞 init 流程
- 空跟踪日志目录：`check` / `report` / `threat` 均输出"暂无跟踪竞品，请先用 track 或 init"并退出
