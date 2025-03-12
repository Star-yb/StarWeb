import logging
import os
import shutil
from typing import List

from aerich import Command
from tortoise import Tortoise

from app.settings.config import DATABASE_URL, BASE_DIR

# 配置日志
logger = logging.getLogger(__name__)

# 迁移文件路径
MIGRATIONS_DIR = os.path.join(BASE_DIR, "resources", "migrations")

# Tortoise ORM模型的导入路径
MODELS_PATH: List[str] = [
    "app.models",  # 所有模型
    "aerich.models",    # aerich迁移工具的模型
]

# 数据库配置
TORTOISE_ORM = {
    "connections": {
        "default": DATABASE_URL
    },
    "apps": {
        "models": {
            "models": MODELS_PATH,
            "default_connection": "default",
        }
    }
}

async def init_db() -> None:
    """
    初始化数据库连接并处理迁移
    """
    try:
        logger.info("正在初始化数据库连接...")
        await Tortoise.init(config=TORTOISE_ORM)
        
        # 创建 aerich 命令实例
        command = Command(
            tortoise_config=TORTOISE_ORM,
            app="models",
            location=MIGRATIONS_DIR  # 指定迁移文件路径
        )
        
        # 确保迁移目录存在
        if not os.path.exists(MIGRATIONS_DIR):
            os.makedirs(MIGRATIONS_DIR)
            logger.info(f"创建迁移目录: {MIGRATIONS_DIR}")
        
        try:
            # 尝试初始化数据库
            logger.info("尝试初始化数据库...")
            await command.init_db(safe=True)
        except FileExistsError:
            logger.info("数据库已存在，跳过初始化")
        
        # 初始化迁移系统
        logger.info("初始化迁移系统...")
        await command.init()
        
        try:
            # 创建新的迁移
            logger.info("检查并创建新的迁移...")
            await command.migrate()
        except AttributeError:
            logger.warning("无法从数据库获取模型历史，将重新创建迁移")
            if os.path.exists(MIGRATIONS_DIR):
                shutil.rmtree(MIGRATIONS_DIR)
                os.makedirs(MIGRATIONS_DIR)
            await command.init_db(safe=True)
        
        # 应用迁移
        logger.info("应用迁移...")
        await command.upgrade(run_in_transaction=True)
        logger.info("数据库初始化和迁移完成！")
            
    except Exception as e:
        logger.error(f"数据库初始化失败: {str(e)}")
        raise

async def close_db() -> None:
    """
    关闭数据库连接
    """
    logger.info("正在关闭数据库连接...")
    await Tortoise.close_connections()
    logger.info("数据库连接已关闭！")
