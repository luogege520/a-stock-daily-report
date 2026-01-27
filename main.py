#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主程序：生成报告并发送邮件
"""

import os
import sys
from datetime import datetime
from generate_report import AStockReportGenerator
from send_email import EmailSender


def main():
    """主函数"""
    print("=" * 60)
    print("🚀 A股晚间复盘报告自动生成系统")
    print("=" * 60)
    print(f"⏰ 运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # 1. 生成报告
        print("📊 步骤 1/2: 生成复盘报告")
        print("-" * 60)
        generator = AStockReportGenerator()
        report_content = generator.generate_report()
        report_filepath = generator.save_report(report_content)
        print()
        
        # 2. 发送邮件
        print("📧 步骤 2/2: 发送邮件")
        print("-" * 60)
        
        # 从环境变量获取收件人邮箱
        recipient_email = os.getenv('RECIPIENT_EMAIL')
        if not recipient_email:
            print("⚠️  未设置 RECIPIENT_EMAIL 环境变量，跳过邮件发送")
            print("💡 提示: 设置 RECIPIENT_EMAIL 环境变量以启用邮件发送功能")
        else:
            sender = EmailSender()
            success = sender.send_report(recipient_email, report_filepath)
            
            if not success:
                print("⚠️  邮件发送失败，但报告已生成")
        
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
