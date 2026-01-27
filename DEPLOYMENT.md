# 部署指南

本文档详细说明如何将 A股晚间复盘报告系统部署到 GitHub，实现自动化运行。

## 📋 前置准备

### 1. GitHub 账号
- 如果没有，请先注册：https://github.com/signup

### 2. StepFun API 密钥
- 访问：https://platform.stepfun.com/
- 注册并获取 API Key

### 3. 邮箱配置

#### Gmail 配置
1. 登录 Google 账号
2. 开启两步验证：https://myaccount.google.com/security
3. 生成应用专用密码：
   - 访问：https://myaccount.google.com/apppasswords
   - 选择"邮件"和"其他设备"
   - 生成密码并保存

#### QQ 邮箱配置
1. 登录 QQ 邮箱
2. 进入"设置" -> "账户"
3. 找到"POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务"
4. 开启"SMTP服务"
5. 生成授权码并保存

#### 163 邮箱配置
1. 登录 163 邮箱
2. 进入"设置" -> "POP3/SMTP/IMAP"
3. 开启"SMTP服务"
4. 设置授权密码

## 🚀 部署步骤

### 步骤 1: Fork 仓库

1. 访问项目仓库（替换为你的仓库地址）
2. 点击右上角的 "Fork" 按钮
3. 等待 Fork 完成

### 步骤 2: 配置 Secrets

1. 进入你 Fork 的仓库
2. 点击 `Settings`（设置）
3. 在左侧菜单中选择 `Secrets and variables` -> `Actions`
4. 点击 `New repository secret` 添加以下配置：

#### 必需的 Secrets

| 名称 | 值 | 说明 |
|------|-----|------|
| `STEPFUN_API_KEY` | `sk-xxxxx` | StepFun API 密钥 |
| `SENDER_EMAIL` | `your@gmail.com` | 发件人邮箱 |
| `SENDER_PASSWORD` | `xxxx xxxx xxxx xxxx` | 邮箱授权码（不是登录密码！） |
| `RECIPIENT_EMAIL` | `recipient@example.com` | 收件人邮箱 |
| `SMTP_SERVER` | `smtp.gmail.com` | SMTP 服务器地址 |
| `SMTP_PORT` | `587` | SMTP 端口号 |

**重要提示**：
- `SENDER_PASSWORD` 是应用专用密码/授权码，不是邮箱登录密码
- 每个 Secret 添加后不可查看，请妥善保管

### 步骤 3: 启用 GitHub Actions

1. 点击仓库顶部的 `Actions` 标签
2. 如果看到提示，点击 "I understand my workflows, go ahead and enable them"
3. 找到 "Daily A-Stock Report" workflow

### 步骤 4: 测试运行

1. 在 Actions 页面，点击 "Daily A-Stock Report"
2. 点击右侧的 "Run workflow" 按钮
3. 选择 "main" 分支
4. 点击绿色的 "Run workflow" 按钮
5. 等待运行完成（约 2-5 分钟）

### 步骤 5: 检查结果

#### 查看运行日志
1. 点击刚才运行的 workflow
2. 点击 "generate-and-send-report" 任务
3. 查看每个步骤的输出

#### 下载报告
1. 在 workflow 运行页面
2. 滚动到底部的 "Artifacts" 部分
3. 下载 "daily-report-xxx" 文件

#### 检查邮箱
1. 打开收件人邮箱
2. 查找标题为 "A股晚间复盘报告 - YYYY年MM月DD日" 的邮件
3. 邮件包含 HTML 格式的报告和 Markdown 附件

## ⏰ 自动运行设置

### 默认运行时间
- 每个交易日（周一至周五）晚上 21:00 (北京时间)
- 对应 UTC 时间 13:00

### 修改运行时间

编辑 `.github/workflows/daily-report.yml` 文件：

```yaml
on:
  schedule:
    # 修改这里的 cron 表达式
    - cron: '0 13 * * 1-5'  # UTC 13:00 = 北京时间 21:00
```

#### Cron 表达式说明

格式：`分钟 小时 日 月 星期`

