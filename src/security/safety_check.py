import logging
from typing import Tuple, Dict, Any
from src.api.gmgn_api import GMGNAPIClient
from config import Config

logger = logging.getLogger(__name__)


class SafetyChecker:
    """代币安全检查器"""

    def __init__(self, api_client: GMGNAPIClient):
        self.api_client = api_client

    async def check_token(
        self, token_address: str
    ) -> Tuple[float, Dict[str, str]]:
        """
        检查代币安全性
        返回: (安全评分 0-100, 检查详情)
        """
        try:
            token_info = await self.api_client.get_token_info(token_address)
            
            score = 100.0
            reasons = {}

            # Honeypot 检查
            if Config.HONEYPOT_CHECK_ENABLED:
                honeypot_score, honeypot_reason = await self._check_honeypot(
                    token_address
                )
                score *= honeypot_score / 100
                if honeypot_reason:
                    reasons["Honeypot"] = honeypot_reason

            # LP 锁定检查
            if Config.LP_LOCK_CHECK_ENABLED:
                lp_score, lp_reason = await self._check_lp_lock(token_address)
                score *= lp_score / 100
                if lp_reason:
                    reasons["LP 锁定"] = lp_reason

            # 开发者抛售风险检查
            if Config.DEV_SELLOFF_CHECK_ENABLED:
                dev_score, dev_reason = await self._check_dev_selloff(
                    token_address
                )
                score *= dev_score / 100
                if dev_reason:
                    reasons["Dev 风险"] = dev_reason

            # 持有者集中度检查
            concentration_score, concentration_reason = (
                await self._check_holder_concentration(token_address)
            )
            score *= concentration_score / 100
            if concentration_reason:
                reasons["持有者集中度"] = concentration_reason

            return max(0, score), reasons

        except Exception as e:
            logger.error(f"安全检查失败: {e}")
            return 0.0, {"错误": str(e)}

    async def _check_honeypot(self, token_address: str) -> Tuple[float, str]:
        """检查honeypot风险"""
        try:
            # 这里应该调用链上数据分析
            # 简化版本: 检查转账问题
            token_info = await self.api_client.get_token_info(token_address)

            # 检查代币是否可转账
            if token_info.get("is_honeypot"):
                return 0.0, "检测到 honeypot 特征"

            if not token_info.get("can_transfer", True):
                return 30.0, "代币转账受限"

            if token_info.get("blacklist_enabled", False):
                return 50.0, "启用了黑名单机制"

            return 100.0, ""

        except Exception as e:
            logger.warning(f"Honeypot 检查失败: {e}")
            return 50.0, "检查失败"

    async def _check_lp_lock(self, token_address: str) -> Tuple[float, str]:
        """检查 LP 是否锁定"""
        try:
            lp_info = await self.api_client.get_liquidity_info(token_address)

            # 检查 LP 锁定
            if not lp_info.get("is_locked", False):
                return 30.0, "LP 未锁定，存在拉盘风险"

            lock_days = lp_info.get("lock_days", 0)
            if lock_days < 30:
                return 50.0, f"LP 锁定时间过短: {lock_days} 天"

            if lock_days >= 365:
                return 100.0, ""

            # 根据锁定时间给分
            score = 50 + (lock_days / 365) * 50
            return min(100.0, score), ""

        except Exception as e:
            logger.warning(f"LP 检查失败: {e}")
            return 50.0, "检查失败"

    async def _check_dev_selloff(self, token_address: str) -> Tuple[float, str]:
        """检查开发者抛售风险"""
        try:
            holders = await self.api_client.get_token_holders(token_address)

            # 查找开发者钱包
            for holder in holders[:5]:  # 检查前5大持有者
                if holder.get("is_contract", False) and holder.get(
                    "is_dev", False
                ):
                    dev_balance = float(holder.get("balance", 0))
                    total_supply = float(
                        await self.api_client.get_token_info(token_address)
                    ).get("total_supply", 1)
                    dev_percent = (dev_balance / total_supply) * 100

                    if dev_percent > 50:
                        return (
                            20.0,
                            f"开发者持有 {dev_percent:.1f}%，存在抛售风险",
                        )
                    elif dev_percent > 30:
                        return (
                            60.0,
                            f"开发者持有 {dev_percent:.1f}%，中等风险",
                        )

            return 100.0, ""

        except Exception as e:
            logger.warning(f"Dev 检查失败: {e}")
            return 50.0, "检查失败"

    async def _check_holder_concentration(
        self, token_address: str
    ) -> Tuple[float, str]:
        """检查持有者集中度"""
        try:
            holders = await self.api_client.get_token_holders(token_address)

            if not holders:
                return 50.0, "无持有者数据"

            # 获取代币信息获取总供应量
            token_info = await self.api_client.get_token_info(token_address)
            total_supply = float(token_info.get("total_supply", 1))

            # 计算前10持有者的集中度
            top_10_percent = 0
            for holder in holders[:10]:
                balance = float(holder.get("balance", 0))
                percentage = (balance / total_supply) * 100
                top_10_percent += percentage

            if top_10_percent > Config.MAX_HOLDER_CONCENTRATION:
                return (
                    40.0,
                    f"持有者集中度过高: 前10持有者占 {top_10_percent:.1f}%",
                )
            elif top_10_percent > 50:
                return 70.0, f"持有者集中度较高: 前10持有者占 {top_10_percent:.1f}%"

            return 100.0, ""

        except Exception as e:
            logger.warning(f"持有者集中度检查失败: {e}")
            return 50.0, "检查失败"
