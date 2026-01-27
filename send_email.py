#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
邮件发送模块
用于发送A股复盘报告到指定邮箱
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from typing import Optional, List


class EmailSender:
    """邮件发送器"""
    
    def __init__(
        self,
        smtp_server: Optional[str] = None,
        smtp_port: Optional[int] = None,
        sender_email: Optional[str] = None,
        sender_password: Optional[str] = None
    ):
        """
        初始化邮件发送器
        
        Args:
            smtp_server: SMTP服务器地址
            smtp_port: SMTP端口
            sender_email: 发件人邮箱
            sender_password: 发件人密码或授权码
        """
        self.smtp_server = smtp_server or os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = smtp_port or int(os.getenv('SMTP_PORT', '587'))
        self.sender_email = sender_email or os.getenv('SENDER_EMAIL')
        self.sender_password = sender_password or os.getenv('SENDER_PASSWORD')
        
        if not self.sender_email or not self.sender_password:
            raise ValueError("请设置 SENDER_EMAIL 和 SENDER_PASSWORD 环境变量")
    
    def send_report(
        self,
        recipient_email: str,
        report_filepath: str,
        subject: Optional[str] = None
    ) -> bool:
        """
        发送报告邮件
        
        Args:
            recipient_email: 收件人邮箱
            report_filepath: 报告文件路径
            subject: 邮件主题
            
        Returns:
            是否发送成功
        """
        try:
            # 读取报告内容
            with open(report_filepath, 'r', encoding='utf-8') as f:
                report_content = f.read()
            
            # 生成邮件主题
            if subject is None:
                date_str = datetime.now().strftime("%Y年%m月%d日")
                subject = f"A股晚间复盘报告 - {date_str}"
            
            # 创建邮件
            message = self._create_message(
                recipient_email,
                subject,
                report_content,
                report_filepath
            )
            
            # 发送邮件
            self._send_email(recipient_email, message)
            
            print(f"✅ 邮件已成功发送到: {recipient_email}")
            return True
            
        except Exception as e:
            print(f"❌ 邮件发送失败: {e}")
            return False
    
    def _create_message(
        self,
        recipient_email: str,
        subject: str,
        report_content: str,
        report_filepath: str
    ) -> MIMEMultipart:
        """创建邮件消息"""
        # 创建邮件对象
        message = MIMEMultipart('alternative')
        message['From'] = self.sender_email
        message['To'] = recipient_email
        message['Subject'] = subject
        
        # 生成HTML内容（将Markdown转换为HTML）
        html_content = self._markdown_to_html(report_content)
        
        # 添加纯文本和HTML版本
        text_part = MIMEText(report_content, 'plain', 'utf-8')
        html_part = MIMEText(html_content, 'html', 'utf-8')
        
        message.attach(text_part)
        message.attach(html_part)
        
        # 添加附件
        self._attach_file(message, report_filepath)
        
        return message
    
    def _markdown_to_html(self, markdown_content: str) -> str:
        """
        将Markdown转换为HTML
        
        Args:
            markdown_content: Markdown内容
            
        Returns:
            HTML内容
        """
        try:
            import markdown
            
            # 使用markdown库转换
            html = markdown.markdown(
                markdown_content,
                extensions=['tables', 'fenced_code', 'nl2br']
            )
            
            # 添加样式
            styled_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                        line-height: 1.6;
                        color: #333;
                        max-width: 1200px;
                        margin: 0 auto;
                        padding: 20px;
                        background-color: #f5f5f5;
                    }}
                    h1, h2, h3 {{
                        color: #2c3e50;
                        border-bottom: 2px solid #3498db;
                        padding-bottom: 10px;
                    }}
                    table {{
                        border-collapse: collapse;
                        width: 100%;
                        margin: 20px 0;
                        background-color: white;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    }}
                    th {{
                        background-color: #3498db;
                        color: white;
                        padding: 12px;
                        text-align: left;
                    }}
                    td {{
                        padding: 10px;
                        border-bottom: 1px solid #ddd;
                    }}
                    tr:hover {{
                        background-color: #f5f5f5;
                    }}
                    code {{
                        background-color: #f4f4f4;
                        padding: 2px 6px;
                        border-radius: 3px;
                        font-family: 'Courier New', monospace;
                    }}
                    blockquote {{
                        border-left: 4px solid #3498db;
                        padding-left: 20px;
                        margin: 20px 0;
                        color: #666;
                    }}
                    .positive {{
                        color: #e74c3c;
                        font-weight: bold;
                    }}
                    .negative {{
                        color: #27ae60;
                        font-weight: bold;
                    }}
                </style>
            </head>
            <body>
                {html}
            </body>
            </html>
            """
            
            return styled_html
            
        except ImportError:
            # 如果没有markdown库，返回简单的HTML
            return f"<html><body><pre>{markdown_content}</pre></body></html>"
    
    def _attach_file(self, message: MIMEMultipart, filepath: str):
        """添加附件"""
        filename = os.path.basename(filepath)
        
        with open(filepath, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
        
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename= {filename}'
        )
        
        message.attach(part)
    
    def _send_email(self, recipient_email: str, message: MIMEMultipart):
        """发送邮件"""
        print(f"📧 正在发送邮件到 {recipient_email}...")
        
        # 连接SMTP服务器
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()  # 启用TLS加密
            server.login(self.sender_email, self.sender_password)
            server.send_message(message)


def main():
    """测试邮件发送"""
    import sys
    
    if len(sys.argv) < 3:
        print("用法: python send_email.py <收件人邮箱> <报告文件路径>")
        sys.exit(1)
    
    recipient = sys.argv[1]
    report_file = sys.argv[2]
    
    sender = EmailSender()
    sender.send_report(recipient, report_file)


if __name__ == "__main__":
    main()
