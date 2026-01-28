# 🚀 GitHub 上传指令

## 方法一：使用自动脚本（推荐）

### Windows 用户

双击运行：
```
D:\阶跃AI\a-stock-daily-report\upload_to_github.bat
```

然后输入你的仓库地址，例如：
```
https://github.com/YOUR_USERNAME/a-stock-daily-report.git
```

---

## 方法二：手动 Git 命令

### 步骤 1：克隆仓库

```bash
cd D:\阶跃AI
git clone https://github.com/YOUR_USERNAME/a-stock-daily-report.git temp-upload
cd temp-upload
```

### 步骤 2：复制文件

```bash
copy "..\a-stock-daily-report\fetch_data.py" . /Y
copy "..\a-stock-daily-report\generate_report.py" . /Y
copy "..\a-stock-daily-report\main.py" . /Y
copy "..\a-stock-daily-report\requirements.txt" . /Y
copy "..\a-stock-daily-report\send_email.py" . /Y
```

### 步骤 3：提交更改

```bash
git add .
git commit -m "Update to v2.0.0: Use AkShare for real market data"
```

### 步骤 4：推送到 GitHub

```bash
git push
```

### 步骤 5：清理临时目录

```bash
cd ..
rmdir /S /Q temp-upload
```

---

## 方法三：网页上传（最简单）

### 1. 上传 fetch_data.py

1. 访问你的 GitHub 仓库
2. 找到 `fetch_data.py` 文件（如果存在）
3. 点击文件 → 点击编辑（铅笔图标）
4. 删除所有内容
5. 打开本地文件 `D:\阶跃AI\a-stock-daily-report\fetch_data.py`
6. 复制所有内容
7. 粘贴到 GitHub 编辑器
8. Commit message: `Update fetch_data.py to use AkShare`
9. 点击 `Commit changes`

**如果文件不存在**：
1. 点击 `Add file` → `Upload files`
2. 拖拽 `fetch_data.py`
3. Commit message: `Add fetch_data.py with AkShare`
4. 点击 `Commit changes`

### 2. 上传 generate_report.py

重复上述步骤，替换/上传 `generate_report.py`

Commit message: `Update generate_report.py to use AkShare`

### 3. 上传 main.py

重复上述步骤，替换/上传 `main.py`

Commit message: `Update main.py to use AkShare`

### 4. 上传 requirements.txt

重复上述步骤，替换/上传 `requirements.txt`

Commit message: `Update requirements.txt with AkShare`

### 5. 确认 send_email.py 存在

检查仓库中是否有 `send_email.py`，如果没有则上传。

---

## ✅ 验证上传

### 检查文件

访问你的仓库，确认以下文件存在且已更新：

- [ ] fetch_data.py（已更新）
- [ ] generate_report.py（已更新）
- [ ] main.py（已更新）
- [ ] requirements.txt（已更新）
- [ ] send_email.py（存在）

### 查看最新提交

在仓库主页，应该看到最新的提交信息：
```
Update to v2.0.0: Use AkShare for real market data
```

---

## 🧪 测试运行

### 1. 进入 Actions 页面

访问：`https://github.com/YOUR_USERNAME/a-stock-daily-report/actions`

### 2. 手动触发 workflow

1. 点击 `Daily A-Stock Report`
2. 点击 `Run workflow`
3. 选择 `main` 分支
4. 点击绿色的 `Run workflow` 按钮

### 3. 查看运行日志

1. 点击刚才触发的运行
2. 点击 `generate-and-send-report`
3. 查看日志输出

**预期看到**：
```
Fetching A-Share market data (AkShare)
Fetching index data...
  上证指数: 4139.90 (+0.18%)
  深证成指: 14329.91 (+0.09%)
Successfully fetched 5 indices
...
Data fetching completed
```

### 4. 检查邮箱

打开收件邮箱，查找 "A股晚间复盘报告" 邮件。

验证数据：
- ✅ 上证指数应该是真实数据
- ✅ 涨跌家数应该是真实数据

---

## 📋 完整命令（复制粘贴）

### 一键上传命令

```bash
# 进入目录
cd D:\阶跃AI

# 克隆仓库（替换 YOUR_USERNAME）
git clone https://github.com/YOUR_USERNAME/a-stock-daily-report.git temp-upload

# 进入仓库
cd temp-upload

# 复制文件
copy "..\a-stock-daily-report\fetch_data.py" . /Y
copy "..\a-stock-daily-report\generate_report.py" . /Y
copy "..\a-stock-daily-report\main.py" . /Y
copy "..\a-stock-daily-report\requirements.txt" . /Y
copy "..\a-stock-daily-report\send_email.py" . /Y

# 提交更改
git add .
git commit -m "Update to v2.0.0: Use AkShare for real market data"

# 推送到 GitHub
git push

# 返回上级目录
cd ..

# 清理临时目录
rmdir /S /Q temp-upload
```

---

## ❓ 常见问题

### Q: Git 推送时要求输入用户名密码？

**A:** 使用 Personal Access Token 作为密码：

1. 访问：https://github.com/settings/tokens
2. 点击 `Generate new token (classic)`
3. 勾选 `repo` 权限
4. 生成并复制 token
5. 推送时使用 token 作为密码

### Q: 提示 "Permission denied"？

**A:** 检查：
1. 仓库是否属于你的账号
2. 是否有写入权限
3. Token 权限是否正确

### Q: 文件上传后没有变化？

**A:** 
1. 刷新页面
2. 检查提交历史
3. 确认文件内容是否正确

---

## 🎉 完成

上传成功后：

1. ✅ 文件已更新到 GitHub
2. ✅ 使用 AkShare 获取真实数据
3. ✅ 数据准确可靠
4. ✅ 每天 21:00 自动运行

**问题解决了！** 🎊

---

**需要帮助？** 告诉我遇到的具体问题！
