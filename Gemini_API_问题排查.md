# ⚠️ Gemini API 调用失败问题排查

## 问题现象

生成的报告显示：
```
⚠️ 提示
AI 服务暂时不可用，以下为基础数据报告。
```

## 根本原因

**环境变量 `GEMINI_API_KEY` 未正确配置**

## 解决方案

### 方案 1：使用配置助手（推荐）

1. 双击运行项目目录中的：
   ```
   setup_gemini.bat
   ```

2. 按提示输入您的 Gemini API 密钥

3. 脚本会自动测试 API 连接

### 方案 2：手动配置

#### 步骤 1：获取 Gemini API 密钥

1. 访问：https://makersuite.google.com/app/apikey
2. 登录 Google 账号
3. 点击 **"Create API Key"** 或 **"Get API Key"**
4. 复制生成的密钥（格式：`AIzaSy...`）

#### 步骤 2：编辑 .env 文件

打开项目目录中的 `.env` 文件，修改：

```env
GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

将 `AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX` 替换为您的真实 API 密钥。

#### 步骤 3：测试 API 连接

运行测试脚本：

```bash
python test_gemini_api.py
```

如果看到 `✅ API 连接成功！`，说明配置正确。

#### 步骤 4：重新生成报告

```bash
python main.py
```

## 详细排查步骤

### 1️⃣ 检查 .env 文件是否存在

在项目目录 `D:\阶跃AI\a-stock-daily-report` 中查找 `.env` 文件。

- ✅ 如果存在，检查内容
- ❌ 如果不存在，从 `.env.example` 复制一份

```bash
copy .env.example .env
```

### 2️⃣ 检查 API Key 格式

正确的 Gemini API Key 格式：
- 以 `AIza` 开头
- 长度约 39 个字符
- 只包含字母、数字、下划线、连字符

**错误示例**：
```env
GEMINI_API_KEY=请在这里填入您的Gemini_API_密钥  ❌
GEMINI_API_KEY=your_gemini_api_key_here  ❌
GEMINI_API_KEY=  ❌（空值）
```

**正确示例**：
```env
GEMINI_API_KEY=AIzaSyABCDEFGHIJKLMNOPQRSTUVWXYZ123456  ✅
```

### 3️⃣ 测试 API 连接

运行测试脚本：

```bash
cd D:\阶跃AI\a-stock-daily-report
python test_gemini_api.py
```

**可能的错误及解决方案**：

#### 错误 1：未找到环境变量

```
❌ 错误：未找到 GEMINI_API_KEY 环境变量
```

**解决**：
- 确认 `.env` 文件存在
- 确认文件中有 `GEMINI_API_KEY=...` 这一行
- 确认没有拼写错误

#### 错误 2：API Key 无效

```
❌ HTTP 错误: 400
错误信息: API key not valid
```

**解决**：
1. 检查 API Key 是否完整复制（没有多余空格或换行）
2. 访问 https://makersuite.google.com/app/apikey 重新生成
3. 确认 API 已启用（首次使用可能需要几分钟激活）

#### 错误 3：配额超限

```
❌ HTTP 错误: 429
错误信息: Resource has been exhausted
```

**解决**：
- 免费版配额：每天 1500 次请求
- 等待配额重置（每天重置）
- 或升级到付费版本

#### 错误 4：网络连接失败

```
❌ 连接错误
无法访问 Google 服务
```

**解决**：
1. 检查网络连接
2. 确认可以访问 Google 服务（可能需要科学上网）
3. 配置代理（如果使用）

### 4️⃣ 检查依赖库

确认已安装 `python-dotenv`：

```bash
pip install python-dotenv
```

或重新安装所有依赖：

```bash
pip install -r requirements.txt
```

## 完整测试流程

### 本地测试

```bash
# 1. 进入项目目录
cd D:\阶跃AI\a-stock-daily-report

# 2. 检查 .env 文件
type .env

# 3. 测试 API 连接
python test_gemini_api.py

# 4. 生成报告
python main.py

# 5. 查看报告
type reports\A股晚间复盘报告_2026-01-29.md
```

### GitHub Actions 测试

如果本地测试成功，但 GitHub Actions 失败：

1. 进入 GitHub 仓库
2. Settings → Secrets and variables → Actions
3. 确认 `GEMINI_API_KEY` Secret 已正确设置
4. 值应该是完整的 API Key（不要包含引号）

## 常见问题 FAQ

### Q1: 为什么本地测试成功，但 GitHub Actions 失败？

**A**: GitHub Actions 使用的是 GitHub Secrets，不是本地的 `.env` 文件。

**解决**：
1. 在 GitHub 仓库设置 Secret：`GEMINI_API_KEY`
2. 值填入您的 API Key
3. 重新运行 GitHub Actions

### Q2: API Key 从哪里获取？

**A**: 
1. 访问：https://makersuite.google.com/app/apikey
2. 登录 Google 账号
3. 点击 "Create API Key"
4. 复制生成的密钥

### Q3: 免费版有什么限制？

**A**: 
- 每分钟：15 次请求
- 每天：1500 次请求
- 对于每日一次的报告生成，完全够用

### Q4: 如何验证 API Key 是否有效？

**A**: 运行测试脚本：
```bash
python test_gemini_api.py
```

### Q5: .env 文件在哪里？

**A**: 
- 位置：`D:\阶跃AI\a-stock-daily-report\.env`
- 如果不存在，从 `.env.example` 复制
- 注意：`.env` 文件可能被隐藏，需要显示隐藏文件

## 快速修复命令

```bash
# 进入项目目录
cd D:\阶跃AI\a-stock-daily-report

# 方法 1：使用配置助手
setup_gemini.bat

# 方法 2：手动创建 .env 文件
echo GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX > .env

# 测试 API
python test_gemini_api.py

# 生成报告
python main.py
```

## 获取帮助

如果以上方法都无法解决问题：

1. 📧 查看测试脚本的详细输出
2. 📋 复制完整的错误信息
3. 🐛 在 GitHub 提交 Issue
4. 📖 查看 [Gemini API 官方文档](https://ai.google.dev/docs)

---

**更新时间**：2026-01-29  
**适用版本**：v2.1.0 (Gemini)
