#!/bin/bash

# GMGN Kime AI startup script

set -e  # 遇到错误立即退出

echo "GMGN Kime AI 启动脚本"
echo "===================="

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 检查依赖
if [ ! -f "venv/pyvenv.cfg" ]; then
    echo "安装依赖..."
    pip install --upgrade pip
    pip install -r requirements.txt
fi

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo "未找到 .env 文件"
    echo "根据 .env.example 创建 .env 文件..."
    cp .env.example .env
    echo ""
    echo "请编辑 .env 文件并填入你的配置:"
    echo ""
    echo "必须配置:"
    echo "  - GMGN_API_KEY"
    echo "  - TELEGRAM_BOT_TOKEN"
    echo "  - TELEGRAM_CHAT_ID"
    echo "  - WALLET_PRIVATE_KEYS"
    echo "  - WALLET_ADDRESSES"
    echo ""
    exit 1
fi

# 检查目录
mkdir -p logs
mkdir -p data

# 启动应用
echo ""
echo "正在启动 GMGN Kime AI..."
echo ""

python main.py
