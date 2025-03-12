import os
from configparser import ConfigParser
from datetime import timedelta
from typing import List

# 获取项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 读取配置文件
config = ConfigParser()
config_file = os.path.join(BASE_DIR, 'config.ini')
config.read(config_file, encoding='utf-8')

# 应用配置
APP_NAME = config.get('APP', 'APP_NAME')
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "StarWeb API服务"
DEBUG = config.getboolean('APP', 'DEBUG')
SECRET_KEY = config.get('APP', 'SECRET_KEY')
ALLOWED_HOSTS: List[str] = config.get('APP', 'ALLOWED_HOSTS').split(',')

# 服务器配置
SERVER_HOST = config.get('SERVER', 'HOST')
SERVER_PORT = config.getint('SERVER', 'PORT')
SERVER_RELOAD = config.getboolean('SERVER', 'RELOAD')
SERVER_WORKERS = config.getint('SERVER', 'WORKERS')
SERVER_LOG_LEVEL = config.get('SERVER', 'LOG_LEVEL').lower()

# 数据库配置
DATABASE_URL = config.get('DATABASE', 'DATABASE_URL')

# JWT配置
JWT_SECRET_KEY = config.get('JWT', 'SECRET_KEY')
JWT_ALGORITHM = config.get('JWT', 'ALGORITHM')
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = config.getint('JWT', 'ACCESS_TOKEN_EXPIRE_MINUTES')
JWT_REFRESH_TOKEN_EXPIRE_DAYS = config.getint('JWT', 'REFRESH_TOKEN_EXPIRE_DAYS')

# 计算token过期时间
ACCESS_TOKEN_EXPIRE_DELTA = timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
REFRESH_TOKEN_EXPIRE_DELTA = timedelta(days=JWT_REFRESH_TOKEN_EXPIRE_DAYS)

# 日志配置
LOG_LEVEL = config.get('LOG', 'LEVEL')
LOG_FORMAT = config.get('LOG', 'FORMAT')
LOG_FILE_ENABLED = config.getboolean('LOG', 'FILE_ENABLED')
LOG_FILE_PATH = os.path.join(BASE_DIR, config.get('LOG', 'FILE_PATH'))
LOG_MAX_SIZE = config.getint('LOG', 'MAX_SIZE') * 1024 * 1024  # 转换为字节
LOG_BACKUP_COUNT = config.getint('LOG', 'BACKUP_COUNT')
LOG_CONSOLE_OUTPUT = config.getboolean('LOG', 'CONSOLE_OUTPUT')

# CORS配置
CORS_ORIGINS = eval(config.get('CORS', 'ORIGINS'))  # 从字符串转换为列表
CORS_METHODS = eval(config.get('CORS', 'METHODS'))
CORS_HEADERS = eval(config.get('CORS', 'HEADERS'))
CORS_CREDENTIALS = config.getboolean('CORS', 'ALLOW_CREDENTIALS')
