import os
from logging.handlers import RotatingFileHandler
from typing import Optional

class CustomRotatingFileHandler(RotatingFileHandler):
    """
    自定义的文件日志处理器
    继承自RotatingFileHandler，增加了自动创建日志目录的功能
    """
    
    def __init__(
        self,
        filename: str,
        mode: str = 'a',
        maxBytes: int = 0,
        backupCount: int = 0,
        encoding: Optional[str] = None,
        delay: bool = False
    ):
        """
        初始化日志处理器
        
        Args:
            filename: 日志文件路径
            mode: 文件打开模式
            maxBytes: 单个日志文件的最大大小
            backupCount: 保留的备份文件数量
            encoding: 文件编码
            delay: 是否延迟创建文件
        """
        # 确保日志目录存在
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        super().__init__(
            filename,
            mode,
            maxBytes,
            backupCount,
            encoding,
            delay
        )
