#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主程序：生成报告并发送邮件 - 多模型版本
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
    
    print("=" * 80)
    print("A股晚间复盘报告系统 v2.2.0 (Multi-Model)")
    print("=" * 80)
    print(f"运行时间: {beijing_time} (北京时间)")
    print(f"支持模型: Gemini / StepFun / DeepSeek")
    print()
    
    # 检查环境变量
    print("-" * 80)
    print("检查 AI 模型配置")
    print("-" * 80)
    
    ai_keys = {
        'GEMINI_API_KEY': os.getenv('GEMINI_API_KEY'),
        'STEPFUN_API_KEY': os.getenv('STEPFUN_API_KEY'),
        'DEEPSEEK_API_KEY': os.getenv('DEEPSEEK_API_KEY'),
    }
    
    available_models = []
    for key, value in ai_keys.items():
        model_name = key.replace('_API_KEY', '')
        if value:
            masked = f"{value[:10]}...{value[-5:]}" if len(value) > 15 else "***"
            print(f"✅ {model_name}: {masked}")
            available_models.append(model_name)
        else:
            print(f"⚠️ {model_name}: 未配置")
    
    if not available_models:
        print("\n❌ 错误：未配置任何 AI 模型")
        print("请至少配置一个 API Key：")
        print("  - GEMINI_API_KEY")
        print("  - STEPFUN_API_KEY")
        print("  - DEEPSEEK_API_KEY")
        return 1
    
    print(f"\n可用模型: {', '.join(available_models)}")
    
    preferred_model = os.getenv('PREFERRED_AI_MODEL')
    if preferred_model:
        print(f"首选模型: {preferred_model}")
    
    print()
    
    try:
        print("=" * 80)
        print("步骤 1/2: 生成报告")
        print("=" * 80)
        
        generator = AStockReportGenerator()
        report_content = generator.generate_report()
        report_filepath = generator.save_report(report_content)
        
        print(f"\n✅ 报告生成完成: {report_filepath}")
        print()
        
        print("=" * 80)
        print("步骤 2/2: 发送邮件")
        print("=" * 80)
        
        recipient_email = os.getenv('RECIPIENT_EMAIL')
        if not recipient_email:
            print("⚠️  未设置 RECIPIENT_EMAIL，跳过邮件发送")
            print("💡 提示: 设置 RECIPIENT_EMAIL 以启用邮件发送")
        else:
            try:
                print(f"收件人: {recipient_email}")
                sender = EmailSender()
                success = sender.send_report(recipient_email, report_filepath)
                
                if success:
                    print("✅ 邮件发送成功")
                else:
                    print("⚠️ 邮件发送失败")
                    print("💡 报告已生成，请手动查看")
            except Exception as e:
                print(f"⚠️  邮件错误: {e}")
                print("💡 报告已生成，请手动查看")
        
        print()
        print("=" * 80)
        print("✅ 任务完成！")
        print(f"📄 报告文件: {report_filepath}")
        print("=" * 80)
        print()
        
        return 0
        
    except Exception as e:
        print()
        print("=" * 80)
        print(f"❌ 错误: {e}")
        print("=" * 80)
        
        import traceback
        traceback.print_exc()
        
        return 1


if __name__ == "__main__":
    sys.exit(main())
