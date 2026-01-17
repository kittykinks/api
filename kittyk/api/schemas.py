from typing import Annotated

from fastapi import Query
from fastapi.responses import JSONResponse

from pydantic import BaseModel, Field


class Error(BaseModel):
    title: str
    message: str


class BaseError(Exception):
    status_code: int = 400
    title: str = "Error"
    message: str = "An error occurred"

    def __init__(
        self,
        title: str | None = None,
        message: str | None = None,
        status_code: int | None = None,
    ):
        if title is not None:
            self.title = title

        if message is not None:
            self.message = message

        if status_code is not None:
            self.status_code = status_code

    @classmethod
    async def handler(cls, _request, exc: "BaseError"):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "title": exc.title if hasattr(exc, "title") else cls.title,
                "message": exc.message if hasattr(exc, "message") else cls.message,
            },
        )


class Page[T](BaseModel):
    items: list[T]
    total: int


class _PageParams(BaseModel):
    limit: int = Field(25, le=100)
    offset: int = 0


PageParams = Annotated[_PageParams, Query()]


class Message(BaseModel):
    message: str
