import os
from dotenv import load_dotenv
from typing import List

load_dotenv()


class Config:
    """全局配置管理"""

    # GMGN API 配置
    GMGN_API_KEY = os.getenv("GMGN_API_KEY", "")
    GMGN_API_BASE_URL = os.getenv("GMGN_API_BASE_URL", "https://openapi.gmgn.ai/v1")

    # 区块链配置
    RPC_URL = os.getenv("RPC_URL", "https://rpc.solana.com")
    CHAIN = os.getenv("CHAIN", "solana")

    # 钱包配置
    WALLET_PRIVATE_KEYS: List[str] = os.getenv("WALLET_PRIVATE_KEYS", "").split(",")
    WALLET_ADDRESSES: List[str] = os.getenv("WALLET_ADDRESSES", "").split(",")

    # Telegram 配置
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

    # 交易配置
    MIN_BUY_AMOUNT = float(os.getenv("MIN_BUY_AMOUNT", "10"))
    MAX_BUY_AMOUNT = float(os.getenv("MAX_BUY_AMOUNT", "100"))
    TAKE_PROFIT_PERCENT = float(os.getenv("TAKE_PROFIT_PERCENT", "500"))
    STOP_LOSS_PERCENT = float(os.getenv("STOP_LOSS_PERCENT", "50"))
    TRAILING_STOP_PERCENT = float(os.getenv("TRAILING_STOP_PERCENT", "10"))

    # 安全配置
    HONEYPOT_CHECK_ENABLED = os.getenv("HONEYPOT_CHECK_ENABLED", "true").lower() == "true"
    LP_LOCK_CHECK_ENABLED = os.getenv("LP_LOCK_CHECK_ENABLED", "true").lower() == "true"
    DEV_SELLOFF_CHECK_ENABLED = os.getenv("DEV_SELLOFF_CHECK_ENABLED", "true").lower() == "true"
    MIN_LIQUIDITY_USD = float(os.getenv("MIN_LIQUIDITY_USD", "5000"))
    MAX_HOLDER_CONCENTRATION = float(os.getenv("MAX_HOLDER_CONCENTRATION", "30"))

    # Web 面板配置
    WEB_PORT = int(os.getenv("WEB_PORT", "8000"))
    WEB_HOST = os.getenv("WEB_HOST", "0.0.0.0")

    # Redis 配置
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

    # 日志配置
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "logs/kime.log")

    # 数据库配置
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./kime.db")

    @classmethod
    def validate(cls):
        """验证必要的配置"""
        required = ["GMGN_API_KEY", "TELEGRAM_BOT_TOKEN"]
        missing = [key for key in required if not getattr(cls, key)]
        if missing:
            raise ValueError(f"缺少必要的配置: {', '.join(missing)}")


# 初始化日志目录
os.makedirs("logs", exist_ok=True)
os.makedirs("data", exist_ok=True)