示例：
- `0 13 * * 1-5`：周一至周五 UTC 13:00（北京时间 21:00）
- `30 12 * * 1-5`：周一至周五 UTC 12:30（北京时间 20:30）
- `0 14 * * *`：每天 UTC 14:00（北京时间 22:00）

**时区转换**：北京时间 = UTC + 8 小时

## 🔧 高级配置

### 1. 修改报告内容

编辑 `generate_report.py` 文件中的 `_build_prompt` 方法：

```python
def _build_prompt(self, date_str: str) -> str:
    """构建生成报告的提示词"""
    # 在这里修改提示词模板
    prompt = f"""请帮我生成一份【{date_str}】A股晚间复盘报告...
    
    # 添加或修改你想要的内容
    """
    return prompt
```

### 2. 修改邮件样式

编辑 `send_email.py` 文件中的 `_markdown_to_html` 方法：

```python
def _markdown_to_html(self, markdown_content: str) -> str:
    """将Markdown转换为HTML"""
    # 修改 CSS 样式
    styled_html = f"""
    <style>
        /* 在这里修改样式 */
        body {{ font-family: Arial, sans-serif; }}
    </style>
    """
    return styled_html
```

### 3. 添加多个收件人

修改 `RECIPIENT_EMAIL` Secret 的值：

```
email1@example.com,email2@example.com,email3@example.com
```

然后修改 `send_email.py` 中的发送逻辑：

```python
def send_report(self, recipient_emails: str, ...):
    # 分割多个邮箱
    recipients = [email.strip() for email in recipient_emails.split(',')]
    
    for recipient in recipients:
        # 发送邮件
        ...
```

## 🐛 故障排查

### 问题 1: Workflow 没有自动运行

**可能原因**：
- GitHub Actions 未启用
- Cron 表达式错误
- 仓库长时间无活动被暂停

**解决方案**：
1. 检查 Actions 是否启用
2. 手动运行一次 workflow
3. 定期（每 60 天）手动运行一次

### 问题 2: 邮件发送失败

**可能原因**：
- 邮箱授权码错误
- SMTP 服务器配置错误
- 邮箱安全设置限制

**解决方案**：
1. 重新生成邮箱授权码
2. 检查 SMTP 服务器和端口
3. 查看 Actions 日志中的详细错误信息

### 问题 3: 报告生成失败

**可能原因**：
- StepFun API 密钥错误
- API 额度不足
- 网络连接问题

**解决方案**：
1. 检查 API 密钥是否正确
2. 登录 StepFun 平台查看额度
3. 查看 Actions 日志中的错误信息

### 问题 4: 报告内容不完整

**可能原因**：
- AI 生成超时
- Token 限制
- 提示词过长

**解决方案**：
1. 增加 API 调用的 timeout 时间
2. 调整 max_tokens 参数
3. 简化提示词模板

## 📊 监控和维护

### 查看运行历史
1. 进入 Actions 页面
2. 查看所有运行记录
3. 点击具体运行查看详细日志

### 下载历史报告
1. 进入 Actions 页面
2. 选择某次运行
3. 在 Artifacts 部分下载报告

### 定期检查
- 每周检查一次运行状态
- 每月检查一次 API 额度
- 每季度检查一次邮箱配置

## 💡 最佳实践

### 1. 安全性
- 不要在代码中硬编码密钥
- 定期更换邮箱授权码
- 使用专门的邮箱账号

### 2. 稳定性
- 设置合理的超时时间
- 添加错误重试机制
- 保持 API 额度充足

### 3. 可维护性
- 定期更新依赖包
- 记录配置变更
- 保留运行日志

## 📞 获取帮助

如果遇到问题：

1. **查看文档**：仔细阅读本部署指南
2. **查看日志**：检查 GitHub Actions 运行日志
3. **搜索 Issues**：在仓库的 Issues 中搜索类似问题
4. **提交 Issue**：如果问题未解决，提交新的 Issue

## 🎉 部署完成

恭喜！如果你完成了以上所有步骤，你的 A股晚间复盘报告系统已经成功部署。

现在，系统将在每个交易日晚上 21:00 自动生成报告并发送到你的邮箱。

---

**祝你投资顺利！** 📈
