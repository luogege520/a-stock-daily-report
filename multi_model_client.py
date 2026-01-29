#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多模型 AI 客户端 - 支持 Gemini、StepFun、DeepSeek
"""

import os
import requests
from typing import Optional, Dict


class AIModelClient:
    """AI 模型客户端基类"""
    
    def __init__(self, api_key: str, model_name: str):
        self.api_key = api_key
        self.model_name = model_name
    
    def generate(self, prompt: str, system_instruction: str = "") -> str:
        """生成内容"""
        raise NotImplementedError


class GeminiClient(AIModelClient):
    """Google Gemini 客户端"""
    
    def __init__(self, api_key: str, model_name: str = "gemini-2.5-pro"):
        super().__init__(api_key, model_name)
        self.base_url = "https://generativelanguage.googleapis.com/v1"
    
    def generate(self, prompt: str, system_instruction: str = "") -> str:
        """调用 Gemini API"""
        print(f"[INFO] 使用 Gemini 模型: {self.model_name}")
        
        url = f"{self.base_url}/models/{self.model_name}:generateContent?key={self.api_key}"
        
        full_prompt = f"{system_instruction}\n\n{prompt}" if system_instruction else prompt
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": full_prompt
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.3,
                "maxOutputTokens": 8192,
                "topP": 0.95,
                "topK": 40
            }
        }
        
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(url, json=payload, headers=headers, timeout=300)
        response.raise_for_status()
        
        result = response.json()
        
        if 'candidates' in result and len(result['candidates']) > 0:
            content = result['candidates'][0]['content']['parts'][0]['text']
            print(f"[INFO] ✅ Gemini 生成成功 (长度: {len(content)} 字符)")
            return content
        else:
            raise Exception("Gemini API 返回格式异常")


class StepFunClient(AIModelClient):
    """StepFun 客户端"""
    
    def __init__(self, api_key: str, model_name: str = "step-2-16k"):
        super().__init__(api_key, model_name)
        self.base_url = "https://api.stepfun.com/v1"
    
    def generate(self, prompt: str, system_instruction: str = "") -> str:
        """调用 StepFun API"""
        print(f"[INFO] 使用 StepFun 模型: {self.model_name}")
        
        url = f"{self.base_url}/chat/completions"
        
        messages = []
        if system_instruction:
            messages.append({
                "role": "system",
                "content": system_instruction
            })
        messages.append({
            "role": "user",
            "content": prompt
        })
        
        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": 0.3,
            "max_tokens": 16000
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=300)
        response.raise_for_status()
        
        result = response.json()
        content = result['choices'][0]['message']['content']
        
        print(f"[INFO] ✅ StepFun 生成成功 (长度: {len(content)} 字符)")
        return content


class DeepSeekClient(AIModelClient):
    """DeepSeek 客户端"""
    
    def __init__(self, api_key: str, model_name: str = "deepseek-chat"):
        super().__init__(api_key, model_name)
        self.base_url = "https://api.deepseek.com/v1"
    
    def generate(self, prompt: str, system_instruction: str = "") -> str:
        """调用 DeepSeek API"""
        print(f"[INFO] 使用 DeepSeek 模型: {self.model_name}")
        
        url = f"{self.base_url}/chat/completions"
        
        messages = []
        if system_instruction:
            messages.append({
                "role": "system",
                "content": system_instruction
            })
        messages.append({
            "role": "user",
            "content": prompt
        })
        
        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": 0.3,
            "max_tokens": 8000
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=300)
        response.raise_for_status()
        
        result = response.json()
        content = result['choices'][0]['message']['content']
        
        print(f"[INFO] ✅ DeepSeek 生成成功 (长度: {len(content)} 字符)")
        return content


class MultiModelManager:
    """多模型管理器 - 支持模型轮换和故障转移"""
    
    def __init__(self):
        self.clients = []
        self._init_clients()
    
    def _init_clients(self):
        """初始化所有可用的客户端"""
        print("[INFO] 初始化 AI 模型客户端...")
        
        # 1. Gemini
        gemini_key = os.getenv('GEMINI_API_KEY')
        if gemini_key:
            try:
                client = GeminiClient(gemini_key)
                self.clients.append(('Gemini', client))
                print("[INFO] ✅ Gemini 客户端已加载")
            except Exception as e:
                print(f"[WARN] ⚠️ Gemini 客户端加载失败: {e}")
        
        # 2. StepFun
        stepfun_key = os.getenv('STEPFUN_API_KEY')
        if stepfun_key:
            try:
                client = StepFunClient(stepfun_key)
                self.clients.append(('StepFun', client))
                print("[INFO] ✅ StepFun 客户端已加载")
            except Exception as e:
                print(f"[WARN] ⚠️ StepFun 客户端加载失败: {e}")
        
        # 3. DeepSeek
        deepseek_key = os.getenv('DEEPSEEK_API_KEY')
        if deepseek_key:
            try:
                client = DeepSeekClient(deepseek_key)
                self.clients.append(('DeepSeek', client))
                print("[INFO] ✅ DeepSeek 客户端已加载")
            except Exception as e:
                print(f"[WARN] ⚠️ DeepSeek 客户端加载失败: {e}")
        
        if not self.clients:
            raise ValueError("没有可用的 AI 模型客户端，请至少配置一个 API Key")
        
        print(f"[INFO] 共加载 {len(self.clients)} 个模型客户端")
    
    def generate(self, prompt: str, system_instruction: str = "", preferred_model: Optional[str] = None) -> tuple:
        """
        生成内容，支持模型选择和故障转移
        
        Args:
            prompt: 用户提示词
            system_instruction: 系统指令
            preferred_model: 首选模型名称 (Gemini/StepFun/DeepSeek)
        
        Returns:
            (content, model_name): 生成的内容和使用的模型名称
        """
        print("=" * 80)
        print("开始调用 AI 模型生成报告")
        print("=" * 80)
        
        # 如果指定了首选模型，先尝试使用
        if preferred_model:
            for name, client in self.clients:
                if name.lower() == preferred_model.lower():
                    try:
                        print(f"[INFO] 尝试使用首选模型: {name}")
                        content = client.generate(prompt, system_instruction)
                        return content, name
                    except Exception as e:
                        print(f"[ERROR] {name} 调用失败: {e}")
                        print(f"[INFO] 尝试切换到备用模型...")
        
        # 依次尝试所有可用的客户端
        for name, client in self.clients:
            try:
                print(f"[INFO] 尝试使用模型: {name}")
                content = client.generate(prompt, system_instruction)
                return content, name
            except requests.exceptions.HTTPError as e:
                print(f"[ERROR] {name} HTTP 错误: {e}")
                if hasattr(e.response, 'text'):
                    print(f"[ERROR] 响应内容: {e.response.text}")
                print(f"[INFO] 切换到下一个模型...")
            except Exception as e:
                print(f"[ERROR] {name} 调用失败: {e}")
                print(f"[INFO] 切换到下一个模型...")
        
        # 所有模型都失败
        raise Exception("所有 AI 模型都调用失败，请检查 API Key 配置和网络连接")


def test_multi_model():
    """测试多模型功能"""
    print("\n" + "=" * 80)
    print("多模型 AI 客户端测试")
    print("=" * 80 + "\n")
    
    try:
        manager = MultiModelManager()
        
        prompt = "请用中文简单回复：你好，这是一个测试。"
        system_instruction = "你是一个友好的助手。"
        
        content, model_name = manager.generate(prompt, system_instruction)
        
        print("\n" + "=" * 80)
        print("测试结果")
        print("=" * 80)
        print(f"✅ 使用模型: {model_name}")
        print(f"✅ 生成内容:\n{content}")
        print("=" * 80 + "\n")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}\n")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_multi_model()
