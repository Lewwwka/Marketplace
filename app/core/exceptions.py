from fastapi import HTTPException, status


class AlredyRegisterException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Этот email уже зарегистрирован",
        )


class NotFoundException(HTTPException):
    def __init__(self, entity: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{entity} не найден"
        )


class ForbiddenException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN, detail="Нет прав доступа"
        )


class UnauthorizedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не авторизован",
        )
