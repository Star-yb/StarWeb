import os
from fastapi.templating import Jinja2Templates
from app.settings.config import BASE_DIR

# 设置资源路径
RESOURCES_PATH = os.path.join(BASE_DIR, "resources")
TEMPLATES_PATH = os.path.join(RESOURCES_PATH, "templates")

# 创建模板引擎
templates = Jinja2Templates(directory=TEMPLATES_PATH)

# 如果模板目录不存在，创建它
os.makedirs(TEMPLATES_PATH, exist_ok=True)
