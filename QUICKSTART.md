🚀 快速入门指南

5分钟快速开始

方式一: 直接运行（推荐新手）

第1步: 准备环境

```bash
克隆项目
git clone https://github.com/GMGNAI/gmgn-skills.git
cd gmgn-skills/gmgn-kime-ai

Linux/Mac: 给启动脚本权限
chmod +x startup.sh
```

第2步: 配置

```bash
复制配置文件
cp .env.example .env

编辑 .env，填入以下必需项:
GMGN_API_KEY=xxx
TELEGRAM_BOT_TOKEN=xxx
TELEGRAM_CHAT_ID=xxx
WALLET_PRIVATE_KEYS=xxx
WALLET_ADDRESSES=xxx
```

第3步: 运行

```bash
Linux/Mac
./startup.sh

Windows
startup.bat

或直接用 Python
python main.py
```

✅ 完成！访问 http://localhost:8000 查看仪表板

---

方式二: Docker 运行（推荐服务器）

```bash
编辑 .env 文件
nano .env

启动容器
docker-compose up -d

查看日志
docker-compose logs -f kime-bot

停止容器
docker-compose down
```

---

获取必需的配置信息

1️⃣ GMGN API Key

访问 https://api.gmgn.ai 注册账户：

1. 登录/注册
2. 进入 API 管理
3. 创建新的 API Key
4. 复制 API Key

2️⃣ Telegram Bot Token

1. 打开 Telegram，搜索 `@BotFather`
2. 发送 `/newbot`
3. 按提示创建机器人
4. 复制得到的 Token

3️⃣ Telegram Chat ID

1. 搜索 `@userinfobot`
2. 发送任意消息
3. 复制返回的 Chat ID

4️⃣ 钱包信息

⚠️ 安全警告：永远不要在公开地方分享私钥！

创建专用钱包用于机器人：

```bash
Solana 钱包示例
使用 Phantom Wallet 或 Sollet 创建钱包
导出私钥并填入 .env

格式: 逗号分隔多个钱包
WALLET_PRIVATE_KEYS=key1,key2,key3
WALLET_ADDRESSES=addr1,addr2,addr3
```

---

配置说明

基础配置（重要）

| 配置项 | 说明 | 示例 |
|--------|------|------|
| `GMGN_API_KEY` | API 密钥 | `sk_xxx` |
| `TELEGRAM_BOT_TOKEN` | Telegram 机器人 Token | `123:abc` |
| `TELEGRAM_CHAT_ID` | 接收通知的 Chat ID | `987654321` |
| `WALLET_PRIVATE_KEYS` | 钱包私钥（逗号分隔） | `key1,key2` |
| `WALLET_ADDRESSES` | 钱包地址（逗号分隔） | `addr1,addr2` |

交易配置（可选）

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `MIN_BUY_AMOUNT` | 10 | 最小买入金额（美元） |
| `MAX_BUY_AMOUNT` | 100 | 最大买入金额（美元） |
| `TAKE_PROFIT_PERCENT` | 500 | 止盈目标（上涨百分比） |
| `STOP_LOSS_PERCENT` | 50 | 止损点（下跌百分比） |
| `TRAILING_STOP_PERCENT` | 10 | 跟踪止损（下跌百分比） |

安全配置（可选）

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `HONEYPOT_CHECK_ENABLED` | true | 是否检查 honeypot |
| `LP_LOCK_CHECK_ENABLED` | true | 是否检查 LP 锁定 |
| `DEV_SELLOFF_CHECK_ENABLED` | true | 是否检查 dev 抛售 |
| `MIN_LIQUIDITY_USD` | 5000 | 最小流动性（美元） |
| `MAX_HOLDER_CONCENTRATION` | 30 | 最大持有者集中度（百分比） |

---

仪表板说明

访问 http://localhost:8000

主要功能

- 💰 钱包管理: 查看活跃钱包和余额
- 📊 投资组合: 查看当前持仓和收益
- 🔍 扫描状态: 启动/停止新币扫描
- 📈 持仓跟踪: 实时查看每个持仓的盈亏
- 📝 实时日志: 查看系统运行日志

快捷操作

点击卡片里的按钮可以：
- 启动扫描
- 停止扫描
- 查看详细信息

---

Telegram 通知示例

机器人会自动发送通知：

```
🎯 发现安全新币!
名称: MemeToken
代码: MEME
💰 流动性: $10,000
👥 持有者: 526
✅ 安全评分: 85/100

💰 买入执行
代币: MEME
入场价: $0.0001
买入金额: $50.00
时间: 2024-04-17 10:30:45

✅ 交易已平仓 (止盈)
盈亏: +$250.00 (+500%)
```

---

常见问题

Q: 需要多少资金才能开始？

A: 建议最少 $100-200，这样可以分散在多个代币中。但即使只有 $10-50 也能开始体验。

Q: 是否支持多个钱包？

A: 是的，可以配置多个钱包分散风险：

```
WALLET_PRIVATE_KEYS=key1,key2,key3
WALLET_ADDRESSES=addr1,addr2,addr3
```

Q: 能否修改止盈止损比例？

A: 可以，编辑 `.env` 文件：

```
TAKE_PROFIT_PERCENT=500   # 上涨500%时止盈
STOP_LOSS_PERCENT=50      # 下跌50%时止损
TRAILING_STOP_PERCENT=10  # 最高价下跌10%时触发
```

Q: Web 仪表板无法访问？

A: 检查：
1. 确认应用正在运行
2. 检查 8000 端口是否被占用
3. 尝试访问 http://127.0.0.1:8000 (本地)

Q: 如何查看日志？

A: 
- 实时日志: 仪表板 → 日志面板
- 文件日志: `logs/kime.log`
- Docker: `docker-compose logs -f kime-bot`

Q: 如何重启机器人？

A: 
```bash
直接运行
Ctrl+C 停止，然后 ./startup.sh 重启

Docker
docker-compose restart
```

---

相关资源

- 📚 [完整文档](README_DEV.md)
- 🔗 [GMGN 官网](https://gmgn.ai)
- 🤖 [Telegram 群组](https://t.me/gmgnai)
- 💬 [讨论区](https://github.com/GMGNAI/gmgn-skills/discussions)

---

安全提示

⚠️ 重要安全事项：

1. 不要分享私钥 - 私钥类似于密码，永远不要分享给任何人
2. 定期检查余额 - 定期查看钱包余额和交易记录
3. 小额测试 - 先用小额资金测试设置
4. 合理分散 - 不要把所有资金放在一个钱包
5. 备份配置 - 备份 `.env` 文件到安全位置
6. 审查代码 - 这是开源项目，欢迎审查代码

---

技术支持

遇到问题？

1. 查看 [FAQ](README_DEV.md)
2. 搜索已有 [Issues](https://github.com/GMGNAI/gmgn-skills/issues)
3. 创建新 Issue 描述问题
4. 加入 Telegram 群组寻求帮助

---

开始体验

现在就准备好了！🎉

```bash
3 个命令快速开始
git clone https://github.com/GMGNAI/gmgn-skills.git
cd gmgn-skills/gmgn-kime-ai
./startup.sh  # 或 startup.bat (Windows)
```

访问 http://localhost:8000 并开始狙击！🎯

---

© GMGN Kime AI - 自专业的 meme 币狙击机器人
