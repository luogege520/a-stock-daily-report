#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gemini API 测试脚本
用于诊断 API 连接问题
"""

import os
import sys
import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_gemini_api():
    """测试 Gemini API 连接"""
    
    print("="*60)
    print("Gemini API 连接测试")
    print("="*60)
    print()
    
    # 1. 检查环境变量
    print("1️⃣ 检查环境变量...")
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("❌ 错误：未找到 GEMINI_API_KEY 环境变量")
        print()
        print("解决方案：")
        print("1. 创建 .env 文件")
        print("2. 添加：GEMINI_API_KEY=your_api_key_here")
        print("3. 或在命令行设置：set GEMINI_API_KEY=your_api_key")
        return False
    
    print(f"✅ 找到 API Key: {api_key[:20]}...{api_key[-10:]}")
    print()
    
    # 2. 测试 API 连接
    print("2️⃣ 测试 API 连接...")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={api_key}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": "请用中文回复：你好，这是一个测试。"
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 100
        }
    }
    
    try:
        print("  发送测试请求...")
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        print(f"  HTTP 状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            if 'candidates' in result and len(result['candidates']) > 0:
                content = result['candidates'][0]['content']['parts'][0]['text']
                print("✅ API 连接成功！")
                print()
                print("AI 回复：")
                print(content)
                print()
                return True
            else:
                print("❌ API 返回格式异常")
                print("响应内容：", result)
                return False
        else:
            print(f"❌ HTTP 错误: {response.status_code}")
            print("响应内容：", response.text)
            
            # 解析错误信息
            try:
                error_data = response.json()
                if 'error' in error_data:
                    error_msg = error_data['error'].get('message', '未知错误')
                    print(f"错误信息: {error_msg}")
                    
                    # 常见错误提示
                    if 'API key not valid' in error_msg:
                        print()
                        print("💡 解决方案：")
                        print("1. 检查 API Key 是否完整复制")
                        print("2. 访问 https://makersuite.google.com/app/apikey 重新生成")
                        print("3. 确认 API Key 没有多余的空格或换行")
                    
                    elif 'quota' in error_msg.lower() or 'exhausted' in error_msg.lower():
                        print()
                        print("💡 解决方案：")
                        print("1. 免费版配额已用完，等待重置（每天重置）")
                        print("2. 查看配额：https://ai.google.dev/pricing")
                        print("3. 考虑升级到付费版本")
            except:
                pass
            
            return False
            
    except requests.exceptions.Timeout:
        print("❌ 请求超时")
        print("可能原因：网络连接慢或 API 服务响应慢")
        return False
        
    except requests.exceptions.ConnectionError as e:
        print("❌ 连接错误")
        print(f"错误详情: {e}")
        print()
        print("可能原因：")
        print("1. 无法访问 Google 服务（需要科学上网）")
        print("2. 网络连接问题")
        print("3. 防火墙阻止")
        return False
        
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_network():
    """测试网络连接"""
    print("3️⃣ 测试网络连接...")
    
    try:
        response = requests.get("https://www.google.com", timeout=10)
        if response.status_code == 200:
            print("✅ 可以访问 Google 服务")
            return True
        else:
            print("⚠️ Google 服务访问异常")
            return False
    except:
        print("❌ 无法访问 Google 服务")
        print("提示：可能需要配置代理或科学上网")
        return False


if __name__ == "__main__":
    print()
    
    # 测试网络
    network_ok = test_network()
    print()
    
    # 测试 API
    api_ok = test_gemini_api()
    
    print()
    print("="*60)
    print("测试总结")
    print("="*60)
    print(f"网络连接: {'✅ 正常' if network_ok else '❌ 异常'}")
    print(f"API 连接: {'✅ 正常' if api_ok else '❌ 异常'}")
    print()
    
    if api_ok:
        print("🎉 恭喜！Gemini API 配置正确，可以正常使用。")
        print()
        print("下一步：")
        print("1. 运行 python main.py 生成报告")
        print("2. 或在 GitHub Actions 中配置 GEMINI_API_KEY Secret")
    else:
        print("⚠️ Gemini API 配置有问题，请根据上述提示解决。")
        print()
        print("常见问题排查：")
        print("1. 确认 .env 文件中有 GEMINI_API_KEY=your_key")
        print("2. 确认 API Key 有效（访问 https://makersuite.google.com/app/apikey）")
        print("3. 确认网络可以访问 Google 服务")
        print("4. 查看详细错误信息")
    
    print()
    sys.exit(0 if api_ok else 1)
