from datetime import datetime

from passlib.hash import bcrypt
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator

from app.models.base import BaseModel


class PasswordMixin:
    """
    密码处理混入类
    包含密码哈希存储和验证方法
    """
    # 密码哈希
    password_hash = fields.CharField(
        max_length=128, 
        description="密码哈希"
    )

    @property
    def password(self):
        """
        密码属性的getter
        防止直接访问密码
        """
        raise AttributeError('密码不可直接访问')

    @password.setter
    def password(self, password: str):
        """
        密码属性的setter
        设置密码时自动进行加密
        
        Args:
            password: 原始密码
        """
        self.password_hash = bcrypt.hash(password)

    def verify_password(self, password: str) -> bool:
        """
        验证密码是否正确
        
        Args:
            password: 待验证的密码
            
        Returns:
            bool: 密码是否正确
        """
        return bcrypt.verify(password, self.password_hash)

class User(BaseModel, PasswordMixin):
    """
    用户模型
    包含用户基本信息和认证相关字段
    """
    class Meta:
        table = "users"
        table_description = "用户信息表"
    
    # 用户名，唯一
    username = fields.CharField(
        max_length=50, 
        unique=True, 
        description="用户名",
        index=True
    )
    
    # 邮箱
    email = fields.CharField(
        max_length=100, 
        description="邮箱地址",
        index=True
    )
    
    # 是否激活
    is_active = fields.BooleanField(
        default=True, 
        description="是否激活"
    )
    
    # 是否是超级管理员
    is_superadmin = fields.BooleanField(
        default=False, 
        description="是否是超级管理员"
    )
    
    # 最后登录时间
    last_login = fields.DatetimeField(
        null=True, 
        description="最后登录时间"
    )
   

    def __str__(self):
        return f"{self.username}"

    async def update_last_login(self):
        """
        更新最后登录时间
        """
        self.last_login = datetime.now()
        await self.save()

    @classmethod
    async def get_active(cls):
        """
        获取所有未删除的活跃用户
        """
        return await cls.filter(is_deleted=False, is_active=True)

    @classmethod
    async def batch_soft_delete(cls, user_ids: list[int]):
        """
        批量软删除用户
        
        Args:
            user_ids: 用户ID列表
        """
        now = datetime.now()
        await cls.filter(id__in=user_ids).update(
            is_deleted=True,
            deleted_at=now
        )

    class PydanticMeta:
        # 在序列化时排除的字段
        exclude = ["password_hash"]

# 创建Pydantic模型，用于API的请求和响应
# 完整用户模型，包含所有字段
UserPydantic = pydantic_model_creator(
    User, name="User"
)

# 创建用户时使用的模型，只包含必要字段
UserCreatePydantic = pydantic_model_creator(
    User, name="UserCreate", 
    exclude=("id", "created_at", "updated_at", "last_login", "password_hash", "is_deleted", "deleted_at"),
    exclude_readonly=True
)

# 更新用户时使用的模型
UserUpdatePydantic = pydantic_model_creator(
    User, name="UserUpdate",
    exclude=("id", "created_at", "updated_at", "last_login", "password_hash", "is_deleted", "deleted_at"),
    exclude_readonly=True,
    optional=["username", "email", "is_active", "is_superadmin"]
)
