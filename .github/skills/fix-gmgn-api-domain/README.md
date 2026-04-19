# 修复GMGN API域名 Skill

这是一个自动化skill，用于修复GMGN API配置中的域名问题。

## 快速开始

### 1. 一键修复并验证

```bash
cd /workspaces/gmgn-kime-ai
python3 .github/skills/fix-gmgn-api-domain/fix_api_domain.py
```

### 2. 验证修复结果

```bash
python3 .github/skills/fix-gmgn-api-domain/verify_api_config.py
```

### 3. 查看所有配置

```bash
grep -n "GMGN_API_BASE_URL" config.py .env.example docker-compose.yml
```

## 脚本说明

### fix_api_domain.py

自动修复脚本，扫描并修复所有配置文件中的GMGN API域名。

**功能：**
- ✓ 自动检测需要修复的配置文件
- ✓ 将 `api.gmgn.ai` 替换为 `openapi.gmgn.ai`
- ✓ 验证修复结果
- ✓ 返回适当的退出码

**使用：**
```bash
python3 fix_api_domain.py
```

**输出示例：**
```
============================================================
GMGN API 域名修复脚本
============================================================

✓ 已修复: config.py
  https://api.gmgn.ai/v1
  → https://openapi.gmgn.ai/v1

✓ 已修复: .env.example
  https://api.gmgn.ai/v1
  → https://openapi.gmgn.ai/v1

✓ 已修复: docker-compose.yml
  https://api.gmgn.ai/v1
  → https://openapi.gmgn.ai/v1

============================================================
验证修复结果
============================================================

✓ config.py: API 域名正确 (openapi.gmgn.ai)
✓ .env.example: API 域名正确 (openapi.gmgn.ai)
✓ docker-compose.yml: API 域名正确 (openapi.gmgn.ai)

============================================================
✓ 修复验证成功！所有API配置都已正确更新
============================================================
```

### verify_api_config.py

验证脚本，检查当前配置是否正确。

**功能：**
- ✓ 导入config.py并读取GMGN_API_BASE_URL配置
- ✓ 验证域名是否正确
- ✓ 提供修复建议（如果有问题）

**使用：**
```bash
python3 verify_api_config.py
```

**输出示例（正确）：**
```
============================================================
GMGN API 配置验证
============================================================

当前API基础URL: https://openapi.gmgn.ai/v1

✓ API 域名正确: openapi.gmgn.ai
✓ 配置已准备好用于AI Agent

============================================================
✓ 验证成功！
============================================================
```

## 修复范围

该skill修复以下文件中的API域名：

| 文件 | 修复前 | 修复后 |
|------|--------|--------|
| `config.py` | `https://api.gmgn.ai/v1` | `https://openapi.gmgn.ai/v1` |
| `.env.example` | `https://api.gmgn.ai/v1` | `https://openapi.gmgn.ai/v1` |
| `docker-compose.yml` | `https://api.gmgn.ai/v1` | `https://openapi.gmgn.ai/v1` |

## 为什么需要此修复

**问题：** 项目使用了 `api.gmgn.ai` 作为API端点
- 这个域名对应的是GMGN网页接口
- 由Cloudflare保护，会拦截AI Agent的请求
- 导致API调用失败

**解决：** 使用 `openapi.gmgn.ai` 作为API端点
- 官方提供的AI Agent专用API端点
- 不受Cloudflare拦截
- 支持完整的API功能

## 常见问题

**Q: 我可以在Docker中运行此脚本吗？**

A: 可以。修改docker-compose.yml后，重建并重启容器：
```bash
docker-compose down
docker-compose up -d --build
```

**Q: 如果我手动修改了.env呢？**

A: 该脚本只修复默认配置文件。如果有自定义.env文件，请手动修改：
```bash
export GMGN_API_BASE_URL=https://openapi.gmgn.ai/v1
```

**Q: 修复后需要做什么？**

A: 
1. 重启应用使用新配置
2. 运行验证脚本确认配置正确
3. 测试API调用是否正常

## 相关资源

- 📖 [GMGN API文档](https://openapi.gmgn.ai/docs)
- 🔧 [项目配置](../../../config.py)
- 🐳 [Docker配置](../../../docker-compose.yml)
- 📝 [环境变量模板](../../../.env.example)
