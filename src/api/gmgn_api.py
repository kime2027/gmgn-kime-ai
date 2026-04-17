import asyncio
import aiohttp
import logging
from typing import Optional, Dict, List, Any
from config import Config

logger = logging.getLogger(__name__)


class GMGNAPIClient:
    """GMGN OpenAPI 客户端"""

    def __init__(self, api_key: str = None, base_url: str = None):
        self.api_key = api_key or Config.GMGN_API_KEY
        self.base_url = base_url or Config.GMGN_API_BASE_URL
        self.session: Optional[aiohttp.ClientSession] = None
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def connect(self) -> bool:
        """保持 GMGN API 会话连接。"""
        if not self.session or self.session.closed:
            self.session = aiohttp.ClientSession()
        return True

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """发起 API 请求"""
        if not self.session:
            self.session = aiohttp.ClientSession()

        url = f"{self.base_url}{endpoint}"
        try:
            async with self.session.request(
                method, url, headers=self.headers, params=params, json=json_data
            ) as response:
                data = await response.json()
                if response.status != 200:
                    logger.error(f"API 错误: {response.status} - {data}")
                    raise Exception(f"API 请求失败: {response.status}")
                return data
        except Exception as e:
            logger.error(f"请求失败: {e}")
            raise

    async def get_new_tokens(
        self, limit: int = 100, sort_by: str = "created_at"
    ) -> List[Dict[str, Any]]:
        """获取新币列表"""
        params = {"limit": limit, "sort": sort_by}
        return await self._request("GET", "/tokens/new", params=params)

    async def get_token_info(self, token_address: str) -> Dict[str, Any]:
        """获取代币信息"""
        return await self._request("GET", f"/tokens/{token_address}")

    async def get_token_holders(self, token_address: str) -> List[Dict[str, Any]]:
        """获取代币持有者"""
        return await self._request("GET", f"/tokens/{token_address}/holders")

    async def get_liquidity_info(self, token_address: str) -> Dict[str, Any]:
        """获取流动性信息"""
        return await self._request("GET", f"/tokens/{token_address}/liquidity")

    async def get_token_trades(
        self, token_address: str, limit: int = 50
    ) -> List[Dict[str, Any]]:
        """获取代币交易历史"""
        params = {"limit": limit}
        return await self._request(
            "GET", f"/tokens/{token_address}/trades", params=params
        )

    async def get_smart_money_trades(
        self, token_address: str, limit: int = 20
    ) -> List[Dict[str, Any]]:
        """获取聪明钱的交易记录"""
        params = {"limit": limit}
        return await self._request(
            "GET", f"/tokens/{token_address}/smart_money_trades", params=params
        )

    async def get_wallet_info(self, wallet_address: str) -> Dict[str, Any]:
        """获取钱包信息"""
        return await self._request("GET", f"/wallets/{wallet_address}")

    async def get_wallet_portfolio(self, wallet_address: str) -> Dict[str, Any]:
        """获取钱包持仓"""
        return await self._request("GET", f"/wallets/{wallet_address}/portfolio")

    async def search_smart_money(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """搜索聪明钱"""
        return await self._request("POST", "/smart_money/search", json_data=criteria)

    async def close(self):
        """关闭连接"""
        if self.session:
            await self.session.close()
