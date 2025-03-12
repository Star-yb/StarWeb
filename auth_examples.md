# 认证与鉴权使用案例

Star Web 项目提供了完整的认证与鉴权系统，支持基于角色和权限的访问控制。所有鉴权相关功能都封装在 `app/core/security/deps.py` 中，便于在 API 路由中使用。

## 认证方式

项目使用 JWT 双令牌认证系统，包含：
- **访问令牌 (Access Token)**: 短期有效，用于 API 访问认证
- **刷新令牌 (Refresh Token)**: 长期有效，用于获取新的访问令牌

## 鉴权装饰器与实际使用案例

项目中提供了多种鉴权装饰器，以下是在 `app/api/rest/user.py` 中的实际使用案例：

### 1. 基础用户认证

使用 `get_current_user` 依赖项来验证用户身份：

```python
@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_user)
):
    """获取用户详情"""
    try:
        user = await UserService.get_user(user_id)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
```

### 2. 超级管理员权限检查

使用 `get_current_active_superuser` 依赖项来验证超级管理员权限：

```python
@router.delete(
    "/{user_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_active_superuser)]  # 只有超级管理员可以删除用户
)
async def delete_user(user_id: int):
    """删除用户 (需要超级管理员权限)"""
    try:
        await UserService.delete_user(user_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
```

或使用 `require_superuser()` 依赖项：

```python
@router.post(
    "/{user_id}/reset-password",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_superuser())]  # 只有超级管理员可以重置密码
)
async def reset_user_password(user_id: int):
    """重置用户密码 (需要超级管理员权限)"""
    return "访问成功"
```

### 3. 活跃用户检查

使用 `require_active_user()` 依赖项确保用户处于活跃状态：

```python
@router.get(
    "/me/me", 
    response_model=UserResponse,
    dependencies=[Depends(require_active_user())]  # 确保用户处于活跃状态
)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """获取当前登录用户信息 (需要用户处于活跃状态)"""
    return current_user
```

### 4. 角色检查

使用 `require_roles()` 依赖项检查用户角色：

```python
@router.get(
    "/admin/dashboard",
    dependencies=[Depends(require_roles("admin"))]  # 只有管理员可以访问仪表盘
)
async def admin_dashboard():
    """管理员仪表盘 (需要admin角色)"""
    return "访问成功"
```

### 5. 获取用户权限和角色

使用 `get_current_user_permissions` 和 `get_current_user_roles` 获取当前用户的权限和角色：

```python
@router.get(
    "/me/permissions", 
    response_model=List[str]
)
async def get_my_permissions(
    current_user: User = Depends(get_current_user)
):
    """获取当前用户的权限列表"""
    permissions = await get_current_user_permissions(current_user)
    return permissions

@router.get(
    "/me/roles", 
    response_model=List[str]
)
async def get_my_roles(
    current_user: User = Depends(get_current_user)
):
    """获取当前用户的角色列表"""
    roles = await get_current_user_roles(current_user)
    return roles
```

### 6. 组合条件检查 - 满足任意条件

使用 `require_any()` 组合多个条件，满足任意一个即可：

```python
@router.post(
    "/{user_id}/activate",
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(require_any(
            lambda: require_roles("admin"),
            lambda: require_permissions(["user.manage", "user.reset-password"])
        ))
    ]
)
async def activate_user(
    user_id: int,
    current_user: User = Depends(get_current_user)
):
    """
    激活用户账号
    
    权限要求（满足以下任意一个条件）：
    - 拥有admin角色
    - 拥有user.manage和user.reset-password权限
    """
    return "访问成功"
```

### 7. 组合条件检查 - 满足所有条件

使用 `require_all()` 组合多个条件，必须同时满足所有条件：

```python
@router.post(
    "/{user_id}/deactivate",
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(require_all(
            lambda: require_permissions("user.manage"),
            lambda: require_roles(["admin", "supervisor"], require_all=False)
        ))
    ]
)
async def deactivate_user(
    user_id: int,
    current_user: User = Depends(get_current_user)
):
    """
    禁用用户账号
    
    权限要求（必须同时满足以下所有条件）：
    - 拥有user.manage权限
    - 拥有admin或supervisor角色之一
    """
    return "访问成功"
```

## 权限检查装饰器的使用方式

项目中提供了多种权限检查装饰器的使用方式：

1. **作为路由依赖项**：直接在路由函数参数中使用
   ```python
   async def some_function(
       current_user: User = Depends(get_current_user)
   ):
       pass
   ```

2. **作为路由装饰器依赖项**：在路由装饰器的 dependencies 参数中使用
   ```python
   @router.post(
       "/some-path",
       dependencies=[Depends(require_permissions("some.permission"))]
   )
   async def some_function():
       pass
   ```

3. **组合多个权限检查**：使用 `require_all` 和 `require_any` 组合多个权限检查
   ```python
   dependencies=[
       Depends(require_all(
           lambda: require_permissions("permission1"),
           lambda: require_roles("role1")
       ))
   ]
   ```

## 在前端使用认证

前端应用需要在请求头中包含访问令牌：

```javascript
// 发送带有认证的请求
async function fetchProtectedResource() {
  const response = await fetch('http://localhost:8005/api/users/me', {
    headers: {
      'Authorization': `Bearer ${accessToken}`
    }
  });
  return await response.json();
}

// 当访问令牌过期时，使用刷新令牌获取新的访问令牌
async function refreshAccessToken() {
  const response = await fetch('http://localhost:8005/api/auth/refresh', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      refresh_token: refreshToken
    })
  });
  
  const data = await response.json();
  // 保存新的访问令牌
  localStorage.setItem('accessToken', data.access_token);
  return data.access_token;
}
```
