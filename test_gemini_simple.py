#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gemini API 简单测试脚本
用于快速验证 API 是否可用
"""

import os
import sys

def test_env():
    """测试环境变量"""
    print("=" * 60)
    print("1. 检查环境变量")
    print("=" * 60)
    
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("❌ 未找到 GEMINI_API_KEY 环境变量")
        print()
        print("请设置环境变量：")
        print("  Windows: set GEMINI_API_KEY=your_key")
        print("  Linux/Mac: export GEMINI_API_KEY=your_key")
        return None
    
    print(f"✅ 找到 API Key")
    print(f"   长度: {len(api_key)} 字符")
    print(f"   前缀: {api_key[:10]}...")
    print(f"   后缀: ...{api_key[-5:]}")
    print()
    
    return api_key


def test_api(api_key):
    """测试 API 调用"""
    print("=" * 60)
    print("2. 测试 Gemini API 调用")
    print("=" * 60)
    
    try:
        import requests
        print("✅ requests 库已安装")
    except ImportError:
        print("❌ 未安装 requests 库")
        print("   请运行: pip install requests")
        return False
    
    # 构建请求
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-3-pro:generateContent?key={api_key}"
    
    print(f"API 端点: {url[:80]}...")
    print()
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": "请用中文简单回复：你好"
                    }
                ]
            }
        ]
    }
    
    print("发送测试请求...")
    print()
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        print(f"HTTP 状态码: {response.status_code}")
        print()
        
        if response.status_code == 200:
            print("✅ API 调用成功！")
            print()
            
            result = response.json()
            
            if 'candidates' in result and len(result['candidates']) > 0:
                content = result['candidates'][0]['content']['parts'][0]['text']
                print("AI 回复：")
                print(content)
                print()
                return True
            else:
                print("⚠️ 响应格式异常")
                print(f"响应内容: {result}")
                return False
        else:
            print(f"❌ API 调用失败")
            print(f"响应内容: {response.text}")
            print()
            
            # 解析错误
            try:
                error_data = response.json()
                if 'error' in error_data:
                    error_msg = error_data['error'].get('message', '未知错误')
                    print(f"错误信息: {error_msg}")
                    print()
                    
                    if 'API key not valid' in error_msg:
                        print("💡 解决方案：")
                        print("   1. 检查 API Key 是否正确")
                        print("   2. 访问 https://makersuite.google.com/app/apikey 重新生成")
                        print("   3. 确认 API Key 没有多余的空格或换行")
                    elif 'quota' in error_msg.lower():
                        print("💡 解决方案：")
                        print("   1. 免费版配额已用完")
                        print("   2. 等待配额重置（每天重置）")
                        print("   3. 或升级到付费版本")
            except:
                pass
            
            return False
            
    except requests.exceptions.Timeout:
        print("❌ 请求超时")
        print("   可能原因：网络连接慢")
        return False
        
    except requests.exceptions.ConnectionError as e:
        print(f"❌ 连接错误: {e}")
        print("   可能原因：")
        print("   1. 无法访问 Google 服务")
        print("   2. 网络连接问题")
        print("   3. 防火墙阻止")
        return False
        
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print()
    print("=" * 60)
    print("Gemini API 快速测试")
    print("=" * 60)
    print()
    
    # 测试环境变量
    api_key = test_env()
    
    if not api_key:
        sys.exit(1)
    
    # 测试 API
    success = test_api(api_key)
    
    print()
    print("=" * 60)
    print("测试结果")
    print("=" * 60)
    
    if success:
        print("✅ Gemini API 配置正确，可以正常使用")
        print()
        print("下一步：运行 python main.py 生成报告")
    else:
        print("❌ Gemini API 配置有问题")
        print()
        print("请根据上述错误信息进行排查")
    
    print()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
