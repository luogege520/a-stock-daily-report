#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股数据获取模块 - 使用 AkShare
"""

import os
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional
import json


class AStockDataFetcher:
    """A股数据获取器"""
    
    def __init__(self):
        """初始化数据获取器"""
        self.check_akshare()
    
    def check_akshare(self):
        """检查并导入 AkShare"""
        try:
            import akshare as ak
            self.ak = ak
            print("✅ AkShare 已加载")
        except ImportError:
            print("❌ 未安装 AkShare，正在安装...")
            import subprocess
            import sys
            subprocess.check_call([sys.executable, "-m", "pip", "install", "akshare", "-i", "https://pypi.tuna.tsinghua.edu.cn/simple"])
            import akshare as ak
            self.ak = ak
            print("✅ AkShare 安装成功")
    
    def fetch_index_data(self) -> Dict:
        """获取主要指数数据"""
        print("\n📊 正在获取指数数据...")
        
        try:
            df = self.ak.stock_zh_index_spot_em()
            
            index_codes = {
                '上证指数': '000001',
                '深证成指': '399001',
                '创业板指': '399006',
                '科创50': '000688',
                '北证50': '899050'
            }
            
            indices = {}
            
            for name, code in index_codes.items():
                row = df[df['代码'] == code]
                
                if not row.empty:
                    row = row.iloc[0]
                    indices[name] = {
                        '收盘点位': float(row['最新价']),
                        '涨跌幅': float(row['涨跌幅']),
                        '涨跌点': float(row['涨跌额']),
                        '成交额': float(row['成交额']) / 100000000,
                        '成交量': float(row['成交量']),
                        '昨收': float(row['昨收']),
                        '今开': float(row['今开']),
                        '最高': float(row['最高']),
                        '最低': float(row['最低']),
                    }
                    print(f"  ✅ {name}: {indices[name]['收盘点位']:.2f} ({indices[name]['涨跌幅']:+.2f}%)")
            
            if indices:
                print(f"✅ 成功获取 {len(indices)} 个指数数据")
                return indices
            else:
                print("❌ 未获取到任何指数数据")
                return {}
                
        except Exception as e:
            print(f"❌ 获取指数数据失败: {e}")
            return {}
    
    def fetch_market_stats(self) -> Dict:
        """获取市场统计数据"""
        print("\n📈 正在获取市场统计数据...")
        
        try:
            df = self.ak.stock_zh_a_spot_em()
            
            up_count = len(df[df['涨跌幅'] > 0])
            down_count = len(df[df['涨跌幅'] < 0])
            flat_count = len(df[df['涨跌幅'] == 0])
            total = len(df)
            
            limit_up = len(df[df['涨跌幅'] >= 9.9])
            limit_down = len(df[df['涨跌幅'] <= -9.9])
            
            stats = {
                '上涨家数': up_count,
                '下跌家数': down_count,
                '平盘家数': flat_count,
                '总家数': total,
                '涨跌比': f"{up_count}/{down_count}",
                '涨停家数': limit_up,
                '跌停家数': limit_down,
            }
            
            print(f"  ✅ 上涨: {up_count} | 下跌: {down_count} | 平盘: {flat_count}")
            print(f"  ✅ 涨停: {limit_up} | 跌停: {limit_down}")
            print(f"✅ 市场统计数据获取成功")
            
            return stats
            
        except Exception as e:
            print(f"❌ 获取市场统计失败: {e}")
            return {
                '上涨家数': 0,
                '下跌家数': 0,
                '平盘家数': 0,
                '总家数': 0,
                '涨跌比': '0/0',
                '涨停家数': 0,
                '跌停家数': 0,
            }
    
    def fetch_sector_data(self) -> Dict:
        """获取板块数据"""
        print("\n📊 正在获取板块数据...")
        
        try:
            df = self.ak.stock_board_industry_name_em()
            df_sorted = df.sort_values('涨跌幅', ascending=False)
            
            top_gainers = []
            for idx, row in df_sorted.head(10).iterrows():
                top_gainers.append({
                    '板块名称': row['板块名称'],
                    '涨跌幅': float(row['涨跌幅']),
                    '领涨股票': row['领涨股票'],
                })
            
            top_losers = []
            for idx, row in df_sorted.tail(5).iterrows():
                top_losers.append({
                    '板块名称': row['板块名称'],
                    '涨跌幅': float(row['涨跌幅']),
                    '领跌股票': row['领涨股票'],
                })
            
            if top_gainers and top_losers:
                print(f"  ✅ 领涨板块: {top_gainers[0]['板块名称']} ({top_gainers[0]['涨跌幅']:+.2f}%)")
                print(f"  ✅ 领跌板块: {top_losers[0]['板块名称']} ({top_losers[0]['涨跌幅']:+.2f}%)")
                print(f"✅ 板块数据获取成功")
            
            return {
                '领涨板块': top_gainers,
                '领跌板块': top_losers,
            }
            
        except Exception as e:
            print(f"❌ 获取板块数据失败: {e}")
            return {
                '领涨板块': [],
                '领跌板块': [],
            }
    
    def fetch_capital_flow(self) -> Dict:
        """获取资金流向数据"""
        print("\n💰 正在获取资金流向数据...")
        
        try:
            df = self.ak.stock_individual_fund_flow_rank(indicator="今日")
            
            top_inflow = []
            for idx, row in df.head(10).iterrows():
                top_inflow.append({
                    '股票名称': row['名称'],
                    '股票代码': row['代码'],
                    '净流入': float(row['主力净流入-净额']) / 100000000,
                    '涨跌幅': float(row['涨跌幅']),
                })
            
            df_sorted = df.sort_values('主力净流入-净额', ascending=True)
            top_outflow = []
            for idx, row in df_sorted.head(10).iterrows():
                top_outflow.append({
                    '股票名称': row['名称'],
                    '股票代码': row['代码'],
                    '净流出': float(row['主力净流入-净额']) / 100000000,
                    '涨跌幅': float(row['涨跌幅']),
                })
            
            if top_inflow and top_outflow:
                print(f"  ✅ 净流入最大: {top_inflow[0]['股票名称']} ({top_inflow[0]['净流入']:.2f}亿)")
                print(f"  ✅ 净流出最大: {top_outflow[0]['股票名称']} ({top_outflow[0]['净流出']:.2f}亿)")
                print(f"✅ 资金流向数据获取成功")
            
            return {
                '净流入TOP10': top_inflow,
                '净流出TOP10': top_outflow,
            }
            
        except Exception as e:
            print(f"❌ 获取资金流向失败: {e}")
            return {
                '净流入TOP10': [],
                '净流出TOP10': [],
            }
    
    def fetch_north_bound_flow(self) -> Dict:
        """获取北向资金流向"""
        print("\n🌏 正在获取北向资金数据...")
        
        try:
            df = self.ak.stock_em_hsgt_north_net_flow_in(indicator="沪股通")
            latest = df.iloc[-1]
            hgt_flow = float(latest['当日资金流入'])
            
            df = self.ak.stock_em_hsgt_north_net_flow_in(indicator="深股通")
            latest = df.iloc[-1]
            sgt_flow = float(latest['当日资金流入'])
            
            total_flow = hgt_flow + sgt_flow
            
            print(f"  ✅ 沪股通: {hgt_flow:.2f}亿")
            print(f"  ✅ 深股通: {sgt_flow:.2f}亿")
            print(f"  ✅ 合计: {total_flow:.2f}亿")
            print(f"✅ 北向资金数据获取成功")
            
            return {
                '沪股通': hgt_flow,
                '深股通': sgt_flow,
                '合计': total_flow,
            }
            
        except Exception as e:
            print(f"❌ 获取北向资金失败: {e}")
            return {
                '沪股通': 0,
                '深股通': 0,
                '合计': 0,
            }
    
    def fetch_all_data(self) -> Dict:
        """获取所有市场数据"""
        print("\n" + "="*60)
        print("🚀 开始获取A股市场数据（AkShare）")
        print("="*60)
        
        indices = self.fetch_index_data()
        stats = self.fetch_market_stats()
        sectors = self.fetch_sector_data()
        capital = self.fetch_capital_flow()
        north_bound = self.fetch_north_bound_flow()
        
        # 获取北京时间
        beijing_tz = timezone(timedelta(hours=8))
        beijing_time = datetime.now(beijing_tz).strftime("%Y-%m-%d %H:%M:%S")
        
        market_data = {
            '获取时间': beijing_time,
            '数据来源': 'AkShare (东方财富)',
            '指数数据': indices,
            '市场统计': stats,
            '板块数据': sectors,
            '资金流向': capital,
            '北向资金': north_bound,
        }
        
        print("\n" + "="*60)
        print("✅ 数据获取完成")
        print("="*60 + "\n")
        
        return market_data
    
    def format_data_for_prompt(self, market_data: Dict) -> str:
        """将市场数据格式化为提示词"""
        lines = []
        lines.append("## 真实市场数据（来自 AkShare）")
        lines.append(f"**数据获取时间**：{market_data['获取时间']}")
        lines.append(f"**数据来源**：{market_data['数据来源']}")
        lines.append("")
        
        lines.append("### 主要指数表现")
        indices = market_data['指数数据']
        for name, data in indices.items():
            lines.append(f"**{name}**：")
            lines.append(f"- 收盘点位：{data['收盘点位']:.2f}")
            lines.append(f"- 涨跌幅：{data['涨跌幅']:+.2f}%")
            lines.append(f"- 涨跌点：{data['涨跌点']:+.2f}")
            lines.append(f"- 成交额：{data['成交额']:.2f}亿元")
            lines.append(f"- 最高：{data['最高']:.2f} | 最低：{data['最低']:.2f}")
            lines.append("")
        
        lines.append("### 市场统计")
        stats = market_data['市场统计']
        lines.append(f"- 上涨家数：{stats['上涨家数']}")
        lines.append(f"- 下跌家数：{stats['下跌家数']}")
        lines.append(f"- 平盘家数：{stats['平盘家数']}")
        lines.append(f"- 涨跌比：{stats['涨跌比']}")
        lines.append(f"- 涨停家数：{stats['涨停家数']}")
        lines.append(f"- 跌停家数：{stats['跌停家数']}")
        lines.append("")
        
        lines.append("### 板块表现")
        sectors = market_data['板块数据']
        
        if sectors['领涨板块']:
            lines.append("**领涨板块TOP5**：")
            for i, sector in enumerate(sectors['领涨板块'][:5], 1):
                lines.append(f"{i}. {sector['板块名称']}：{sector['涨跌幅']:+.2f}% (领涨股：{sector['领涨股票']})")
            lines.append("")
        
        if sectors['领跌板块']:
            lines.append("**领跌板块TOP5**：")
            for i, sector in enumerate(sectors['领跌板块'][:5], 1):
                lines.append(f"{i}. {sector['板块名称']}：{sector['涨跌幅']:+.2f}%")
            lines.append("")
        
        lines.append("### 资金流向")
        capital = market_data['资金流向']
        
        if capital['净流入TOP10']:
            lines.append("**主力净流入TOP5**：")
            for i, stock in enumerate(capital['净流入TOP10'][:5], 1):
                lines.append(f"{i}. {stock['股票名称']}：{stock['净流入']:.2f}亿元 ({stock['涨跌幅']:+.2f}%)")
            lines.append("")
        
        if capital['净流出TOP10']:
            lines.append("**主力净流出TOP5**：")
            for i, stock in enumerate(capital['净流出TOP10'][:5], 1):
                lines.append(f"{i}. {stock['股票名称']}：{stock['净流出']:.2f}亿元 ({stock['涨跌幅']:+.2f}%)")
            lines.append("")
        
        lines.append("### 北向资金")
        north = market_data['北向资金']
        lines.append(f"- 沪股通：{north['沪股通']:.2f}亿元")
        lines.append(f"- 深股通：{north['深股通']:.2f}亿元")
        lines.append(f"- **合计**：{north['合计']:.2f}亿元")
        lines.append("")
        
        return "\n".join(lines)


def main():
    """测试数据获取"""
    fetcher = AStockDataFetcher()
    market_data = fetcher.fetch_all_data()
    formatted = fetcher.format_data_for_prompt(market_data)
    print(formatted)
    
    with open('market_data.json', 'w', encoding='utf-8') as f:
        json.dump(market_data, f, ensure_ascii=False, indent=2)
    print("\n💾 数据已保存到 market_data.json")


if __name__ == "__main__":
    main()
