from fastapi import HTTPException, status


class MarketplaceException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


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
