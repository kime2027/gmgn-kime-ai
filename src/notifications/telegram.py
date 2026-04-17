import logging
from typing import Optional
from telegram import Bot
from telegram.error import TelegramError

logger = logging.getLogger(__name__)


class TelegramNotifier:
    """Telegram 通知器"""

    def __init__(self, bot_token: str, chat_id: str):
        self.bot = Bot(token=bot_token)
        self.chat_id = chat_id
        self.is_connected = False

    async def connect(self) -> bool:
        """连接到 Telegram"""
        try:
            await self.bot.get_me()
            self.is_connected = True
            logger.info("Telegram 连接成功")
            return True
        except TelegramError as e:
            logger.error(f"Telegram 连接失败: {e}")
            self.is_connected = False
            return False

    async def send_message(self, message: str) -> bool:
        """发送消息"""
        if not self.is_connected:
            logger.warning("Telegram 未连接，跳过消息发送")
            return False

        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode="HTML"
            )
            return True
        except TelegramError as e:
            logger.error(f"发送消息失败: {e}")
            return False

    async def send_alert(self, title: str, message: str) -> bool:
        """发送警报"""
        alert_message = f"""
🚨 <b>{title}</b>

{message}
        """
        return await self.send_message(alert_message)

    async def send_trade_update(
        self,
        action: str,
        token_symbol: str,
        price: float,
        amount_usd: float,
    ) -> bool:
        """发送交易更新"""
        message = f"""
🔔 <b>交易更新: {action}</b>

代币: <code>{token_symbol}</code>
价格: ${price:.6f}
金额: ${amount_usd:.2f}
        """
        return await self.send_message(message)

    async def send_portfolio_summary(self, summary: str) -> bool:
        """发送投资组合摘要"""
        return await self.send_message(summary)

    async def disconnect(self):
        """断开连接"""
        try:
            await self.bot.session.close()
            self.is_connected = False
            logger.info("Telegram 连接已关闭")
        except Exception as e:
            logger.error(f"关闭 Telegram 连接失败: {e}")
