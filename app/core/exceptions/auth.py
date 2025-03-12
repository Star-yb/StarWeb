from fastapi import HTTPException, status


class AuthenticationError(HTTPException):
    """认证相关错误的基类"""

    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class InvalidCredentialsError(AuthenticationError):
    """无效的凭证"""

    def __init__(self):
        super().__init__("Incorrect username or password")


class InvalidTokenError(AuthenticationError):
    """无效的令牌"""

    def __init__(self):
        super().__init__("Token has expired or is invalid")


class InvalidTokenTypeError(AuthenticationError):
    """无效的令牌类型"""

    def __init__(self):
        super().__init__("Invalid token type")


class UserNotFoundError(AuthenticationError):
    """用户不存在"""

    def __init__(self):
        super().__init__("User not found")


class MissingTokenError(HTTPException):
    """缺少令牌"""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Missing token"
        )
