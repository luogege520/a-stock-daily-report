# 快速开始指南

5分钟快速部署 A股晚间复盘报告系统！

## 🎯 目标

完成部署后，系统将：
- ✅ 每个交易日晚上 21:00 自动生成报告
- ✅ 自动发送到你的邮箱
- ✅ 保存历史报告供下载

## ⚡ 快速部署（5步）

### 第1步：准备材料（5分钟）

准备以下信息：

| 项目 | 获取方式 | 示例 |
|------|---------|------|
| **StepFun API Key** | [注册获取](https://platform.stepfun.com/) | `sk-xxxxx` |
| **Gmail 邮箱** | 已有 Gmail 账号 | `your@gmail.com` |
| **Gmail 授权码** | [生成授权码](https://myaccount.google.com/apppasswords) | `xxxx xxxx xxxx xxxx` |
| **收件邮箱** | 任意邮箱 | `recipient@example.com` |

**💡 提示**：
- StepFun 新用户有免费额度
- Gmail 授权码不是登录密码，需要单独生成
- 收件邮箱可以是任意邮箱（包括 QQ、163 等）

### 第2步：Fork 仓库（1分钟）

1. 访问项目地址（替换为实际地址）
2. 点击右上角 **Fork** 按钮
3. 等待 Fork 完成

### 第3步：配置 Secrets（3分钟）

1. 进入你 Fork 的仓库
2. 点击 **Settings** → **Secrets and variables** → **Actions**
3. 点击 **New repository secret**，依次添加：

```
名称: STEPFUN_API_KEY
值: 你的 StepFun API Key
```

```
名称: SENDER_EMAIL
值: your@gmail.com
```

```
名称: SENDER_PASSWORD
值: 你的 Gmail 授权码
```

```
名称: RECIPIENT_EMAIL
值: recipient@example.com
```

```
名称: SMTP_SERVER
值: smtp.gmail.com
```

```
名称: SMTP_PORT
值: 587
```

### 第4步：启用 Actions（30秒）

1. 点击仓库顶部的 **Actions** 标签
2. 点击 **I understand my workflows, go ahead and enable them**

### 第5步：测试运行（1分钟）

1. 在 Actions 页面，点击 **Daily A-Stock Report**
2. 点击 **Run workflow** → **Run workflow**
3. 等待运行完成（约2-5分钟）
4. 检查邮箱是否收到报告

## ✅ 完成！

恭喜！你的系统已经部署成功。

现在，系统将在每个交易日晚上 21:00 自动运行。

## 📧 Gmail 授权码获取详细步骤

### 方法一：快速链接
1. 访问：https://myaccount.google.com/apppasswords
2. 选择"邮件"和"其他设备"
3. 点击"生成"
4. 复制 16 位授权码（格式：xxxx xxxx xxxx xxxx）

### 方法二：手动操作
1. 登录 Google 账号
2. 进入"管理您的 Google 账号"
3. 点击左侧"安全性"
4. 找到"两步验证"并开启
5. 返回"安全性"，找到"应用专用密码"
6. 选择"邮件"和"其他设备"
7. 生成并复制授权码

**重要**：
- 授权码只显示一次，请妥善保存
- 授权码是 16 位，包含空格
- 不是你的 Gmail 登录密码

## 🔧 使用其他邮箱

### QQ 邮箱

**Secrets 配置**：
```
SENDER_EMAIL: your@qq.com
SENDER_PASSWORD: QQ邮箱授权码
SMTP_SERVER: smtp.qq.com
SMTP_PORT: 587
```

**授权码获取**：
1. 登录 QQ 邮箱
2. 设置 → 账户 → POP3/IMAP/SMTP
3. 开启 SMTP 服务
4. 生成授权码

### 163 邮箱

**Secrets 配置**：
```
SENDER_EMAIL: your@163.com
SENDER_PASSWORD: 163邮箱授权码
SMTP_SERVER: smtp.163.com
SMTP_PORT: 465
```

**授权码获取**：
1. 登录 163 邮箱
2. 设置 → POP3/SMTP/IMAP
3. 开启 SMTP 服务
4. 设置授权密码

## ❓ 常见问题

### Q: 测试运行失败怎么办？

**A:** 点击失败的运行 → 查看日志 → 根据错误信息排查：
- `Authentication failed`: 邮箱授权码错误
- `API key invalid`: StepFun API Key 错误
- `Connection timeout`: 网络问题，重试即可

### Q: 没有收到邮件？

**A:** 检查：
1. 垃圾邮件文件夹
2. 收件邮箱地址是否正确
3. Actions 运行日志是否显示"邮件发送成功"

### Q: 如何修改运行时间？

**A:** 编辑 `.github/workflows/daily-report.yml`：
```yaml
schedule:
  - cron: '0 13 * * 1-5'  # UTC 13:00 = 北京时间 21:00
```

改为你想要的时间（注意时区转换）。

### Q: 报告内容可以自定义吗？

**A:** 可以！编辑 `generate_report.py` 中的提示词模板。

## 📚 更多文档

- [完整部署指南](DEPLOYMENT.md)
- [项目说明](README.md)
- [提交 Issue](https://github.com/YOUR_USERNAME/a-stock-daily-report/issues)

## 🎉 开始使用

现在，你可以：
- ⏰ 等待每天 21:00 自动运行
- 📧 在邮箱中查看报告
- 📊 在 Actions 中下载历史报告
- 🔧 根据需要自定义配置

**祝你投资顺利！** 📈

---

**需要帮助？** 查看 [完整部署指南](DEPLOYMENT.md) 或 [提交 Issue](https://github.com/YOUR_USERNAME/a-stock-daily-report/issues)
