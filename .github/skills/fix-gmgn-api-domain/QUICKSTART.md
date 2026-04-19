# GMGN API Domain Fix Skill - 使用指南

## 📦 Skill 包结构

```
.github/skills/fix-gmgn-api-domain/
├── SKILL.md                    # Skill 定义和元数据
├── README.md                   # 详细使用文档
├── fix_api_domain.py           # 修复脚本（核心功能）
├── verify_api_config.py        # 验证脚本
└── run_all.py                  # 综合运行脚本
```

## 🚀 快速使用

### 方式1：一键修复和验证（推荐）
```bash
cd /workspaces/gmgn-kime-ai
python3 .github/skills/fix-gmgn-api-domain/run_all.py
```

### 方式2：仅修复
```bash
python3 .github/skills/fix-gmgn-api-domain/fix_api_domain.py
```

### 方式3：仅验证
```bash
python3 .github/skills/fix-gmgn-api-domain/verify_api_config.py
```

## 📋 功能概述

| 脚本 | 功能 | 输入 | 输出 |
|------|------|------|------|
| `fix_api_domain.py` | 自动修复API域名 | 无 | 修复结果和验证报告 |
| `verify_api_config.py` | 验证配置正确性 | 无 | 验证结果和建议 |
| `run_all.py` | 一键修复+验证 | 无 | 完整的执行总结 |

## 🔧 修复范围

该skill修复以下文件和配置：

- **config.py** (第13行) - Python配置中的GMGN_API_BASE_URL
- **.env.example** (第3行) - 环境变量示例
- **docker-compose.yml** (第12行) - Docker启动环境变量

**修改内容：**
```
旧版本: https://api.gmgn.ai/v1
新版本: https://openapi.gmgn.ai/v1
```

## ✅ 验证成功标志

运行脚本后，应该看到以下输出：

```
✓ config.py: API 域名正确 (openapi.gmgn.ai)
✓ .env.example: API 域名正确 (openapi.gmgn.ai)  
✓ docker-compose.yml: API 域名正确 (openapi.gmgn.ai)
✓ 修复验证成功！所有API配置都已正确更新
```

## 🐳 Docker 用户

修复后需要重启容器：

```bash
docker-compose down
docker-compose up -d --build
```

## 🎯 适用场景

✓ **初始化项目**：第一次设置项目时运行
✓ **故障排查**：API请求被拦截时运行
✓ **迁移升级**：从旧版API端点迁移时运行
✓ **自动化部署**：CI/CD流程中的配置验证

## 📖 详细文档

查看详细使用指南：
```bash
cat .github/skills/fix-gmgn-api-domain/README.md
```

查看Skill定义：
```bash
cat .github/skills/fix-gmgn-api-domain/SKILL.md
```

## 🆘 故障排查

**问题：脚本找不到config.py**
- 解决：确保从项目根目录运行
```bash
cd /workspaces/gmgn-kime-ai
python3 .github/skills/fix-gmgn-api-domain/run_all.py
```

**问题：验证失败，显示"api.gmgn.ai"**
- 解决：运行修复脚本
```bash
python3 .github/skills/fix-gmgn-api-domain/fix_api_domain.py
```

**问题：Docker里修改后没生效**
- 解决：重构并重启容器
```bash
docker-compose down && docker-compose up -d --build
```

## 🔗 相关资源

- GMGN 官方API: https://openapi.gmgn.ai/docs
- Skill文档: [SKILL.md](SKILL.md)
- 使用指南: [README.md](README.md)
- 项目配置: [config.py](../../../config.py)

## 📝 修改日志

- **v1.0** (2024-04-17)
  - 初始化skill版本
  - 创建自动修复脚本
  - 创建验证脚本
  - 创建综合运行脚本
