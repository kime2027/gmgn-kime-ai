import pytest
from src.wallet.manager import WalletManager, Wallet


@pytest.fixture
def wallet_manager():
    """创建 WalletManager 实例"""
    addresses = ["wallet1", "wallet2", "wallet3"]
    keys = ["key1", "key2", "key3"]
    return WalletManager(addresses, keys)


class TestWallet:
    """Wallet 类单元测试"""

    def test_wallet_creation(self):
        """测试钱包创建"""
        wallet = Wallet(address="0x123", private_key="abc")

        assert wallet.address == "0x123"
        assert wallet.private_key == "abc"
        assert wallet.balance_sol == 0.0
        assert wallet.is_active is True


class TestWalletManager:
    """WalletManager 类单元测试"""

    def test_initialization(self, wallet_manager):
        """测试初始化"""
        assert len(wallet_manager.wallets) == 3
        assert all(w.is_active for w in wallet_manager.wallets.values())

    def test_get_wallet(self, wallet_manager):
        """测试获取钱包"""
        wallet = wallet_manager.get_wallet("wallet1")
        assert wallet is not None
        assert wallet.address == "wallet1"

    def test_rotate_wallet(self, wallet_manager):
        """测试钱包轮换"""
        wallet1 = wallet_manager.get_wallet()
        wallet2 = wallet_manager.rotate_wallet()

        assert wallet1.address != wallet2.address

    def test_disable_wallet(self, wallet_manager):
        """测试禁用钱包"""
        wallet_manager.disable_wallet("wallet1")

        wallet = wallet_manager.get_wallet("wallet1")
        assert wallet.is_active is False

    def test_get_active_wallets(self, wallet_manager):
        """测试获取活跃钱包"""
        wallet_manager.disable_wallet("wallet1")

        active = wallet_manager.get_active_wallets()
        assert len(active) == 2

    def test_portfolio_summary(self, wallet_manager):
        """测试投资组合摘要"""
        wallet_manager.update_wallet_balance("wallet1", 10.0)
        wallet_manager.update_wallet_balance("wallet2", 20.0)

        summary = wallet_manager.get_portfolio_summary()

        assert summary["total_wallets"] == 3
        assert summary["total_balance_sol"] == 30.0

    def test_get_all_wallets(self, wallet_manager):
        """测试获取所有钱包"""
        wallets = wallet_manager.get_all_wallets()

        assert len(wallets) == 3
        assert all(w.address for w in wallets)
