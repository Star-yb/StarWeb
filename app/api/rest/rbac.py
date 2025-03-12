from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.rbac import (
    RoleCreate, RoleUpdate, RoleResponse, RoleList,
    PermissionCreate, PermissionUpdate, PermissionResponse, PermissionList, PermissionTreeNode
)
from app.services.rbac import RoleService, PermissionService
from app.models.user import User
from app.core.security.deps import get_current_user

roles_router = APIRouter(prefix="", tags=["角色管理"])
permissions_router = APIRouter(prefix="", tags=["权限管理"])


@roles_router.post("", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(
    role_data: RoleCreate,
    current_user: User = Depends(get_current_user)
):
    """创建角色"""
    try:
        role = await RoleService.create_role(role_data)
        return role
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@roles_router.put("/{role_id}", response_model=RoleResponse)
async def update_role(
    role_id: int,
    role_data: RoleUpdate,
    current_user: User = Depends(get_current_user)
):
    """更新角色"""
    try:
        role = await RoleService.update_role(role_id, role_data)
        return role
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@roles_router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
    role_id: int,
    current_user: User = Depends(get_current_user)
):
    """删除角色"""
    try:
        await RoleService.delete_role(role_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@roles_router.get("/{role_id}", response_model=RoleResponse)
async def get_role(
    role_id: int,
    current_user: User = Depends(get_current_user)
):
    """获取角色详情"""
    role = await RoleService.get_role(role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="角色不存在"
        )
    return role

@roles_router.get("", response_model=RoleList)
async def list_roles(
    page: int = 1,
    page_size: int = 10,
    name: Optional[str] = None,
    code: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """获取角色列表"""
    roles, total = await RoleService.list_roles(page, page_size, name, code)
    return {
        "total": total,
        "items": roles
    }

# 权限相关接口
@permissions_router.post("", response_model=PermissionResponse, status_code=status.HTTP_201_CREATED)
async def create_permission(
    permission_data: PermissionCreate,
    current_user: User = Depends(get_current_user)
):
    """创建权限"""
    try:
        permission = await PermissionService.create_permission(permission_data)
        return permission
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@permissions_router.put("/{permission_id}", response_model=PermissionResponse)
async def update_permission(
    permission_id: int,
    permission_data: PermissionUpdate,
    current_user: User = Depends(get_current_user)
):
    """更新权限"""
    try:
        permission = await PermissionService.update_permission(permission_id, permission_data)
        return permission
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@permissions_router.delete("/{permission_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_permission(
    permission_id: int,
    current_user: User = Depends(get_current_user)
):
    """删除权限"""
    try:
        await PermissionService.delete_permission(permission_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@permissions_router.get("/{permission_id}", response_model=PermissionResponse)
async def get_permission(
    permission_id: int,
    current_user: User = Depends(get_current_user)
):
    """获取权限详情"""
    try:
        permission = await PermissionService.get_permission(permission_id)
        return permission
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@permissions_router.get("", response_model=PermissionList)
async def list_permissions(
    page: int = 1,
    page_size: int = 10,
    name: Optional[str] = None,
    code: Optional[str] = None,
    type: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """获取权限列表"""
    try:
        permissions, total = await PermissionService.list_permissions(
            page=page,
            page_size=page_size,
            name=name,
            code=code,
            type=type
        )
        return {
            "total": total,
            "items": permissions
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@permissions_router.get("/tree", response_model=List[PermissionTreeNode])
async def get_permission_tree(
    current_user: User = Depends(get_current_user)
):
    """获取权限树"""
    return await PermissionService.get_permission_tree()
