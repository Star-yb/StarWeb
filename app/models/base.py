from datetime import datetime

from tortoise import fields, models


class TimestampMixin:
    """
    时间戳混入类
    包含创建时间和更新时间字段
    """
    # 创建时间
    created_at = fields.DatetimeField(
        auto_now_add=True,
        description="创建时间"
    )
    
    # 更新时间
    updated_at = fields.DatetimeField(
        auto_now=True,
        description="更新时间"
    )

class LogicalDeleteMixin:
    """
    逻辑删除混入类
    包含逻辑删除标记和删除时间字段
    """
    # 逻辑删除
    is_deleted = fields.BooleanField(
        default=False,
        description="是否逻辑删除"
    )
    
    # 删除时间
    deleted_at = fields.DatetimeField(
        null=True,
        description="删除时间"
    )
    
    async def soft_delete(self):
        """
        软删除方法
        """
        self.is_deleted = True
        self.deleted_at = datetime.now()
        await self.save()

class AbstractBaseModel(models.Model):
    """
    抽象基础模型
    包含所有模型通用的配置
    """
    class Meta:
        abstract = True
    
    class PydanticMeta:
        exclude = []  # 在API响应中排除的字段
        computed = []  # 计算后的字段

class BaseModel(AbstractBaseModel, TimestampMixin, LogicalDeleteMixin):
    """
    基础模型类（使用自增整型主键）
    """
    # ID主键，自增
    id = fields.IntField(
        pk=True,
        description="主键ID"
    )
    class Meta:
        abstract = True

class UUIDBaseModel(AbstractBaseModel, TimestampMixin, LogicalDeleteMixin):
    """
    UUID基础模型类
    使用UUID作为主键
    """
    # UUID主键
    uuid = fields.UUIDField(
        pk=True,
        description="UUID主键"
    )
    class Meta:
        abstract = True

class BigIDBaseModel(AbstractBaseModel, TimestampMixin, LogicalDeleteMixin):
    """
    大整数基础模型类
    使用BigInt作为主键
    """
    # BigInt主键
    id = fields.BigIntField(
        pk=True,
        description="主键ID"
    )
    class Meta:
        abstract = True
