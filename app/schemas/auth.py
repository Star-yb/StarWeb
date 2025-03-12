from pydantic import BaseModel

class TokenResponse(BaseModel):
    """令牌响应模型"""
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    refresh_expires_in: int

class RefreshTokenResponse(BaseModel):
    """刷新令牌的响应模型"""
    access_token: str
    expires_in: int

class LoginRequest(BaseModel):
    """登录请求模型"""
    username: str
    password: str

class RefreshTokenRequest(BaseModel):
    """刷新令牌请求模型"""
    refresh_token: str

class TokenRequest(BaseModel):
    """令牌请求模型"""
    token: str
