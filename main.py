from app.core.events.system import system
from app.log.config.log_config import get_logger
from app.settings.config import (
    SERVER_HOST,
    SERVER_PORT,
    SERVER_RELOAD,
    SERVER_WORKERS,
    SERVER_LOG_LEVEL
)

# 初始化应用
app = system.init_app()
logger = get_logger(__name__)


if __name__ == "__main__":
    import uvicorn

    logger.info("正在启动开发服务器")
    uvicorn.run(
        "main:app",
        host=SERVER_HOST,
        port=SERVER_PORT,
        reload=SERVER_RELOAD,
        workers=SERVER_WORKERS or None,
        log_level=SERVER_LOG_LEVEL,
    )
