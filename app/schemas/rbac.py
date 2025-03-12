from typing import Optional, List
from pydantic import BaseModel

class RoleCreate(BaseModel):
    """创建角色的请求模型"""
    name: str
    code: str
    description: Optional[str] = None

class RoleUpdate(BaseModel):
    """更新角色的请求模型"""
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None

class RoleResponse(BaseModel):
    """角色响应模型"""
    id: int
    name: str
    code: str
    description: Optional[str] = None
    
    class Config:
        from_attributes = True

class RoleList(BaseModel):
    """角色列表响应模型"""
    total: int
    items: List[RoleResponse]

class PermissionCreate(BaseModel):
    """创建权限的请求模型"""
    name: str
    code: str
    description: Optional[str] = None
    type: str  # menu/button/api
    path: Optional[str] = None
    parent_id: Optional[int] = None
    sort_order: Optional[int] = 0

class PermissionUpdate(BaseModel):
    """更新权限的请求模型"""
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    path: Optional[str] = None
    parent_id: Optional[int] = None
    sort_order: Optional[int] = None

class PermissionResponse(BaseModel):
    """权限响应模型"""
    id: int
    name: str
    code: str
    description: Optional[str] = None
    type: str
    path: Optional[str] = None
    parent_id: Optional[int] = None
    sort_order: int
    
    class Config:
        from_attributes = True

class PermissionTreeNode(PermissionResponse):
    """权限树节点"""
    children: List['PermissionTreeNode'] = []

class PermissionList(BaseModel):
    """权限列表响应模型"""
    total: int
    items: List[PermissionResponse]
