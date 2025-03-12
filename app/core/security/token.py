from datetime import datetime, timedelta, timezone
    
from typing import Dict, Any

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from app.settings.config import (
    JWT_SECRET_KEY,
    JWT_ALGORITHM,
    ACCESS_TOKEN_EXPIRE_DELTA,
    REFRESH_TOKEN_EXPIRE_DELTA
)

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """获取密码哈希"""
    return pwd_context.hash(password)


def create_token(data: Dict[str, Any], expires_delta: timedelta) -> str:
    """
    创建JWT token
    :param data: token数据
    :param expires_delta: 过期时间
    :return: token字符串
    """
    to_encode = data.copy()
    expire = datetime.now(tz=timezone.utc)+ expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def create_access_token(data: Dict[str, Any]) -> str:
    """创建访问令牌"""
    return create_token(data, ACCESS_TOKEN_EXPIRE_DELTA)


def create_refresh_token(data: Dict[str, Any]) -> str:
    """创建刷新令牌"""
    return create_token(data, REFRESH_TOKEN_EXPIRE_DELTA)


def verify_token(token: str) -> Dict[str, Any]:
    """
    验证JWT token
    :param token: token字符串
    :return: token数据
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
