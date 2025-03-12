from fastapi import APIRouter

from app.api.rest import api_router
from app.api.views import view_router

# 创建主路由
router = APIRouter()

# 注册子路由
router.include_router(api_router)  # API 接口路由
router.include_router(view_router)  # 视图路由
