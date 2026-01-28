# 🚀 Gemini API 快速配置指南

## 第一步：获取 Gemini API 密钥

1. 访问 **Google AI Studio**：https://makersuite.google.com/app/apikey
2. 使用您的 Google 账号登录
3. 点击 **"Create API Key"** 按钮
4. 选择一个 Google Cloud 项目（或创建新项目）
5. 复制生成的 API 密钥（格式类似：`AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`）

## 第二步：在 GitHub 配置 Secret

1. 进入您的 GitHub 仓库
2. 点击 **Settings** （设置）
3. 在左侧菜单选择 **Secrets and variables** → **Actions**
4. 点击 **New repository secret** 按钮
5. 添加以下 Secret：
   - **Name（名称）**：`GEMINI_API_KEY`
   - **Secret（值）**：粘贴您的 Gemini API 密钥
6. 点击 **Add secret** 保存

## 第三步：验证配置

### 方法 1：手动触发测试

1. 进入仓库的 **Actions** 标签
2. 选择 **Daily A-Stock Report** 工作流
3. 点击 **Run workflow** 按钮
4. 选择分支（通常是 `main`）
5. 点击绿色的 **Run workflow** 按钮
6. 等待运行完成，查看日志确认是否成功

### 方法 2：本地测试（可选）

```bash
# 克隆仓库到本地
git clone https://github.com/YOUR_USERNAME/a-stock-daily-report.git
cd a-stock-daily-report

# 安装依赖
pip install -r requirements.txt

# 创建 .env 文件
echo "GEMINI_API_KEY=your_actual_api_key_here" > .env

# 运行测试
python generate_report.py
```

## 完整的 GitHub Secrets 列表

确保您已配置以下所有 Secrets：

| Secret 名称 | 必需 | 说明 | 获取方式 |
|------------|------|------|---------|
| `GEMINI_API_KEY` | ✅ 是 | Google Gemini API 密钥 | [Google AI Studio](https://makersuite.google.com/app/apikey) |
| `SENDER_EMAIL` | ✅ 是 | 发件人邮箱地址 | 您的邮箱账号 |
| `SENDER_PASSWORD` | ✅ 是 | 邮箱授权码（非登录密码） | 邮箱设置中生成 |
| `RECIPIENT_EMAIL` | ✅ 是 | 收件人邮箱地址 | 接收报告的邮箱 |
| `SMTP_SERVER` | ✅ 是 | SMTP 服务器地址 | Gmail: `smtp.gmail.com` |
| `SMTP_PORT` | ✅ 是 | SMTP 端口号 | Gmail: `587` |

## 邮箱授权码获取方式

### Gmail

1. 进入 Google 账号管理：https://myaccount.google.com/
2. 选择 **安全性** → **两步验证**（需先启用）
3. 滚动到底部，选择 **应用专用密码**
4. 选择应用：**邮件**，设备：**其他（自定义名称）**
5. 输入名称（如 "A股报告系统"）
6. 点击 **生成**，复制 16 位密码
7. 将此密码作为 `SENDER_PASSWORD`

### QQ 邮箱

1. 登录 QQ 邮箱：https://mail.qq.com/
2. 点击 **设置** → **账户**
3. 找到 **POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务**
4. 开启 **SMTP 服务**
5. 点击 **生成授权码**
6. 按提示发送短信验证
7. 复制生成的授权码作为 `SENDER_PASSWORD`
8. SMTP 配置：
   - `SMTP_SERVER`: `smtp.qq.com`
   - `SMTP_PORT`: `587`

### 163 邮箱

1. 登录 163 邮箱：https://mail.163.com/
2. 点击 **设置** → **POP3/SMTP/IMAP**
3. 开启 **SMTP 服务**
4. 点击 **客户端授权密码** → **设置授权密码**
5. 按提示验证并设置授权密码
6. 将授权密码作为 `SENDER_PASSWORD`
7. SMTP 配置：
   - `SMTP_SERVER`: `smtp.163.com`
   - `SMTP_PORT`: `465` 或 `25`

## 常见问题

### ❓ API 密钥无效

**错误信息**：`API key not valid`

**解决方案**：
1. 检查密钥是否完整复制（包含 `AIza` 开头）
2. 确认密钥没有多余的空格或换行
3. 在 Google AI Studio 中重新生成密钥
4. 确认 API 已启用（首次使用可能需要几分钟激活）

### ❓ API 配额超限

**错误信息**：`Resource has been exhausted`

**解决方案**：
1. 查看 [Gemini API 定价](https://ai.google.dev/pricing)
2. 免费版限制：
   - 每分钟 15 次请求
   - 每天 1500 次请求
3. 如需更高配额，考虑升级到付费版本

### ❓ 网络连接失败

**错误信息**：`Connection timeout` 或 `DNS resolution failed`

**解决方案**：
1. GitHub Actions 运行在国外服务器，通常无此问题
2. 如果本地测试失败，检查网络是否可访问 Google 服务
3. 可以使用代理或 VPN

### ❓ 邮件发送失败

**错误信息**：`Authentication failed` 或 `SMTP error`

**解决方案**：
1. 确认使用的是**授权码**而非登录密码
2. 检查 SMTP 服务器和端口是否正确
3. 确认邮箱已开启 SMTP 服务
4. 查看 GitHub Actions 日志中的详细错误

## 测试清单

配置完成后，请检查：

- [ ] Gemini API 密钥已添加到 GitHub Secrets
- [ ] 邮箱相关的 6 个 Secrets 都已配置
- [ ] 手动触发 GitHub Actions 测试成功
- [ ] 收到测试邮件
- [ ] 报告内容正常生成

## 下一步

配置完成后，系统将：

- ✅ 每个交易日（周一至周五）晚上 21:00 自动运行
- ✅ 自动生成当日 A股复盘报告
- ✅ 自动发送邮件到指定邮箱
- ✅ 报告文件保存在 `reports/` 目录
- ✅ GitHub Actions 保留最近 30 天的报告

## 需要帮助？

- 📖 查看 [完整文档](README.md)
- 🔧 查看 [API 迁移说明](GEMINI_API_迁移说明.md)
- 🐛 提交 [Issue](https://github.com/YOUR_USERNAME/a-stock-daily-report/issues)

---

**配置时间**：约 5-10 分钟  
**难度等级**：⭐⭐☆☆☆（简单）
