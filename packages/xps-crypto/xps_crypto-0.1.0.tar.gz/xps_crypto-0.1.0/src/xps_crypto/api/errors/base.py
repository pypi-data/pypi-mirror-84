from __future__ import annotations

from typing import List, Union

from pydantic.main import BaseModel


class ApiError(BaseModel):
    code: int
    detail: str

    def as_api_exception(self, status_code: int) -> ApiErrorException:
        return ApiErrorException(status_code, self)


class FieldsValidationError(BaseModel):
    field_name: str
    error: ApiError


class ValidationErrorsAggregate(BaseModel):
    errors: List[FieldsValidationError]

    def as_api_exception(self, status_code: int) -> ApiErrorException:
        return ApiErrorException(status_code, self)


class ApiErrorException(Exception):
    status_code: int
    error: Union[ApiError, ValidationErrorsAggregate]

    def __init__(self, status_code: int, error: Union[ApiError, ValidationErrorsAggregate]):
        self.status_code = status_code
        self.error = error
