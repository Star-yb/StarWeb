import os
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api import router as main_router
from app.core.events.database import init_db, close_db
from app.log.config.log_config import setup_logging, get_logger
from app.settings.config import (
    APP_NAME,
    APP_VERSION,
    APP_DESCRIPTION,
    CORS_ORIGINS,
    CORS_METHODS,
    CORS_HEADERS,
    CORS_CREDENTIALS,
    BASE_DIR
)

logger = get_logger(__name__)


class SystemInit:
    """系统初始化类"""

    def __init__(self):
        self.app: Optional[FastAPI] = None
        
        # 设置资源路径（使用项目根目录）
        self.resources_path = os.path.join(BASE_DIR, "resources")
        self.static_path = os.path.join(self.resources_path, "static")

    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        """应用生命周期管理"""
        # 启动时执行
        logger.info("应用程序启动")
        # 初始化数据库连接
        await init_db()
        logger.info("数据库连接已建立")

        yield

        # 关闭时执行
        await close_db()
        logger.info("应用程序关闭")

    def init_app(self) -> FastAPI:
        """初始化FastAPI应用"""
        # 设置日志
        setup_logging()
        
        # 创建FastAPI应用
        self.app = FastAPI(
            title=APP_NAME,
            version=APP_VERSION,
            description=APP_DESCRIPTION,
            lifespan=self.lifespan,
        )

        # 配置CORS
        self._init_middleware()
        
        # 配置静态文件
        self._init_static()
        
        # 注册路由
        self._init_routes()
        
        return self.app

    def _init_middleware(self):
        """初始化中间件"""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=CORS_ORIGINS,
            allow_methods=CORS_METHODS,
            allow_headers=CORS_HEADERS,
            allow_credentials=CORS_CREDENTIALS,
        )

    def _init_static(self):
        """初始化静态文件"""
        # 如果静态文件目录不存在，创建它
        os.makedirs(self.static_path, exist_ok=True)
        self.app.mount("/static", StaticFiles(directory=self.static_path), name="static")

    def _init_routes(self):
        """初始化路由"""
        # 注册主路由
        self.app.include_router(main_router)


# 创建全局实例
system = SystemInit()
