# 如何让Copilot直接运行此Skill

## 快速命令

直接在Copilot Chat中输入以下命令：

### 方式1：一键修复+验证（最推荐）
```bash
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

---

## Copilot Chat 使用示例

### **输入1：快速修复**
```
修复GMGN API域名配置
```
Copilot会自动调用此skill

### **输入2：完整修复+验证**  
```
运行GMGN API域名修复脚本，并验证配置
```
Copilot会执行：
```bash
python3 .github/skills/fix-gmgn-api-domain/run_all.py
```

### **输入3：仅验证**
```
验证GMGN API配置是否正确
```
Copilot会执行：
```bash
python3 .github/skills/fix-gmgn-api-domain/verify_api_config.py
```

---

## 直接在终端运行

如果您想完全跳过Copilot，直接运行：

```bash
cd /workspaces/gmgn-kime-ai
python3 .github/skills/fix-gmgn-api-domain/run_all.py
```

---

## Skill 被自动识别的条件

✓ SKILL.md 文件在正确位置：`.github/skills/fix-gmgn-api-domain/SKILL.md`
✓ 包含正确的 frontmatter（name, description）
✓ description 中包含 "Use when:" 关键词

现在此skill已被Copilot认可，您可以：
- 直接chat述说需求，Copilot会自动匹配
- 或直接运行上述任何命令
- Copilot会自动执行相应的脚本
