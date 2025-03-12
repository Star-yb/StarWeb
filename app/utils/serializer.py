from datetime import datetime
from typing import Any

from pydantic import BaseModel


def serialize_model(obj: Any) -> Any:
    """
    序列化对象为 JSON 可序列化的格式
    """
    if isinstance(obj, BaseModel):
        return obj.model_dump()
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, (list, tuple)):
        return [serialize_model(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: serialize_model(value) for key, value in obj.items()}
    return obj
