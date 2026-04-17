"""
GMGN 统计数据获取模块
调用 GMGN /v1/user/holdings 等接口获取真实数据
"""

import logging
from typing import Dict, Any, Optional
from src.api.gmgn_api import GMGNAPIClient

logger = logging.getLogger(__name__)


class StatsCollector:
    """统计数据收集器"""

    def __init__(self, api_client: GMGNAPIClient):
        self.api_client = api_client
        self.cache = {}

    async def get_user_holdings(self, wallet_address: str) -> Dict[str, Any]:
        """
        获取用户持仓数据
        调用 GMGN /v1/user/holdings 接口
        """
        try:
            data = await self.api_client._request(
                "GET", f"/user/holdings/{wallet_address}"
            )
            
            return {
                "total_pnl": data.get("total_pnl", 0),
                "total_pnl_percent": data.get("total_pnl_percent", 0),
                "win_rate": data.get("win_rate", 0),
                "total_trades": data.get("total_trades", 0),
                "winning_trades": data.get("winning_trades", 0),
                "losing_trades": data.get("losing_trades", 0),
                "total_invested": data.get("total_invested", 0),
                "current_value": data.get("current_value", 0),
                "holdings": data.get("holdings", []),
            }
        except Exception as e:
            logger.error(f"Failed to get user holdings: {e}")
            return {}

    async def get_portfolio_stats(
        self, wallet_addresses: list
    ) -> Dict[str, Any]:
        """
        获取投资组合统计数据
        """
        try:
            all_holdings = []
            total_invested = 0
            total_current = 0
            total_pnl = 0
            total_trades = 0
            winning_trades = 0

            for address in wallet_addresses:
                if not address:
                    continue

                holdings = await self.get_user_holdings(address)

                if holdings:
                    all_holdings.extend(holdings.get("holdings", []))
                    total_invested += holdings.get("total_invested", 0)
                    total_current += holdings.get("current_value", 0)
                    total_pnl += holdings.get("total_pnl", 0)
                    total_trades += holdings.get("total_trades", 0)
                    winning_trades += holdings.get("winning_trades", 0)

            win_rate = (
                (winning_trades / total_trades * 100)
                if total_trades > 0
                else 0
            )
            total_pnl_percent = (
                (total_pnl / total_invested * 100)
                if total_invested > 0
                else 0
            )

            return {
                "total_invested": total_invested,
                "total_current": total_current,
                "total_pnl": total_pnl,
                "total_pnl_percent": total_pnl_percent,
                "total_trades": total_trades,
                "winning_trades": winning_trades,
                "losing_trades": total_trades - winning_trades,
                "win_rate": win_rate,
                "holdings": all_holdings,
            }

        except Exception as e:
            logger.error(f"Failed to get portfolio stats: {e}")
            return {}

    async def get_token_stats(self, token_address: str) -> Dict[str, Any]:
        """获取代币统计数据"""
        try:
            data = await self.api_client._request(
                "GET", f"/tokens/{token_address}/stats"
            )

            return {
                "token_address": token_address,
                "holders_count": data.get("holders_count", 0),
                "total_volume": data.get("total_volume", 0),
                "price_change_24h": data.get("price_change_24h", 0),
                "market_cap": data.get("market_cap", 0),
                "liquidity": data.get("liquidity", 0),
            }
        except Exception as e:
            logger.error(f"Failed to get token stats: {e}")
            return {}

    async def get_market_summary(self) -> Dict[str, Any]:
        """获取市场摘要"""
        try:
            data = await self.api_client._request(
                "GET", "/market/summary"
            )

            return {
                "active_traders": data.get("active_traders", 0),
                "total_volume_24h": data.get("total_volume_24h", 0),
                "new_tokens_24h": data.get("new_tokens_24h", 0),
                "top_gainers": data.get("top_gainers", []),
                "top_losers": data.get("top_losers", []),
            }
        except Exception as e:
            logger.error(f"Failed to get market summary: {e}")
            return {}
