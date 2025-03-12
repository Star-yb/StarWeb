from functools import wraps
from typing import List, Optional, Set, Union, Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt


from app.models.rbac import Permission, Role, UserRole
from app.settings import config as settings
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """获取当前用户，如果token无效则抛出异常"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效的认证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: str = payload.get("uid")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = await User.get_or_none(id=user_id)
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户已被禁用"
        )
    return user

async def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    """获取当前超级管理员用户"""
    if not current_user.is_superadmin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足，需要超级管理员权限"
        )
    return current_user

async def get_current_user_permissions(
    current_user: User = Depends(get_current_user)
) -> Set[str]:
    """获取当前用户的权限集合"""
    if current_user.is_superadmin:
        return set("*")  # 超级用户返回所有权限

   # 获取当前用户的所有角色
    roles = await UserRole.filter(user=current_user).values_list("role__id", flat=True)

    # 获取这些角色的所有权限代码
    # 返回权限集合
    return set(await Permission.filter(roles__id__in=roles).values_list('code', flat=True))

async def get_current_user_roles(
    current_user: User = Depends(get_current_user)
) -> Set[str]:
    """获取当前用户的角色集合"""
    
    return set(await UserRole.filter(user=current_user).values_list("role__code", flat=True))

def require_permissions(permissions: Union[str, List[str]], require_all: bool = True):
    """
    权限检查装饰器
    :param permissions: 单个权限字符串或权限列表
    :param require_all: True表示需要所有权限，False表示只需要其中一个权限
    """
    if isinstance(permissions, str):
        permissions = [permissions]

    async def check_permissions(current_user: User = Depends(get_current_user)):
        if current_user.is_superadmin:
            return
        
        user_permissions = await get_current_user_permissions(current_user)
        if require_all:
            if not all(perm in user_permissions for perm in permissions):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"权限不足，需要以下所有权限: {', '.join(permissions)}"
                )
        else:
            if not any(perm in user_permissions for perm in permissions):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"权限不足，需要以下任意一个权限: {', '.join(permissions)}"
                )
    
    return check_permissions

def require_roles(roles: Union[str, List[str]], require_all: bool = True):
    """
    角色检查装饰器
    :param roles: 单个角色字符串或角色列表
    :param require_all: True表示需要所有角色，False表示只需要其中一个角色
    """
    if isinstance(roles, str):
        roles = [roles]

    async def check_roles(current_user: User = Depends(get_current_user)):
        if current_user.is_superadmin:
            return
        
        user_roles = await get_current_user_roles(current_user)
        if require_all:
            if not all(role in user_roles for role in roles):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"角色不足，需要以下所有角色: {', '.join(roles)}"
                )
        else:
            if not any(role in user_roles for role in roles):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"角色不足，需要以下任意一个角色: {', '.join(roles)}"
                )
    
    return check_roles

def require_active_user():
    """检查用户是否处于活动状态"""
    async def check_active(current_user: User = Depends(get_current_user)):
        if not current_user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="用户已被禁用"
            )
        return current_user
    return check_active

def require_superuser():
    """检查用户是否是超级管理员"""
    async def check_superuser(current_user: User = Depends(get_current_user)):
        if not current_user.is_superadmin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="需要超级管理员权限"
            )
        return current_user
    return check_superuser

def require_any(*requirements: Callable) -> Callable:
    """
    组合多个权限检查，只要满足其中任意一个即可
    :param requirements: 权限检查函数列表
    """
    async def check_any(current_user: User = Depends(get_current_user)):
        if current_user.is_superadmin:
            return
        
        # 收集所有错误信息
        errors = []
        for requirement in requirements:
            try:
                # 尝试执行每个权限检查
                await requirement()(current_user)
                # 如果有一个检查通过，直接返回
                return
            except HTTPException as e:
                # 收集错误信息
                errors.append(e.detail)
        
        # 如果所有检查都失败，抛出组合的错误信息

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"需要满足以下条件之一: {' 或 '.join(errors)}"
        )
    
    return check_any

def require_all(*requirements: Callable) -> Callable:
    """
    组合多个权限检查，必须同时满足所有条件
    :param requirements: 权限检查函数列表
    """
    async def check_all(current_user: User = Depends(get_current_user)):
        if current_user.is_superadmin:
            return
        
        # 依次执行所有权限检查
        for requirement in requirements:
            await requirement()(current_user)
        
        # 如果所有检查都通过，返回
        return
    
    return check_all