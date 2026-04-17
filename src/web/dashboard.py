import logging
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from typing import Optional, Dict, Any
import json

logger = logging.getLogger(__name__)


def create_dashboard_app(
    position_manager=None,
    wallet_manager=None,
    scanner=None,
) -> FastAPI:
    """创建仪表板应用"""
    app = FastAPI(title="GMGN Kime AI Dashboard")

    # 存储连接的 WebSocket 客户端
    active_connections = []

    @app.get("/", response_class=HTMLResponse)
    async def get_dashboard():
        """获取仪表板 HTML"""
        return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GMGN Kime AI - 实time交易仪表板</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        header {
            color: white;
            margin-bottom: 30px;
            text-align: center;
        }
        
        h1 {
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .subtitle {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s;
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 12px rgba(0, 0, 0, 0.2);
        }
        
        .card h2 {
            margin-bottom: 15px;
            color: #667eea;
            font-size: 1.3em;
        }
        
        .stat {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #eee;
        }
        
        .stat:last-child {
            border-bottom: none;
        }
        
        .stat-label {
            color: #666;
            font-weight: 500;
        }
        
        .stat-value {
            color: #333;
            font-weight: bold;
            font-size: 1.1em;
        }
        
        .positive {
            color: #10b981;
        }
        
        .negative {
            color: #ef4444;
        }
        
        .position-list {
            list-style: none;
        }
        
        .position-item {
            background: #f5f5f5;
            padding: 12px;
            margin: 8px 0;
            border-radius: 6px;
            border-left: 4px solid #667eea;
        }
        
        .position-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
        }
        
        .position-symbol {
            font-weight: bold;
            font-size: 1.1em;
        }
        
        .position-pnl {
            font-weight: bold;
        }
        
        .status-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: bold;
        }
        
        .status-scanning {
            background: #fbbf24;
            color: #78350f;
        }
        
        .status-monitoring {
            background: #a78bfa;
            color: white;
        }
        
        .status-idle {
            background: #d1d5db;
            color: #374151;
        }
        
        .button-group {
            display: flex;
            gap: 10px;
            margin-top: 15px;
        }
        
        button {
            flex: 1;
            padding: 10px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.2s;
        }
        
        .btn-primary {
            background: #667eea;
            color: white;
        }
        
        .btn-primary:hover {
            background: #5a67d8;
        }
        
        .btn-danger {
            background: #ef4444;
            color: white;
        }
        
        .btn-danger:hover {
            background: #dc2626;
        }
        
        .log-panel {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            grid-column: 1 / -1;
        }
        
        .log-content {
            background: #1e1e1e;
            color: #d4d4d4;
            padding: 15px;
            border-radius: 6px;
            max-height: 300px;
            overflow-y: auto;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            line-height: 1.6;
        }
        
        .log-line {
            padding: 2px 0;
        }
        
        .log-info { color: #6a9955; }
        .log-warning { color: #ce9178; }
        .log-error { color: #f48771; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🤖 GMGN Kime AI</h1>
            <p class="subtitle">下一代 Meme 币自动狙击机器人</p>
        </header>
        
        <div class="grid">
            <!-- 钱包概览 -->
            <div class="card">
                <h2>💰 钱包管理</h2>
                <div class="stat">
                    <span class="stat-label">活跃钱包</span>
                    <span class="stat-value" id="active-wallets">-</span>
                </div>
                <div class="stat">
                    <span class="stat-label">总余额</span>
                    <span class="stat-value" id="total-balance">-</span>
                </div>
                <div class="stat">
                    <span class="stat-label">状态</span>
                    <span class="status-badge status-monitoring" id="wallet-status">就绪</span>
                </div>
            </div>
            
            <!-- 持仓概览 -->
            <div class="card">
                <h2>📊 投资组合</h2>
                <div class="stat">
                    <span class="stat-label">持仓数量</span>
                    <span class="stat-value" id="open-positions">-</span>
                </div>
                <div class="stat">
                    <span class="stat-label">总投入</span>
                    <span class="stat-value" id="total-entry">-</span>
                </div>
                <div class="stat">
                    <span class="stat-label">总收益</span>
                    <span class="stat-value" id="total-pnl">-</span>
                </div>
            </div>
            
            <!-- 扫描状态 -->
            <div class="card">
                <h2>🔍 扫描状态</h2>
                <div class="stat">
                    <span class="stat-label">状态</span>
                    <span class="status-badge status-scanning" id="scanner-status">待命</span>
                </div>
                <div class="stat">
                    <span class="stat-label">已扫描</span>
                    <span class="stat-value" id="scanned-tokens">0</span>
                </div>
                <div class="stat">
                    <span class="stat-label">发现安全币</span>
                    <span class="stat-value positive" id="safe-tokens">0</span>
                </div>
                <div class="button-group">
                    <button class="btn-primary" id="start-scanner">启动扫描</button>
                    <button class="btn-danger" id="stop-scanner">停止</button>
                </div>
            </div>
            
            <!-- 持仓列表 -->
            <div class="card" style="grid-column: 1 / -1;">
                <h2>📈 活跃持仓</h2>
                <ul class="position-list" id="positions-list">
                    <li class="position-item">暂无持仓</li>
                </ul>
            </div>
            
            <!-- 实时日志 -->
            <div class="log-panel">
                <h2>📝 实时日志</h2>
                <div class="log-content" id="log-content">
                    <div class="log-line log-info">系统已启动，等待连接...</div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // WebSocket 连接
        const ws = new WebSocket(`ws://${window.location.host}/ws`);
        
        ws.onopen = () => {
            addLog('WebSocket 连接已建立', 'info');
        };
        
        ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                updateDashboard(data);
            } catch (e) {
                console.error('解析消息失败:', e);
            }
        };
        
        ws.onerror = () => {
            addLog('WebSocket 连接错误', 'error');
        };
        
        function updateDashboard(data) {
            if (data.type === 'portfolio') {
                document.getElementById('open-positions').textContent = 
                    data.payload.open_positions;
                document.getElementById('total-entry').textContent = 
                    `$${data.payload.total_entry_usd.toFixed(2)}`;
                const pnl = data.payload.total_pnl_usd;
                const pnlPercent = data.payload.total_pnl_percent;
                const className = pnl >= 0 ? 'positive' : 'negative';
                document.getElementById('total-pnl').innerHTML = 
                    `<span class="${className}">$${pnl.toFixed(2)} (${pnlPercent.toFixed(2)}%)</span>`;
            }
        }
        
        function addLog(message, type = 'info') {
            const logContent = document.getElementById('log-content');
            const line = document.createElement('div');
            line.className = `log-line log-${type}`;
            const now = new Date().toLocaleTimeString();
            line.textContent = `[${now}] ${message}`;
            logContent.appendChild(line);
            logContent.scrollTop = logContent.scrollHeight;
        }
        
        // 按钮事件
        document.getElementById('start-scanner').onclick = () => {
            addLog('扫描已启动', 'info');
        };
        
        document.getElementById('stop-scanner').onclick = () => {
            addLog('扫描已停止', 'warning');
        };
    </script>
</body>
</html>
        """

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        """WebSocket 端点用于实时数据推送"""
        await websocket.accept()
        active_connections.append(websocket)

        try:
            while True:
                # 接收消息（保持连接活跃）
                data = await websocket.receive_text()
        except Exception as e:
            logger.error(f"WebSocket 错误: {e}")
        finally:
            active_connections.remove(websocket)

    @app.get("/api/portfolio")
    async def get_portfolio():
        """获取投资组合信息"""
        if not position_manager:
            return {"error": "Position manager not available"}

        return position_manager.get_portfolio_summary()

    @app.get("/api/wallets")
    async def get_wallets():
        """获取钱包信息"""
        if not wallet_manager:
            return {"error": "Wallet manager not available"}

        return wallet_manager.get_portfolio_summary()

    @app.post("/api/scanner/start")
    async def start_scanner():
        """启动扫描"""
        if scanner:
            # 在后台启动扫描
            return {"status": "started"}
        return {"error": "Scanner not available"}

    @app.post("/api/scanner/stop")
    async def stop_scanner():
        """停止扫描"""
        if scanner:
            scanner.stop_scanning()
            return {"status": "stopped"}
        return {"error": "Scanner not available"}

    async def broadcast_update(data: Dict[str, Any]):
        """广播更新到所有连接的客户端"""
        for connection in active_connections:
            try:
                await connection.send_json(data)
            except Exception as e:
                logger.error(f"广播失败: {e}")

    app.broadcast_update = broadcast_update

    return app
