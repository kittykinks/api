from typing import Annotated

from fastapi import APIRouter, Path, Query

from tortoise import transactions
from tortoise.models import Q

from pydantic_core import MISSING

from kittyk.db import Site
from kittyk.api.errors import ConflictError, ValidationError, NotFoundError
from kittyk.api.schemas import Page
from kittyk.api.dependencies import UserAuth
from kittyk.api.sites.schemas import (
    SiteSchema,
    LinkSchema,
    CreateLinkSchema,
    UpdateLinkSchema,
)


router = APIRouter(tags=["Sites"])


@router.get("/site/me")
async def get_my_site(auth: UserAuth) -> SiteSchema:
    site = (
        await auth.user.site.get()
        .prefetch_related("kink_ratings", "kink_ratings__kink", "links")
        .select_related("user")
    )

    return SiteSchema.from_orm(site)


@router.post("/site/me")
@transactions.atomic()
async def update_my_site(auth: UserAuth, site_update: SiteSchema) -> SiteSchema:
    site = await auth.user.site.get().select_related("user")

    existing_site = await Site.get_or_none(slug=site_update.slug)

    if existing_site and existing_site.id != site.id:
        raise ConflictError("The site slug is already in use.")

    site.slug = site_update.slug
    site.name = site_update.name
    site.bio = site_update.bio
    site.avatar_url = site_update.avatar_url
    site.banner_url = site_update.banner_url

    await site.links.all().delete()

    for link_data in site_update.links:
        await site.links.create(
            user_id=auth.user.id,
            source=link_data.source,
            pointer=link_data.pointer,
        )

    await site.kink_ratings.all().delete()

    for kink_rating_data in site_update.kinks:
        if kink_rating_data.rating is None:
            raise ValidationError("All kinks must have a rating. This one doesn't?")

        await site.kink_ratings.create(
            kink_id=kink_rating_data.id,
            user_id=auth.user.id,
            rating=kink_rating_data.rating,
            comment=kink_rating_data.comment,
        )

    await site.save()
    await site.fetch_related("kink_ratings", "kink_ratings__kink", "links")

    return SiteSchema.from_orm(site)


@router.get("/site/me/links")
async def get_my_site_links(auth: UserAuth) -> Page[LinkSchema]:
    links = await auth.user.links.all()

    return Page(
        total=len(links),
        items=[LinkSchema.from_orm(link) for link in links],
    )


@router.post("/site/me/links")
async def create_my_site_link(
    auth: UserAuth, create_link: CreateLinkSchema
) -> LinkSchema:
    site = await auth.user.site.get()

    link = await site.links.create(
        user_id=auth.user.id,
        source=create_link.source,
        url=create_link.url,
    )

    return LinkSchema.from_orm(link)


@router.get("/site/me/links/{link_id}")
async def get_my_site_link(auth: UserAuth, link_id: str) -> LinkSchema:
    site = await auth.user.site.get()
    link = await site.links.get_or_none(id=link_id)

    if link is None:
        raise ValidationError("link")

    return LinkSchema.from_orm(link)


@router.patch("/site/me/links/{link_id}")
async def update_my_site_link(
    auth: UserAuth, link_id: str, update_link: UpdateLinkSchema
) -> LinkSchema:
    site = await auth.user.site.get()
    link = await site.links.get_or_none(id=link_id)

    if link is None:
        raise ValidationError("link")

    if update_link.source is not MISSING:
        link.source = update_link.source

    if update_link.url is not MISSING:
        link.url = update_link.url

    await link.save()

    return LinkSchema.from_orm(link)


@router.delete("/site/me/links/{link_id}")
async def delete_my_site_link(auth: UserAuth, link_id: str) -> None:
    site = await auth.user.site.get()
    link = await site.links.get_or_none(id=link_id)

    if link is None:
        raise ValidationError("link")

    await link.delete()


@router.get("/sites/exists")
async def check_if_site_exists(
    query: Annotated[str, Query(description="The slug or ID of the site to check.")],
) -> bool:
    exists = await Site.filter(Q(id=query) | Q(slug=query)).exists()

    return exists


@router.get("/site/{site_id}")
async def get_site_by_slug(
    site_id: Annotated[
        str, Path(description="The ID of the site to retrieve, or its slug.")
    ],
) -> SiteSchema:
    site = (
        await Site.get_or_none(Q(id=site_id) | Q(slug=site_id))
        .prefetch_related("kink_ratings", "kink_ratings__kink", "links")
        .select_related("user")
    )

    if site is None:
        raise NotFoundError("site")

    return SiteSchema.from_orm(site)
