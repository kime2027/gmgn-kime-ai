#!/bin/bash

# GMGN Kime AI startup script

set -e  # 遇到错误立即退出

# 配置环境变量设置函数
setup_env() {
    echo ""
    echo "首次运行配置向导"
    echo "=================="
    echo "请按照提示输入您的配置信息"
    echo ""

    # GMGN API 配置
    read -p "请输入 GMGN API Key: " GMGN_API_KEY
    echo "GMGN_API_BASE_URL=https://openapi.gmgn.ai/v1" >> .env

    # 区块链配置
    echo "RPC_URL=https://rpc.solana.com" >> .env
    echo "CHAIN=solana" >> .env

    # 钱包配置
    read -p "请输入钱包私钥 (多个用逗号分隔): " WALLET_PRIVATE_KEYS
    read -p "请输入钱包地址 (多个用逗号分隔): " WALLET_ADDRESSES

    # Telegram 配置
    read -p "请输入 Telegram Bot Token: " TELEGRAM_BOT_TOKEN
    read -p "请输入 Telegram Chat ID: " TELEGRAM_CHAT_ID

    # 交易配置
    read -p "请输入最小买入金额 (默认10): " MIN_BUY_AMOUNT
    MIN_BUY_AMOUNT=${MIN_BUY_AMOUNT:-10}
    read -p "请输入最大买入金额 (默认100): " MAX_BUY_AMOUNT
    MAX_BUY_AMOUNT=${MAX_BUY_AMOUNT:-100}
    read -p "请输入止盈百分比 (默认500): " TAKE_PROFIT_PERCENT
    TAKE_PROFIT_PERCENT=${TAKE_PROFIT_PERCENT:-500}
    read -p "请输入止损百分比 (默认50): " STOP_LOSS_PERCENT
    STOP_LOSS_PERCENT=${STOP_LOSS_PERCENT:-50}
    read -p "请输入跟踪止损百分比 (默认10): " TRAILING_STOP_PERCENT
    TRAILING_STOP_PERCENT=${TRAILING_STOP_PERCENT:-10}

    # 安全配置
    echo "HONEYPOT_CHECK_ENABLED=true" >> .env
    echo "LP_LOCK_CHECK_ENABLED=true" >> .env
    echo "DEV_SELLOFF_CHECK_ENABLED=true" >> .env
    read -p "请输入最小流动性 USD (默认5000): " MIN_LIQUIDITY_USD
    MIN_LIQUIDITY_USD=${MIN_LIQUIDITY_USD:-5000}
    read -p "请输入最大持有人集中度 (默认30): " MAX_HOLDER_CONCENTRATION
    MAX_HOLDER_CONCENTRATION=${MAX_HOLDER_CONCENTRATION:-30}

    # Web 面板配置
    read -p "请输入 Web 端口 (默认8000): " WEB_PORT
    WEB_PORT=${WEB_PORT:-8000}
    echo "WEB_HOST=0.0.0.0" >> .env

    # Redis 配置 (可选)
    read -p "请输入 Redis URL (可选，直接回车跳过): " REDIS_URL
    if [ -n "$REDIS_URL" ]; then
        echo "REDIS_URL=$REDIS_URL" >> .env
    fi

    # 日志配置
    echo "LOG_LEVEL=INFO" >> .env
    echo "LOG_FILE=logs/kime.log" >> .env

    # 数据库配置
    echo "DATABASE_URL=sqlite:///./kime.db" >> .env

    # 写入配置到 .env 文件
    cat > .env << EOF
# GMGN API 配置
GMGN_API_KEY=$GMGN_API_KEY
GMGN_API_BASE_URL=https://openapi.gmgn.ai/v1

# 区块链配置
RPC_URL=https://rpc.solana.com
CHAIN=solana

# 钱包配置
WALLET_PRIVATE_KEYS=$WALLET_PRIVATE_KEYS
WALLET_ADDRESSES=$WALLET_ADDRESSES

# Telegram 配置
TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID=$TELEGRAM_CHAT_ID

# 交易配置
MIN_BUY_AMOUNT=$MIN_BUY_AMOUNT
MAX_BUY_AMOUNT=$MAX_BUY_AMOUNT
TAKE_PROFIT_PERCENT=$TAKE_PROFIT_PERCENT
STOP_LOSS_PERCENT=$STOP_LOSS_PERCENT
TRAILING_STOP_PERCENT=$TRAILING_STOP_PERCENT

# 安全配置
HONEYPOT_CHECK_ENABLED=true
LP_LOCK_CHECK_ENABLED=true
DEV_SELLOFF_CHECK_ENABLED=true
MIN_LIQUIDITY_USD=$MIN_LIQUIDITY_USD
MAX_HOLDER_CONCENTRATION=$MAX_HOLDER_CONCENTRATION

# Web 面板配置
WEB_PORT=$WEB_PORT
WEB_HOST=0.0.0.0

EOF

    if [ -n "$REDIS_URL" ]; then
        echo "# Redis 配置" >> .env
        echo "REDIS_URL=$REDIS_URL" >> .env
        echo "" >> .env
    fi

    cat >> .env << EOF
# 日志配置
LOG_LEVEL=INFO
LOG_FILE=logs/kime.log

# 数据库配置
DATABASE_URL=sqlite:///./kime.db
EOF

    echo ""
    echo "配置完成！已生成 .env 文件"
    echo ""
}

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
    echo "未找到 .env 文件，开始首次配置..."
    setup_env
fi

# 检查目录
mkdir -p logs
mkdir -p data

# 启动应用
echo ""
echo "正在启动 GMGN Kime AI..."
echo ""

python main.py
