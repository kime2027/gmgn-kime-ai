"""
轻量级 Flask 仪表板 - Web3 风格
支持实时持仓、统计数据、配置开关
"""

from flask import Flask, render_template_string, jsonify
from flask_cors import CORS
import asyncio
import json
from datetime import datetime
from typing import Dict, Any, Optional

app = Flask(__name__)
CORS(app)


class DashboardData:
    """仪表板数据管理"""

    def __init__(self):
        self.portfolio = None
        self.wallets = None
        self.stats = None
        self.recent_trades = []
        self.system_status = "running"
        self.config = {}
        self.scanner_status = "stopped"
        self.logs = []

    def update_portfolio(self, position_manager):
        """更新投资组合数据"""
        try:
            summary = position_manager.get_portfolio_summary()
            positions = position_manager.get_all_positions()

            self.portfolio = {
                "total_entry_usd": summary["total_entry_usd"],
                "total_current_usd": summary["total_current_usd"],
                "total_pnl_usd": summary["total_pnl_usd"],
                "total_pnl_percent": summary["total_pnl_percent"],
                "open_positions": summary["open_positions"],
                "positions": [
                    {
                        "symbol": p.token_symbol,
                        "address": p.token_address,
                        "quantity": p.quantity,
                        "entry_price": p.entry_price,
                        "current_price": p.current_price or 0,
                        "entry_usd": p.entry_usd,
                        "current_usd": p.current_usd or 0,
                        "pnl_usd": (p.current_usd or 0) - p.entry_usd,
                        "pnl_percent": p.get_pnl_percent(),
                        "buy_time": p.buy_time.isoformat(),
                    }
                    for p in positions.values()
                ],
            }
        except Exception as e:
            print(f"Error updating portfolio: {e}")

    def update_wallets(self, wallet_manager):
        """更新钱包数据"""
        try:
            summary = wallet_manager.get_portfolio_summary()
            self.wallets = summary
        except Exception as e:
            print(f"Error updating wallets: {e}")

    def add_trade(self, trade_info: Dict[str, Any]):
        """添加交易记录"""
        trade = {
            **trade_info,
            "timestamp": datetime.now().isoformat(),
        }
        self.recent_trades.insert(0, trade)
        self.recent_trades = self.recent_trades[:50]  # 保留最近50条

    def add_log(self, message: str, level: str = "info"):
        """添加日志"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message,
        }
        self.logs.insert(0, log_entry)
        self.logs = self.logs[:100]  # 保留最近100条


dashboard_data = DashboardData()


@app.route("/")
def index():
    """主仪表板页面"""
    return render_template_string(DASHBOARD_HTML)


@app.route("/api/portfolio")
def get_portfolio():
    """获取投资组合数据"""
    return jsonify(dashboard_data.portfolio or {})


@app.route("/api/wallets")
def get_wallets():
    """获取钱包数据"""
    return jsonify(dashboard_data.wallets or {})


@app.route("/api/stats")
def get_stats():
    """获取统计数据"""
    portfolio = dashboard_data.portfolio or {}
    wallets = dashboard_data.wallets or {}

    return jsonify({
        "total_invested": portfolio.get("total_entry_usd", 0),
        "total_current": portfolio.get("total_current_usd", 0),
        "total_pnl": portfolio.get("total_pnl_usd", 0),
        "total_pnl_percent": portfolio.get("total_pnl_percent", 0),
        "position_count": portfolio.get("open_positions", 0),
        "wallet_count": wallets.get("total_wallets", 0),
        "total_balance_sol": wallets.get("total_balance_sol", 0),
    })


@app.route("/api/trades")
def get_trades():
    """获取最近交易"""
    return jsonify(dashboard_data.recent_trades)


@app.route("/api/logs")
def get_logs():
    """获取系统日志"""
    return jsonify(dashboard_data.logs)


@app.route("/api/system-status")
def get_system_status():
    """获取系统状态"""
    return jsonify({
        "status": dashboard_data.system_status,
        "scanner": dashboard_data.scanner_status,
        "timestamp": datetime.now().isoformat(),
    })


def create_flask_app(position_manager=None, wallet_manager=None):
    """创建 Flask 应用实例"""
    dashboard_data.position_manager = position_manager
    dashboard_data.wallet_manager = wallet_manager
    return app


def start_dashboard_server(host: str = "0.0.0.0", port: int = 5000):
    """启动仪表板服务器"""
    app.run(host=host, port=port, debug=False, use_reloader=False)


# HTML 模板 - Web3 风格，采用 GMGN 色系
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GMGN Kime AI - 交易仪表板</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --primary: #667eea;
            --primary-dark: #5a67d8;
            --primary-light: #7c8fee;
            --secondary: #764ba2;
            --success: #10b981;
            --danger: #ef4444;
            --warning: #f59e0b;
            --dark: #1a202c;
            --darker: #0f172a;
            --border: #2d3748;
            --text-primary: #f5f7fa;
            --text-secondary: #cbd5e0;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, var(--dark) 0%, var(--darker) 100%);
            color: var(--text-primary);
            overflow-x: hidden;
        }

        .container {
            max-width: 1600px;
            margin: 0 auto;
            padding: 20px;
        }

        header {
            background: rgba(102, 126, 234, 0.05);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
        }

        header h1 {
            font-size: 2em;
            margin-bottom: 10px;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        header .status {
            display: flex;
            gap: 15px;
            margin-top: 15px;
            flex-wrap: wrap;
        }

        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 16px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border);
            border-radius: 8px;
            font-size: 0.9em;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--success);
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .card {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }

        .card:hover {
            border-color: var(--primary);
            box-shadow: 0 0 20px rgba(102, 126, 234, 0.2);
        }

        .card h3 {
            font-size: 0.9em;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 15px;
        }

        .card .value {
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 10px;
        }

        .card .subtext {
            font-size: 0.85em;
            color: var(--text-secondary);
        }

        .positive { color: var(--success); }
        .negative { color: var(--danger); }
        .neutral { color: var(--text-secondary); }

        .chart-container {
            grid-column: 1 / -1;
        }

        .positions-grid {
            grid-column: 1 / -1;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }

        .position-card {
            background: rgba(102, 126, 234, 0.05);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 16px;
            transition: all 0.3s ease;
        }

        .position-card:hover {
            border-color: var(--primary-light);
            background: rgba(102, 126, 234, 0.1);
        }

        .position-header {
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 12px;
        }

        .position-symbol {
            font-weight: bold;
            font-size: 1.1em;
        }

        .position-pnl {
            font-weight: bold;
            font-size: 1em;
        }

        .position-details {
            font-size: 0.85em;
            color: var(--text-secondary);
            line-height: 1.6;
        }

        .position-details div {
            display: flex;
            justify-content: space-between;
        }

        .trades-container {
            grid-column: 1 / -1;
        }

        .trades-list {
            max-height: 400px;
            overflow-y: auto;
        }

        .trade-item {
            background: rgba(255, 255, 255, 0.02);
            border-left: 3px solid var(--primary);
            padding: 12px;
            margin-bottom: 10px;
            border-radius: 6px;
            font-size: 0.9em;
        }

        .trade-type {
            font-weight: bold;
            text-transform: uppercase;
            font-size: 0.8em;
        }

        .logs-container {
            grid-column: 1 / -1;
        }

        .logs-display {
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 16px;
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 0.85em;
            max-height: 300px;
            overflow-y: auto;
            line-height: 1.6;
        }

        .log-entry {
            padding: 4px 0;
            display: flex;
            gap: 10px;
        }

        .log-time {
            color: var(--primary);
            min-width: 100px;
        }

        .log-level {
            min-width: 60px;
            font-weight: bold;
        }

        .log-info { color: var(--primary); }
        .log-success { color: var(--success); }
        .log-warning { color: var(--warning); }
        .log-error { color: var(--danger); }

        .log-message {
            color: var(--text-primary);
            flex: 1;
        }

        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }

        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb {
            background: var(--primary);
            border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: var(--primary-light);
        }

        .loading {
            text-align: center;
            color: var(--text-secondary);
            padding: 20px;
        }

        @media (max-width: 768px) {
            .grid {
                grid-template-columns: 1fr;
            }
            
            .positions-grid {
                grid-template-columns: 1fr;
            }

            header h1 {
                font-size: 1.5em;
            }

            .card .value {
                font-size: 1.5em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>GMGN Kime AI</h1>
            <p>Web3 自动交易仪表板</p>
            <div class="status">
                <div class="status-badge">
                    <div class="status-dot"></div>
                    <span id="system-status">连接中...</span>
                </div>
                <div class="status-badge">
                    <span id="local-time"></span>
                </div>
            </div>
        </header>

        <!-- 统计卡片 -->
        <div class="grid">
            <div class="card">
                <h3>总投入</h3>
                <div class="value" id="total-invested">$0.00</div>
                <div class="subtext">全部钱包</div>
            </div>

            <div class="card">
                <h3>当前价值</h3>
                <div class="value" id="total-current">$0.00</div>
                <div class="subtext">实时更新</div>
            </div>

            <div class="card">
                <h3>未实现PNL</h3>
                <div class="value" id="total-pnl">$0.00</div>
                <div class="subtext" id="total-pnl-percent">0.00%</div>
            </div>

            <div class="card">
                <h3>持仓数量</h3>
                <div class="value" id="position-count">0</div>
                <div class="subtext">个代币</div>
            </div>

            <div class="card">
                <h3>钱包数量</h3>
                <div class="value" id="wallet-count">0</div>
                <div class="subtext">活跃账户</div>
            </div>

            <div class="card">
                <h3>SOL 余额</h3>
                <div class="value" id="total-balance-sol">0.00</div>
                <div class="subtext">用于gas费</div>
            </div>
        </div>

        <!-- 持仓列表 -->
        <div class="card">
            <h3>活跃持仓</h3>
            <div class="positions-grid" id="positions-grid">
                <div class="loading">暂无持仓</div>
            </div>
        </div>

        <!-- 最近交易 -->
        <div class="card trades-container">
            <h3>最近交易</h3>
            <div class="trades-list" id="trades-list">
                <div class="loading">暂无交易</div>
            </div>
        </div>

        <!-- 系统日志 -->
        <div class="card logs-container">
            <h3>系统日志</h3>
            <div class="logs-display" id="logs-display">
                <div class="log-entry">
                    <span class="log-time">[系统]</span>
                    <span class="log-level log-info">INFO</span>
                    <span class="log-message">仪表板已连接</span>
                </div>
            </div>
        </div>
    </div>

    <script>
        // 自动更新时间
        function updateTime() {
            const now = new Date();
            document.getElementById('local-time').textContent = 
                now.toLocaleTimeString('zh-CN');
        }
        setInterval(updateTime, 1000);
        updateTime();

        // 刷新数据（每5秒）
        async function refreshData() {
            try {
                // 获取统计数据
                const statsRes = await fetch('/api/stats');
                const stats = await statsRes.json();

                // 获取投资组合
                const portfolioRes = await fetch('/api/portfolio');
                const portfolio = await portfolioRes.json();

                // 获取交易
                const tradesRes = await fetch('/api/trades');
                const trades = await tradesRes.json();

                // 获取日志
                const logsRes = await fetch('/api/logs');
                const logs = await logsRes.json();

                // 更新统计数据
                document.getElementById('total-invested').textContent = 
                    '$' + stats.total_invested.toFixed(2);
                document.getElementById('total-current').textContent = 
                    '$' + stats.total_current.toFixed(2);
                
                const pnlClass = stats.total_pnl >= 0 ? 'positive' : 'negative';
                document.getElementById('total-pnl').className = 'value ' + pnlClass;
                document.getElementById('total-pnl').textContent = 
                    '$' + stats.total_pnl.toFixed(2);
                
                document.getElementById('total-pnl-percent').className = 
                    'subtext ' + pnlClass;
                document.getElementById('total-pnl-percent').textContent = 
                    stats.total_pnl_percent.toFixed(2) + '%';

                document.getElementById('position-count').textContent = 
                    stats.position_count;
                document.getElementById('wallet-count').textContent = 
                    stats.wallet_count;
                document.getElementById('total-balance-sol').textContent = 
                    stats.total_balance_sol.toFixed(4);

                // 更新持仓
                if (portfolio.positions && portfolio.positions.length > 0) {
                    const posGrid = document.getElementById('positions-grid');
                    posGrid.innerHTML = portfolio.positions.map(pos => {
                        const pnlClass = pos.pnl_usd >= 0 ? 'positive' : 'negative';
                        return `
                            <div class="position-card">
                                <div class="position-header">
                                    <div class="position-symbol">${pos.symbol}</div>
                                    <div class="position-pnl ${pnlClass}">
                                        ${pos.pnl_usd >= 0 ? '+' : ''}${pos.pnl_usd.toFixed(2)}
                                    </div>
                                </div>
                                <div class="position-details">
                                    <div>
                                        <span>数量:</span>
                                        <span>${pos.quantity.toFixed(6)}</span>
                                    </div>
                                    <div>
                                        <span>入场:</span>
                                        <span>${pos.entry_price.toFixed(6)}</span>
                                    </div>
                                    <div>
                                        <span>当前:</span>
                                        <span>${pos.current_price.toFixed(6)}</span>
                                    </div>
                                    <div>
                                        <span>成本:</span>
                                        <span>$${pos.entry_usd.toFixed(2)}</span>
                                    </div>
                                    <div>
                                        <span>价值:</span>
                                        <span>$${pos.current_usd.toFixed(2)}</span>
                                    </div>
                                    <div>
                                        <span>收益率:</span>
                                        <span class="${pnlClass}">
                                            ${pos.pnl_percent.toFixed(2)}%
                                        </span>
                                    </div>
                                </div>
                            </div>
                        `;
                    }).join('');
                }

                // 更新交易
                if (trades && trades.length > 0) {
                    const tradesList = document.getElementById('trades-list');
                    tradesList.innerHTML = trades.map(trade => {
                        return `
                            <div class="trade-item">
                                <div class="trade-type">${trade.action}</div>
                                <div>${trade.token} - $${trade.amount.toFixed(2)}</div>
                                <div style="color: var(--text-secondary); font-size: 0.85em;">
                                    ${new Date(trade.timestamp).toLocaleString('zh-CN')}
                                </div>
                            </div>
                        `;
                    }).join('');
                }

                // 更新日志
                if (logs && logs.length > 0) {
                    const logsDisplay = document.getElementById('logs-display');
                    logsDisplay.innerHTML = logs.map(log => {
                        const levelClass = 'log-' + log.level;
                        const time = new Date(log.timestamp).toLocaleTimeString('zh-CN');
                        return `
                            <div class="log-entry">
                                <span class="log-time">[${time}]</span>
                                <span class="log-level ${levelClass}">${log.level.toUpperCase()}</span>
                                <span class="log-message">${log.message}</span>
                            </div>
                        `;
                    }).join('');
                }

            } catch (error) {
                console.error('Failed to fetch data:', error);
            }
        }

        // 初始刷新和定时刷新
        refreshData();
        setInterval(refreshData, 5000);
    </script>
</body>
</html>
"""
