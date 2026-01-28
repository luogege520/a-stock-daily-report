#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主程序：生成报告并发送邮件 - AkShare 版本
"""

import os
import sys
from datetime import datetime
from generate_report import AStockReportGenerator
from send_email import EmailSender


def main():
    print("=" * 60)
    print("A-Share Evening Review Report System v2.0.0 (AkShare)")
    print("=" * 60)
    print(f"Run time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        print("Step 1/2: Generating report")
        print("-" * 60)
        generator = AStockReportGenerator()
        report_content = generator.generate_report()
        report_filepath = generator.save_report(report_content)
        print()
        
        print("Step 2/2: Sending email")
        print("-" * 60)
        
        recipient_email = os.getenv('RECIPIENT_EMAIL')
        if not recipient_email:
            print("Warning: RECIPIENT_EMAIL not set, skipping email")
            print("Tip: Set RECIPIENT_EMAIL to enable email sending")
        else:
            try:
                sender = EmailSender()
                success = sender.send_report(recipient_email, report_filepath)
                
                if not success:
                    print("Warning: Email sending failed, but report generated")
            except Exception as e:
                print(f"Warning: Email error: {e}")
                print("Tip: Report generated, please check manually")
        
        print()
        print("=" * 60)
        print("Task completed!")
        print(f"Report file: {report_filepath}")
        print("=" * 60)
        
        return 0
        
    except Exception as e:
        print()
        print("=" * 60)
        print(f"Error: {e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
