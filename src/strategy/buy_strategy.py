import logging
import asyncio
from typing import Tuple, Optional
from src.api.gmgn_api import GMGNAPIClient
from src.strategy.position import PositionManager
from src.notifications.telegram import TelegramNotifier
from config import Config

logger = logging.getLogger(__name__)


class BuyStrategy:
    """买入策略"""

    def __init__(
        self,
        api_client: GMGNAPIClient,
        position_manager: PositionManager,
        notifier: Optional[TelegramNotifier] = None,
    ):
        self.api_client = api_client
        self.position_manager = position_manager
        self.notifier = notifier

    async def execute_buy(
        self,
        token_address: str,
        token_symbol: str,
        buy_amount_usd: float,
    ) -> Optional[str]:
        """执行买入"""
        try:
            # 获取当前价格
            token_info = await self.api_client.get_token_info(token_address)
            current_price = float(token_info.get("price", 0))

            if current_price <= 0:
                logger.error(f"无法获取 {token_symbol} 的价格")
                return None

            # 验证买入金额
            if buy_amount_usd < Config.MIN_BUY_AMOUNT:
                logger.warning(f"买入金额过小: ${buy_amount_usd} < ${Config.MIN_BUY_AMOUNT}")
                return None

            if buy_amount_usd > Config.MAX_BUY_AMOUNT:
                logger.warning(f"买入金额过大: ${buy_amount_usd} > ${Config.MAX_BUY_AMOUNT}")
                buy_amount_usd = Config.MAX_BUY_AMOUNT

            # 开立持仓
            position = self.position_manager.open_position(
                token_address=token_address,
                token_symbol=token_symbol,
                entry_price=current_price,
                amount_usd=buy_amount_usd,
                take_profit_percent=Config.TAKE_PROFIT_PERCENT,
                stop_loss_percent=Config.STOP_LOSS_PERCENT,
            )

            # 发送通知
            await self._notify_buy(position)

            return token_address

        except Exception as e:
            logger.error(f"买入失败: {e}")
            return None

    async def _notify_buy(self, position):
        """通知买入"""
        if not self.notifier:
            return

        message = f"""
💰 买入执行

代币: {position.token_symbol}
地址: {position.token_address[:10]}...

入场价格: ${position.entry_price:.6f}
买入金额: ${position.entry_usd:.2f}
数量: {position.quantity:.6f}

目标: ${position.take_profit_price:.6f} ({Config.TAKE_PROFIT_PERCENT:.0f}%)
止损: ${position.stop_loss_price:.6f} ({Config.STOP_LOSS_PERCENT:.0f}%)
时间: {position.buy_time.strftime('%Y-%m-%d %H:%M:%S')}
        """

        await self.notifier.send_message(message)

    async def check_smart_money_buys(self) -> int:
        """检查聪明钱的买入"""
        try:
            # 搜索最近的聪明钱购买
            smart_money_wallets = await self.api_client.search_smart_money({
                "min_pnl_percent": 100,  # 至少赚100%
                "recent_days": 30,
            })

            count = 0
            for wallet in smart_money_wallets[:10]:  # 限制10个
                # 获取钱包的最新持仓
                portfolio = await self.api_client.get_wallet_portfolio(wallet["address"])

                for token in portfolio.get("tokens", [])[:3]:  # 取前3个代币
                    token_addr = token.get("address")
                    token_symbol = token.get("symbol")

                    # 检查是否已经持仓
                    if self.position_manager.get_position(token_addr):
                        continue

                    # 获取代币信息
                    token_info = await self.api_client.get_token_info(token_addr)
                    liquidity = token_info.get("liquidity", 0)

                    # 流动性检查
                    if liquidity >= Config.MIN_LIQUIDITY_USD:
                        # 自动跟随购买
                        buy_amount = min(
                            Config.MAX_BUY_AMOUNT,
                            liquidity * 0.05,  # 购买流动性的5%
                        )

                        await self.execute_buy(
                            token_address=token_addr,
                            token_symbol=token_symbol,
                            buy_amount_usd=buy_amount,
                        )
                        count += 1

            logger.info(f"根据聪明钱执行了 {count} 笔买入")
            return count

        except Exception as e:
            logger.error(f"检查聪明钱买入失败: {e}")
            return 0
