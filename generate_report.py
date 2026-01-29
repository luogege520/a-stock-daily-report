#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股晚间复盘报告生成器 - 中文版本
"""

import os
import sys
from datetime import datetime, timezone, timedelta
from typing import Dict, Optional
from fetch_data import AStockDataFetcher


class AStockReportGenerator:
    """A股复盘报告生成器"""
    
    def __init__(self, api_key: Optional[str] = None):
        # 检查 API Key
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        
        print(f"[DEBUG] 检查 GEMINI_API_KEY 环境变量...")
        if not self.api_key:
            print(f"[ERROR] 未找到 GEMINI_API_KEY 环境变量")
            raise ValueError("请设置 GEMINI_API_KEY 环境变量")
        
        # 隐藏敏感信息
        masked_key = f"{self.api_key[:10]}...{self.api_key[-5:]}" if len(self.api_key) > 15 else "***"
        print(f"[INFO] ✅ 成功读取 API Key: {masked_key} (长度: {len(self.api_key)})")
        
        self.data_fetcher = AStockDataFetcher()
    
    def generate_report(self, date_str: Optional[str] = None) -> str:
        if date_str is None:
            # 使用北京时间
            beijing_tz = timezone(timedelta(hours=8))
            date_str = datetime.now(beijing_tz).strftime("%Y-%m-%d")
        
        print(f"\n正在生成 {date_str} 的A股复盘报告...")
        print("="*60)
        
        print("\n步骤 1/3: 获取市场数据 (AkShare)")
        market_data = self.data_fetcher.fetch_all_data()
        
        if not market_data.get('指数数据'):
            print("警告: 未获取到指数数据")
        
        print("\n步骤 2/3: 构建提示词")
        prompt = self._build_prompt_with_data(date_str, market_data)
        
        print("\n步骤 3/3: 生成报告")
        report_content = self._call_ai_api(prompt)
        
        print("\n" + "="*60)
        print("报告生成完成")
        print("="*60 + "\n")
        
        return report_content
    
    def _build_prompt_with_data(self, date_str: str, market_data: Dict) -> str:
        """构建中文提示词"""
        year, month, day = date_str.split('-')
        real_data = self.data_fetcher.format_data_for_prompt(market_data)
        
        prompt = f"""请基于以下**真实市场数据**生成一份【{year}年{month}月{day}日】A股晚间复盘报告。

{real_data}

**重要说明**：
1. ✅ **必须使用上述真实数据**作为报告的基础
2. ✅ 指数点位、涨跌幅、成交额**必须与真实数据完全一致**
3. ✅ 涨跌家数**必须与真实数据完全一致**
4. ✅ 板块涨跌、资金流向**必须基于真实数据**
5. ❌ **严禁编造或修改任何数值数据**
6. ✅ 可以基于数据进行合理的市场分析和投资建议
7. ✅ **报告必须使用中文**

## 报告要求

### 一、报告结构（Markdown格式）

#### 1. 市场概况
- 主要指数表现（**使用真实数据，精确到小数点后2位**）
- 市场特征总结（基于真实的涨跌家数、成交额）
- 外围市场表现（可简要提及）

**示例格式**：
```markdown
| 指数名称 | 收盘点位 | 涨跌幅 | 成交额(亿元) | 涨跌家数 |
|---------|---------|--------|-------------|---------|
| 上证指数 | {market_data['指数数据'].get('上证指数', {}).get('收盘点位', 0):.2f} | {market_data['指数数据'].get('上证指数', {}).get('涨跌幅', 0):+.2f}% | {market_data['指数数据'].get('上证指数', {}).get('成交额', 0):.2f} | {market_data['市场统计'].get('涨跌比', '0/0')} |
```

#### 2. 板块表现分析
- 领涨板块TOP10（使用真实数据）
- 领跌板块TOP5（使用真实数据）
- 分析板块涨跌的驱动因素

#### 3. 资金流向分析
- 主力资金净流入/流出TOP10（使用真实数据）
- 北向资金流向（使用真实数据）
- 分析资金流向特征

#### 4. 热点题材深度解析
- 基于领涨板块和资金流向，分析3-5个核心热点
- 每个热点包括：催化剂、产业逻辑、代表个股

#### 5. 技术面分析
- 上证指数：基于真实点位（{market_data['指数数据'].get('上证指数', {}).get('收盘点位', 0):.2f}）进行技术分析
- 创业板指：基于真实点位（{market_data['指数数据'].get('创业板指', {}).get('收盘点位', 0):.2f}）进行技术分析
- 支撑阻力位、趋势判断

#### 6. 投资策略建议
- 短期策略（1-2周）
- 中长期策略（1-3个月）
- 基于当日市场表现给出合理建议

#### 7. 风险提示
- 五大风险维度分析

#### 8. 总结与展望
- 当日市场特征总结
- 后市展望

### 二、格式要求

