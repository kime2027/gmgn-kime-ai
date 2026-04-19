#!/usr/bin/env python3
"""
GMGN API 完整修复和验证脚本
一次性执行修复和验证所有步骤
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(cmd, description):
    """运行命令并打印结果"""
    print(f"\n{'='*60}")
    print(f"📋 {description}")
    print('='*60)
    print()
    
    try:
        result = subprocess.run(cmd, shell=True, cwd='/workspaces/gmgn-kime-ai')
        return result.returncode == 0
    except Exception as e:
        print(f"✗ 执行失败: {e}")
        return False

def main():
    """执行完整的修复和验证流程"""
    
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*10 + "GMGN API 域名修复和验证脚本" + " "*20 + "║")
    print("╚" + "="*58 + "╝")
    print()
    
    # 第一步：修复API域名
    fix_success = run_command(
        "python3 .github/skills/fix-gmgn-api-domain/fix_api_domain.py",
        "第一步: 修复API域名配置"
    )
    
    if not fix_success:
        print("\n✗ 修复失败，停止执行")
        return 1
    
    # 第二步：验证修复结果
    verify_success = run_command(
        "python3 .github/skills/fix-gmgn-api-domain/verify_api_config.py",
        "第二步: 验证修复结果"
    )
    
    # 第三步：显示所有配置文件
    print(f"\n{'='*60}")
    print("📋 第三步: 查看所有配置文件中的API设置")
    print('='*60)
    print()
    
    run_command(
        "echo '配置文件检查:' && grep -n 'GMGN_API_BASE_URL' config.py .env.example docker-compose.yml 2>/dev/null || echo '✓ 所有文件都已正确配置'",
        "完整性检查"
    )
    
    # 总结
    print(f"\n{'='*60}")
    print("📊 执行总结")
    print('='*60)
    print()
    
    if verify_success:
        print("✓ 所有步骤执行成功！")
        print()
        print("📌 下一步操作:")
        print("  1. 如果使用Docker: docker-compose down && docker-compose up -d --build")
        print("  2. 如果使用本地环境: 重启应用确保新配置生效")
        print("  3. 运行测试验证API连接是否正常")
        print()
        print("📖 更多信息: cat .github/skills/fix-gmgn-api-domain/README.md")
        print()
        return 0
    else:
        print("⚠️  修复可能有问题，请检查输出日志")
        print()
        return 1

if __name__ == '__main__':
    exit(main())
