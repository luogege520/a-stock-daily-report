@echo off
REM 将 Gemini API 更改推送到 GitHub (Windows 版本)

echo ======================================
echo 推送 Gemini API 更新到 GitHub
echo ======================================
echo.

REM 检查是否在正确的目录
if not exist "generate_report.py" (
    echo ❌ 错误：请在项目根目录运行此脚本
    exit /b 1
)

echo 📝 添加更改的文件...
git add generate_report.py
git add .env.example
git add .github/workflows/daily-report.yml
git add README.md
git add GEMINI_API_迁移说明.md
git add GEMINI_配置指南.md
git add update-to-gemini.sh
git add update-to-gemini.bat

echo.
echo 📊 查看更改内容...
git status

echo.
echo 💾 提交更改...
git commit -m "🔄 迁移到 Google Gemini API - 更新 generate_report.py 使用 Gemini API - 修改环境变量从 STEPFUN_API_KEY 到 GEMINI_API_KEY - 更新 GitHub Actions 工作流配置 - 更新 README 和配置文档 - 添加 Gemini API 迁移说明和配置指南 - 使用 gemini-1.5-pro 模型"

echo.
echo 🚀 推送到 GitHub...
git push origin main

echo.
echo ======================================
echo ✅ 推送完成！
echo ======================================
echo.
echo 下一步：
echo 1. 访问 GitHub 仓库 Settings → Secrets
echo 2. 添加 GEMINI_API_KEY Secret
echo 3. 在 Actions 页面手动触发测试
echo.
echo 详细配置说明请查看：
echo - GEMINI_配置指南.md
echo - GEMINI_API_迁移说明.md
echo.
pause
