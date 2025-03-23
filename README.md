# Star Web 项目

一个基于 FastAPI 框架的 Python Web 应用，提供完整的用户认证和管理功能。

## 项目简介

Star Web 是一个使用 Python 和 FastAPI 框架开发的 Web 应用骨架，集成了用户认证、权限管理、数据库操作等常用功能，为快速开发企业级 Web 应用提供基础架构。

## 技术栈

- **Python**: 3.8+ 
- **FastAPI**: 高性能异步 Web 框架
- **Tortoise ORM**: 异步 ORM 数据库操作
- **SQLite/MySQL/PostgreSQL**: 数据库支持
- **JWT**: 双令牌认证系统（访问令牌 + 刷新令牌）
- **Pydantic**: 数据验证和设置管理
- **Uvicorn**: ASGI 服务器
- **Starlette**: Web 工具包

## 项目结构

```
star_web/
├── app/                    # 应用主目录
│   ├── api/               # API 接口和路由
│   │   ├── endpoints/     # API 端点实现
│   │   └── views/        # 视图函数
│   ├── core/             # 核心功能模块
│   │   ├── events/       # 应用事件处理（启动、关闭等）
│   │   ├── exceptions/   # 自定义异常类
│   │   ├── security/     # 安全相关（认证、令牌）
│   │   ├── database.py   # 数据库配置
│   │   ├── system.py     # 系统配置和启动
│   │   └── templates.py  # 模板引擎配置
│   ├── log/              # 日志配置
│   │   ├── config/       # 日志配置
│   │   ├── formatters/   # 日志格式化器
│   │   └── handlers/     # 日志处理器
│   ├── models/           # 数据库模型
│   ├── schemas/          # 数据验证模型（Pydantic）
│   ├── services/         # 业务逻辑服务
│   ├── settings/         # 配置管理
│   └── utils/           # 工具函数
│       ├── decorators/  # 装饰器函数
│       ├── helpers/     # 辅助函数
│       ├── validators/  # 数据验证器
│       ├── serializer.py # 数据序列化工具
│       └── token_parser.py # JWT令牌解析工具
├── logs/                # 日志文件目录
├── resources/          # 资源文件目录
│   ├── migrations/      # 数据库迁移文件
│   ├── static/          # 静态资源文件
│   └── templates/       # HTML 模板文件
├── tests/             # 测试目录
├── config.ini         # 配置文件
├── main.py            # 应用入口
└── requirements.txt   # 项目依赖
```

## 功能特性

### 用户管理
- 用户注册、登录、退出
- 用户信息查询与更新
- 密码修改与重置
- 用户状态管理

### 权限控制
- 基于 JWT 的双令牌认证系统
- 角色权限管理（管理员、普通用户、访客）
- 接口访问控制
- 权限验证装饰器

### 系统功能
- 完善的日志系统
- 请求限流
- 跨域支持
- 全局异常处理
- 数据库自动迁移
- 优雅启动和关闭
- 详细的 API 文档（Swagger UI 和 ReDoc）

## 核心组件说明

### 应用核心 (app/core)
- 应用程序初始化和生命周期管理
- 优雅启动和关闭
- 组件集成
- 异常处理

### 配置管理 (app/settings)
- 基于 Pydantic 的配置管理
- 支持 INI 格式配置文件
- 环境变量覆盖
- 服务器、数据库、JWT等配置

### 数据库 (app/core/database.py)
- 基于 Tortoise ORM 的异步数据库连接
- 连接池配置
- 数据库迁移
- 模型注册

### 日志系统 (app/log)
- 灵活的日志配置
- 日志分级
- 日志轮转
- 支持开发和生产环境配置
- JSON 和文本格式支持

### 安全系统 (app/core/security)
- JWT 令牌生成与验证
- 密码哈希与验证
- 访问控制
- 双令牌刷新机制

### API 路由 (app/api)
- RESTful API 设计
- 版本化 API
- 公开和私有路由分组
- 自动生成 API 文档

### 数据模型 (app/models)
- 用户模型
- 角色模型
- 数据验证
- 密码加密

## 数据架构设计

Star Web 采用了传统的角色-权限-用户模型设计，实现了基于角色的访问控制 (RBAC) 系统。

### 数据模型关系