1. **数据精确性**：
   - 所有数值必须与提供的真实数据完全一致
   - 点位保留2位小数
   - 涨跌幅保留2位小数，带正负号
   - 成交额保留2位小数

2. **表格格式**：
   - 使用Markdown表格
   - 数据对齐清晰

3. **符号使用**：
   - 🔥 热点题材
   - 📊 数据分析
   - 💰 资金流向
   - ✅ 正面因素
   - ⚠️ 风险提示

4. **语言风格**：
   - **必须使用中文**
   - 专业、客观、简洁
   - 基于数据分析，避免主观臆断

### 三、数据来源标注

报告末尾必须注明：

```markdown
---

## 数据来源

- **数据获取时间**：{market_data['获取时间']}
- **数据来源**：{market_data['数据来源']}
- **数据准确性**：✅ 真实市场数据

## 免责声明

本报告基于公开市场数据生成，仅供参考，不构成任何投资建议。
投资有风险，入市需谨慎。

---

**报告生成时间**：{datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")} (北京时间)  
**版本**：v2.1.0 (Gemini)
```

请严格按照以上要求生成**中文**报告，**确保所有数值数据的准确性**。"""
        
        return prompt
    
    def _call_ai_api(self, prompt: str) -> str:
        """调用 Google Gemini API 生成报告"""
        print("正在调用 Google Gemini AI 生成报告...")
        print(f"[DEBUG] API Key 长度: {len(self.api_key)}")
        print(f"[DEBUG] API Key 前缀: {self.api_key[:10]}...")
        
        try:
            import requests
            
            url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent?key={self.api_key}"
            print(f"[DEBUG] API 端点: {url[:80]}...")
            
            headers = {
                "Content-Type": "application/json"
            }
            
            # 构建系统指令和用户提示
            system_instruction = "你是一个专业的A股市场分析师。你必须严格基于提供的真实数据进行分析，不能编造或修改任何数值。你的分析应该客观、专业，基于数据给出合理的市场解读和投资建议。你必须使用中文回复。"
            
            full_prompt = f"{system_instruction}\n\n{prompt}"
            
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
            
            print("  等待 AI 响应...")
            print(f"[DEBUG] 发送 POST 请求...")
            
            response = requests.post(url, json=payload, headers=headers, timeout=300)
            
            print(f"[DEBUG] HTTP 状态码: {response.status_code}")
            
            response.raise_for_status()
            
            result = response.json()
            
            # 解析 Gemini 响应格式
            if 'candidates' in result and len(result['candidates']) > 0:
                content = result['candidates'][0]['content']['parts'][0]['text']
                print(f"[INFO] ✅ AI 报告生成成功 (长度: {len(content)} 字符)")
                return content
            else:
                print(f"[ERROR] Gemini API 返回格式异常")
                print(f"[DEBUG] 响应内容: {result}")
                raise Exception("Gemini API 返回格式异常")
            
        except requests.exceptions.HTTPError as e:
            print(f"[ERROR] HTTP 错误: {e}")
            print(f"[ERROR] 状态码: {e.response.status_code}")
            if hasattr(e.response, 'text'):
                print(f"[ERROR] 响应内容: {e.response.text}")
            return self._generate_fallback_report(prompt)
        except Exception as e:
            print(f"[ERROR] AI 生成失败: {e}")
            import traceback
            traceback.print_exc()
            return self._generate_fallback_report(prompt)
    
    def _generate_fallback_report(self, prompt: str) -> str:
        """生成备用报告（当 AI 调用失败时）"""
        return f"""# A股晚间复盘报告

## ⚠️ 提示

AI 服务暂时不可用，以下为基础数据报告。

{prompt}

---

**注意**：请检查 GEMINI_API_KEY 配置或稍后重试。

可能的原因：
1. API Key 未设置或错误
2. API 额度不足
3. 网络连接问题
4. API 服务暂时不可用

请检查环境变量 GEMINI_API_KEY 是否正确设置。
"""
    
    def save_report(self, content: str, output_dir: str = "reports") -> str:
        """保存报告到文件"""
        os.makedirs(output_dir, exist_ok=True)
        
        # 使用北京时间
        beijing_tz = timezone(timedelta(hours=8))
        date_str = datetime.now(beijing_tz).strftime("%Y-%m-%d")
        filename = f"A股晚间复盘报告_{date_str}.md"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"报告已保存到: {filepath}")
        return filepath


def main():
    """主函数"""
    try:
        print("\n" + "="*60)
        print("A股晚间复盘报告生成系统 v2.1.0 (Gemini)")
        print("="*60 + "\n")
        
        generator = AStockReportGenerator()
        report_content = generator.generate_report()
        filepath = generator.save_report(report_content)
        
        print(f"\n报告生成完成！")
        print(f"文件路径: {filepath}")
        print("\n" + "="*60)
        
        return filepath
        
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
