#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股晚间复盘报告生成器 - AkShare 版本
"""

import os
import sys
from datetime import datetime
from typing import Dict, Optional
from fetch_data import AStockDataFetcher


class AStockReportGenerator:
    """A股复盘报告生成器"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('STEPFUN_API_KEY')
        if not self.api_key:
            raise ValueError("Please set STEPFUN_API_KEY environment variable")
        self.data_fetcher = AStockDataFetcher()
    
    def generate_report(self, date_str: Optional[str] = None) -> str:
        if date_str is None:
            date_str = datetime.now().strftime("%Y-%m-%d")
        
        print(f"\nGenerating A-Share report for {date_str}...")
        print("="*60)
        
        print("\nStep 1/3: Fetching market data (AkShare)")
        market_data = self.data_fetcher.fetch_all_data()
        
        if not market_data.get('指数数据'):
            print("Warning: No index data fetched")
        
        print("\nStep 2/3: Building prompt")
        prompt = self._build_prompt_with_data(date_str, market_data)
        
        print("\nStep 3/3: Generating report")
        report_content = self._call_ai_api(prompt)
        
        print("\n" + "="*60)
        print("Report generation completed")
        print("="*60 + "\n")
        
        return report_content
    
    def _build_prompt_with_data(self, date_str: str, market_data: Dict) -> str:
        year, month, day = date_str.split('-')
        real_data = self.data_fetcher.format_data_for_prompt(market_data)
        
        prompt = f"""Please generate an A-Share evening review report for [{year}-{month}-{day}] based on the following **real market data**.

{real_data}

**Important Instructions**:
1. You MUST use the above real data as the foundation of the report
2. Index points, changes, and volumes MUST match the real data exactly
3. Up/down counts MUST match the real data exactly
4. Sector and capital flow data MUST be based on real data
5. DO NOT fabricate or modify any numerical data
6. You may provide reasonable market analysis and investment advice based on the data

## Report Requirements

### Report Structure (Markdown format)

#### 1. Market Overview
- Index performance (use real data, accurate to 2 decimal places)
- Market characteristics (based on real up/down counts, volume)
- Overseas market performance (brief mention)

#### 2. Sector Analysis
- Top 10 gaining sectors (use real data)
- Top 5 losing sectors (use real data)
- Analysis of sector drivers

#### 3. Capital Flow Analysis
- Top 10 main capital inflow/outflow (use real data)
- North-bound capital flow (use real data)
- Capital flow characteristics

#### 4. Hot Topics Analysis
- Based on leading sectors and capital flow, analyze 3-5 core themes
- Each theme includes: catalyst, industry logic, representative stocks

#### 5. Technical Analysis
- Shanghai Composite: technical analysis based on real price ({market_data['指数数据'].get('上证指数', {}).get('收盘点位', 0):.2f})
- ChiNext: technical analysis based on real price ({market_data['指数数据'].get('创业板指', {}).get('收盘点位', 0):.2f})
- Support/resistance levels, trend judgment

#### 6. Investment Strategy
- Short-term strategy (1-2 weeks)
- Medium-term strategy (1-3 months)
- Reasonable suggestions based on market performance

#### 7. Risk Warning
- Five risk dimensions

#### 8. Summary and Outlook
- Daily market characteristics
- Market outlook

### Format Requirements

1. **Data Accuracy**:
   - All values must match the provided real data exactly
   - Keep 2 decimal places for points
   - Keep 2 decimal places for changes, with +/- sign
   - Keep 2 decimal places for volume

2. **Table Format**:
   - Use Markdown tables
   - Clear data alignment

3. **Symbol Usage**:
   - 🔥 Hot topics
   - 📊 Data analysis
   - 💰 Capital flow
   - ✅ Positive factors
   - ⚠️ Risk warning

4. **Language Style**:
   - Professional, objective, concise
   - Based on data analysis, avoid subjective speculation

### Data Source Attribution

Must note at the end of the report:

```markdown
---

## Data Source

- **Data Time**: {market_data['获取时间']}
- **Data Source**: {market_data['数据来源']}
- **Data Accuracy**: ✅ Real market data

## Disclaimer

This report is generated based on public market data and is for reference only. 
It does not constitute any investment advice.
Investment involves risks. Please be cautious.

---

**Report Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Version**: v2.0.0 (AkShare)
```

Please generate the report strictly according to the above requirements, **ensuring the accuracy of all numerical data**."""
        
        return prompt
    
    def _call_ai_api(self, prompt: str) -> str:
        print("Calling StepFun AI to generate report...")
        
        try:
            import requests
            
            url = "https://api.stepfun.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "step-1-flash",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a professional A-share market analyst. You must strictly base your analysis on the provided real data and cannot fabricate or modify any values. Your analysis should be objective and professional, providing reasonable market interpretation and investment advice based on the data."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.3,
                "max_tokens": 16000
            }
            
            print("  Waiting for AI response...")
            response = requests.post(url, json=payload, headers=headers, timeout=300)
            response.raise_for_status()
            
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            print("  AI report generated successfully")
            return content
            
        except Exception as e:
            print(f"  AI generation failed: {e}")
            print("  Returning basic data report")
            return self._generate_fallback_report(prompt)
    
    def _generate_fallback_report(self, prompt: str) -> str:
        return f"""# A-Share Evening Review Report

## Notice

AI service is temporarily unavailable. Below is the basic data report.

{prompt}

---

**Note**: Please check STEPFUN_API_KEY configuration or try again later.
"""
    
    def save_report(self, content: str, output_dir: str = "reports") -> str:
        os.makedirs(output_dir, exist_ok=True)
        
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"A股晚间复盘报告_{date_str}.md"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Report saved to: {filepath}")
        return filepath


def main():
    try:
        print("\n" + "="*60)
        print("A-Share Evening Review Report System v2.0.0 (AkShare)")
        print("="*60 + "\n")
        
        generator = AStockReportGenerator()
        report_content = generator.generate_report()
        filepath = generator.save_report(report_content)
        
        print(f"\nReport generation completed!")
        print(f"File path: {filepath}")
        print("\n" + "="*60)
        
        return filepath
        
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
