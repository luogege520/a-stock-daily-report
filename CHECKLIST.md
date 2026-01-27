# ✅ 部署检查清单

在部署到 GitHub 之前，请逐项检查以下内容。

---

## 📋 部署前检查

### ✅ 1. 文件完整性检查

- [ ] `generate_report.py` - 报告生成模块
- [ ] `send_email.py` - 邮件发送模块
- [ ] `main.py` - 主程序入口
- [ ] `requirements.txt` - Python 依赖
- [ ] `.github/workflows/daily-report.yml` - GitHub Actions 配置
- [ ] `.env.example` - 环境变量示例
- [ ] `.gitignore` - Git 忽略配置
- [ ] `LICENSE` - 许可证
- [ ] `README.md` - 项目说明
- [ ] `QUICKSTART.md` - 快速开始指南
- [ ] `DEPLOYMENT.md` - 部署指南
- [ ] `PROJECT_STRUCTURE.md` - 项目结构
- [ ] `SETUP_COMPLETE.md` - 设置完成指南
- [ ] `PROJECT_SUMMARY.md` - 项目总结
- [ ] `init-git.sh` - Git 初始化脚本（Linux/Mac）
- [ ] `init-git.bat` - Git 初始化脚本（Windows）
- [ ] `reports/README.md` - 报告目录说明

### ✅ 2. 配置文件检查

#### `.github/workflows/daily-report.yml`
- [ ] cron 表达式正确（默认：`0 13 * * 1-5`）
- [ ] Python 版本正确（默认：`3.11`）
- [ ] Secrets 名称正确
- [ ] Artifacts 配置正确

#### `requirements.txt`
- [ ] 包含 `requests`
- [ ] 包含 `markdown`
- [ ] 包含 `python-dotenv`

#### `.gitignore`
- [ ] 忽略 `__pycache__/`
- [ ] 忽略 `*.pyc`
- [ ] 忽略 `.env`
- [ ] 忽略 `venv/`

---

## 🔑 准备材料检查

### ✅ 3. StepFun API

- [ ] 已注册 StepFun 账号
- [ ] 已获取 API Key
- [ ] API Key 格式正确（`sk-xxxxx`）
- [ ] 确认有足够的额度

### ✅ 4. 邮箱配置

#### Gmail（推荐）
- [ ] 已有 Gmail 账号
- [ ] 已开启两步验证
- [ ] 已生成应用专用密码
- [ ] 授权码格式正确（16位，含空格）

#### QQ 邮箱
- [ ] 已开启 SMTP 服务
- [ ] 已生成授权码
- [ ] SMTP 服务器：`smtp.qq.com`
- [ ] SMTP 端口：`587`

#### 163 邮箱
- [ ] 已开启 SMTP 服务
- [ ] 已设置授权密码
- [ ] SMTP 服务器：`smtp.163.com`
- [ ] SMTP 端口：`465`

### ✅ 5. 收件邮箱

- [ ] 已确认收件邮箱地址
- [ ] 邮箱地址格式正确
- [ ] 可以正常接收邮件

---

## 🐙 GitHub 准备检查

### ✅ 6. GitHub 账号

- [ ] 已有 GitHub 账号
- [ ] 已登录 GitHub
- [ ] 已安装 Git 客户端

### ✅ 7. 创建仓库

- [ ] 仓库名称：`a-stock-daily-report`
- [ ] 仓库类型：Public 或 Private
- [ ] **未**勾选任何初始化选项
- [ ] 已复制仓库 URL

---

## 🚀 部署步骤检查

### ✅ 8. 初始化 Git

- [ ] 已运行 `init-git.bat`（Windows）或 `init-git.sh`（Linux/Mac）
- [ ] Git 仓库初始化成功
- [ ] 已创建初始提交

### ✅ 9. 推送代码

- [ ] 已关联远程仓库
  ```bash
  git remote add origin https://github.com/YOUR_USERNAME/a-stock-daily-report.git
  ```
- [ ] 已切换到 main 分支
  ```bash
  git branch -M main
  ```
- [ ] 已推送代码
  ```bash
  git push -u origin main
  ```
- [ ] 代码推送成功

### ✅ 10. 配置 Secrets

在 GitHub 仓库的 `Settings` -> `Secrets and variables` -> `Actions` 中添加：

- [ ] `STEPFUN_API_KEY` = 你的 StepFun API Key
- [ ] `SENDER_EMAIL` = 发件人邮箱
- [ ] `SENDER_PASSWORD` = 邮箱授权码
- [ ] `RECIPIENT_EMAIL` = 收件人邮箱
- [ ] `SMTP_SERVER` = SMTP 服务器地址
- [ ] `SMTP_PORT` = SMTP 端口号

