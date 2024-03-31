from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Схема для отображения пользователей."""
    pass


class UserCreate(schemas.BaseUserCreate):
    """схема для создания пользователей."""
    pass


class UserUpdate(schemas.BaseUserUpdate):
    """Схема для изменения пользователей."""
    pass