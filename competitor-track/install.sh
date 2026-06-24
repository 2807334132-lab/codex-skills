#!/bin/bash
# install.sh — 竞品跟踪技能 独立安装脚本
# 使用方法：bash install.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$HOME/.claude/skills/competitor-track"
COMMAND_DIR="$HOME/.claude/commands"
TRACKING_DIR="$HOME/WorkBuddy/Claw/竞品跟踪"

echo "=============================="
echo " 竞品跟踪技能 — 安装脚本"
echo "=============================="
echo ""

# 1. 检查依赖
echo "[1/6] 检查环境..."
if ! command -v claude &> /dev/null; then
  echo "  ⚠️  未检测到 Claude Code CLI，请先安装"
fi
if [ ! -d "$HOME/.claude" ]; then
  echo "  ⚠️  未检测到 .claude 目录，请先运行一次 Claude Code"
fi
echo "  ✓ 环境就绪"

# 2. 创建目录结构
echo "[2/6] 创建目录..."
mkdir -p "$SKILL_DIR/modules"
mkdir -p "$SKILL_DIR/templates"
mkdir -p "$TRACKING_DIR"
echo "  ✓ $SKILL_DIR"
echo "  ✓ $TRACKING_DIR"

# 3. 复制主 SKILL.md
echo "[3/6] 安装主技能文件..."
cp "$SCRIPT_DIR/SKILL.md" "$SKILL_DIR/SKILL.md"
echo "  ✓ SKILL.md"

# 4. 复制模块
echo "[4/6] 安装分析模块..."
for mod in competitor-analysis threat-scoring knowledge-discovery report-synthesis; do
  cp "$SCRIPT_DIR/modules/$mod.md" "$SKILL_DIR/modules/$mod.md"
  echo "  ✓ modules/$mod.md"
done

# 5. 复制模板
echo "[5/6] 安装模板..."
cp "$SCRIPT_DIR/templates/tracking-log-template.md" "$SKILL_DIR/templates/"
cp "$SCRIPT_DIR/templates/init-report-template.md" "$SKILL_DIR/templates/"
cp "$SCRIPT_DIR/templates/report-template.html" "$SKILL_DIR/templates/"
echo "  ✓ 3 个模板"

# 6. 注册斜杠命令
echo "[6/6] 注册斜杠命令..."
mkdir -p "$COMMAND_DIR"
if [ -f "$SCRIPT_DIR/commands/competitor.md" ]; then
  cp "$SCRIPT_DIR/commands/competitor.md" "$COMMAND_DIR/competitor.md"
  cp "$SCRIPT_DIR/commands/competitor-setup-cron.md" "$COMMAND_DIR/competitor-setup-cron.md"
  echo "  ✓ commands/competitor*"
else
  # 从技能目录找 commands（某些版本结构不同）
  echo "  ⚠️  commands 目录未找到，跳过斜杠命令注册"
fi

echo ""
echo "=============================="
echo " ✅ 安装完成！"
echo "=============================="
echo ""
echo "可用命令："
echo "  /competitor              — 竞品跟踪（主命令）"
echo "  /competitor-setup-cron   — 设置定时任务"
echo ""
echo "快速开始："
echo "  1. 查看跟踪列表：/competitor list"
echo "  2. 导入资料：    /competitor init <文件夹路径>"
echo "  3. 新增竞品：    /competitor track <竞品名>"
echo "  4. 查询动态：    /competitor check <竞品名>"
echo "  5. 月报生成：    /competitor report"
echo ""
echo "数据目录：$TRACKING_DIR"
echo "技能路径：$SKILL_DIR"
