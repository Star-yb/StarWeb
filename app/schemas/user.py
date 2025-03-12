from typing import Optional, List
from pydantic import BaseModel, constr, Field
import re

# 邮箱格式验证正则表达式
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

class UserCreate(BaseModel):
    """
    创建用户的请求模型
    """
    username: str  # 用户名
    email: str = Field(..., pattern=EMAIL_PATTERN)  # 邮箱，使用正则验证
    password: str  # 密码
    is_active: Optional[bool] = True  # 是否激活，默认激活
    
class UserUpdate(BaseModel):
    """
    更新用户的请求模型
    """
    username: Optional[str] = None  # 用户名
    email: Optional[str] = Field(None, pattern=EMAIL_PATTERN)  # 邮箱，使用正则验证
    password: Optional[str] = None  # 密码
    is_active: Optional[bool] = None  # 是否激活

class UserResponse(BaseModel):
    """
    用户响应模型
    """
    id: int  # 用户ID
    username: str  # 用户名
    email: str  # 邮箱
    is_active: bool  # 是否激活
    
    class Config:
        from_attributes = True  # 允许从ORM模型创建

class UserList(BaseModel):
    """
    用户列表响应模型
    """
    total: int  # 总数
    items: List[UserResponse]  # 用户列表
