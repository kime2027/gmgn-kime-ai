#!/usr/bin/env python3
"""
GMGN API 域名验证脚本
验证config.py中的API配置是否正确
"""

import sys
import os

# 获取项目根目录（假设此脚本在 .github/skills/fix-gmgn-api-domain/目录中）
script_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))

# 添加项目根目录到Python路径
sys.path.insert(0, root_dir)
os.chdir(root_dir)

def verify_api_config():
    """验证API配置是否正确"""
    
    try:
        from config import Config
        
        print("=" * 60)
        print("GMGN API 配置验证")
        print("=" * 60)
        print()
        
        api_url = Config.GMGN_API_BASE_URL
        print(f"当前API基础URL: {api_url}")
        print()
        
        # 验证域名
        if 'openapi.gmgn.ai' in api_url:
            print("✓ API 域名正确: openapi.gmgn.ai")
            print("✓ 配置已准备好用于AI Agent")
            print()
            print("=" * 60)
            print("✓ 验证成功！")
            print("=" * 60)
            return 0
        
        elif 'api.gmgn.ai' in api_url:
            print("✗ API 域名错误: api.gmgn.ai")
            print("✗ 该域名对应的是GMGN网页接口，被Cloudflare保护，不允许AI Agent访问")
            print()
            print("建议操作:")
            print("1. 运行修复脚本: python3 .github/skills/fix-gmgn-api-domain/fix_api_domain.py")
            print("2. 或手动更新.env: export GMGN_API_BASE_URL=https://openapi.gmgn.ai/v1")
            print()
            print("=" * 60)
            print("✗ 验证失败！")
            print("=" * 60)
            return 1
        
        else:
            print("⚠️  无法识别的API域名")
            print()
            print("=" * 60)
            print("⚠️  验证异常！")
            print("=" * 60)
            return 2
    
    except Exception as e:
        print(f"✗ 验证异常: {e}")
        print()
        print("=" * 60)
        print("✗ 验证失败！")
        print("=" * 60)
        return 1

if __name__ == '__main__':
    exit(verify_api_config())
