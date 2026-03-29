# 部署指南

本文档介绍如何将AI智能投顾助手部署到不同平台。

## 目录

- [Streamlit Cloud](#streamlit-cloud-推荐)
- [Hugging Face Spaces](#hugging-face-spaces)
- [Docker部署](#docker部署)
- [本地服务器](#本地服务器)

## Streamlit Cloud（推荐）

### 优点
- 完全免费（公开仓库）
- 一键部署
- 自动更新
- 原生支持Streamlit

### 步骤

1. **准备GitHub仓库**
   - 确保代码已推送到GitHub
   - 仓库设置为Public

2. **部署**
   - 访问 [share.streamlit.io](https://share.streamlit.io/)
   - 点击 "New app"
   - 选择仓库：`adong-bit/ai-financial-advisor-demo`
   - 主文件：`app.py`
   - 点击 "Deploy"

3. **配置环境变量**（可选）
   - 在应用设置中添加Secrets
   - 添加`OPENAI_API_KEY`等环境变量

4. **访问应用**
   - 部署完成后，会获得一个URL
   - 格式：`https://your-app-name.streamlit.app`

## Hugging Face Spaces

### 优点
- 完全免费
- 支持私有仓库
- 更好的CPU配置

### 步骤

1. **创建Space**
   - 访问 [huggingface.co/spaces](https://huggingface.co/spaces)
   - 点击 "Create new Space"
   - SDK：Streamlit
   - License：MIT

2. **配置文件**

创建 `README.md`（在Space根目录）：
```yaml
---
title: AI智能投顾助手
emoji: 📈
colorFrom: blue
colorTo: red
sdk: streamlit
sdk_version: 1.28.1
app_file: app.py
pinned: false
license: mit
---
```

3. **上传代码**
   - 通过Git上传
   - 或直接在网页上编辑

4. **配置Secrets**（可选）
   - 在Settings → Repository secrets中添加
   - `OPENAI_API_KEY`等

## Docker部署

### 构建镜像

```bash
# 构建Docker镜像
docker build -t ai-financial-advisor .

# 运行容器
docker run -p 8501:8501 ai-financial-advisor
```

### Dockerfile示例

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    restart: unless-stopped
```

## 本地服务器

### 使用systemd（Linux）

创建服务文件 `/etc/systemd/system/ai-advisor.service`：

```ini
[Unit]
Description=AI Financial Advisor Streamlit App
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/ai-financial-advisor-demo
ExecStart=/usr/bin/python3 -m streamlit run app.py --server.port=8502
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：
```bash
sudo systemctl daemon-reload
sudo systemctl enable ai-advisor
sudo systemctl start ai-advisor
```

### 使用screen/tmux

```bash
# 创建会话
screen -S ai-advisor

# 启动应用
cd /path/to/ai-financial-advisor-demo
./run.sh

# 分离会话：Ctrl+A, D
# 重新连接：screen -r ai-advisor
```

## Nginx反向代理

如果使用域名，配置Nginx：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8502;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 环境变量配置

创建 `.env` 文件：

```bash
# AI模型配置
OPENAI_API_KEY=your_api_key_here
OPENAI_API_BASE=https://api.openai.com/v1

# 或使用其他API
ANTHROPIC_API_KEY=your_claude_key
MINIMAX_API_KEY=your_minimax_key
MINIMAX_GROUP_ID=your_group_id
```

## 性能优化

1. **启用缓存**
   ```python
   # 在app.py中添加
   @st.cache_data(ttl=3600)
   def get_fund_data(code):
       return fund_query.get_fund_info(code)
   ```

2. **使用Watchdog**
   ```bash
   pip install watchdog
   ```

3. **配置Session State**
   - 避免重复计算
   - 缓存用户数据

## 监控和日志

### Streamlit日志

```bash
# 查看日志
tail -f ~/.streamlit/logs/your_app.log
```

### 自定义日志

```python
import logging

logging.basicConfig(filename='app.log', level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Application started")
```

## 安全建议

1. **不要提交敏感信息**
   - 使用`.env.example`
   - 添加`.env`到`.gitignore`

2. **API密钥管理**
   - 使用平台Secrets功能
   - 定期轮换密钥

3. **访问控制**
   - 添加用户认证
   - 限制访问频率

4. **HTTPS**
   - 使用Let's Encrypt证书
   - 强制HTTPS重定向

## 常见问题

### Q: 内存不足怎么办？
A: 优化数据加载，使用分页或懒加载。

### Q: 如何处理并发？
A: Streamlit Cloud有自动扩容。自建建议使用负载均衡。

### Q: 应用崩溃了怎么排查？
A: 查看日志，检查内存使用，验证数据源可用性。

## 获取帮助

- GitHub Issues: https://github.com/adong-bit/ai-financial-advisor-demo/issues
- Streamlit文档: https://docs.streamlit.io/
