from pydantic import BaseModel, Field

from kittyk.db import Kink, KinkRating


class KinkSchema(BaseModel):
    id: str

    name: str
    description: str

    rating: int | None = Field(ge=0, le=10)
    comment: str | None = Field(max_length=32)

    @classmethod
    def from_orm(cls, kink: Kink, rating: KinkRating | None) -> "KinkSchema":
        return cls(
            id=kink.id,
            name=kink.name,
            description=kink.description,
            rating=rating.rating if rating else None,
            comment=rating.comment if rating else None,
        )


class RateKinkSchema(BaseModel):
    rating: int = Field(ge=0, le=10)
    comment: str | None = Field(min_length=1, max_length=32)
