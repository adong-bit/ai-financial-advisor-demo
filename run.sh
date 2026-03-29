#!/bin/bash

echo "======================================"
echo "  📈 AI智能投顾助手 Demo"
echo "======================================"
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装Python 3.8+"
    exit 1
fi

echo "✅ Python版本: $(python3 --version)"
echo ""

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "📥 安装依赖包..."
pip install -q -r requirements.txt

echo ""
echo "✅ 依赖安装完成！"
echo ""

# 检查.env文件
if [ ! -f ".env" ]; then
    echo "⚠️  未找到.env文件"
    echo "📝 复制示例配置..."
    cp .env.example .env
    echo "✅ 已创建.env文件"
    echo ""
    echo "📌 如需使用AI功能，请编辑.env文件填入API密钥"
    echo "   (不配置也可运行，将使用内置规则回复)"
    echo ""
fi

echo "🚀 启动应用（端口8502）..."
echo ""
streamlit run app.py --server.port 8502
