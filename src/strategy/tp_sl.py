import logging
import asyncio
from typing import Dict, List
from src.api.gmgn_api import GMGNAPIClient
from src.strategy.position import PositionManager
from src.notifications.telegram import TelegramNotifier
from config import Config

logger = logging.getLogger(__name__)


class ProfitLossManager:
    """止盈止损管理器"""

    def __init__(
        self,
        api_client: GMGNAPIClient,
        position_manager: PositionManager,
        notifier: TelegramNotifier,
    ):
        self.api_client = api_client
        self.position_manager = position_manager
        self.notifier = notifier
        self.is_running = False

    async def start_monitoring(self, interval: int = 60):
        """启动止盈止损监控"""
        self.is_running = True
        logger.info("启动止盈止损监控...")

        while self.is_running:
            try:
                await self.check_and_close_positions()
            except Exception as e:
                logger.error(f"监控出错: {e}")

            await asyncio.sleep(interval)

    async def check_and_close_positions(self) -> Dict[str, List[str]]:
        """检查所有持仓并执行平仓"""
        closed = {"take_profit": [], "stop_loss": [], "trailing_stop": []}

        positions = self.position_manager.get_all_positions()

        for token_address, position in positions.items():
            try:
                # 获取最新价格
                token_info = await self.api_client.get_token_info(token_address)
                current_price = float(token_info.get("price", 0))

                if current_price <= 0:
                    continue

                # 更新持仓价格
                self.position_manager.update_position_price(token_address, current_price)

                # 检查止盈
                if position.should_take_profit(Config.TAKE_PROFIT_PERCENT):
                    result = self.position_manager.close_position(
                        token_address, current_price, "止盈"
                    )
                    if result:
                        await self._notify_close(result)
                        closed["take_profit"].append(position.token_symbol)
                        continue

                # 检查止损
                if position.should_stop_loss(Config.STOP_LOSS_PERCENT):
                    result = self.position_manager.close_position(
                        token_address, current_price, "止损"
                    )
                    if result:
                        await self._notify_close(result)
                        closed["stop_loss"].append(position.token_symbol)
                        continue

                # 检查跟踪止损
                if position.should_trailing_stop(Config.TRAILING_STOP_PERCENT):
                    result = self.position_manager.close_position(
                        token_address, current_price, f"跟踪止损 ({Config.TRAILING_STOP_PERCENT:.1f}%)"
                    )
                    if result:
                        await self._notify_close(result)
                        closed["trailing_stop"].append(position.token_symbol)

            except Exception as e:
                logger.error(f"处理持仓 {position.token_symbol} 时出错: {e}")

        return closed

    async def _notify_close(self, result: Dict):
        """通知平仓"""
        status_emoji = "✅" if result["pnl_usd"] >= 0 else "❌"

        message = f"""
{status_emoji} 交易已平仓

代币: {result['token']}
原因: {result['reason']}

入场: ${result['entry_price']:.6f}
退出: ${result['exit_price']:.6f}
数量: {result['quantity']:.6f}

成本: ${result['entry_usd']:.2f}
收益: ${result['exit_usd']:.2f}
盈亏: ${result['pnl_usd']:.2f} ({result['pnl_percent']:.2f}%)
        """

        await self.notifier.send_message(message)

    def stop_monitoring(self):
        """停止监控"""
        self.is_running = False
        logger.info("止盈止损监控已停止")

    async def get_active_monitoring_summary(self) -> str:
        """获取监控摘要"""
        portfolio = self.position_manager.get_portfolio_summary()

        summary = f"""
📊 投资组合监控

持仓数: {portfolio['open_positions']}
已平仓: {portfolio['closed_positions']}

总成本: ${portfolio['total_entry_usd']:.2f}
当前价值: ${portfolio['total_current_usd']:.2f}
总盈亏: ${portfolio['total_pnl_usd']:.2f} ({portfolio['total_pnl_percent']:.2f}%)
        """

        return summary
