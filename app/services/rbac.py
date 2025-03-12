from typing import Optional, List
from app.models.rbac import Role, Permission
from app.schemas.rbac import RoleCreate, RoleUpdate, PermissionCreate, PermissionUpdate, PermissionTreeNode
from tortoise.expressions import Q

class RoleService:
    @staticmethod
    async def create_role(role_data: RoleCreate) -> Role:
        """创建角色"""
        # 检查角色名称和代码是否已存在
        existing_role = await Role.filter(
            Q(name=role_data.name) | Q(code=role_data.code)
        ).first()
        if existing_role:
            if existing_role.name == role_data.name:
                raise ValueError("角色名称已存在")
            raise ValueError("角色代码已存在")
            
        # 创建角色
        role = await Role.create(**role_data.model_dump())
        return role

    @staticmethod
    async def update_role(role_id: int, role_data: RoleUpdate) -> Role:
        """更新角色"""
        role = await Role.get_or_none(id=role_id)
        if not role:
            raise ValueError("角色不存在")
        
        # 检查更新的名称或代码是否与其他角色冲突
        update_data = role_data.model_dump(exclude_unset=True)
        if update_data:
            if 'name' in update_data or 'code' in update_data:
                query = Q()
                if 'name' in update_data:
                    query |= Q(name=update_data['name'])
                if 'code' in update_data:
                    query |= Q(code=update_data['code'])
                existing_role = await Role.filter(query).exclude(id=role_id).first()
                if existing_role:
                    if 'name' in update_data and existing_role.name == update_data['name']:
                        raise ValueError("角色名称已存在")
                    if 'code' in update_data and existing_role.code == update_data['code']:
                        raise ValueError("角色代码已存在")
            
            # 更新角色
            await role.update_from_dict(update_data)
            await role.save()
        
        return role

    @staticmethod
    async def delete_role(role_id: int) -> None:
        """删除角色"""
        role = await Role.get_or_none(id=role_id)
        if not role:
            raise ValueError("角色不存在")
        await role.delete()

    @staticmethod
    async def get_role(role_id: int) -> Optional[Role]:
        """获取角色详情"""
        return await Role.get_or_none(id=role_id)

    @staticmethod
    async def list_roles(
        page: int = 1,
        page_size: int = 10,
        name: Optional[str] = None,
        code: Optional[str] = None
    ) -> tuple[List[Role], int]:
        """获取角色列表"""
        query = Role.all()
        
        # 添加过滤条件
        if name:
            query = query.filter(name__icontains=name)
        if code:
            query = query.filter(code__icontains=code)
        
        # 获取总数
        total = await query.count()
        
        # 分页
        roles = await query.offset((page - 1) * page_size).limit(page_size)
        return roles, total

