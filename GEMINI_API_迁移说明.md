# Google Gemini API 迁移说明

## 📋 更新内容

项目已从 StepFun API 迁移到 Google Gemini API。

### 修改的文件

1. **generate_report.py**
   - 更改 API 端点为 Google Gemini API
   - 使用模型：`gemini-1.5-pro`
   - 调整请求格式以符合 Gemini API 规范
   - 环境变量从 `STEPFUN_API_KEY` 改为 `GEMINI_API_KEY`

2. **.env.example**
   - 更新环境变量配置示例
   - `STEPFUN_API_KEY` → `GEMINI_API_KEY`

3. **.github/workflows/daily-report.yml**
   - 更新 GitHub Actions 密钥引用
   - `secrets.STEPFUN_API_KEY` → `secrets.GEMINI_API_KEY`

## 🔧 配置步骤

### 1. 本地开发配置

创建 `.env` 文件（从 `.env.example` 复制）：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入您的 Gemini API 密钥：

```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

### 2. GitHub Actions 配置

在 GitHub 仓库中设置 Secret：

1. 进入仓库 Settings → Secrets and variables → Actions
2. 点击 "New repository secret"
3. 添加以下 Secret：
   - **Name**: `GEMINI_API_KEY`
   - **Value**: 您的 Gemini API 密钥

### 3. 获取 Gemini API 密钥

1. 访问 [Google AI Studio](https://makersuite.google.com/app/apikey)
2. 登录您的 Google 账号
3. 点击 "Create API Key"
4. 复制生成的 API 密钥

## 🚀 使用说明

### 本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 运行报告生成
python main.py
```

### GitHub Actions 自动运行

- **自动触发**：每个交易日晚上 21:00 (北京时间)
- **手动触发**：在 GitHub Actions 页面点击 "Run workflow"

## 📊 API 对比

| 特性 | StepFun API | Google Gemini API |
|------|-------------|-------------------|
| 模型 | step-1-flash | gemini-1.5-pro |
| 最大输出 Token | 16,000 | 8,192 |
| Temperature | 0.3 | 0.3 |
| 认证方式 | Bearer Token | API Key in URL |
| 请求格式 | OpenAI 兼容 | Gemini 原生格式 |

## ⚠️ 注意事项

1. **API 配额**：
   - Gemini API 有免费配额限制
   - 请查看 [定价页面](https://ai.google.dev/pricing) 了解详情

2. **模型选择**：
   - 当前使用 `gemini-1.5-pro`（平衡性能和成本）
   - 如需更快速度，可改为 `gemini-1.5-flash`
   - 如需更强能力，可改为 `gemini-1.5-pro-latest`

3. **网络要求**：
   - Gemini API 需要访问 `generativelanguage.googleapis.com`
   - 确保网络环境可以访问 Google 服务

## 🔄 回滚到 StepFun API

如需回滚，请执行：

```bash
git checkout HEAD~1 -- generate_report.py .env.example .github/workflows/daily-report.yml
```

## 📝 更新日志

- **2026-01-29**: 迁移到 Google Gemini API
  - 使用 gemini-1.5-pro 模型
  - 更新所有配置文件
  - 保持原有功能不变

## 🆘 故障排查

### 问题：API 调用失败

**可能原因**：
1. API 密钥未设置或错误
2. API 配额已用完
3. 网络连接问题

**解决方案**：
```bash
# 检查环境变量
echo $GEMINI_API_KEY

# 测试 API 连接
curl -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"Hello"}]}]}' \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key=YOUR_API_KEY"
```

### 问题：GitHub Actions 失败

**检查清单**：
- [ ] 确认 `GEMINI_API_KEY` Secret 已正确设置
- [ ] 检查 Actions 日志中的错误信息
- [ ] 验证 API 密钥是否有效

## 📚 相关文档

- [Google Gemini API 文档](https://ai.google.dev/docs)
- [API 快速入门](https://ai.google.dev/tutorials/python_quickstart)
- [定价信息](https://ai.google.dev/pricing)

---

**更新时间**：2026-01-29  
**版本**：v2.1.0 (Gemini)
