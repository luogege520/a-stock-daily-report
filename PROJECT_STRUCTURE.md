# 项目文件清单

## 📁 项目结构

```
a-stock-daily-report/
│
├── .github/
│   └── workflows/
│       └── daily-report.yml          # GitHub Actions 工作流配置
│
├── reports/                           # 报告存储目录（自动创建）
│   └── A股晚间复盘报告_YYYY-MM-DD.md
│
├── generate_report.py                 # 核心：报告生成模块
├── send_email.py                      # 核心：邮件发送模块
├── main.py                            # 核心：主程序入口
│
├── requirements.txt                   # Python 依赖包列表
├── .env.example                       # 环境变量配置示例
├── .gitignore                         # Git 忽略文件配置
│
├── README.md                          # 项目说明文档
├── QUICKSTART.md                      # 快速开始指南
├── DEPLOYMENT.md                      # 详细部署指南
│
├── init-git.sh                        # Git 初始化脚本（Linux/Mac）
└── init-git.bat                       # Git 初始化脚本（Windows）
```

## 📄 文件说明

### 核心代码文件

#### `generate_report.py`
- **功能**：生成 A股复盘报告
- **主要类**：`AStockReportGenerator`
- **核心方法**：
  - `generate_report()`: 生成报告
  - `save_report()`: 保存报告
  - `_build_prompt()`: 构建 AI 提示词
  - `_call_ai_api()`: 调用 AI API

#### `send_email.py`
- **功能**：发送邮件
- **主要类**：`EmailSender`
- **核心方法**：
  - `send_report()`: 发送报告邮件
  - `_create_message()`: 创建邮件消息
  - `_markdown_to_html()`: Markdown 转 HTML
  - `_send_email()`: 发送邮件

#### `main.py`
- **功能**：主程序入口
- **流程**：
  1. 生成报告
  2. 发送邮件
  3. 错误处理

### 配置文件

#### `.github/workflows/daily-report.yml`
- **功能**：GitHub Actions 自动化配置
- **触发条件**：
  - 定时：每个交易日 21:00
  - 手动：可随时手动触发
- **运行环境**：Ubuntu Latest + Python 3.11

#### `requirements.txt`
- **功能**：Python 依赖包
- **包含**：
  - `requests`: HTTP 请求
  - `markdown`: Markdown 转 HTML
  - `python-dotenv`: 环境变量管理

#### `.env.example`
- **功能**：环境变量配置示例
- **用途**：本地开发时复制为 `.env`

#### `.gitignore`
- **功能**：Git 忽略文件配置
- **忽略**：
  - Python 缓存文件
  - 虚拟环境
  - 环境变量文件
  - IDE 配置

### 文档文件

#### `README.md`
- **内容**：项目完整说明
- **包含**：
  - 功能介绍
  - 快速开始
  - 配置说明
  - 常见问题

#### `QUICKSTART.md`
- **内容**：5分钟快速部署指南
- **适合**：新手用户快速上手

#### `DEPLOYMENT.md`
- **内容**：详细部署指南
- **包含**：
  - 前置准备
  - 部署步骤
  - 高级配置
  - 故障排查

### 工具脚本

#### `init-git.sh` / `init-git.bat`
- **功能**：初始化 Git 仓库
- **用途**：首次部署时使用

## 🔧 自定义修改指南

### 修改报告内容

**文件**：`generate_report.py`

**位置**：`_build_prompt()` 方法

```python
def _build_prompt(self, date_str: str) -> str:
    prompt = f"""
    # 在这里修改报告模板
    # 可以添加、删除或修改任何章节
    """
    return prompt
```

### 修改邮件样式

**文件**：`send_email.py`

**位置**：`_markdown_to_html()` 方法

```python
def _markdown_to_html(self, markdown_content: str) -> str:
    styled_html = f"""
    <style>
        /* 在这里修改 CSS 样式 */
        body {{ ... }}
        table {{ ... }}
    </style>
    """
    return styled_html
```

### 修改运行时间

**文件**：`.github/workflows/daily-report.yml`

**位置**：`schedule` 部分

```yaml
schedule:
  - cron: '0 13 * * 1-5'  # 修改这里
```

### 添加新功能

1. **添加数据源**：在 `generate_report.py` 中添加新的搜索方法
2. **添加通知方式**：创建新的通知模块（如微信、钉钉）
3. **添加数据分析**：在报告生成前进行数据预处理

## 📊 数据流程

```
1. GitHub Actions 定时触发
   ↓
2. 运行 main.py
   ↓
3. generate_report.py 生成报告
   ├─ 调用 AI API
   ├─ 搜索市场数据
   └─ 生成 Markdown 报告
   ↓
4. send_email.py 发送邮件
   ├─ 转换为 HTML
   ├─ 添加样式
   └─ 发送邮件
   ↓
5. 保存报告到 Artifacts
```

## 🔐 安全性说明

### Secrets 管理
- 所有敏感信息存储在 GitHub Secrets
- 代码中不包含任何密钥
- Secrets 加密存储，无法查看

### 最佳实践
1. 定期更换邮箱授权码
2. 使用专门的邮箱账号
3. 不要在公开场合分享 Secrets
4. 定期检查 API 使用情况

## 📈 性能优化

### API 调用优化
- 设置合理的 timeout
- 添加重试机制
- 缓存常用数据

### 邮件发送优化
- 压缩附件大小
- 优化 HTML 样式
- 批量发送（多收件人）

### 存储优化
- 定期清理旧报告
- 压缩历史文件
- 使用 Git LFS（大文件）

## 🐛 调试技巧

### 本地调试
```bash
# 安装依赖
pip install -r requirements.txt

# 设置环境变量
cp .env.example .env
# 编辑 .env 文件

# 运行程序
python main.py
```

### 查看日志
1. GitHub Actions 页面
2. 点击具体运行
3. 查看每个步骤的输出

### 常见错误
- `ImportError`: 依赖未安装
- `KeyError`: 环境变量未设置
- `ConnectionError`: 网络问题
- `AuthenticationError`: 认证失败

## 📞 获取支持

### 文档资源
- [README.md](README.md): 完整项目说明
- [QUICKSTART.md](QUICKSTART.md): 快速开始
- [DEPLOYMENT.md](DEPLOYMENT.md): 部署指南

### 社区支持
- GitHub Issues: 提交问题
- GitHub Discussions: 讨论交流
- Pull Requests: 贡献代码

## 🎯 下一步

### 功能扩展
- [ ] 支持微信推送
- [ ] 支持钉钉推送
- [ ] 添加数据可视化
- [ ] 支持自定义模板
- [ ] 添加回测功能

### 优化改进
- [ ] 提高报告生成速度
- [ ] 优化邮件样式
- [ ] 添加更多数据源
- [ ] 支持多语言

## 📝 更新日志

### v1.0.0 (2026-01-27)
- ✨ 初始版本发布
- 🤖 支持 AI 自动生成报告
- 📧 支持邮件自动发送
- ⏰ 支持定时任务
- 📁 支持报告存档

---

**项目维护者**：[Your Name]  
**最后更新**：2026-01-27  
**许可证**：MIT License
