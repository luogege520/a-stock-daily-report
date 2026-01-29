@echo off
chcp 65001 >nul
echo ======================================
echo 推送代码到 GitHub
echo ======================================
echo.

cd /d "%~dp0"

echo 📝 当前状态：
git status
echo.

echo 🚀 推送到 GitHub...
git push origin main

if %errorlevel% equ 0 (
    echo.
    echo ======================================
    echo ✅ 推送成功！
    echo ======================================
    echo.
    echo 下一步：
    echo 1. 访问 GitHub 仓库查看更新
    echo 2. 进入 Actions 标签
    echo 3. 点击 "Daily A-Stock Report"
    echo 4. 点击 "Run workflow" 手动触发测试
    echo 5. 查看运行日志确认 Gemini API 是否正常调用
    echo.
) else (
    echo.
    echo ======================================
    echo ❌ 推送失败
    echo ======================================
    echo.
    echo 可能原因：
    echo 1. 网络连接问题
    echo 2. 需要配置代理
    echo 3. GitHub 服务暂时不可用
    echo.
    echo 解决方案：
    echo 1. 检查网络连接
    echo 2. 稍后重试
    echo 3. 或使用 GitHub Desktop 推送
    echo.
)

pause
