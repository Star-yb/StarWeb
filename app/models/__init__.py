# 只导出具体的数据库模型
from app.models.user import User
from app.models.rbac import Permission, Role, UserRole


__all__ = [
    'User',  # 用户模型
    'Permission', 'Role', 'UserRole',  # 权限相关模型
]
