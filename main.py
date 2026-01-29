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
from logger_config import setup_logger, get_log_file_path

# 加载 .env 文件（本地运行时使用，GitHub Actions 会直接使用 Secrets）
load_dotenv()

# 设置日志
logger = setup_logger('main', get_log_file_path())


def main():
    # 使用北京时间
    beijing_tz = timezone(timedelta(hours=8))
    beijing_time = datetime.now(beijing_tz).strftime('%Y-%m-%d %H:%M:%S')
    
    logger.info("=" * 80)
    logger.info("A股晚间复盘报告系统启动")
    logger.info("=" * 80)
    logger.info(f"版本: v2.1.0 (Gemini)")
    logger.info(f"运行时间: {beijing_time} (北京时间)")
    logger.info(f"Python 版本: {sys.version}")
    logger.info(f"工作目录: {os.getcwd()}")
    logger.info(f"日志文件: {get_log_file_path()}")
    
    # 检查环境变量
    logger.info("-" * 80)
    logger.info("检查环境变量配置")
    logger.info("-" * 80)
    
    env_vars = {
        'GEMINI_API_KEY': os.getenv('GEMINI_API_KEY'),
        'SENDER_EMAIL': os.getenv('SENDER_EMAIL'),
        'RECIPIENT_EMAIL': os.getenv('RECIPIENT_EMAIL'),
    }
    
    for key, value in env_vars.items():
        if value:
            if 'KEY' in key:
                # 隐藏 API Key
                masked = f"{value[:10]}...{value[-5:]}" if len(value) > 15 else "***"
                logger.info(f"✅ {key}: {masked}")
            else:
                logger.info(f"✅ {key}: {value}")
        else:
            logger.warning(f"⚠️ {key}: 未设置")
    
    print("=" * 60)
    print("A股晚间复盘报告系统 v2.0.0 (AkShare)")
    print("=" * 60)
    print(f"运行时间: {beijing_time} (北京时间)")
    print(f"日志文件: {get_log_file_path()}")
    print()
    
    try:
        print("步骤 1/2: 生成报告")
        print("-" * 60)
        logger.info("=" * 80)
        logger.info("步骤 1/2: 生成报告")
        logger.info("=" * 80)
        
        generator = AStockReportGenerator()
        report_content = generator.generate_report()
        report_filepath = generator.save_report(report_content)
        
        logger.info(f"✅ 报告生成完成: {report_filepath}")
        print()
        
        print("步骤 2/2: 发送邮件")
        print("-" * 60)
        logger.info("=" * 80)
        logger.info("步骤 2/2: 发送邮件")
        logger.info("=" * 80)
        
        recipient_email = os.getenv('RECIPIENT_EMAIL')
        if not recipient_email:
            logger.warning("未设置 RECIPIENT_EMAIL，跳过邮件发送")
            print("⚠️  未设置 RECIPIENT_EMAIL，跳过邮件发送")
            print("💡 提示: 设置 RECIPIENT_EMAIL 以启用邮件发送")
        else:
            try:
                logger.info(f"收件人: {recipient_email}")
                sender = EmailSender()
                success = sender.send_report(recipient_email, report_filepath)
                
                if success:
                    logger.info("✅ 邮件发送成功")
                else:
                    logger.warning("⚠️ 邮件发送失败")
                    print("⚠️  邮件发送失败，但报告已生成")
            except Exception as e:
                logger.error(f"❌ 邮件发送错误: {e}", exc_info=True)
                print(f"⚠️  邮件错误: {e}")
                print("💡 报告已生成，请手动查看")
        
        print()
        print("=" * 60)
        print("✅ 任务完成！")
        print(f"📄 报告文件: {report_filepath}")
        print(f"📋 日志文件: {get_log_file_path()}")
        print("=" * 60)
        
        logger.info("=" * 80)
        logger.info("✅ 任务完成")
        logger.info("=" * 80)
        
        return 0
        
    except Exception as e:
        print()
        print("=" * 60)
        print(f"❌ 错误: {e}")
        print(f"📋 查看详细日志: {get_log_file_path()}")
        print("=" * 60)
        
        logger.error("=" * 80)
        logger.error(f"❌ 任务失败: {e}")
        logger.error("=" * 80)
        
        import traceback
        logger.error(traceback.format_exc())
        traceback.print_exc()
        
        return 1


if __name__ == "__main__":
    sys.exit(main())
