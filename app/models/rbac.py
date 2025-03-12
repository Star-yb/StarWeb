from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

from app.models.base import BaseModel,TimestampMixin


class Permission(BaseModel):
    """权限模型"""
    name = fields.CharField(max_length=100, unique=True, description="权限名称")
    code = fields.CharField(max_length=100, unique=True, description="权限代码")
    description = fields.TextField(null=True, description="权限描述")

    # 权限类型：菜单/按钮/接口等
    TYPE_CHOICES = {
        "menu": "菜单",
        "button": "按钮",
        "api": "接口"
    }
    type = fields.CharField(max_length=20, description="权限类型")
    
    # 如果是菜单类型，可以设置路由路径
    path = fields.CharField(max_length=200, null=True, description="路由路径")
    
    # 父权限，用于构建权限树
    parent = fields.ForeignKeyField(
        'models.Permission',
        related_name='children',
        null=True,
        on_delete=fields.SET_NULL,  # 父权限删除时，子权限的parent设为NULL
        description="父权限"
    )

    # 排序字段
    sort_order = fields.IntField(default=0, description="排序序号")

    class Meta:
        table = "permissions"
        table_description = "权限表"


class Role(BaseModel):
    """角色模型"""
    name = fields.CharField(max_length=50, unique=True, description="角色名称")
    code = fields.CharField(max_length=50, unique=True, description="角色代码")
    description = fields.TextField(null=True, description="角色描述")
    
    # 是否是系统内置角色
    is_system = fields.BooleanField(default=False, description="是否系统内置")
    
    # 角色-权限多对多关系
    permissions = fields.ManyToManyField(
        'models.Permission',
        related_name='roles',
        description="角色拥有的权限"
    )

    class Meta:
        table = "roles"
        table_description = "角色表"


class UserRole(models.Model,TimestampMixin):
    """用户-角色关联模型"""
    # ID主键，自增
    id = fields.IntField(
        pk=True,
        description="主键ID"
    )
    user = fields.ForeignKeyField(
        'models.User',  
        related_name='user_roles',
        on_delete=fields.CASCADE,  # 用户删除时，自动删除用户角色关联
        description="用户"
    )
    role = fields.ForeignKeyField(
        'models.Role',
        related_name='user_roles',
        on_delete=fields.CASCADE,  # 角色删除时，自动删除用户角色关联
        description="角色"
    )
    
    # 数据权限范围：全部数据/本部门数据/本人数据
    DATA_SCOPE_CHOICES = {
        "all": "全部数据",
        "department": "本部门数据",
        "self": "本人数据"
    }
    data_scope = fields.CharField(
        max_length=20,
        default="self",
        description="数据权限范围"
    )

    class Meta:
        table = "user_roles"
        table_description = "用户角色关联表"
        unique_together = ("user_id", "role_id")


# 创建Pydantic模型
PermissionPydantic = pydantic_model_creator(Permission, name="Permission")
RolePydantic = pydantic_model_creator(Role, name="Role")
UserRolePydantic = pydantic_model_creator(UserRole, name="UserRole")
