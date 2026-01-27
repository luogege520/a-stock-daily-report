#!/bin/bash
# Git 仓库初始化脚本

echo "🚀 初始化 Git 仓库..."

# 初始化 Git
git init

# 添加所有文件
git add .

# 创建初始提交
git commit -m "Initial commit: A股晚间复盘报告自动生成系统"

echo ""
echo "✅ Git 仓库初始化完成！"
echo ""
echo "📝 下一步操作："
echo "1. 在 GitHub 上创建新仓库"
echo "2. 运行以下命令关联远程仓库："
echo ""
echo "   git remote add origin https://github.com/YOUR_USERNAME/a-stock-daily-report.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. 配置 GitHub Secrets（参考 DEPLOYMENT.md）"
echo "4. 启用 GitHub Actions"
echo ""