class PermissionService:
    @staticmethod
    async def create_permission(permission_data: PermissionCreate) -> Permission:
        """创建权限"""
        # 检查权限名称和代码是否已存在
        existing_permission = await Permission.filter(
            Q(name=permission_data.name) | Q(code=permission_data.code)
        ).first()
        if existing_permission:
            if existing_permission.name == permission_data.name:
                raise ValueError("权限名称已存在")
            raise ValueError("权限代码已存在")
        
        # 检查权限类型是否有效
        if permission_data.type not in Permission.TYPE_CHOICES:
            raise ValueError(f"无效的权限类型，可选值：{list(Permission.TYPE_CHOICES.keys())}")
        
        # 如果指定了父权限，检查父权限是否存在
        if permission_data.parent_id:
            parent = await Permission.get_or_none(id=permission_data.parent_id)
            if not parent:
                raise ValueError("父权限不存在")
        
        # 创建权限
        permission_dict = permission_data.model_dump()
        if permission_data.parent_id:
            permission_dict["parent_id"] = permission_data.parent_id
        permission = await Permission.create(**permission_dict)
        return permission

    @staticmethod
    async def update_permission(permission_id: int, permission_data: PermissionUpdate) -> Permission:
        """更新权限"""
        permission = await Permission.get_or_none(id=permission_id)
        if not permission:
            raise ValueError("权限不存在")
        
        # 检查更新的名称或代码是否与其他权限冲突
        update_data = permission_data.model_dump(exclude_unset=True)
        if update_data:
            if 'name' in update_data or 'code' in update_data:
                query = Q()
                if 'name' in update_data:
                    query |= Q(name=update_data['name'])
                if 'code' in update_data:
                    query |= Q(code=update_data['code'])
                existing_permission = await Permission.filter(query).exclude(id=permission_id).first()
                if existing_permission:
                    if 'name' in update_data and existing_permission.name == update_data['name']:
                        raise ValueError("权限名称已存在")
                    if 'code' in update_data and existing_permission.code == update_data['code']:
                        raise ValueError("权限代码已存在")
            
            # 检查权限类型是否有效
            if 'type' in update_data and update_data['type'] not in Permission.TYPE_CHOICES:
                raise ValueError(f"无效的权限类型，可选值：{list(Permission.TYPE_CHOICES.keys())}")
            
            # 检查父权限是否存在且不是自己
            if 'parent_id' in update_data:
                if update_data['parent_id'] == permission_id:
                    raise ValueError("不能将自己设为父权限")
                if update_data['parent_id']:
                    parent = await Permission.get_or_none(id=update_data['parent_id'])
                    if not parent:
                        raise ValueError("父权限不存在")
            
            # 更新权限
            await permission.update_from_dict(update_data)
            await permission.save()
        
        return permission

    @staticmethod
    async def delete_permission(permission_id: int):
        """删除权限"""
        permission = await Permission.get_or_none(id=permission_id)
        if not permission:
            raise ValueError("权限不存在")
        
        # 检查是否有子权限
        has_children = await Permission.filter(parent_id=permission_id).exists()
        if has_children:
            raise ValueError("该权限存在子权限，无法删除")
        
        # 删除权限
        await permission.delete()

    @staticmethod
    async def get_permission(permission_id: int) -> Permission:
        """获取权限详情"""
        permission = await Permission.get_or_none(id=permission_id)
        if not permission:
            raise ValueError("权限不存在")
        return permission

    @staticmethod
    async def list_permissions(
        page: int = 1,
        page_size: int = 10,
        name: Optional[str] = None,
        code: Optional[str] = None,
        type: Optional[str] = None
    ) -> tuple[List[Permission], int]:
        """获取权限列表"""
        query = Permission.all()
        
        # 应用过滤条件
        if name:
            query = query.filter(name__icontains=name)
        if code:
            query = query.filter(code__icontains=code)
        if type:
            if type not in Permission.TYPE_CHOICES:
                raise ValueError(f"无效的权限类型，可选值：{list(Permission.TYPE_CHOICES.keys())}")
            query = query.filter(type=type)
        
        # 计算总数
        total = await query.count()
        
        # 分页查询
        permissions = await query.offset((page - 1) * page_size).limit(page_size).all()
        
        return permissions, total

    @staticmethod
    async def get_permission_tree() -> List[PermissionTreeNode]:
        """获取权限树"""
        # 获取所有权限
        permissions = await Permission.all().order_by('sort_order')
        
        # 构建权限字典，key 是权限 ID
        permission_dict = {p.id: PermissionTreeNode(
            id=p.id,
            name=p.name,
            code=p.code,
            description=p.description,
            type=p.type,
            path=p.path,
            parent_id=p.parent_id,
            sort_order=p.sort_order,
            children=[]
        ) for p in permissions}
        
        # 构建树形结构
        root_nodes = []
        for permission in permission_dict.values():
            if permission.parent_id is None:
                root_nodes.append(permission)
            else:
                parent = permission_dict.get(permission.parent_id)
                if parent:
                    parent.children.append(permission)
        
        return root_nodes
