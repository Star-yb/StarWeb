import datetime
import json
from typing import Any, Dict


class JsonFormatter:
    """
    JSON格式的日志格式化器
    将日志记录转换为JSON格式，便于日志分析和处理
    """
    
    def __init__(self):
        self.default_fields = ['时间', '级别', '消息']
    
    def format(self, record: Any) -> str:
        """
        格式化日志记录为JSON字符串
        
        Args:
            record: 日志记录对象
            
        Returns:
            str: JSON格式的日志字符串
        """
        log_data: Dict[str, Any] = {
            '时间': datetime.datetime.fromtimestamp(record.created).isoformat(),
            '级别': record.levelname,
            '消息': record.getMessage(),
            '记录器': record.name,
            '模块': record.module,
            '行号': record.lineno
        }
        
        # 添加异常信息（如果存在）
        if record.exc_info:
            log_data['异常'] = {
                '类型': str(record.exc_info[0].__name__),
                '消息': str(record.exc_info[1]),
                '追踪': record.exc_text
            }
            
        # 添加额外的字段
        if hasattr(record, 'extra_fields'):
            for key, value in record.extra_fields.items():
                if key not in self.default_fields:
                    log_data[key] = value
                    
        return json.dumps(log_data, ensure_ascii=False)
