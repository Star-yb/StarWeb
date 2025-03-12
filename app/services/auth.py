from datetime import datetime, timedelta
from typing import Dict, Any, Tuple, Optional, Annotated

from fastapi import Depends
from app.models.user import User
from app.core.security.token import (
    create_access_token,
    create_refresh_token,
    verify_password,
    verify_token,
    oauth2_scheme
)
from app.core.exceptions.auth import (
    InvalidCredentialsError,
    InvalidTokenError,
    UserNotFoundError,
    InvalidTokenTypeError
)
from app.schemas.auth import TokenResponse, RefreshTokenResponse
from app.settings.config import (
    ACCESS_TOKEN_EXPIRE_DELTA,
    REFRESH_TOKEN_EXPIRE_DELTA,
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES
)


class AuthService:
    """认证服务"""
    
    @staticmethod
    async def authenticate_user(username: str, password: str) -> User:
        """验证用户凭据"""
        user = await User.get_or_none(username=username)
        if not user or not user.verify_password(password):
            raise InvalidCredentialsError()
        return user

    @classmethod
    async def verify_token_and_get_user(cls, token: str) -> Tuple[User, Dict[str, Any]]:
        """
        验证令牌并获取用户
        :param token: JWT令牌
        :return: (用户对象, 解码后的令牌数据)
        :raises: InvalidTokenError 当令牌无效时
        :raises: UserNotFoundError 当用户不存在时
        """
        try:
            # 验证令牌
            decoded_token = verify_token(token)
            
            # 获取用户
            user = await User.get_or_none(id=decoded_token["uid"])
            if not user:
                raise UserNotFoundError()
                
            return user, decoded_token
            
        except Exception as e:
            raise InvalidTokenError()

    @staticmethod
    def create_tokens(user: User) -> TokenResponse:
        """创建访问令牌和刷新令牌"""
        token_data = {
            "uid": user.id,
            "sub": user.username,
            "scopes": [],  # 可以根据需要添加权限范围
        }
        
        access_token = create_access_token({**token_data, "type": "access"})
        refresh_token = create_refresh_token({**token_data, "type": "refresh"})
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=int(ACCESS_TOKEN_EXPIRE_DELTA.total_seconds()),
            refresh_expires_in=int(REFRESH_TOKEN_EXPIRE_DELTA.total_seconds()),
        )

    @classmethod
    async def get_current_user(
            cls,
            token: Annotated[str, Depends(oauth2_scheme)]
    ) -> User:
        """
        获取当前用户
        
        Args:
            token: JWT token
            
        Returns:
            User: 当前用户对象
            
        Raises:
            InvalidTokenError: 令牌无效或过期
            InvalidTokenTypeError: 令牌类型错误
            UserNotFoundError: 用户不存在
        """
        try:
            # 验证令牌
            payload = verify_token(token)
            uid: str = payload.get("uid")
            username: str = payload.get("sub")
            token_type: str = payload.get("type")

            if not uid or not username or not token_type:
                raise InvalidTokenError()

            # 确保是访问令牌
            if token_type != "access":
                raise InvalidTokenTypeError()

            # 获取用户
            user = await User.get_or_none(id=uid)
            if user is None:
                raise UserNotFoundError()

            return user

        except Exception:
            raise InvalidTokenError()

    @classmethod
    async def get_optional_user(
            cls,
            token: Annotated[str, Depends(oauth2_scheme)] = None
    ) -> Optional[User]:
        """
        获取可选的当前用户
        如果没有提供令牌或令牌无效，返回 None
        
        Args:
            token: JWT token，可选
            
        Returns:
            User | None: 当前用户对象，如果没有有效的令牌则返回 None
        """
        if not token:
            return None
            
        try:
            return await cls.get_current_user(token)
        except Exception:
            return None

    @staticmethod
    async def update_last_login(user: User) -> None:
        """更新用户最后登录时间"""
        user.last_login = datetime.now()
        await user.save()

    @staticmethod
    def get_user_response(user: User) -> Dict[str, Any]:
        """获取用户响应数据"""
        return {
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active,
            "is_superadmin": user.is_superadmin,
            "last_login": user.last_login
        }
        
    @classmethod
    async def login(cls, username: str, password: str) -> TokenResponse:
        """用户登录流程"""
        user = await cls.authenticate_user(username, password)
        await cls.update_last_login(user)
        return cls.create_tokens(user)
        
    @classmethod
    async def refresh_token(cls, token: str) -> RefreshTokenResponse:
        """
        刷新令牌流程
        仅生成新的访问令牌
        """
        user, _ = await cls.verify_token_and_get_user(token)
        
        # 创建新的访问令牌
        token_data = {
            "uid": user.id,
            "sub": user.username,
            "scopes": [],
        }
        access_token = create_access_token({**token_data, "type": "access"})
        
        return RefreshTokenResponse(
            access_token=access_token,
            expires_in=JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60  # 转换为秒
        )
        
    @classmethod
    async def get_user_by_token(cls, token: str) -> Dict[str, Any]:
        """通过令牌获取用户信息"""
        user, token_type = await cls.verify_token_and_get_user(token)
        return {
            "token_type": token_type.get("type"),
            "user": cls.get_user_response(user)
        }