```
┌─────────┐       ┌─────────┐       ┌─────────┐
│  User   │       │UserRole │       │  Role   │
├─────────┤       ├─────────┤       ├─────────┤
│ ID      │       │ ID      │       │ ID      │
│ Username│◄──────┤ UserID  │       │ Name    │
│ Password│       │ RoleID  │──────►│ Code    │
│ Email   │       └─────────┘       │ Desc    │
└─────────┘                         └─────────┘
                                        │
                                        │
                                        ▼
                                    ┌─────────┐       ┌─────────┐
                                    │RolePerm │       │Permission│
                                    ├─────────┤       ├─────────┤
                                    │ ID      │       │ ID      │
                                    │ RoleID  │       │ Name    │
                                    │ PermID  │──────►│ Code    │
                                    └─────────┘       │ Desc    │
                                                      └─────────┘
```

### 核心表结构

#### 用户表 (users)
```python
class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=255)
    email = fields.CharField(max_length=100, unique=True)
    nickname = fields.CharField(max_length=50, null=True)
    avatar = fields.CharField(max_length=255, null=True)
    status = fields.IntField(default=1)  # 1:正常 0:禁用
    last_login = fields.DatetimeField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
    roles: fields.ManyToManyRelation["Role"] = fields.ManyToManyField(
        "models.Role", related_name="users", through="user_role"
    )
```

#### 角色表 (roles)
```python
class Role(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, unique=True)
    code = fields.CharField(max_length=50, unique=True)
    description = fields.CharField(max_length=200, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
    permissions: fields.ManyToManyRelation["Permission"] = fields.ManyToManyField(
        "models.Permission", related_name="roles", through="role_permission"
    )
```

#### 权限表 (permissions)
```python
class Permission(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)
    code = fields.CharField(max_length=50, unique=True)
    description = fields.CharField(max_length=200, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
```

## 认证与鉴权

参考文件 [点击查看认证与鉴权](./auth_examples.md)


## 配置文件

项目的主要配置位于 `config.ini`：

```ini
[APP]
# 应用名称
APP_NAME = StarWeb
# 调试模式
DEBUG = True
# 密钥
SECRET_KEY = your-secret-key-here
# 允许的主机
ALLOWED_HOSTS = localhost,127.0.0.1

[SERVER]
# 服务器配置
HOST = 127.0.0.1
PORT = 8005
RELOAD = True
WORKERS = 0
LOG_LEVEL = info

[DATABASE]
# 数据库连接
DATABASE_URL = sqlite:///resources/db.sqlite3

[JWT]
# JWT 认证配置
SECRET_KEY = your-jwt-secret-key-here
ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

[LOG]
# 日志配置
LEVEL = INFO
FORMAT = json
FILE_ENABLED = False  # 开发环境下禁用文件日志
FILE_PATH = logs/app.log
MAX_SIZE = 10  # MB
BACKUP_COUNT = 5
CONSOLE_OUTPUT = True

[CORS]
# CORS 配置
ALLOW_ORIGINS = *
ALLOW_METHODS = *
ALLOW_HEADERS = *
ALLOW_CREDENTIALS = True
```

## 开发环境配置

1. 克隆项目并安装依赖：
```bash
git clone <repository-url>
cd star_web
pip install -r requirements.txt
```

2. 配置 `config.ini`：
- 修改 `SECRET_KEY` 和 `JWT_SECRET_KEY`
- 配置数据库连接 `DATABASE_URL`
- 开发环境下建议设置 `DEBUG = True` 和 `LOG.FILE_ENABLED = False`

3. 运行项目：
```bash
python main.py
```

访问 http://localhost:8005/docs 查看 API 文档。

## API 认证

项目使用 JWT 双令牌认证系统，主要端点：

### 1. 用户登录
```http
POST /api/auth/login
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}
```

### 2. 刷新令牌
```http
POST /api/auth/refresh
Content-Type: application/json

{
    "refresh_token": "your_refresh_token"
}
```

### 3. 获取用户信息
```http
GET /api/users/me
Authorization: Bearer your_access_token
```

## 日志配置

项目支持灵活的日志配置：

- 开发环境：建议设置 `LOG.FILE_ENABLED = False`，日志只输出到控制台
- 生产环境：设置 `LOG.FILE_ENABLED = True`，日志同时输出到文件和控制台
- 支持 JSON 和文本两种日志格式
- 文件日志支持自动轮转

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详情请参阅 [LICENSE](LICENSE) 文件。

## 联系方式

项目维护者 - 邮箱地址

Email: starloongyibao@qq.com

项目链接: [StarWeb](https://gitee.com/chenwm-star/star-web.git)

