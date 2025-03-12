from fastapi import APIRouter

from app.api.views.home import router as home_router

# 创建视图路由
view_router = APIRouter()

# 注册视图子路由
view_router.include_router(home_router)
