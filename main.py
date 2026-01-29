#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主程序：生成报告并发送邮件 - AkShare 版本
"""

import os
import sys
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from generate_report import AStockReportGenerator
from send_email import EmailSender

# 加载 .env 文件（本地运行时使用，GitHub Actions 会直接使用 Secrets）
load_dotenv()


def main():
    # 使用北京时间
    beijing_tz = timezone(timedelta(hours=8))
    beijing_time = datetime.now(beijing_tz).strftime('%Y-%m-%d %H:%M:%S')
    
    print("=" * 60)
    print("A股晚间复盘报告系统 v2.0.0 (AkShare)")
    print("=" * 60)
    print(f"运行时间: {beijing_time} (北京时间)")
    print()
    
    try:
        print("步骤 1/2: 生成报告")
        print("-" * 60)
        generator = AStockReportGenerator()
        report_content = generator.generate_report()
        report_filepath = generator.save_report(report_content)
        print()
        
        print("步骤 2/2: 发送邮件")
        print("-" * 60)
        
        recipient_email = os.getenv('RECIPIENT_EMAIL')
        if not recipient_email:
            print("⚠️  未设置 RECIPIENT_EMAIL，跳过邮件发送")
            print("💡 提示: 设置 RECIPIENT_EMAIL 以启用邮件发送")
        else:
            try:
                sender = EmailSender()
                success = sender.send_report(recipient_email, report_filepath)
                
                if not success:
                    print("⚠️  邮件发送失败，但报告已生成")
            except Exception as e:
                print(f"⚠️  邮件错误: {e}")
                print("💡 报告已生成，请手动查看")
        
        print()
        print("=" * 60)
        print("✅ 任务完成！")
        print(f"📄 报告文件: {report_filepath}")
        print("=" * 60)
        
        return 0
        
    except Exception as e:
        print()
        print("=" * 60)
        print(f"❌ 错误: {e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
