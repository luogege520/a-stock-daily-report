#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股晚间复盘报告生成器 - 支持多模型
"""

import os
import sys
from datetime import datetime, timezone, timedelta
from typing import Dict, Optional
from fetch_data import AStockDataFetcher
from multi_model_client import MultiModelManager


class AStockReportGenerator:
    """A股复盘报告生成器"""
    
    def __init__(self, preferred_model: Optional[str] = None):
        """
        初始化报告生成器
        
        Args:
            preferred_model: 首选模型 (Gemini/StepFun/DeepSeek)，如果为 None 则自动选择
        """
        print("[INFO] 初始化 A股复盘报告生成器")
        
        self.preferred_model = preferred_model or os.getenv('PREFERRED_AI_MODEL')
        if self.preferred_model:
            print(f"[INFO] 首选模型: {self.preferred_model}")
        
        # 初始化多模型管理器
        self.ai_manager = MultiModelManager()
        
        # 初始化数据获取器
        self.data_fetcher = AStockDataFetcher()
        print("[INFO] ✅ 初始化完成")
    
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
        report_content, used_model = self._call_ai_api(prompt)
        
        print(f"\n✅ 使用模型: {used_model}")
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
- 上证指数：基于真实点位进行技术分析
- 创业板指：基于真实点位进行技术分析
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
**版本**：v2.1.0 (Multi-Model)
```

请严格按照以上要求生成**中文**报告，**确保所有数值数据的准确性**。"""
        
        return prompt
    
    def _call_ai_api(self, prompt: str) -> tuple:
        """
        调用 AI API 生成报告
        
        Returns:
            (content, model_name): 生成的内容和使用的模型名称
        """
        system_instruction = "你是一个专业的A股市场分析师。你必须严格基于提供的真实数据进行分析，不能编造或修改任何数值。你的分析应该客观、专业，基于数据给出合理的市场解读和投资建议。你必须使用中文回复。"
        
        try:
            content, model_name = self.ai_manager.generate(
                prompt=prompt,
                system_instruction=system_instruction,
                preferred_model=self.preferred_model
            )
            return content, model_name
            
        except Exception as e:
            print(f"[ERROR] 所有 AI 模型调用失败: {e}")
            import traceback
            traceback.print_exc()
            return self._generate_fallback_report(prompt), "Fallback"
    
    def _generate_fallback_report(self, prompt: str) -> str:
        """生成备用报告（当所有 AI 调用都失败时）"""
        return f"""# A股晚间复盘报告

## ⚠️ 提示

所有 AI 服务暂时不可用，以下为基础数据报告。

{prompt}

---

**注意**：请检查以下配置：

1. **Gemini API**: 检查 GEMINI_API_KEY 环境变量
2. **StepFun API**: 检查 STEPFUN_API_KEY 环境变量  
3. **DeepSeek API**: 检查 DEEPSEEK_API_KEY 环境变量

至少需要配置一个 API Key。

可能的原因：
1. API Key 未设置或错误
2. API 额度不足
3. 网络连接问题
4. API 服务暂时不可用

请检查环境变量配置。
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
        print("A股晚间复盘报告生成系统 v2.1.0 (Multi-Model)")
        print("="*60 + "\n")
        
        # 可以通过环境变量 PREFERRED_AI_MODEL 指定首选模型
        # 或者直接传参：generator = AStockReportGenerator(preferred_model="Gemini")
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
