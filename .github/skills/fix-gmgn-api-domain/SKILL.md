---
name: fix-gmgn-api-domain
description: "修复GMGN API配置，将api.gmgn.ai域名更新为openapi.gmgn.ai。Use when: 启动应用前、API调用被Cloudflare拦截、或需要验证API端点配置。"
tools:
  - run_in_terminal
  - read_file
  - replace_string_in_file
---

# 修复GMGN API域名

## 问题

- **api.gmgn.ai** = GMGN网页界面，由Cloudflare保护 ❌ AI Agent无法访问
- **openapi.gmgn.ai** = 官方API端点 ✓ AI Agent可以访问

## 任务

修复以下文件中的API域名配置：
- `config.py` (行13)
- `.env.example` (行3)  
- `docker-compose.yml` (行12)

**修改:** `https://api.gmgn.ai/v1` → `https://openapi.gmgn.ai/v1`

## 执行

```bash
# 一键修复+验证（推荐）
python3 .github/skills/fix-gmgn-api-domain/run_all.py
```

或单独执行：
```bash
# 仅修复
python3 .github/skills/fix-gmgn-api-domain/fix_api_domain.py

# 仅验证
python3 .github/skills/fix-gmgn-api-domain/verify_api_config.py
```

## 验证结果

看到以下输出表示成功：
```
✓ config.py: API 域名正确 (openapi.gmgn.ai)
✓ .env.example: API 域名正确 (openapi.gmgn.ai)  
✓ docker-compose.yml: API 域名正确 (openapi.gmgn.ai)
✓ 修复验证成功！
```

## 修复后

- **本地环境:** 重启应用
- **Docker:** `docker-compose down && docker-compose up -d --build`

## 详细文档
- [快速开始](QUICKSTART.md)
- [完整指南](README.md)
