贡献指南

感谢您对 GMGN Kime AI 的兴趣！我们欢迎所有形式的贡献。

📋 目录

- [行为准则](#行为准则)
- [如何贡献](#如何贡献)
- [开发流程](#开发流程)
- [代码标准](#代码标准)
- [提交指南](#提交指南)
- [获取帮助](#获取帮助)

---

行为准则

我们的承诺

为了营造开放和欢迎的环境，我们：

- 对所有参与者保持包容和尊重
- 欢迎不同的观点和经验
- 优雅地接受建设性批评
- 专注于对整个社区最有利的事情

不可接受的行为

包括但不限于：

- 骚扰、欺凌或恐吓行为
- 仇恨言论或仇恨行为
- 性骚扰或性别歧视
- 不请自来的报价、投资建议或营销

---

如何贡献

1. 报告 Bug

发现 Bug？请通过 [GitHub Issues](https://github.com/GMGNAI/gmgn-skills/issues) 报告。

提前检查：确保不是重复的 Issue。

提供信息：

```
描述：简要说明 Bug

复现步骤：
1. 第一步
2. 第二步
3. 预期结果
4. 实际结果

日志：
提供相关的日志片段（隐藏敏感信息）

环境：
- Python 版本：3.11
- 操作系统：Linux/macOS/Windows
- GMGN API 版本：
```

2. 建议功能

有好主意？在 [Discussions](https://github.com/GMGNAI/gmgn-skills/discussions) 分享。

提供信息：

```
功能描述：您想要什么和为什么？

使用场景：
- 当前困境
- 建议的解决方案
- 替代方案

额外上下文：
- 相关的研究链接
- 类似项目的实现
```

3. 代码贡献

想修复 Bug 或添加功能？

```bash
1. Fork 仓库到您的账户

2. Clone 到本地
git clone https://github.com/YOUR_USERNAME/gmgn-skills.git
cd gmgn-skills/gmgn-kime-ai

3. 创建功能分支
git checkout -b feature/your-feature
或 fix bug
git checkout -b fix/your-bugfix

4. 开发并测试
... 编写代码 ...
pytest tests/

5. 提交更改
git add .
git commit -m "feat: add your feature"

6. 推送到 GitHub
git push origin feature/your-feature

7. 创建 Pull Request
在 GitHub 上创建 PR，填写详细说明
```

---

开发流程

环境设置

```bash
创建虚拟环境
python3 -m venv venv
source venv/bin/activate

安装开发依赖
pip install -r requirements.txt
pip install pytest pytest-cov pytest-asyncio black flake8 mypy

安装预提交钩子（可选）
pip install pre-commit
pre-commit install
```

开发工作流

```bash
1. 创建新分支
git checkout -b feature/your-feature

2. 编写代码
... 开发功能 ...

3. 格式化代码
black src/ tests/
flake8 src/ tests/

4. 类型检查
mypy src/

5. 运行测试
pytest tests/ -v --cov=src

6. 提交代码
git add .
git commit -m "feat: description"

7. 推送到远程
git push origin feature/your-feature
```

测试要求

- 所有新代码必须有对应的测试
- 测试覆盖率必须 ≥ 80%
- 所有测试必须通过

```bash
运行测试with覆盖率
pytest tests/ --cov=src --cov-report=html

查看覆盖率报告
open htmlcov/index.html
```

---

代码标准

编码风格

遵循 PEP 8：

```python
✅ 好的
def calculate_position_value(entry_price: float, quantity: int) -> float:
    """计算持仓价值。"""
    return entry_price  quantity


❌ 坏的
def calc_pos_val(entry_price, quantity):
    return entry_pricequantity
```

注释和文档

```python
def check_honeypot(token_address: str) -> tuple[float, str]:
    """
    检查代币是否为 honeypot。
    
    Args:
        token_address: 代币地址

    Returns:
        tuple: (评分: 0-100, 原因说明)
        
    Raises:
        ValueError: 如果地址无效
        
    Example:
        >>> score, reason = check_honeypot("0x123")
        >>> assert score >= 0 and score <= 100
    """
    pass
```

类型提示

```python
使用类型提示
from typing import Optional, List, Dict

def process_tokens(
    tokens: List[str],
    max_count: Optional[int] = None,
) -> Dict[str, float]:
    """处理代币列表。"""
    pass
```

性能考虑

```python
✅ 异步调用
async def fetch_tokens() -> list:
    async with GMGNAPIClient() as client:
        return await client.get_new_tokens()

❌ 同步阻塞
def fetch_tokens():
    # 会阻塞事件循环
    time.sleep(1)
    return api.get_tokens()
```

---

提交指南

提交消息格式

遵循 Conventional Commits：

```
<type>[optional scope]: <description>

[optional body]

[optional footer]
```

类型

- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码风格改变（不影响功能）
- `refactor`: 代码重构
- `perf`: 性能改进
- `test`: 测试相关
- `chore`: 构建或依赖相关

例子

```bash
git commit -m "feat: add honeypot detection"
git commit -m "fix: correct position calculation bug"
git commit -m "docs: update API documentation"
git commit -m "refactor: simplify token scanner logic"
```

Pull Request 模板

```markdown
描述
简要描述您的更改。

相关 Issue
修复 #issue_number

类型
- [ ] 新功能
- [ ] Bug 修复
- [ ] 文档更新
- [ ] 性能改进
- [ ] 重构

做了什么
简要列出主要改动。

测试
- [ ] 添加了相应的测试
- [ ] 所有测试通过
- [ ] 测试覆盖率 > 80%

检查清单
- [ ] 代码遵循项目风格
- [ ] 进行了自我审查
- [ ] 更新了相关文档
- [ ] 没有引入新的警告
```

---

获取帮助

问题或困惑？

1. 查看文档
   - [README.md](README.md) - 项目概述
   - [README_DEV.md](README_DEV.md) - 开发指南
   - [WORKFLOW.md](WORKFLOW.md) - 工作流程

2. 搜索已有 Issues
   - 可能有人遇到过相同问题

3. 提问
   - [GitHub Discussions](https://github.com/GMGNAI/gmgn-skills/discussions)
   - 描述您遇到的问题和您已经尝试的

4. 联系核心团队
   - Email: dev@gmgn.ai
   - Telegram: [@gmgn_ai](https://t.me/gmgn_ai)

---

贡献者致谢

感谢所有为项目做出贡献的人！

贡献者列表

<!-- 会自动更新 -->

参与本项目的贡献者：
- 代码贡献
- Bug 报告
- 文档改进
- 社区支持

---

许可证

通过提交贡献，您同意您的代码在 MIT 许可证下许可。

---

社区

- 🐦 [Twitter](https://twitter.com/GMGNAI)
- 💬 [Telegram](https://t.me/gmgn_ai)
- 💻 [GitHub](https://github.com/GMGNAI)
- 📧 [Email](mailto:dev@gmgn.ai)

---

再次感谢您对 GMGN Kime AI 的支持！ ❤️
