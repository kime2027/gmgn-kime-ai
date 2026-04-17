@echo off
REM GMGN Kime AI startup script for Windows

setlocal enabledelayedexpansion

echo GMGN Kime AI 启动脚本
echo ====================

REM 检查虚拟环境
if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境
echo 激活虚拟环境...
call venv\Scripts\activate.bat

REM 检查依赖
if not exist "venv\Lib\site-packages" (
    echo 安装依赖...
    python -m pip install --upgrade pip
    pip install -r requirements.txt
)

REM 检查 .env 文件
if not exist ".env" (
    echo 未找到 .env 文件
    echo 根据 .env.example 创建 .env 文件...
    copy .env.example .env
    echo.
    echo 请编辑 .env 文件并填入你的配置:
    echo.
    echo 必须配置:
    echo   - GMGN_API_KEY
    echo   - TELEGRAM_BOT_TOKEN
    echo   - TELEGRAM_CHAT_ID
    echo   - WALLET_PRIVATE_KEYS
    echo   - WALLET_ADDRESSES
    echo.
    exit /b 1
)

REM 检查日志目录
if not exist "logs" mkdir logs
if not exist "data" mkdir data

REM 启动应用
echo.
echo 正在启动 GMGN Kime AI...
echo.

python main.py

pause
