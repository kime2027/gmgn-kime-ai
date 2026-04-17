开发指南

快速开始

1. 环境设置

```bash
克隆仓库
git clone https://github.com/GMGNAI/gmgn-skills.git
cd gmgn-skills

创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
或
venv\Scripts\activate  # Windows

安装依赖
pip install -r requirements.txt
```

2. 配置

复制 `.env.example` 到 `.env` 并填入你的配置：

```bash
cp .env.example .env
```

必须填入的字段：
- `GMGN_API_KEY`: GMGN OpenAPI 密钥
- `TELEGRAM_BOT_TOKEN`: Telegram 机器人 Token
- `TELEGRAM_CHAT_ID`: 接收通知的 Chat ID
- `WALLET_PRIVATE_KEYS`: 钱包私钥（逗号分隔）
- `WALLET_ADDRESSES`: 钱包地址（逗号分隔）

3. 运行

```bash
python main.py
```

项目结构

```
gmgn-kime-ai/
├── src/
│   ├── api/                 # API 客户端
│   │   ├── gmgn_api.py     # GMGN OpenAPI 客户端
│   │   └── blockchain.py   # 区块链交互
│   ├── scanner/            # 新币扫描
│   │   └── token_scanner.py
│   ├── security/           # 安全检查
│   │   ├── honeypot.py
│   │   ├── lp_analyzer.py
│   │   └── safety_check.py
│   ├── strategy/           # 交易策略
│   │   ├── buy_strategy.py
│   │   ├── tp_sl.py
│   │   └── position.py
│   ├── wallet/             # 钱包管理
│   │   └── manager.py
│   ├── notifications/      # 通知
│   │   └── telegram.py
│   └── web/                # Web 面板
│       └── dashboard.py
├── tests/                  # 单元测试
├── config.py              # 配置管理
├── main.py                # 主程序
└── requirements.txt       # 依赖
```

核心概念

TokenScanner（新币扫描器）

实时扫描 GMGN 的新币列表，并进行初步过滤：

```python
scanner = TokenScanner(api_client, safety_checker, notifier)
await scanner.start_scanning(interval=30)  # 每30秒扫描一次
```

SafetyChecker（安全检查器）

评估代币的安全性，检查项包括：
- Honeypot 检测
- LP 锁定状态
- Dev 抛售风险
- 持有者集中度

```python
score, reasons = await safety_checker.check_token(token_address)
```

BuyStrategy（买入策略）

自动执行买入决策：

```python
await buy_strategy.execute_buy(
    token_address="...",
    token_symbol="MEME",
    buy_amount_usd=50.0
)
```

PositionManager（持仓管理）

管理当前持仓，计算盈亏：

```python
position = position_manager.open_position(...)
position_manager.update_position_price(token_address, new_price)
position_manager.close_position(token_address, exit_price)
```

ProfitLossManager（止盈止损管理）

监控持仓，自动触发止盈止损：

```python
await tp_sl_manager.start_monitoring(interval=60)  # 每60秒检查一次
```

API 使用示例

获取新币

```python
async with GMGNAPIClient() as client:
    new_tokens = await client.get_new_tokens(limit=100)
    for token in new_tokens:
        print(f"{token['symbol']}: ${token['price']}")
```

检查聪明钱

```python
smart_money_trades = await client.get_smart_money_trades(token_address)
for trade in smart_money_trades:
    if trade['pnl_percent'] > 200:  # 至少赚200%
        print(f"发现聪明钱: {trade}")
```

获取持有者

```python
holders = await client.get_token_holders(token_address)
for holder in holders[:10]:
    percent = holder['percent']
    print(f"{holder['address']}: {percent}%")
```

配置说明

交易配置

- `MIN_BUY_AMOUNT`: 最小买入金额（$）
- `MAX_BUY_AMOUNT`: 最大买入金额（$）
- `TAKE_PROFIT_PERCENT`: 止盈百分比（对应上涨%）
- `STOP_LOSS_PERCENT`: 止损百分比（对应下跌%）
- `TRAILING_STOP_PERCENT`: 跟踪止损百分比

安全配置

- `HONEYPOT_CHECK_ENABLED`: 是否检查 honeypot
- `LP_LOCK_CHECK_ENABLED`: 是否检查 LP 锁定
- `DEV_SELLOFF_CHECK_ENABLED`: 是否检查 dev 抛售
- `MIN_LIQUIDITY_USD`: 最小流动性（$）
- `MAX_HOLDER_CONCENTRATION`: 最大持有者集中度（%）

高级功能

聪明钱跟单

启用聪明钱跟单功能：

```python
定期调用此方法
await buy_strategy.check_smart_money_buys()
```

多钱包配置

支持多个钱包以分散风险：

```python
wallet = wallet_manager.rotate_wallet()  # 轮换钱包
wallets = wallet_manager.get_active_wallets()  # 获取活跃钱包
```

Anti-MEV 防护

在交易执行时添加延迟和随机性防止 MEV：

```python
可在 buy_strategy 中添加随机延迟
await asyncio.sleep(random.uniform(1, 5))
```

日志

日志同时输出到文件和控制台：

- 文件位置: `logs/kime.log`
- 日志级别: `INFO`

可通过修改 `config.py` 的 `LOG_LEVEL` 调整。

Web 仪表板

访问 http://localhost:8000 查看实时仪表板

功能

- 📊 投资组合概览
- 💰 钱包管理
- 📈 持仓跟踪
- 🔍 扫描状态
- 📝 实时日志

Telegram 通知

机器人会推送以下通知：

- 🎯 发现安全新币
- 💰 买入执行
- ✅ 止盈平仓
- ❌ 止损平仓
- 📊 投资组合摘要

常见问题

Q: 如何获取 GMGN API Key？

访问 https://api.gmgn.ai 注册并创建 API Key

Q: 如何配置 Telegram 通知？

1. 创建 Telegram 机器人（@BotFather）
2. 获取 Chat ID（发送消息给 @userinfobot）
3. 填入 `.env` 文件

Q: 作为没有经验的新手是否适合使用？

可以，但建议：
- 从小额开始（$10-50）
- 仔细阅读配置说明
- 在测试网或模拟环境中先试用
- 定期监控 Web 仪表板

贡献

欢迎提交 Issue 和 Pull Request！

免责声明

本项目仅为教育和研究用途。交易存在风险，请谨慎使用。

---

© GMGN Kime AI 2024
