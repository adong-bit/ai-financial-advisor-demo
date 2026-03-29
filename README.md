# 📈 AI智能投顾助手

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![GitHub stars](https://img.shields.io/github/stars/adong-bit/ai-financial-advisor-demo?style=social)](https://github.com/adong-bit/ai-financial-advisor-demo)

一款基于**核心-卫星策略**和**买方投顾理念**的AI智能投顾助手原型系统，专为证券公司AI产品经理岗位设计。

## 📸 项目截图

> 注意：添加项目截图可以让仓库更专业。建议截图：
> - 首页概览
> - 风险评估问卷
> - 资产配置方案（饼图）
> - AI对话界面

[添加您的项目截图 - 点击编辑上传图片]

<!--
上传截图到GitHub仓库后，使用以下格式：
![首页](screenshots/homepage.png)
![风险评估](screenshots/risk-assessment.png)
![资产配置](screenshots/portfolio.png)
-->

## 🌐 在线演示

[![Try on Streamlit Cloud](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)

<!--
部署到Streamlit Cloud后，替换上面的链接为您的实际地址
格式：[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)
-->

## 🎯 产品亮点

### 核心理念
- **买方投顾导向**：以客户利益为中心，而非销售导向
- **核心-卫星策略**：75%核心配置获取市场平均收益，25%卫星配置追求超额收益
- **科学资产配置**：基于现代投资组合理论(MPT)
- **长期陪伴服务**：不止于推荐，更注重持续优化

### 功能模块
1. **风险评估**：多维度评估用户风险承受能力
2. **资产配置**：根据风险类型生成个性化配置方案
3. **基金筛选**：基于akshare获取真实基金数据
4. **AI顾问**：智能对话解答投资疑问
5. **投资知识**：系统化的投资知识库

## 🚀 快速开始

### 1. 环境准备

确保您已安装 Python 3.8+

```bash
# 克隆或下载项目
cd /Users/ohmygodcurry/Desktop/炒股1号

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置AI模型（可选）

如果需要使用AI功能，创建 `.env` 文件：

```bash
cp .env.example .env
```

然后编辑 `.env` 文件，填入您的API密钥（支持OpenAI/Claude/minimax）：

```bash
# 选择以下任一API配置

# OpenAI API (推荐，国内可用各种中转API)
OPENAI_API_KEY=your_api_key
OPENAI_API_BASE=https://api.openai.com/v1

# 或使用Claude API
ANTHROPIC_API_KEY=your_api_key
```

**注意**：如果不配置API，系统会使用内置的规则回复，基本功能可正常运行。

### 3. 启动应用

```bash
# 方式1：使用启动脚本（推荐）
./run.sh

# 方式2：直接运行
streamlit run app.py --server.port 8502
```

浏览器将自动打开 `http://localhost:8502`

**注意**：如果您的8501端口已被占用，请使用8502端口启动。

## 📁 项目结构

```
.
├── app.py                  # Streamlit主应用
├── fund_data.py            # 基金数据查询模块
├── portfolio_advisor.py    # 资产配置建议引擎
├── ai_assistant.py         # AI对话模块
├── requirements.txt        # 依赖包列表
├── .env.example           # 环境变量示例
└── README.md              # 项目说明
```

## 💡 使用流程

1. **风险评估** → 回答5个问题，了解您的风险类型
2. **资产配置** → 获得基于您风险类型的配置方案
3. **基金筛选** → 查看推荐基金或搜索特定基金
4. **AI顾问** → 咨询任何投资相关问题
5. **投资知识** → 学习投资基础知识

## 🎨 面试展示建议

### 1. 买方投顾理解
- 强调"以客户利益为中心"vs"销售导向"
- 展示对投资者适当性的理解
- 说明长期陪伴的价值

### 2. 理论支撑
- 核心-卫星策略（成熟且易理解）
- 现代投资组合理论（MPT）
- 行为金融学（情绪化管理）

### 3. AI能力
- **不是替代人，而是增强投顾效率**
- 可解释性强（展示配置理由）
- 个性化推荐（基于用户画像）

### 4. 风险意识
- 强调不承诺收益
- 展示风险评估机制
- 说明投资者教育的重要性

## 🔧 技术栈

**前端框架**
- Streamlit 1.28+ - 快速构建数据应用

**数据源**
- akshare - 免费基金数据接口

**AI能力**
- 支持多种API：OpenAI / Claude / minimax
- 内置规则引擎（无需API也能运行）

**数据处理**
- pandas - 数据分析
- plotly - 交互式图表

## 📊 后续优化方向

- [ ] **数据增强**
  - [ ] 接入更多数据源（Wind、同花顺）
  - [ ] 增加实时行情
  - [ ] 添加更多基金指标

- [ ] **功能完善**
  - [ ] 投资组合跟踪
  - [ ] 再平衡提醒
  - [ ] 业绩归因分析

- [ ] **AI优化**
  - [ ] 增加RAG（检索增强生成）
  - [ ] 构建投资知识图谱
  - [ ] 个性化推荐算法

- [ ] **用户体验**
  - [ ] 美化UI界面
  - [ ] 增加移动端适配
  - [ ] 优化交互流程

## 🚀 部署到云端

### Streamlit Cloud（推荐）

1. 将代码推送到GitHub（已完成）
2. 访问 [share.streamlit.io](https://share.streamlit.io/)
3. 点击 "New app"
4. 选择您的GitHub仓库
5. 主文件：`app.py`
6. 点击 "Deploy"

### 其他平台

- **Hugging Face Spaces**：免费托管，支持Streamlit
- **Railway**：支持更多自定义配置
- **Render**：免费套餐，支持后台任务

## 📝 许可证

MIT License

## 👨‍💻 作者

Created for AI Product Manager Interview

---

**祝您面试成功！** 🎉
