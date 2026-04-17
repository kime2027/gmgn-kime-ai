#!/usr/bin/env python3
"""
GMGN Kime AI - 自动化狙击机器人主程序

基于 GMGN OpenAPI 的 Meme 币狙击机器人，支持：
- 实时新币扫描
- 智能安全审查
- 自动交易执行
- 止盈止损管理
- 聪明钱跟单
- Telegram 实时通知
- Web 仪表板 (Flask 轻量级 + FastAPI)
"""

import asyncio
import logging
import sys
import threading
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from config import Config
from src.api.gmgn_api import GMGNAPIClient
from src.api.stats_collector import StatsCollector
from src.scanner.token_scanner import TokenScanner
from src.security.safety_check import SafetyChecker
from src.strategy.position import PositionManager
from src.strategy.buy_strategy import BuyStrategy
from src.strategy.tp_sl import ProfitLossManager
from src.wallet.manager import WalletManager
from src.notifications.telegram import TelegramNotifier
from src.web.dashboard import create_dashboard_app
from src.web.flask_dashboard import create_flask_app, start_dashboard_server, dashboard_data
import uvicorn

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(Config.LOG_FILE),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)


class KimeAIBot:
    """GMGN Kime AI 主机器人类"""

    def __init__(self):
        logger.info("=" * 50)
        logger.info("GMGN Kime AI 初始化中...")
        logger.info("=" * 50)

        # 初始化组件
        self.api_client = GMGNAPIClient()
        self.stats_collector = StatsCollector(self.api_client)
        self.safety_checker = SafetyChecker(self.api_client)
        self.position_manager = PositionManager()
        self.wallet_manager = WalletManager(
            Config.WALLET_ADDRESSES, Config.WALLET_PRIVATE_KEYS
        )

        # 初始化通知器
        self.notifier = TelegramNotifier(
            Config.TELEGRAM_BOT_TOKEN, Config.TELEGRAM_CHAT_ID
        )

        # 初始化策略
        self.scanner = TokenScanner(
            self.api_client, self.safety_checker, self.notifier
        )
        self.buy_strategy = BuyStrategy(
            self.api_client, self.position_manager, self.notifier
        )
        self.tp_sl_manager = ProfitLossManager(
            self.api_client, self.position_manager, self.notifier
        )

        # Web 应用
        self.fastapi_app = create_dashboard_app(
            self.position_manager, self.wallet_manager, self.scanner
        )
        self.flask_app = create_flask_app()

        # 任务列表
        self.tasks = []
        self.flask_thread = None

    async def initialize(self):
        """初始化所有组件"""
        try:
            # 验证配置
            Config.validate()
            logger.info("✅ 配置验证通过")

            # 连接 Telegram
            if await self.notifier.connect():
                logger.info("✅ Telegram 连接成功")
            else:
                logger.warning("⚠️ Telegram 连接失败，将继续运行但不发送通知")

            # 验证 API 连接并保持会话
            await self.api_client.connect()
            logger.info("✅ GMGN API 连接成功")

            logger.info("=" * 50)
            logger.info("初始化完成!")
            logger.info("=" * 50)

        except Exception as e:
            logger.error(f"初始化失败: {e}")
            raise

    async def run(self):
        """运行主程序"""
        await self.initialize()

        try:
            # 更新 Flask 仪表板数据
            dashboard_data.update_portfolio(self.position_manager)
            dashboard_data.update_wallets(self.wallet_manager)
            dashboard_data.config = {
                "min_buy": Config.MIN_BUY_AMOUNT,
                "max_buy": Config.MAX_BUY_AMOUNT,
                "take_profit": Config.TAKE_PROFIT_PERCENT,
                "stop_loss": Config.STOP_LOSS_PERCENT,
            }

            # 创建异步任务
            tasks = [
                asyncio.create_task(self.scanner.start_scanning(interval=30)),
                asyncio.create_task(
                    self.tp_sl_manager.start_monitoring(interval=60)
                ),
                asyncio.create_task(self.run_fastapi_server()),
                asyncio.create_task(self.run_flask_server()),
                asyncio.create_task(self.update_dashboard_data()),
            ]

            logger.info("🚀 所有组件已启动")
            logger.info(f"📱 Flask 仪表板 (轻量): http://localhost:5000")
            logger.info(f"🚀 FastAPI 仪表板: http://localhost:{Config.WEB_PORT}")
            logger.info("📨 Telegram 通知已启用")

            # 发送启动通知
            startup_message = f"""
GMGN Kime AI 已启动

配置信息:
• 扫描间隔: 30秒
• 买入范围: ${Config.MIN_BUY_AMOUNT} - ${Config.MAX_BUY_AMOUNT}
• 止盈: {Config.TAKE_PROFIT_PERCENT:.0f}%
• 止损: {Config.STOP_LOSS_PERCENT:.0f}%
• 跟踪止损: {Config.TRAILING_STOP_PERCENT:.0f}%

活跃钱包:
• 总数: {len(self.wallet_manager.get_active_wallets())}

准备就绪，开始狙击!
            """
            await self.notifier.send_message(startup_message)

            # 等待所有任务
            await asyncio.gather(*tasks)

        except KeyboardInterrupt:
            logger.info("收到中断信号，正在关闭...")
            await self.shutdown()
        except Exception as e:
            logger.error(f"运行出错: {e}")
            await self.shutdown()

    async def run_flask_server(self):
        """在后台线程运行 Flask 服务器"""
        try:
            logger.info("启动 Flask 仪表板服务器...")
            self.flask_thread = threading.Thread(
                target=start_dashboard_server,
                kwargs={"host": "0.0.0.0", "port": 5000},
                daemon=True
            )
            self.flask_thread.start()
            logger.info("✅ Flask 服务器运行在 http://localhost:5000")
            
            # 保持线程活跃
            while True:
                await asyncio.sleep(1)
        except Exception as e:
            logger.error(f"Flask 服务器错误: {e}")

    async def run_fastapi_server(self):
        """运行 FastAPI 服务器"""
        try:
            config = uvicorn.Config(
                self.fastapi_app,
                host=Config.WEB_HOST,
                port=Config.WEB_PORT,
                log_level="info",
            )
            server = uvicorn.Server(config)
            await server.serve()
        except Exception as e:
            logger.error(f"FastAPI 服务器错误: {e}")

    async def update_dashboard_data(self):
        """定期更新仪表板数据"""
        try:
            while True:
                # 每10秒更新一次
                await asyncio.sleep(10)
                
                # 更新投资组合
                dashboard_data.update_portfolio(self.position_manager)
                dashboard_data.update_wallets(self.wallet_manager)
                
                # 从 API 获取统计数据
                stats = await self.stats_collector.get_portfolio_stats(
                    Config.WALLET_ADDRESSES
                )
                if stats:
                    dashboard_data.stats = stats
                    
        except Exception as e:
            logger.error(f"更新仪表板数据失败: {e}")

    async def shutdown(self):
        """关闭应用"""
        logger.info("正在关闭应用...")

        # 取消所有任务
        for task in asyncio.all_tasks():
            task.cancel()

        # 关闭扫描
        self.scanner.stop_scanning()

        # 关闭监控
        self.tp_sl_manager.stop_monitoring()

        # 关闭通知器
        await self.notifier.disconnect()

        # 关闭 API 客户端
        await self.api_client.close()

        logger.info("应用已关闭")


def main():
    """主函数"""
    try:
        bot = KimeAIBot()
        asyncio.run(bot.run())
    except Exception as e:
        logger.error(f"致命错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