**重要提示**：
- [ ] 所有 Secrets 名称拼写正确（区分大小写）
- [ ] 所有 Secrets 值正确无误
- [ ] `SENDER_PASSWORD` 是授权码，不是登录密码

### ✅ 11. 启用 GitHub Actions

- [ ] 已进入 `Actions` 页面
- [ ] 已点击 "I understand my workflows, go ahead and enable them"
- [ ] 可以看到 "Daily A-Stock Report" workflow

### ✅ 12. 测试运行

- [ ] 已点击 "Daily A-Stock Report"
- [ ] 已点击 "Run workflow"
- [ ] 已选择 "main" 分支
- [ ] 已点击绿色的 "Run workflow" 按钮
- [ ] Workflow 开始运行

---

## 🧪 测试结果检查

### ✅ 13. 运行状态

- [ ] Workflow 运行完成（绿色✓）
- [ ] 没有错误（红色✗）
- [ ] 运行时间合理（约2-5分钟）

### ✅ 14. 日志检查

点击运行 -> `generate-and-send-report` -> 查看日志：

- [ ] "Checkout repository" 成功
- [ ] "Set up Python" 成功
- [ ] "Install dependencies" 成功
- [ ] "Generate and send report" 成功
  - [ ] 看到 "生成报告..." 日志
  - [ ] 看到 "报告生成成功" 日志
  - [ ] 看到 "发送邮件..." 日志
  - [ ] 看到 "邮件发送成功" 日志
- [ ] "Upload report artifact" 成功

### ✅ 15. Artifacts 检查

- [ ] 在运行页面底部可以看到 "Artifacts"
- [ ] 可以下载 `daily-report-xxx.zip`
- [ ] 解压后可以看到 Markdown 报告文件

### ✅ 16. 邮件检查

- [ ] 收件邮箱收到邮件
- [ ] 邮件主题正确：`A股晚间复盘报告 - YYYY年MM月DD日`
- [ ] 邮件正文显示正常（HTML 格式）
- [ ] 邮件附件存在（Markdown 文件）
- [ ] 附件可以正常打开

---

## 🎯 最终确认

### ✅ 17. 功能确认

- [ ] 报告内容完整
- [ ] 数据格式正确
- [ ] 表格显示正常
- [ ] 样式美观

### ✅ 18. 自动运行确认

- [ ] 已确认运行时间（默认：每天 21:00）
- [ ] 已确认运行频率（默认：周一至周五）
- [ ] 已了解如何修改运行时间

### ✅ 19. 监控和维护

- [ ] 已知道如何查看运行历史
- [ ] 已知道如何下载历史报告
- [ ] 已知道如何查看错误日志
- [ ] 已知道如何手动触发运行

---

## 📚 文档阅读确认

### ✅ 20. 已阅读文档

- [ ] [README.md](README.md) - 项目说明
- [ ] [QUICKSTART.md](QUICKSTART.md) - 快速开始
- [ ] [DEPLOYMENT.md](DEPLOYMENT.md) - 部署指南
- [ ] [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - 项目结构

---

## 🎉 部署完成

如果以上所有项目都已勾选 ✅，恭喜你！部署成功！

### 下一步

1. ⏰ 等待每个交易日晚上 21:00 自动运行
2. 📧 在邮箱中查看报告
3. 📊 在 Actions 中查看运行历史
4. 🔧 根据需要自定义配置

---

## ⚠️ 常见问题

### Q: 某个步骤失败了怎么办？

**A:** 
1. 查看 [DEPLOYMENT.md](DEPLOYMENT.md) 中的"故障排查"部分
2. 查看 GitHub Actions 运行日志
3. 检查 Secrets 配置是否正确
4. 提交 Issue 寻求帮助

### Q: 如何修改配置？

**A:**
1. 修改代码后提交到 GitHub
2. 修改 Secrets 在 GitHub 仓库设置中操作
3. 修改运行时间编辑 `.github/workflows/daily-report.yml`

### Q: 如何停止自动运行？

**A:**
1. 进入仓库的 `Actions` 页面
2. 点击 "Daily A-Stock Report"
3. 点击右上角的 "..." -> "Disable workflow"

---

## 📞 获取帮助

如果遇到问题：

1. 📖 查看文档
2. 🔍 搜索 Issues
3. 💬 提交 Issue
4. 📧 联系作者

---

**祝你部署顺利！** 🎊

**检查清单版本**：v1.0.0  
**最后更新**：2026-01-27
