import logging
import sys
from typing import Dict, Any

from app.log.formatters.color_formatter import ColorFormatter
from app.log.formatters.json_formatter import JsonFormatter
from app.log.handlers.file_handler import CustomRotatingFileHandler
from app.settings.config import (
    LOG_LEVEL,
    LOG_FORMAT,
    LOG_FILE_ENABLED,
    LOG_FILE_PATH,
    LOG_MAX_SIZE,
    LOG_BACKUP_COUNT,
    LOG_CONSOLE_OUTPUT
)


def setup_logging() -> None:
    """
    配置日志系统
    设置日志级别、格式化器和处理器
    """
    # 创建根日志记录器
    logger = logging.getLogger()
    logger.setLevel(LOG_LEVEL)
    
    # 清除现有的处理器
    logger.handlers.clear()
    
    # 创建JSON格式化器（用于文件输出）
    json_formatter = JsonFormatter()
    
    # 如果启用了文件日志，添加文件处理器
    if LOG_FILE_ENABLED:
        file_handler = CustomRotatingFileHandler(
            filename=LOG_FILE_PATH,
            maxBytes=LOG_MAX_SIZE,
            backupCount=LOG_BACKUP_COUNT,
            encoding='utf-8'
        )
        file_handler.setFormatter(json_formatter)
        logger.addHandler(file_handler)
    
    # 如果配置了控制台输出，添加控制台处理器
    if LOG_CONSOLE_OUTPUT:
        console_handler = logging.StreamHandler(sys.stdout)
        # 根据配置选择控制台输出格式
        if LOG_FORMAT.lower() == 'json':
            console_formatter = json_formatter
        else:
            # 使用彩色文本格式化器
            console_formatter = ColorFormatter()
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

def get_logger(name: str) -> logging.Logger:
    """
    获取指定名称的日志记录器
    
    Args:
        name: 日志记录器名称
        
    Returns:
        logging.Logger: 日志记录器实例
    """
    return logging.getLogger(name)

class LoggerMixin:
    """
    日志记录器混入类
    为类提供日志记录功能
    """
    
    @property
    def logger(self) -> logging.Logger:
        """
        获取当前类的日志记录器
        
        Returns:
            logging.Logger: 日志记录器实例
        """
        return get_logger(self.__class__.__name__)

def log_exception(logger: logging.Logger, exc: Exception, extra: Dict[str, Any] = None) -> None:
    """
    记录异常信息
    
    Args:
        logger: 日志记录器
        exc: 异常对象
        extra: 额外的日志信息
    """
    error_info = {
        'error_type': exc.__class__.__name__,
        'error_message': str(exc),
        **(extra or {})
    }
    logger.error(
        f"发生异常: {exc.__class__.__name__}",
        extra={'extra_fields': error_info},
        exc_info=True
    )
