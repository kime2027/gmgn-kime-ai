import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class Wallet:
    """钱包信息"""
    address: str
    private_key: str
    balance_sol: float = 0.0  # SOL 余额
    balance_usd: float = 0.0  # USD 余额
    nonce: int = 0
    is_active: bool = True


class WalletManager:
    """多钱包管理器"""

    def __init__(self, wallet_addresses: List[str], private_keys: List[str]):
        self.wallets: Dict[str, Wallet] = {}
        self._init_wallets(wallet_addresses, private_keys)
        self.current_wallet_index = 0

    def _init_wallets(self, addresses: List[str], keys: List[str]):
        """初始化钱包"""
        if len(addresses) != len(keys):
            raise ValueError("钱包地址和私钥数量不匹配")

        for addr, key in zip(addresses, keys):
            if addr and key:  # 跳过空值
                wallet = Wallet(address=addr, private_key=key)
                self.wallets[addr] = wallet
                logger.info(f"初始化钱包: {addr[:10]}...")

    def get_wallet(self, address: str = None) -> Optional[Wallet]:
        """获取钱包"""
        if address:
            return self.wallets.get(address)

        # 返回当前活跃钱包
        if self.wallets:
            return list(self.wallets.values())[self.current_wallet_index]
        return None

    def get_all_wallets(self) -> List[Wallet]:
        """获取所有钱包"""
        return list(self.wallets.values())

    def get_active_wallets(self) -> List[Wallet]:
        """获取活跃钱包"""
        return [w for w in self.wallets.values() if w.is_active]

    def update_wallet_balance(self, address: str, balance_sol: float):
        """更新钱包余额"""
        if address in self.wallets:
            self.wallets[address].balance_sol = balance_sol
            # 这里可以根据汇率计算 USD 余额
            # self.wallets[address].balance_usd = balance_sol * SOL_PRICE
            logger.debug(f"更新钱包 {address[:10]} 余额: {balance_sol} SOL")

    def rotate_wallet(self) -> Optional[Wallet]:
        """轮换钱包（用于分散风险）"""
        active_wallets = self.get_active_wallets()
        if not active_wallets:
            return None

        self.current_wallet_index = (self.current_wallet_index + 1) % len(active_wallets)
        return active_wallets[self.current_wallet_index]

    def disable_wallet(self, address: str):
        """禁用钱包（如果出现错误）"""
        if address in self.wallets:
            self.wallets[address].is_active = False
            logger.warning(f"钱包已禁用: {address[:10]}")

    def enable_wallet(self, address: str):
        """启用钱包"""
        if address in self.wallets:
            self.wallets[address].is_active = True
            logger.info(f"钱包已启用: {address[:10]}")

    def get_portfolio_summary(self) -> Dict[str, Any]:
        """获取钱包组合摘要"""
        total_balance_sol = sum(w.balance_sol for w in self.wallets.values())
        total_balance_usd = sum(w.balance_usd for w in self.wallets.values())
        active_count = len(self.get_active_wallets())

        return {
            "total_wallets": len(self.wallets),
            "active_wallets": active_count,
            "total_balance_sol": total_balance_sol,
            "total_balance_usd": total_balance_usd,
            "wallets": [
                {
                    "address": w.address,
                    "balance_sol": w.balance_sol,
                    "balance_usd": w.balance_usd,
                    "is_active": w.is_active,
                }
                for w in self.wallets.values()
            ],
        }
