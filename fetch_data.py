#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股数据获取模块 - 使用 AkShare
从 AkShare 获取真实、准确的市场数据
"""

import os
from datetime import datetime
from typing import Dict, List, Optional
import json


class AStockDataFetcher:
    """A股数据获取器 - 基于 AkShare"""
    
    def __init__(self):
        """初始化数据获取器"""
        self.check_akshare()
    
    def check_akshare(self):
        """检查并导入 AkShare"""
        try:
            import akshare as ak
            self.ak = ak
            print("AkShare loaded successfully")
        except ImportError:
            print("AkShare not installed. Installing...")
            import subprocess
            import sys
            subprocess.check_call([sys.executable, "-m", "pip", "install", "akshare", "-i", "https://pypi.tuna.tsinghua.edu.cn/simple"])
            import akshare as ak
            self.ak = ak
            print("AkShare installed successfully")
    
    def fetch_index_data(self) -> Dict:
        """获取主要指数数据"""
        print("\nFetching index data...")
        
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
                    print(f"  {name}: {indices[name]['收盘点位']:.2f} ({indices[name]['涨跌幅']:+.2f}%)")
            
            if indices:
                print(f"Successfully fetched {len(indices)} indices")
                return indices
            else:
                print("No index data fetched")
                return {}
                
        except Exception as e:
            print(f"Error fetching index data: {e}")
            return {}
    
    def fetch_market_stats(self) -> Dict:
        """获取市场统计数据"""
        print("\nFetching market statistics...")
        
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
            
            print(f"  Up: {up_count} | Down: {down_count} | Flat: {flat_count}")
            print(f"  Limit up: {limit_up} | Limit down: {limit_down}")
            print("Market statistics fetched successfully")
            
            return stats
            
        except Exception as e:
            print(f"Error fetching market stats: {e}")
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
        print("\nFetching sector data...")
        
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
            
            print(f"  Top gainer: {top_gainers[0]['板块名称']} ({top_gainers[0]['涨跌幅']:+.2f}%)")
            print(f"  Top loser: {top_losers[0]['板块名称']} ({top_losers[0]['涨跌幅']:+.2f}%)")
            print("Sector data fetched successfully")
            
            return {
                '领涨板块': top_gainers,
                '领跌板块': top_losers,
            }
            
        except Exception as e:
            print(f"Error fetching sector data: {e}")
            return {
                '领涨板块': [],
                '领跌板块': [],
            }
    
    def fetch_capital_flow(self) -> Dict:
        """获取资金流向数据"""
        print("\nFetching capital flow data...")
        
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
            
            print(f"  Top inflow: {top_inflow[0]['股票名称']} ({top_inflow[0]['净流入']:.2f}B)")
            print(f"  Top outflow: {top_outflow[0]['股票名称']} ({top_outflow[0]['净流出']:.2f}B)")
            print("Capital flow data fetched successfully")
            
            return {
                '净流入TOP10': top_inflow,
                '净流出TOP10': top_outflow,
            }
            
        except Exception as e:
            print(f"Error fetching capital flow: {e}")
            return {
                '净流入TOP10': [],
                '净流出TOP10': [],
            }
    
    def fetch_north_bound_flow(self) -> Dict:
        """获取北向资金流向"""
        print("\nFetching north-bound capital flow...")
        
        try:
            df = self.ak.stock_em_hsgt_north_net_flow_in(indicator="沪股通")
            latest = df.iloc[-1]
            hgt_flow = float(latest['当日资金流入'])
            
            df = self.ak.stock_em_hsgt_north_net_flow_in(indicator="深股通")
            latest = df.iloc[-1]
            sgt_flow = float(latest['当日资金流入'])
            
            total_flow = hgt_flow + sgt_flow
            
            print(f"  Shanghai-HK Connect: {hgt_flow:.2f}B")
            print(f"  Shenzhen-HK Connect: {sgt_flow:.2f}B")
            print(f"  Total: {total_flow:.2f}B")
            print("North-bound capital flow fetched successfully")
            
            return {
                '沪股通': hgt_flow,
                '深股通': sgt_flow,
                '合计': total_flow,
            }
            
        except Exception as e:
            print(f"Error fetching north-bound flow: {e}")
            return {
                '沪股通': 0,
                '深股通': 0,
                '合计': 0,
            }
    
    def fetch_all_data(self) -> Dict:
        """获取所有市场数据"""
        print("\n" + "="*60)
        print("Fetching A-Share market data (AkShare)")
        print("="*60)
        
        indices = self.fetch_index_data()
        stats = self.fetch_market_stats()
        sectors = self.fetch_sector_data()
        capital = self.fetch_capital_flow()
        north_bound = self.fetch_north_bound_flow()
        
        market_data = {
            '获取时间': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            '数据来源': 'AkShare (East Money)',
            '指数数据': indices,
            '市场统计': stats,
            '板块数据': sectors,
            '资金流向': capital,
            '北向资金': north_bound,
        }
        
        print("\n" + "="*60)
        print("Data fetching completed")
        print("="*60 + "\n")
        
        return market_data
    
    def format_data_for_prompt(self, market_data: Dict) -> str:
        """将市场数据格式化为提示词"""
        lines = []
        lines.append("## Real Market Data (from AkShare)")
        lines.append(f"**Data Time**: {market_data['获取时间']}")
        lines.append(f"**Data Source**: {market_data['数据来源']}")
        lines.append("")
        
        lines.append("### Index Performance")
        indices = market_data['指数数据']
        for name, data in indices.items():
            lines.append(f"**{name}**:")
            lines.append(f"- Close: {data['收盘点位']:.2f}")
            lines.append(f"- Change: {data['涨跌幅']:+.2f}%")
            lines.append(f"- Change Points: {data['涨跌点']:+.2f}")
            lines.append(f"- Volume: {data['成交额']:.2f}B CNY")
            lines.append(f"- High: {data['最高']:.2f} | Low: {data['最低']:.2f}")
            lines.append("")
        
        lines.append("### Market Statistics")
        stats = market_data['市场统计']
        lines.append(f"- Up: {stats['上涨家数']}")
        lines.append(f"- Down: {stats['下跌家数']}")
        lines.append(f"- Flat: {stats['平盘家数']}")
        lines.append(f"- Up/Down Ratio: {stats['涨跌比']}")
        lines.append(f"- Limit Up: {stats['涨停家数']}")
        lines.append(f"- Limit Down: {stats['跌停家数']}")
        lines.append("")
        
        lines.append("### Sector Performance")
        sectors = market_data['板块数据']
        
        lines.append("**Top 5 Gainers**:")
        for i, sector in enumerate(sectors['领涨板块'][:5], 1):
            lines.append(f"{i}. {sector['板块名称']}: {sector['涨跌幅']:+.2f}% (Leader: {sector['领涨股票']})")
        lines.append("")
        
        lines.append("**Top 5 Losers**:")
        for i, sector in enumerate(sectors['领跌板块'][:5], 1):
            lines.append(f"{i}. {sector['板块名称']}: {sector['涨跌幅']:+.2f}%")
        lines.append("")
        
        lines.append("### Capital Flow")
        capital = market_data['资金流向']
        
        lines.append("**Top 5 Inflow**:")
        for i, stock in enumerate(capital['净流入TOP10'][:5], 1):
            lines.append(f"{i}. {stock['股票名称']}: {stock['净流入']:.2f}B ({stock['涨跌幅']:+.2f}%)")
        lines.append("")
        
        lines.append("**Top 5 Outflow**:")
        for i, stock in enumerate(capital['净流出TOP10'][:5], 1):
            lines.append(f"{i}. {stock['股票名称']}: {stock['净流出']:.2f}B ({stock['涨跌幅']:+.2f}%)")
        lines.append("")
        
        lines.append("### North-bound Capital")
        north = market_data['北向资金']
        lines.append(f"- Shanghai-HK Connect: {north['沪股通']:.2f}B")
        lines.append(f"- Shenzhen-HK Connect: {north['深股通']:.2f}B")
        lines.append(f"- **Total**: {north['合计']:.2f}B")
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
    print("\nData saved to market_data.json")


if __name__ == "__main__":
    main()
