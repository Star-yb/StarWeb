from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "permissions" (
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP /* 创建时间 */,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP /* 更新时间 */,
    "is_deleted" INT NOT NULL  DEFAULT 0 /* 是否逻辑删除 */,
    "deleted_at" TIMESTAMP   /* 删除时间 */,
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL /* 主键ID */,
    "name" VARCHAR(100) NOT NULL UNIQUE /* 权限名称 */,
    "code" VARCHAR(100) NOT NULL UNIQUE /* 权限代码 */,
    "description" TEXT   /* 权限描述 */,
    "type" VARCHAR(20) NOT NULL  /* 权限类型 */,
    "path" VARCHAR(200)   /* 路由路径 */,
    "sort_order" INT NOT NULL  DEFAULT 0 /* 排序序号 */,
    "parent_id" INT REFERENCES "permissions" ("id") ON DELETE SET NULL /* 父权限 */
) /* 权限表 */;
CREATE TABLE IF NOT EXISTS "roles" (
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP /* 创建时间 */,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP /* 更新时间 */,
    "is_deleted" INT NOT NULL  DEFAULT 0 /* 是否逻辑删除 */,
    "deleted_at" TIMESTAMP   /* 删除时间 */,
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL /* 主键ID */,
    "name" VARCHAR(50) NOT NULL UNIQUE /* 角色名称 */,
    "code" VARCHAR(50) NOT NULL UNIQUE /* 角色代码 */,
    "description" TEXT   /* 角色描述 */,
    "is_system" INT NOT NULL  DEFAULT 0 /* 是否系统内置 */
) /* 角色表 */;
CREATE TABLE IF NOT EXISTS "users" (
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP /* 创建时间 */,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP /* 更新时间 */,
    "is_deleted" INT NOT NULL  DEFAULT 0 /* 是否逻辑删除 */,
    "deleted_at" TIMESTAMP   /* 删除时间 */,
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL /* 主键ID */,
    "password_hash" VARCHAR(128) NOT NULL  /* 密码哈希 */,
    "username" VARCHAR(50) NOT NULL UNIQUE /* 用户名 */,
    "email" VARCHAR(100) NOT NULL  /* 邮箱地址 */,
    "is_active" INT NOT NULL  DEFAULT 1 /* 是否激活 */,
    "is_superadmin" INT NOT NULL  DEFAULT 0 /* 是否是超级管理员 */,
    "last_login" TIMESTAMP   /* 最后登录时间 */
) /* 用户信息表 */;
CREATE INDEX IF NOT EXISTS "idx_users_usernam_266d85" ON "users" ("username");
CREATE INDEX IF NOT EXISTS "idx_users_email_133a6f" ON "users" ("email");
CREATE TABLE IF NOT EXISTS "user_roles" (
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP /* 创建时间 */,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP /* 更新时间 */,
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL /* 主键ID */,
    "data_scope" VARCHAR(20) NOT NULL  DEFAULT 'self' /* 数据权限范围 */,
    "role_id" INT NOT NULL REFERENCES "roles" ("id") ON DELETE CASCADE /* 角色 */,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE /* 用户 */,
    CONSTRAINT "uid_user_roles_user_id_63f1a8" UNIQUE ("user_id", "role_id")
) /* 用户角色关联表 */;
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);
CREATE TABLE IF NOT EXISTS "roles_permissions" (
    "roles_id" INT NOT NULL REFERENCES "roles" ("id") ON DELETE CASCADE,
    "permission_id" INT NOT NULL REFERENCES "permissions" ("id") ON DELETE CASCADE
) /* 角色拥有的权限 */;
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_roles_permi_roles_i_74c3df" ON "roles_permissions" ("roles_id", "permission_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
