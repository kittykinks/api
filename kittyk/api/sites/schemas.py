from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl
from pydantic_core import MISSING

from kittyk.db import Site, Link, LinkSource
from kittyk.api.kinks.schemas import KinkSchema


class SiteSchema(BaseModel):
    id: str

    slug: str = Field(max_length=32)
    name: str = Field(max_length=64)
    bio: str | None = Field(max_length=128)

    avatar_url: HttpUrl | None = Field(max_length=256)
    banner_url: HttpUrl | None = Field(max_length=256)

    kinks: list[KinkSchema] = Field(max_length=25)
    links: list["LinkSchema"] = Field(max_length=25)

    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_orm(cls, obj: Site) -> "SiteSchema":
        return cls(
            id=obj.id,
            slug=obj.slug,
            name=obj.name,
            bio=obj.bio,
            avatar_url=obj.avatar_url,
            banner_url=obj.banner_url,
            kinks=[
                KinkSchema.from_orm(kink_rating.kink, kink_rating)
                for kink_rating in obj.kink_ratings
            ],
            links=[LinkSchema.from_orm(link) for link in obj.links],
            created_at=obj.user.created_at,
            updated_at=obj.user.updated_at,
        )


class LinkSchema(BaseModel):
    id: str

    source: LinkSource
    pointer: str = Field(max_length=128)

    @classmethod
    def from_orm(cls, obj: Link) -> "LinkSchema":
        return cls(
            id=obj.id,
            source=obj.source,
            pointer=obj.pointer,
        )


class CreateLinkSchema(BaseModel):
    source: LinkSource
    url: str = Field(max_length=256)


class UpdateLinkSchema(BaseModel):
    source: LinkSource = MISSING
    url: str | None = MISSING
