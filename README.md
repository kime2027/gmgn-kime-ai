GMGN Kime AI
===========

开源 Meme 币自动狙击机器人，基于 GMGN OpenAPI 开发

![License](https://img.shields.io/badge/License-MIT-green.svg)
![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

---

项目特色
--------

核心功能

- 实时新币扫描：依托 GMGN OpenAPI 实时监控链上新发币种，毫秒级反应速度
- 智能安全审查：多维度安全检查，覆盖 honeypot、LP 锁定、dev 风险和持有者分析
- 自动交易执行：智能买入决策，自动计算仓位和资金分配
- 精准风险控制：止盈 500%、止损 50%、跟踪止损 10% 全覆盖
- 聪明钱跟单：自动识别并跟踪高效率钱包的交易行为
- 多钱包支持：支持多个钱包同时工作，分散风险和规避 MEV
- Telegram 实时通知：交易、风控与发现结果及时推送
- 轻量级 Web 仪表板：Flask 端口 5000，FastAPI 端口 8000

安全设计

- 完全开源代码，任何人都可审查
- 不包含恶意代码或隐藏逻辑
- 集成多层安全检查机制
- 支持 Anti-MEV 和防 frontrun
- 持仓管理与资金安全优先

适用场景

| 用户类型 | 适合程度 | 推荐资金 |
|---------|---------|--------|
| 小额投资者 | 非常适合 | $10-100 |
| 自动化爱好者 | 非常适合 | - |
| 开发者 / 研究者 | 非常适合 | - |
| 大额交易者 | 适合 | $100+ |

---

快速开始
---------

最速启动

1. 克隆项目
2. 运行启动脚本（首次运行会进行交互式配置）
3. 打开浏览器

```bash
git clone https://github.com/GMGNAI/gmgn-skills.git
cd gmgn-skills/gmgn-kime-ai
chmod +x startup.sh
./startup.sh
```

**注意：** 首次运行时，脚本会自动启动配置向导，要求您输入必要的配置信息，包括：
- GMGN API Key
- Telegram Bot Token 和 Chat ID
- 钱包私钥和地址
- 交易参数等

配置完成后，应用将自动启动。

在浏览器中打开：

- Flask 轻量仪表板： http://localhost:5000
- FastAPI 仪表板： http://localhost:8000

详细步骤请查看 [快速入门指南](QUICKSTART.md)

Docker 快速部署

```bash
docker-compose up -d
docker-compose logs -f kime-bot
```

---

工作流程
--------

```
新币发现 → 安全评分 → 自动买入 → 风险监控 → 止盈 / 止损
   ↓
实时通知 ← Web 仪表板显示 ← 聪明钱跟单
```

详细工作流请参见 [完整文档](WORKFLOW.md)

---

项目结构
--------

```
gmgn-kime-ai/
├── src/
│   ├── api/              - API 客户端
│   │   ├── gmgn_api.py
│   │   └── stats_collector.py
│   ├── scanner/          - 新币扫描模块
│   │   └── token_scanner.py
│   ├── security/         - 安全检查模块
│   │   └── safety_check.py
│   ├── strategy/         - 交易策略模块
│   │   ├── buy_strategy.py
│   │   ├── tp_sl.py
│   │   └── position.py
│   ├── wallet/           - 钱包管理模块
│   │   └── manager.py
│   ├── notifications/    - 通知模块
│   │   └── telegram.py
│   └── web/              - Web 仪表板模块
│       ├── dashboard.py
│       └── flask_dashboard.py
├── tests/                - 单元测试
├── config.py             - 配置管理
├── main.py               - 主程序
├── requirements.txt      - 依赖
├── docker-compose.yml    - Docker 配置
└── README.md             - 当前文档
```

---

配置说明
---------

必需配置

```bash
GMGN_API_KEY=your_api_key_here
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
WALLET_PRIVATE_KEYS=key1,key2,key3
WALLET_ADDRESSES=addr1,addr2,addr3
```

请按以下方式填写：

- GMGN_API_KEY 为 GMGN API 密钥
- TELEGRAM_BOT_TOKEN 为 Telegram 机器人 Token
- TELEGRAM_CHAT_ID 为 Telegram Chat ID
- WALLET_PRIVATE_KEYS 为钱包私钥列表，用逗号分隔
- WALLET_ADDRESSES 为钱包地址列表，用逗号分隔

可选配置

```bash
MIN_BUY_AMOUNT=10
MAX_BUY_AMOUNT=100
TAKE_PROFIT_PERCENT=500
STOP_LOSS_PERCENT=50
TRAILING_STOP_PERCENT=10
HONEYPOT_CHECK_ENABLED=true
LP_LOCK_CHECK_ENABLED=true
MIN_LIQUIDITY_USD=5000
```

完整配置说明请参见 [开发文档](README_DEV.md)

---

完整文档
---------

| 文档 | 说明 |
|------|------|
| [快速入门](QUICKSTART.md) | 5 分钟快速上手 |
| [开发文档](README_DEV.md) | 详细开发与配置说明 |
| [工作流程](WORKFLOW.md) | 系统架构与数据流说明 |
| [开发路线](ROADMAP.md) | 功能规划与发布计划 |
| [贡献指南](CONTRIBUTING.md) | 如何参与 |

---

核心概念
--------

安全评分系统

自动化评分机制（0-100 分）：

| 检查项 | 权重 | 说明 |
|--------|------|------|
| Honeypot | 25% | 检测无法转账的欺骗币 |
| LP 锁定 | 25% | 验证流动性池锁定情况 |
| Dev 风险 | 25% | 分析开发者持仓和抛售风险 |
| 持有者集中 | 25% | 评估持有者分布情况 |

判断标准：评分 ≥ 60 即触发买入

止盈止损机制

```bash
入场价格: $0.0001

止盈: $0.0006 (上涨 500%)
止损: $0.00005 (下跌 50%)
跟踪: 最高价的 90% (10% 回落)
```

---

Web 仪表板
---------

Flask 轻量仪表板 (localhost:5000)

超轻量级 Web3 风格仪表板，包含：

- 实时投资组合统计（总投入、当前价值、未实现 PNL）
- 活跃持仓列表（代币数量、价值、盈亏率）
- SOL 余额显示，用于 gas 费用管理
- 钱包管理（活跃钱包数、余额汇总）
- 最近交易记录（类型、金额、时间）
- 系统日志实时输出
- 每 5 秒自动刷新

通过 GMGN /v1/user/holdings 接口获取实时统计：

- 总胜率
- 总交易数
- 今日投入
- 未实现总 PNL
- 持仓详情

Web3 风格设计：

- 深色主题
- GMGN 配色
- Glassmorphism 视觉风格
- 实时数据跳动效果
- 响应式布局

FastAPI 仪表板 (localhost:8000)

完整功能仪表板，支持 WebSocket 实时推送

---

Telegram 通知示例
--------------

```bash
发现安全新币!
名称: MemeToken
流动性: $10,000
持有者: 526
安全评分: 85/100

买入执行
代币: MEME
成本: $50.00
数量: 500,000

止盈平仓
收益: +$250.00 (+500%)
```

---

测试
---

```bash
pytest tests/
pytest tests/test_position.py -v
pytest --cov=src tests/
```

---

更新日志
------

v0.1.0 (2024-04-17)

- 初版发布
- 新币扫描功能
- 多层安全审查系统
- 持仓与风险管理
- Web 仪表板
- Telegram 通知集成
- Flask 轻量级仪表板

---

贡献
---

欢迎提交 Issue 和 Pull Request！

开发流程

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

---

免责声明
---

重要提示：

- 本项目仅为教育和研究用途，不是投资建议
- 虽然有安全检查，但不能保证 100% 安全
- 交易存在风险，可能导致资金损失
- 请从小额开始，逐步增加资金
- 定期检查钱包和交易记录
- 保护好私钥，不要分享给任何人

使用本项目即表示您理解并接受所有风险。

---

许可证
---

此项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

---

相关资源
---

- [GMGN 官方网站](https://gmgn.ai)
- [GMGN API 文档](https://api.gmgn.ai/docs)
- [Telegram 讨论群](https://t.me/gmgnai)
- [提交问题](https://github.com/GMGNAI/gmgn-skills/issues)

---

社区
---

- Email: team@gmgn.ai
- Twitter: [@GMGNAI](https://twitter.com/gmgnai)

作者
---

- 作者: X
- X (Twitter): [@Kime_Crypto](https://x.com/Kime_Crypto)
- Telegram: [@kime2026](https://t.me/kime2026)

---

项目统计
-------

- Stars: ![GitHub stars](https://img.shields.io/github/stars/GMGNAI/gmgn-skills)
- Forks: ![GitHub forks](https://img.shields.io/github/forks/GMGNAI/gmgn-skills)

---

Made with ❤️ by GMGN Team

自动化交易，让 meme 币狙击变得简单
