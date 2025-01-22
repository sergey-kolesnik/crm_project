from typing import Optional

from fastapi import (
    HTTPException,
    status,
)


class DatabaseError(HTTPException):
    """
    Исключение, которое используется для обработки ошибок, связанных с базой данных.

    Возвращает HTTP-ответ со статусом 500 (Внутренняя ошибка сервера)
    и подробным описанием ошибки.

    Args:
        detail: Подробное описание ошибки, связанной с базой данных.
    """
    def __init__(self, detail: str, headers: Optional[dict] = None):
        """
    Инициализирует исключение DatabaseError.

    Args:
        detail: Подробное описание ошибки, связанной с базой данных.
        headers: Дополнительные заголовки HTTP-ответа.
        """
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=detail,
            headers=headers,
            )
        

class UniqueViolationError(HTTPException):
    """
    Исключение, которое используется, когда нарушается уникальное ограничение.

    Возвращает HTTP-ответ со статусом 400 (Неверный запрос)
    и подробным описанием ошибки.
    """
     
    def __init__(self, detail = None, headers: Optional[dict] = None):
        """
        Инициализирует исключение UniqueViolationError.

        Args:
            detail: Подробное описание ошибки, связанной с базой данных.
            headers: Дополнительные заголовки HTTP-ответа.
        """
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail, headers=headers)


class NotFoundError(HTTPException):
    """
    Исключение, которое используется когда сущность не найдена
    Возвращает
    """

    def __init__(self, detail = None, headers: Optional[dict] = None):
        """
        Инициализирует исключение NotFoundError.
        Args:
            detail: Подробное описание ошибки, связанной с базой данных.
            headers: Дополнительные заголовки HTTP-ответа
        """

        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail, headers=headers)