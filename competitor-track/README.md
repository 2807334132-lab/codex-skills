# 竞品跟踪 Skill（Competitor Tracking Skill）

> 昆仑元出品 — 面向市场部/产品部/任何需要跟踪竞品动态的团队
>
> 在 Claude Code 中实现"丢文件就能跟踪"的竞品情报自动化工具体系。

## 一句话介绍

把竞品资料丢进一个文件夹，跑 `/competitor init`，系统自动扫描文件、识别竞品、建立跟踪基线、生成全景报告。

## 快速开始

### 安装

```bash
# 方式一：直接运行安装脚本（推荐）
git clone <仓库地址>
cd competitor-track-skill
bash install.sh

# 方式二：手动复制
# 1. 将 competitor-track-skill 整个文件夹复制到 ~/.claude/skills/
# 2. 复制 commands 文件
#    cp commands/competitor.md ~/.claude/commands/
#    cp commands/competitor-setup-cron.md ~/.claude/commands/
```

安装后，在 Claude Code 中运行 `/competitor list` 验证是否加载成功。

### 首次运行

```bash
# 1. 如果有现成的竞品资料（MD/PDF/DOCX），直接导入
/competitor init /path/to/your/files

# 2. 或者手动新增一个竞品
/competitor track "MiniMax"

# 3. 查看跟踪列表
/competitor list

# 4. 设置定时任务（可选）
/competitor-setup-cron
```

## 全部命令

| 命令 | 作用 | 适合谁用 |
|------|------|---------|
| `/competitor init <目录>` | 扫描目录中的文件，自动发现竞品并建立基线 | **所有人** — 零门槛 |
| `/competitor check <名称>` | 查询竞品最新动态（GitHub/新闻/社区） | 日常使用 |
| `/competitor report` | 生成月度全景报告（含 HTML + Feishu 推送） | 月报负责人 |
| `/competitor track <名称>` | 手动新增竞品跟踪基线 | 信息收集人员 |
| `/competitor compare <A> <B>` | 头对头对比两个竞品 | 产品/分析岗 |
| `/competitor threat` | 威胁评估总览 | 管理层看板 |
| `/competitor list` | 列出所有跟踪竞品 | 快速了解范围 |
| `/competitor weekly` | 周度情报采集（配合 Cron） | 自动运行 |

## 目录结构

```
competitor-track-skill/
├── SKILL.md                       ← 主技能文件（唯一注册入口）
├── install.sh                     ← 一键安装脚本
├── README.md                      ← 本文件
│
├── modules/                       ← 分析框架（被主SKILL引用）
│   ├── competitor-analysis.md     ← 通用竞品分析框架
│   ├── threat-scoring.md          ← 威胁评分方法
│   ├── knowledge-discovery.md     ← 知识发现引擎（/init 用）
│   └── report-synthesis.md        ← 报告合成规程
│
├── templates/                     ← 输出模板
│   ├── tracking-log-template.md   ← 跟踪日志模板
│   ├── init-report-template.md    ← 发现报告模板
│   └── report-template.html       ← 全景报告HTML模板
│
├── commands/                      ← Claude Code 斜杠命令
│   ├── competitor.md              ← /competitor
│   └── competitor-setup-cron.md   ← /competitor-setup-cron
│
└── examples/                      ← 示例文件
    └── 示例资料_MiniMax.md        ← 用于测试 init 功能
```

## 核心设计

### 数据驱动
- **不写死任何竞品名、评分、分层** — 所有数据从跟踪日志自动读取
- 新竞品自动进入 P3，评分后自动升级
- P0/P1 数量不固定，取决于竞品池规模

### 评分模型（6维度加权）
| 维度 | 权重 | 含义 |
|------|------|------|
| 产品重叠度 | 25% | 与昆仑元的功能/客户/定位重合度 |
| 市场影响力 | 20% | 品牌认知度 + 媒体覆盖 |
| 技术实力 | 20% | 技术深度 + 研发速度 |
| 商业模式威胁 | 15% | 定价竞争 + 客户争夺 |
| 生态成熟度 | 10% | 社区/合作伙伴规模 |
| 叙事竞争力 | 10% | 品牌故事对昆仑元叙事的侵蚀 |

### 信息可信度标注
所有输出中的每条信息标注来源可信度：
- ✅ 已验证 — 官方或一手来源
- 📄 来源单一 — 仅一个可靠来源
- 🔍 需核实 — 二手渠道
- 💡 推测 — 基于趋势的推测
- ⏳ 过期 — 超过 30 天

## 数据文件约定

所有跟踪数据存储在 `WorkBuddy/Claw/竞品跟踪/`（可自定义路径）：
- `{竞品名}_跟踪日志_{YYYYMMDD}.md` — 单竞品跟踪日志
- `竞品发现报告_{YYYYMMDD}.md` — init 产出
- `竞品全景快照_{YYYYMM}.md` — 月报（Markdown）
- `竞品全景报告_{YYYYMM}.html` — 月报（HTML）
- `竞品对比_{A}_{B}_{YYYYMMDD}.md` — 对比产出

## 与昆仑元现有系统集成

| 系统 | 集成方式 | 状态 |
|------|---------|------|
| Feishu 飞书 | 月报通过 lark-im 推送 Miss Claudian | 待配置 |
| Obsidian | sync_to_obsidian.sh 自动同步 | ✅ 无需配置 |
| Cron 定时 | CronCreate 每周一/每月初 | 需运行 setup-cron |
| doc-parse | init 解析 PDF/DOCX | ✅ 自动调用 |
| 工作记忆 | 新基线注册到 MEMORY.md | ✅ 手动记录 |

## 常见问题

**Q: 需要学 Claude Code 才能用吗？**
A: 不需要。拿到资料后跑 `/competitor init <文件夹路径>` 就行，其他命令是进阶功能。

**Q: 支持哪些文件格式？**
A: `.md` / `.pdf` / `.docx` / `.txt` / `.html`。PDF 和 DOCX 需要 doc-parse skill 可用。

**Q: 跟踪数据存在哪？**
A: `WorkBuddy/Claw/竞品跟踪/` 下，纯 Markdown 文件，可 git 管理可同步 Obsidian。

**Q: 如何把数据给其他同事？**
A: 把 `WorkBuddy/Claw/竞品跟踪/` 整个目录发给对方，他们装上 skill 后自动识别。

---

> 昆仑元 AI · 竞品跟踪系统 · v1.0.0
