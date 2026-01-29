#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志配置模块
"""

import logging
import os
from datetime import datetime, timezone, timedelta


def setup_logger(name='a-stock-report', log_file=None, level=logging.INFO):
    """
    配置日志记录器
    
    Args:
        name: 日志记录器名称
        log_file: 日志文件路径，如果为 None 则只输出到控制台
        level: 日志级别
    
    Returns:
        logger: 配置好的日志记录器
    """
    # 创建日志记录器
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 避免重复添加处理器
    if logger.handlers:
        return logger
    
    # 日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 文件处理器（如果指定了日志文件）
    if log_file:
        # 确保日志目录存在
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_log_file_path():
    """
    获取日志文件路径
    
    Returns:
        str: 日志文件路径
    """
    # 使用北京时间
    beijing_tz = timezone(timedelta(hours=8))
    date_str = datetime.now(beijing_tz).strftime("%Y-%m-%d")
    
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    return os.path.join(log_dir, f"report_{date_str}.log")
