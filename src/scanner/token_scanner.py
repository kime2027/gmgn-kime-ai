import asyncio
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from src.api.gmgn_api import GMGNAPIClient
from src.security.safety_check import SafetyChecker
from src.notifications.telegram import TelegramNotifier
from config import Config

logger = logging.getLogger(__name__)


@dataclass
class NewToken:
    """新币信息"""
    address: str
    name: str
    symbol: str
    created_at: datetime
    liquidity_usd: float
    holders_count: int
    market_cap: float
    safety_score: float = 0.0
    is_safe: bool = False


class TokenScanner:
    """新币扫描器"""

    def __init__(
        self,
        api_client: GMGNAPIClient,
        safety_checker: SafetyChecker,
        notifier: Optional[TelegramNotifier] = None,
    ):
        self.api_client = api_client
        self.safety_checker = safety_checker
        self.notifier = notifier
        self.scanned_tokens: set = set()
        self.is_running = False

    async def start_scanning(self, interval: int = 30):
        """启动扫描循环"""
        self.is_running = True
        logger.info("开始扫描新币...")

        while self.is_running:
            try:
                new_tokens = await self.scan_new_tokens()
                logger.info(f"本次扫描发现 {len(new_tokens)} 个新币")

                for token in new_tokens:
                    await self._process_token(token)

            except Exception as e:
                logger.error(f"扫描出错: {e}")

            await asyncio.sleep(interval)

    async def scan_new_tokens(self, limit: int = 100) -> List[NewToken]:
        """扫描新币"""
        try:
            tokens_data = await self.api_client.get_new_tokens(limit=limit)
            new_tokens = []

            for token_data in tokens_data:
                token_address = token_data.get("address")

                # 跳过已扫描的
                if token_address in self.scanned_tokens:
                    continue

                try:
                    token = NewToken(
                        address=token_address,
                        name=token_data.get("name", "Unknown"),
                        symbol=token_data.get("symbol", ""),
                        created_at=datetime.fromisoformat(
                            token_data.get("created_at", "")
                        ),
                        liquidity_usd=float(token_data.get("liquidity", 0)),
                        holders_count=int(token_data.get("holders", 0)),
                        market_cap=float(token_data.get("market_cap", 0)),
                    )
                    new_tokens.append(token)
                    self.scanned_tokens.add(token_address)
                except Exception as e:
                    logger.warning(f"解析代币数据失败: {e}")

            return new_tokens
        except Exception as e:
            logger.error(f"获取新币失败: {e}")
            return []

    async def _process_token(self, token: NewToken):
        """处理单个代币"""
        try:
            # 初步过滤
            if not self._initial_filter(token):
                logger.debug(f"代币 {token.symbol} 未通过初步过滤")
                return

            # 进行详细安全检查
            safety_score, reasons = await self.safety_checker.check_token(
                token.address
            )
            token.safety_score = safety_score
            token.is_safe = safety_score >= 60

            logger.info(
                f"代币 {token.symbol} 安全评分: {safety_score:.0f}, "
                f"是否安全: {token.is_safe}"
            )

            # 如果通过检查，发送通知
            if token.is_safe:
                await self._notify_token_found(token, reasons)

        except Exception as e:
            logger.error(f"处理代币 {token.address} 时出错: {e}")

    def _initial_filter(self, token: NewToken) -> bool:
        """初步过滤代币"""
        # 最小流动性检查
        if token.liquidity_usd < Config.MIN_LIQUIDITY_USD:
            return False

        # 最小持有者数检查
        if token.holders_count < 10:
            return False

        return True

    async def _notify_token_found(self, token: NewToken, reasons: Dict[str, str]):
        """通知发现新的安全代币"""
        if not self.notifier:
            return

        message = f"""
🎯 发现安全新币!

名称: {token.name}
代码: {token.symbol}
地址: {token.address[:10]}...

💰 流动性: ${token.liquidity_usd:,.0f}
👥 持有者: {token.holders_count}
📊 市值: ${token.market_cap:,.0f}
✅ 安全评分: {token.safety_score:.0f}/100

检查详情:
{self._format_reasons(reasons)}
        """

        await self.notifier.send_message(message)

    @staticmethod
    def _format_reasons(reasons: Dict[str, str]) -> str:
        """格式化检查原因"""
        lines = []
        for key, value in reasons.items():
            lines.append(f"• {key}: {value}")
        return "\n".join(lines)

    def stop_scanning(self):
        """停止扫描"""
        self.is_running = False
        logger.info("扫描已停止")
