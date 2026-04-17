import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from src.strategy.position import Position, PositionManager, OrderType
from datetime import datetime


@pytest.fixture
def position_manager():
    """创建 PositionManager 实例"""
    return PositionManager()


class TestPosition:
    """Position 类单元测试"""

    def test_position_creation(self):
        """测试持仓创建"""
        pos = Position(
            token_address="0x123",
            token_symbol="TEST",
            entry_price=1.0,
            entry_amount=100,
            entry_usd=100,
            buy_time=datetime.now(),
        )

        assert pos.token_address == "0x123"
        assert pos.token_symbol == "TEST"
        assert pos.entry_price == 1.0
        assert pos.get_pnl_percent() == 0.0

    def test_position_pnl_calculation(self):
        """测试盈亏计算"""
        pos = Position(
            token_address="0x123",
            token_symbol="TEST",
            entry_price=1.0,
            entry_amount=100,
            entry_usd=100,
            buy_time=datetime.now(),
            current_price=2.0,
            current_usd=200,
        )

        assert pos.get_pnl_percent() == 100.0
        assert pos.get_pnl_usd() == 100.0

    def test_take_profit_trigger(self):
        """测试止盈判断"""
        pos = Position(
            token_address="0x123",
            token_symbol="TEST",
            entry_price=1.0,
            entry_amount=100,
            entry_usd=100,
            buy_time=datetime.now(),
            current_price=3.0,
        )

        assert pos.should_take_profit(200) is True
        assert pos.should_take_profit(400) is False

    def test_stop_loss_trigger(self):
        """测试止损判断"""
        pos = Position(
            token_address="0x123",
            token_symbol="TEST",
            entry_price=1.0,
            entry_amount=100,
            entry_usd=100,
            buy_time=datetime.now(),
            current_price=0.4,
        )

        assert pos.should_stop_loss(50) is True
        assert pos.should_stop_loss(70) is False


class TestPositionManager:
    """PositionManager 类单元测试"""

    def test_open_position(self, position_manager):
        """测试开立持仓"""
        pos = position_manager.open_position(
            token_address="0x123",
            token_symbol="TEST",
            entry_price=1.0,
            amount_usd=100,
            take_profit_percent=200,
            stop_loss_percent=50,
        )

        assert pos.token_symbol == "TEST"
        assert pos.entry_usd == 100
        assert len(position_manager.positions) == 1

    def test_close_position(self, position_manager):
        """测试平仓"""
        position_manager.open_position(
            token_address="0x123",
            token_symbol="TEST",
            entry_price=1.0,
            amount_usd=100,
        )

        result = position_manager.close_position("0x123", 2.0)

        assert result is not None
        assert result["pnl_percent"] == 100.0
        assert len(position_manager.positions) == 0

    def test_get_portfolio_summary(self, position_manager):
        """测试投资组合摘要"""
        # 开立两个持仓
        position_manager.open_position(
            token_address="0x123",
            token_symbol="TEST1",
            entry_price=1.0,
            amount_usd=100,
        )

        position_manager.open_position(
            token_address="0x456",
            token_symbol="TEST2",
            entry_price=2.0,
            amount_usd=200,
        )

        # 更新价格
        position_manager.update_position_price("0x123", 1.5)
        position_manager.update_position_price("0x456", 2.5)

        summary = position_manager.get_portfolio_summary()

        assert summary["open_positions"] == 2
        assert summary["total_entry_usd"] == 300
        assert summary["total_pnl_usd"] == 100  # (100 + 50)
