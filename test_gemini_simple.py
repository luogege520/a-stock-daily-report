#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版 Gemini API 测试脚本（不依赖 dotenv）
"""

import os
import sys
import requests

def test_gemini_api():
    """测试 Gemini API 连接"""
    
    print("="*60)
    print("Gemini API 连接测试")
    print("="*60)
    print()
    
    # 1. 检查环境变量
    print("1️⃣ 检查 API Key...")
    
    # 尝试从环境变量读取
    api_key = os.getenv('GEMINI_API_KEY')
    
    # 如果环境变量没有，尝试从 .env 文件读取
    if not api_key:
        try:
            with open('.env', 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('GEMINI_API_KEY='):
                        api_key = line.split('=', 1)[1].strip()
                        break
        except FileNotFoundError:
            pass
    
    # 如果还是没有，提示用户输入
    if not api_key or api_key == '请在这里填入您的Gemini_API_密钥' or api_key == 'your_gemini_api_key_here':
        print("❌ 未找到有效的 GEMINI_API_KEY")
        print()
        print("请输入您的 Gemini API 密钥：")
        print("（从 https://makersuite.google.com/app/apikey 获取）")
        print()
        api_key = input("API Key: ").strip()
        
        if not api_key:
            print("❌ API Key 不能为空")
            return False
        
        # 保存到 .env 文件
        save_choice = input("\n是否保存到 .env 文件？(Y/N): ").strip().upper()
        if save_choice == 'Y':
            try:
                # 读取现有内容
                env_content = []
                try:
                    with open('.env', 'r', encoding='utf-8') as f:
                        env_content = f.readlines()
                except FileNotFoundError:
                    pass
                
                # 更新或添加 GEMINI_API_KEY
                found = False
                for i, line in enumerate(env_content):
                    if line.strip().startswith('GEMINI_API_KEY='):
                        env_content[i] = f'GEMINI_API_KEY={api_key}\n'
                        found = True
                        break
                
                if not found:
                    if env_content and not env_content[-1].endswith('\n'):
                        env_content.append('\n')
                    env_content.append(f'GEMINI_API_KEY={api_key}\n')
                
                # 写入文件
                with open('.env', 'w', encoding='utf-8') as f:
                    f.writelines(env_content)
                
                print("✅ 已保存到 .env 文件")
            except Exception as e:
                print(f"⚠️ 保存失败: {e}")
    
    print(f"✅ API Key: {api_key[:20]}...{api_key[-10:]}")
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
                        "text": "请用中文回复：你好，这是一个测试。请简短回复。"
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
            print()
            
            # 解析错误信息
            try:
                error_data = response.json()
                print("完整响应：", error_data)
                print()
                
                if 'error' in error_data:
                    error_msg = error_data['error'].get('message', '未知错误')
                    print(f"错误信息: {error_msg}")
                    
                    # 常见错误提示
                    if 'API key not valid' in error_msg:
                        print()
                        print("💡 解决方案：")
                        print("1. 检查 API Key 是否完整复制（包含 AIza 开头）")
                        print("2. 访问 https://makersuite.google.com/app/apikey 重新生成")
                        print("3. 确认 API Key 没有多余的空格或换行")
                    
                    elif 'quota' in error_msg.lower() or 'exhausted' in error_msg.lower():
                        print()
                        print("💡 解决方案：")
                        print("1. 免费版配额已用完，等待重置（每天重置）")
                        print("2. 查看配额：https://ai.google.dev/pricing")
                        print("3. 考虑升级到付费版本")
            except:
                print("响应内容：", response.text)
            
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
        print("1. 无法访问 Google 服务（可能需要科学上网）")
        print("2. 网络连接问题")
        print("3. 防火墙阻止")
        return False
        
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print()
    
    # 测试 API
    api_ok = test_gemini_api()
    
    print()
    print("="*60)
    print("测试总结")
    print("="*60)
    print(f"API 连接: {'✅ 正常' if api_ok else '❌ 异常'}")
    print()
    
    if api_ok:
        print("🎉 恭喜！Gemini API 配置正确，可以正常使用。")
        print()
        print("下一步：")
        print("1. 运行：python main.py 生成报告")
        print("2. 或在 GitHub Actions 中配置 GEMINI_API_KEY Secret")
    else:
        print("⚠️ Gemini API 配置有问题，请根据上述提示解决。")
        print()
        print("获取 API Key：https://makersuite.google.com/app/apikey")
    
    print()
    input("按回车键退出...")
    sys.exit(0 if api_ok else 1)
