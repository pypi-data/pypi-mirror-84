from .base import ApiError

ForbiddenOperation = ApiError(code=1000, detail="Данная операция запрещена для аккаунта.")
UnAuthorized = ApiError(code=1001, detail="Пользователь не авторизован.")
MethodNotImplemented = ApiError(code=1002, detail="Метод не реализован.")
