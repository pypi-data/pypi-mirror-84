from pydantic import BaseModel


class SomeRequest(BaseModel):
    key: str
    value: str


class SomeResponse(BaseModel):
    success: bool
