#!/usr/bin/env python3
"""
GMGN API 域名修复脚本
将api.gmgn.ai改为openapi.gmgn.ai
"""

import os
import re
from pathlib import Path

def fix_gmgn_api_domain():
    """修复所有配置文件中的GMGN API域名"""
    
    # 定义要修复的文件和替换规则
    files_to_fix = [
        {
            'path': 'config.py',
            'old': 'https://api.gmgn.ai/v1',
            'new': 'https://openapi.gmgn.ai/v1'
        },
        {
            'path': '.env.example',
            'old': 'https://api.gmgn.ai/v1',
            'new': 'https://openapi.gmgn.ai/v1'
        },
        {
            'path': 'docker-compose.yml',
            'old': 'https://api.gmgn.ai/v1',
            'new': 'https://openapi.gmgn.ai/v1'
        }
    ]
    
    print("=" * 60)
    print("GMGN API 域名修复脚本")
    print("=" * 60)
    print()
    
    fixed_files = []
    
    # 处理每个文件
    for file_info in files_to_fix:
        file_path = Path(file_info['path'])
        
        if not file_path.exists():
            print(f"⚠️  文件不存在: {file_path}")
            continue
        
        try:
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否需要修复
            if file_info['old'] in content:
                # 替换内容
                new_content = content.replace(file_info['old'], file_info['new'])
                
                # 写入修改后的内容
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"✓ 已修复: {file_path}")
                print(f"  {file_info['old']}")
                print(f"  → {file_info['new']}")
                print()
                fixed_files.append(file_path)
            else:
                print(f"✓ 已是最新版本: {file_path}")
                print()
        
        except Exception as e:
            print(f"✗ 修复失败: {file_path}")
            print(f"  错误: {e}")
            print()
    
    print("=" * 60)
    print("验证修复结果")
    print("=" * 60)
    print()
    
    # 验证修复结果
    all_correct = True
    for file_info in files_to_fix:
        file_path = Path(file_info['path'])
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if file_info['new'] in content:
                print(f"✓ {file_path}: API 域名正确 (openapi.gmgn.ai)")
            elif file_info['old'] in content:
                print(f"✗ {file_path}: API 域名有误 (api.gmgn.ai)")
                all_correct = False
            else:
                print(f"⚠️  {file_path}: 未找到API域名配置")
    
    print()
    print("=" * 60)
    
    if all_correct:
        print("✓ 修复验证成功！所有API配置都已正确更新")
        return 0
    else:
        print("✗ 修复验证失败！请检查配置文件")
        return 1

if __name__ == '__main__':
    exit(fix_gmgn_api_domain())
