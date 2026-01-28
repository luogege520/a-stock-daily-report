# 🔑 API Key 问题解决方案

## 🔴 问题确认

### 您提供的密钥
```
7imwvXl7xSHKMRFRPYvzBRrlhryoSif6MzSImEbomiKz7XdR7l9q1doOEwMTU39M8
```

### 问题
**这不是 StepFun 的 API Key！**

**StepFun API Key 的正确格式**：
```
sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

必须以 `sk-` 开头！

---

## 🔍 您的密钥是什么

您提供的密钥格式看起来像：
- ❌ 不是 API Key
- 可能是应用密钥（App Secret）
- 可能是访问令牌（Access Token）
- 可能是其他类型的凭证

---

## ✅ 解决方案

### 方案一：获取正确的 API Key

#### 步骤 1：登录 StepFun 平台

访问：https://platform.stepfun.com/

#### 步骤 2：进入 API Keys 页面

查找以下入口：
- **API Keys** 菜单
- **密钥管理**
- **API 管理**
- **开发者设置**

#### 步骤 3：创建新的 API Key

1. 点击 **创建 API Key** 或 **新建密钥**
2. 设置名称（如：`a-stock-report`）
3. 点击创建
4. **立即复制 API Key**（只显示一次！）

#### 步骤 4：验证格式

**正确的 API Key 格式**：
```
sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**特征**：
- ✅ 以 `sk-` 开头
- ✅ 后面跟随一串字母和数字
- ✅ 总长度约 40-50 个字符

---

### 方案二：检查是否有多种密钥

StepFun 平台可能有多种密钥：

1. **API Key**（用于 API 调用）
   - 格式：`sk-xxxxx`
   - 用途：调用 API

2. **App Secret**（用于应用认证）
   - 格式：长串字符（无 `sk-` 前缀）
   - 用途：应用级别的认证

**您需要的是 API Key，不是 App Secret！**

---

### 方案三：联系 StepFun 支持

如果找不到 API Key 页面：

1. 查看平台文档：https://platform.stepfun.com/docs
2. 联系客服或技术支持
3. 查看帮助中心

---

## 🧪 如何验证 API Key

### 测试 API Key 是否有效

创建测试文件 `test_api.py`：

```python
import requests

api_key = "sk-你的API密钥"  # 替换为你的 API Key

url = "https://api.stepfun.com/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

payload = {
    "model": "step-1-flash",
    "messages": [
        {"role": "user", "content": "你好"}
    ],
    "max_tokens": 100
}

try:
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text}")
    
    if response.status_code == 200:
        print("\n✅ API Key 有效！")
    else:
        print("\n❌ API Key 无效或有其他问题")
        
except Exception as e:
    print(f"\n❌ 错误: {e}")
```

运行测试：
```bash
python test_api.py
```

**预期结果**：
- ✅ 状态码 200：API Key 有效
- ❌ 状态码 401：API Key 无效
- ❌ 状态码 429：额度不足

---

## 📝 正确配置步骤

### 1. 获取正确的 API Key

确保格式为：`sk-xxxxx`

### 2. 更新 GitHub Secrets

1. 进入仓库 Settings
2. Secrets and variables → Actions
3. 找到 `STEPFUN_API_KEY`
4. 点击编辑（铅笔图标）
5. 粘贴新的 API Key（`sk-` 开头）
6. 点击 Update secret

### 3. 测试运行

1. 进入 Actions 页面
2. 手动触发 workflow
3. 查看日志

**预期看到**：
```
正在调用 StepFun AI 生成报告...
  等待 AI 响应...
  AI 报告生成成功  ✅
```

---

## 🔍 常见错误

### 错误 1：API Key 格式错误

**错误信息**：
```
AI service is temporarily unavailable
```

**原因**：
- API Key 不是以 `sk-` 开头
- API Key 有多余的空格
- 复制时漏掉了部分字符

**解决**：
- 重新复制 API Key
- 确认格式为 `sk-xxxxx`
- 去掉前后空格

### 错误 2：API Key 无效

**错误信息**：
```
HTTP 错误: 401
响应内容: {"error": "Invalid API key"}
```

**原因**：
- API Key 已过期
- API Key 已删除
- API Key 输入错误

**解决**：
- 重新创建 API Key
- 确认复制完整

### 错误 3：额度不足

**错误信息**：
```
HTTP 错误: 429
响应内容: {"error": "Rate limit exceeded"}
```

**原因**：
- API 调用次数超限
- 账户余额不足

**解决**：
- 登录平台查看额度
- 充值或等待额度恢复

---

## 📸 参考截图说明

### 正确的 API Key 页面应该包含：

1. **API Keys** 标题
2. **创建 API Key** 按钮
3. **已有的 API Key 列表**
   - 名称
   - 创建时间
   - 状态（启用/禁用）
   - 操作（删除/编辑）

### 创建 API Key 时：

1. 输入名称
2. 选择权限（如果有）
3. 点击创建
4. **立即复制**（只显示一次！）
5. 格式应该是：`sk-xxxxx`

---

## 🎯 总结

### 问题

您提供的密钥：
```
7imwvXl7xSHKMRFRPYvzBRrlhryoSif6MzSImEbomiKz7XdR7l9q1doOEwMTU39M8
```

**不是** StepFun 的 API Key！

### 解决方案

1. ✅ 登录 https://platform.stepfun.com/
2. ✅ 找到 **API Keys** 页面
3. ✅ 创建新的 API Key
4. ✅ 复制 **以 `sk-` 开头** 的密钥
5. ✅ 更新 GitHub Secrets
6. ✅ 测试运行

### 正确的 API Key 格式

```
sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**必须以 `sk-` 开头！**

---

## 📞 需要帮助？

如果您：
1. 找不到 API Keys 页面
2. 创建的密钥还是不对
3. 不确定哪个是 API Key

**建议**：
- 截图发给我看
- 或者联系 StepFun 技术支持
- 查看平台文档

---

**获取正确的 API Key 后，问题就能解决了！** 🔑
