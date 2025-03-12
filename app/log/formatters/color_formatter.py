import logging
from typing import Any

from colorama import Fore, Style, init

# 初始化colorama
init()

class ColorFormatter(logging.Formatter):
    """
    彩色日志格式化器
    为不同级别的日志添加不同的颜色
    """
    
    # 定义不同日志级别对应的颜色
    COLORS = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Style.BRIGHT
    }
    
    def __init__(self, fmt: str = None):
        """
        初始化格式化器
        
        Args:
            fmt: 日志格式字符串
        """
        super().__init__(fmt or '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    def format(self, record: Any) -> str:
        """
        格式化日志记录
        
        Args:
            record: 日志记录对象
            
        Returns:
            str: 格式化后的彩色日志字符串
        """
        # 保存原始的levelname
        original_levelname = record.levelname
        # 为日志级别添加颜色
        color = self.COLORS.get(record.levelname, '')
        record.levelname = f"{color}{record.levelname}{Style.RESET_ALL}"
        
        # 格式化日志消息
        formatted = super().format(record)
        
        # 恢复原始的levelname
        record.levelname = original_levelname
        return formatted
