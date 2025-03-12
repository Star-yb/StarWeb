from fastapi import APIRouter, Request

from app.core.exceptions.auth import MissingTokenError
from app.schemas.auth import TokenResponse,RefreshTokenResponse
from app.services.auth import AuthService

router = APIRouter()
auth_service = AuthService()


@router.post("/login", response_model=TokenResponse)
async def login(request: Request) -> TokenResponse:
    """
    用户登录接口
    
    支持两种方式传参：
    1. Form表单格式：
       - username: 用户名
       - password: 密码
       
    2. JSON格式：
    ```json
    {
        "username": "用户名",
        "password": "密码"
    }
    ```
    """
    # 获取请求内容类型
    content_type = request.headers.get("content-type", "").lower()

    # 获取用户名和密码
    try:
        if "application/json" in content_type:
            # JSON 数据
            body = await request.json()
            username = body.get("username")
            password = body.get("password")
        else:
            # Form 表单数据
            form = await request.form()
            username = form.get("username")
            password = form.get("password")

        if not username or not password:
            raise MissingTokenError()

    except Exception:
        raise MissingTokenError()

    # 验证用户并创建令牌
    return await AuthService.login(username, password)


@router.post("/refresh", response_model=RefreshTokenResponse)
async def refresh_token(request: Request) -> RefreshTokenResponse:
    """
    使用刷新令牌获取新的访问令牌
    
    支持两种方式传参：
    1. Form表单格式：
       - refresh_token: 刷新令牌
       
    2. JSON格式：
    ```json
    {
        "refresh_token": "刷新令牌"
    }
    ```
    """
    # 获取请求内容类型
    content_type = request.headers.get("content-type", "").lower()

    # 获取刷新令牌
    try:
        if "application/json" in content_type:
            # JSON 数据
            body = await request.json()
            token = body.get("refresh_token")
        else:
            # Form 表单数据
            form = await request.form()
            token = form.get("refresh_token")

        if not token:
            raise MissingTokenError()

    except Exception:
        raise MissingTokenError()

    # 验证令牌并创建新令牌
    return await AuthService.refresh_token(token)


@router.post("/me")
async def read_users_me(request: Request):
    """
    验证令牌并获取用户信息
    
    支持两种方式传参：
    1. Form表单格式：
       - token: 令牌（可以是访问令牌或刷新令牌）
       
    2. JSON格式：
    ```json
    {
        "token": "令牌（可以是访问令牌或刷新令牌）"
    }
    ```
    
    返回：
    - 如果令牌有效：返回用户信息和令牌类型
    - 如果令牌无效或过期：返回相应的错误信息
    """
    # 获取请求内容类型
    content_type = request.headers.get("content-type", "").lower()

    # 获取令牌
    try:
        if "application/json" in content_type:
            # JSON 数据
            body = await request.json()
            token = body.get("token")
        else:
            # Form 表单数据
            form = await request.form()
            token = form.get("token")

        if not token:
            raise MissingTokenError()

    except Exception:
        raise MissingTokenError()

    # 验证令牌并获取用户
    return await AuthService.get_user_by_token(token)
