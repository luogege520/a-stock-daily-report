#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查询 Gemini API 可用模型列表
"""

import os
import sys
import requests


def list_models():
    """列出所有可用的 Gemini 模型"""
    
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("❌ 未找到 GEMINI_API_KEY 环境变量")
        print("请设置: export GEMINI_API_KEY=your_key")
        return
    
    print("=" * 80)
    print("查询 Gemini API 可用模型列表")
    print("=" * 80)
    print()
    
    # 列出模型
    url = f"https://generativelanguage.googleapis.com/v1/models?key={api_key}"
    
    print(f"请求 URL: {url[:60]}...")
    print()
    
    try:
        response = requests.get(url, timeout=30)
        
        print(f"HTTP 状态码: {response.status_code}")
        print()
        
        if response.status_code == 200:
            result = response.json()
            
            if 'models' in result:
                models = result['models']
                print(f"✅ 找到 {len(models)} 个可用模型：")
                print()
                print("-" * 80)
                
                for model in models:
                    name = model.get('name', 'Unknown')
                    display_name = model.get('displayName', 'N/A')
                    description = model.get('description', 'N/A')
                    supported_methods = model.get('supportedGenerationMethods', [])
                    
                    print(f"模型名称: {name}")
                    print(f"显示名称: {display_name}")
                    print(f"描述: {description}")
                    print(f"支持的方法: {', '.join(supported_methods)}")
                    print("-" * 80)
                
                # 筛选支持 generateContent 的模型
                print()
                print("=" * 80)
                print("支持 generateContent 的模型：")
                print("=" * 80)
                print()
                
                for model in models:
                    supported_methods = model.get('supportedGenerationMethods', [])
                    if 'generateContent' in supported_methods:
                        name = model.get('name', 'Unknown')
                        display_name = model.get('displayName', 'N/A')
                        print(f"✅ {name}")
                        print(f"   显示名称: {display_name}")
                        print()
            else:
                print("⚠️ 响应中没有 models 字段")
                print(f"响应内容: {result}")
        else:
            print(f"❌ 请求失败")
            print(f"响应内容: {response.text}")
            
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    list_models()
