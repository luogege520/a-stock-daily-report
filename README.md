# A股晚间复盘报告自动生成系统

[![Daily Report](https://github.com/YOUR_USERNAME/a-stock-daily-report/actions/workflows/daily-report.yml/badge.svg)](https://github.com/YOUR_USERNAME/a-stock-daily-report/actions/workflows/daily-report.yml)

每个交易日晚上自动生成A股市场复盘报告，并通过邮件发送到指定邮箱。

## ✨ 功能特点

- 🤖 **自动化生成**：使用 Google Gemini AI 自动生成专业的市场复盘报告
- 📊 **全面数据**：涵盖指数、板块、资金流向、热点题材等
- 📧 **邮件推送**：自动发送到指定邮箱，支持 HTML 格式
- ⏰ **定时运行**：每个交易日晚上 21:00 自动执行
- 📁 **报告存档**：自动保存历史报告,方便回顾

## 📋 报告内容

1. **市场概况**：主要指数表现、成交额、涨跌家数
2. **板块分析**：领涨/领跌板块TOP10，核心驱动因素
3. **资金流向**：主力资金、北向资金详细分析
4. **热点题材**：3-5个核心热点深度解析
5. **政策面**：货币政策、产业政策、监管态度
6. **技术面**：上证指数、创业板指技术分析
7. **投资策略**：短期、中长期投资建议
8. **风险提示**：五大风险维度分析
9. **总结展望**：市场特征、驱动因素、后市展望

## 🚀 快速开始

### 1. Fork 本仓库

点击右上角的 "Fork" 按钮，将仓库复制到你的 GitHub 账号下。

### 2. 配置 Secrets

在你的仓库中，进入 `Settings` -> `Secrets and variables` -> `Actions`，添加以下 Secrets：

| Secret 名称 | 说明 | 示例 |
|------------|------|------|
| `GEMINI_API_KEY` | Google Gemini API 密钥 | `AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX` |
| `SENDER_EMAIL` | 发件人邮箱 | `your-email@gmail.com` |
| `SENDER_PASSWORD` | 邮箱授权码 | `your-app-password` |
| `RECIPIENT_EMAIL` | 收件人邮箱 | `recipient@example.com` |
| `SMTP_SERVER` | SMTP 服务器 | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP 端口 | `587` |

#### 🔑 获取 Gemini API 密钥

1. 访问 [Google AI Studio](https://makersuite.google.com/app/apikey)
2. 登录您的 Google 账号
3. 点击 "Create API Key" 或 "Get API Key"
4. 复制生成的 API 密钥
5. 将密钥添加到 GitHub Secrets 中的 `GEMINI_API_KEY`

#### 📧 邮箱配置说明

**Gmail 用户：**
1. 开启两步验证
2. 生成应用专用密码：[https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
3. 使用生成的密码作为 `SENDER_PASSWORD`

**QQ 邮箱用户：**
1. 进入 QQ 邮箱设置 -> 账户
2. 开启 SMTP 服务
3. 生成授权码，使用授权码作为 `SENDER_PASSWORD`
4. SMTP 服务器：`smtp.qq.com`，端口：`587`

**163 邮箱用户：**
1. 进入邮箱设置 -> POP3/SMTP/IMAP
2. 开启 SMTP 服务
3. 设置授权密码
4. SMTP 服务器：`smtp.163.com`，端口：`465` 或 `25`

### 3. 启用 GitHub Actions

1. 进入你的仓库
2. 点击 `Actions` 标签
3. 如果提示启用 workflows，点击 "I understand my workflows, go ahead and enable them"

### 4. 测试运行

点击 `Actions` -> `Daily A-Stock Report` -> `Run workflow` 手动触发一次测试。

## 📅 运行时间

- **自动运行**：每个交易日（周一至周五）晚上 21:00 (UTC+8)
- **手动运行**：随时可以在 Actions 页面手动触发

## 📂 项目结构

```
a-stock-daily-report/
├── .github/
│   └── workflows/
│       └── daily-report.yml      # GitHub Actions 工作流
├── reports/                       # 报告存储目录
├── generate_report.py             # 报告生成模块
├── send_email.py                  # 邮件发送模块
├── main.py                        # 主程序
├── requirements.txt               # Python 依赖
└── README.md                      # 项目说明
```

## 🔧 本地开发

### 环境准备

```bash
# 克隆仓库
git clone https://github.com/YOUR_USERNAME/a-stock-daily-report.git
cd a-stock-daily-report

# 安装依赖
pip install -r requirements.txt

# 创建 .env 文件
cat > .env << EOF
GEMINI_API_KEY=your_gemini_api_key
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_password
RECIPIENT_EMAIL=recipient@example.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EOF
```

### 运行程序

```bash
# 生成报告并发送邮件
python main.py

# 仅生成报告
python generate_report.py

# 仅发送邮件（需要先有报告文件）
python send_email.py recipient@example.com reports/报告文件.md
```

## 📊 报告示例

查看 [示例报告](reports/A股晚间复盘报告_2026-01-23.md)

## 🛠️ 自定义配置

### 修改运行时间

编辑 `.github/workflows/daily-report.yml` 文件中的 cron 表达式：

```yaml
schedule:
  # 每天 21:00 (UTC+8) = 13:00 (UTC)
  - cron: '0 13 * * 1-5'
```

### 修改报告模板

编辑 `generate_report.py` 中的 `_build_prompt` 方法，自定义报告结构和内容。

### 修改邮件样式

编辑 `send_email.py` 中的 `_markdown_to_html` 方法，自定义 HTML 样式。

## ❓ 常见问题

### Q1: 邮件发送失败怎么办？

**A:** 检查以下几点：
1. 邮箱授权码是否正确
2. SMTP 服务器和端口是否正确
3. 邮箱是否开启了 SMTP 服务
4. 检查 GitHub Actions 日志中的错误信息

### Q2: 如何查看历史报告？

**A:** 进入 `Actions` -> 选择某次运行 -> `Artifacts` 下载报告文件。

### Q3: 可以发送到多个邮箱吗？

**A:** 可以，修改 `RECIPIENT_EMAIL` 为多个邮箱，用逗号分隔：
```
recipient1@example.com,recipient2@example.com
```

### Q4: 报告生成失败怎么办？

**A:** 
1. 检查 Gemini API 密钥是否正确
2. 检查 API 额度是否充足（免费版有限制）
3. 确认网络可以访问 Google 服务
4. 查看 GitHub Actions 日志中的详细错误信息

### Q5: 如何修改报告内容？

**A:** 编辑 `generate_report.py` 中的提示词模板，可以自定义报告的结构、内容和风格。

## 📝 更新日志

### v2.1.0 (2026-01-29)
- 🔄 迁移到 Google Gemini API
- 🤖 使用 gemini-1.5-pro 模型
- 📝 更新所有配置文档

### v1.0.0 (2026-01-27)
- ✨ 初始版本发布
- 🤖 支持 AI 自动生成报告
- 📧 支持邮件自动发送
- ⏰ 支持定时任务
- 📁 支持报告存档

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🙏 致谢

- [Google Gemini](https://ai.google.dev/) - AI 模型支持
- [GitHub Actions](https://github.com/features/actions) - 自动化运行
- 数据来源：AkShare 开源金融数据接口

## 📮 联系方式

如有问题或建议，请提交 [Issue](https://github.com/YOUR_USERNAME/a-stock-daily-report/issues)。

---

**免责声明**：本项目生成的报告仅供参考，不构成任何投资建议。投资有风险，入市需谨慎。
