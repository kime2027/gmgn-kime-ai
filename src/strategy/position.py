import logging
from typing import Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class OrderType(Enum):
    """订单类型"""
    BUY = "buy"
    SELL = "sell"
    TAKE_PROFIT = "take_profit"
    STOP_LOSS = "stop_loss"


@dataclass
class Position:
    """持仓信息"""
    token_address: str
    token_symbol: str
    entry_price: float
    entry_amount: float  # 代币数量
    entry_usd: float  # 美元金额
    buy_time: datetime
    current_price: Optional[float] = None
    current_usd: Optional[float] = None
    quantity: float = 0.0  # 持有数量
    take_profit_price: Optional[float] = None
    stop_loss_price: Optional[float] = None
    trailing_stop_price: Optional[float] = None
    max_price: Optional[float] = None  # 最高价格（用于tracking）
    status: str = "OPEN"  # OPEN, CLOSED, PARTIAL

    def get_pnl_percent(self) -> float:
        """获取盈亏百分比"""
        if not self.current_price:
            return 0.0
        return ((self.current_price - self.entry_price) / self.entry_price) * 100

    def get_pnl_usd(self) -> float:
        """获取盈亏美元值"""
        if not self.current_usd:
            return 0.0
        return self.current_usd - self.entry_usd

    def should_take_profit(self, take_profit_percent: float) -> bool:
        """检查是否应该止盈"""
        if not self.current_price:
            return False
        target_price = self.entry_price * (1 + take_profit_percent / 100)
        return self.current_price >= target_price

    def should_stop_loss(self, stop_loss_percent: float) -> bool:
        """检查是否应该止损"""
        if not self.current_price:
            return False
        target_price = self.entry_price * (1 - stop_loss_percent / 100)
        return self.current_price <= target_price

    def should_trailing_stop(self, trailing_stop_percent: float) -> bool:
        """检查是否应该跟踪止损"""
        if not self.current_price or not self.max_price:
            return False

        # 更新最高价格
        if self.current_price > self.max_price:
            self.max_price = self.current_price
            return False

        # 计算跟踪止损价格
        trigger_price = self.max_price * (1 - trailing_stop_percent / 100)
        return self.current_price <= trigger_price


class PositionManager:
    """持仓管理器"""

    def __init__(self):
        self.positions: Dict[str, Position] = {}  # key: token_address
        self.closed_positions = []

    def open_position(
        self,
        token_address: str,
        token_symbol: str,
        entry_price: float,
        amount_usd: float,
        take_profit_percent: float = None,
        stop_loss_percent: float = None,
    ) -> Position:
        """开立新持仓"""
        quantity = amount_usd / entry_price

        position = Position(
            token_address=token_address,
            token_symbol=token_symbol,
            entry_price=entry_price,
            entry_amount=quantity,
            entry_usd=amount_usd,
            buy_time=datetime.now(),
            quantity=quantity,
        )

        # 设置止盈止损
        if take_profit_percent:
            position.take_profit_price = entry_price * (1 + take_profit_percent / 100)

        if stop_loss_percent:
            position.stop_loss_price = entry_price * (1 - stop_loss_percent / 100)

        # 初始化最高价格用于trailing stop
        position.max_price = entry_price

        self.positions[token_address] = position
        logger.info(
            f"开立持仓: {token_symbol}, 数量: {quantity:.6f}, 成本: ${amount_usd:.2f}"
        )

        return position

    def close_position(
        self, token_address: str, exit_price: float, reason: str = ""
    ) -> Optional[Dict[str, Any]]:
        """平仓"""
        if token_address not in self.positions:
            return None

        position = self.positions[token_address]
        exit_usd = exit_price * position.quantity
        pnl_usd = exit_usd - position.entry_usd
        pnl_percent = (pnl_usd / position.entry_usd) * 100

        logger.info(
            f"平仓: {position.token_symbol}, "
            f"退出价: ${exit_price:.6f}, "
            f"盈亏: ${pnl_usd:.2f} ({pnl_percent:.2f}%), "
            f"原因: {reason}"
        )

        position.status = "CLOSED"
        self.closed_positions.append(position)
        del self.positions[token_address]

        return {
            "token": position.token_symbol,
            "entry_price": position.entry_price,
            "exit_price": exit_price,
            "quantity": position.quantity,
            "entry_usd": position.entry_usd,
            "exit_usd": exit_usd,
            "pnl_usd": pnl_usd,
            "pnl_percent": pnl_percent,
            "reason": reason,
        }

    def update_position_price(self, token_address: str, current_price: float):
        """更新持仓价格"""
        if token_address in self.positions:
            position = self.positions[token_address]
            position.current_price = current_price
            position.current_usd = current_price * position.quantity

            # 更新最高价格（用于trailing stop）
            if not position.max_price or current_price > position.max_price:
                position.max_price = current_price

    def get_position(self, token_address: str) -> Optional[Position]:
        """获取持仓"""
        return self.positions.get(token_address)

    def get_all_positions(self) -> Dict[str, Position]:
        """获取所有持仓"""
        return self.positions.copy()

    def get_portfolio_summary(self) -> Dict[str, Any]:
        """获取投资组合摘要"""
        total_entry = sum(p.entry_usd for p in self.positions.values())
        total_current = sum(p.current_usd or 0 for p in self.positions.values())
        total_pnl = total_current - total_entry
        total_pnl_percent = (
            (total_pnl / total_entry * 100) if total_entry > 0 else 0
        )

        return {
            "open_positions": len(self.positions),
            "total_entry_usd": total_entry,
            "total_current_usd": total_current,
            "total_pnl_usd": total_pnl,
            "total_pnl_percent": total_pnl_percent,
            "closed_positions": len(self.closed_positions),
        }
