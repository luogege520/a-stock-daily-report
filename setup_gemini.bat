@echo off
chcp 65001 >nul
echo ======================================
echo Gemini API 配置助手
echo ======================================
echo.

echo 📝 此脚本将帮助您配置 Gemini API 密钥
echo.

:input_key
echo 请输入您的 Gemini API 密钥：
echo （格式类似：AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX）
echo.
set /p API_KEY="API Key: "

if "%API_KEY%"=="" (
    echo.
    echo ❌ API Key 不能为空！
    echo.
    goto input_key
)

echo.
echo 🔍 验证 API Key 格式...

:: 检查是否以 AIza 开头
echo %API_KEY% | findstr /B "AIza" >nul
if errorlevel 1 (
    echo.
    echo ⚠️ 警告：API Key 通常以 AIza 开头
    echo 您输入的密钥可能不正确
    echo.
    set /p CONFIRM="是否继续？(Y/N): "
    if /i not "%CONFIRM%"=="Y" goto input_key
)

echo.
echo 💾 保存到 .env 文件...

:: 创建 .env 文件
(
echo # 环境变量配置文件
echo # Google Gemini API 配置
echo GEMINI_API_KEY=%API_KEY%
echo.
echo # 邮件发送配置
echo SENDER_EMAIL=your_email@gmail.com
echo SENDER_PASSWORD=your_app_password_here
echo RECIPIENT_EMAIL=recipient@example.com
echo.
echo # SMTP 服务器配置
echo SMTP_SERVER=smtp.gmail.com
echo SMTP_PORT=587
) > .env

echo ✅ 配置已保存到 .env 文件
echo.

echo 🧪 测试 API 连接...
echo.

python test_gemini_api.py

echo.
echo ======================================
echo 配置完成
echo ======================================
echo.
echo 下一步：
echo 1. 如果测试成功，运行：python main.py
echo 2. 如果测试失败，检查 API Key 是否正确
echo 3. 获取 API Key：https://makersuite.google.com/app/apikey
echo.

pause
