from fastapi import APIRouter

from app.api.rest.auth import router as auth_router
from app.api.rest.user import router as user_router
from app.api.rest.rbac import permissions_router,roles_router

# 创建 API 路由
api_router = APIRouter(prefix="/api")

# 注册 API 子路由
api_router.include_router(auth_router, prefix="/auth", tags=["认证"])
api_router.include_router(roles_router, prefix="/roles", tags=["角色管理"])
api_router.include_router(permissions_router, prefix="/permissions", tags=["权限管理"])
api_router.include_router(user_router, prefix="/users", tags=["用户管理"])
