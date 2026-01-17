from fastapi import APIRouter

from kittyk.db import Kink, KinkRating
from kittyk.api.errors import NotFoundError
from kittyk.api.schemas import Page
from kittyk.api.dependencies import UserAuth
from kittyk.api.kinks.schemas import KinkSchema, RateKinkSchema


router = APIRouter(prefix="/kinks", tags=["Kinks"])


@router.get("")
async def list_kinks(auth: UserAuth) -> Page[KinkSchema]:
    """List all kinks."""

    kinks = await Kink.all().order_by("name")
    ratings = await KinkRating.filter(user_id=auth.user.id).all()

    return Page(
        total=len(kinks),
        items=[
            KinkSchema.from_orm(
                kink,
                next((rating for rating in ratings if rating.kink_id == kink.id), None),
            )
            for kink in kinks
        ],
    )


@router.get("/{kink_id}")
async def get_kink(auth: UserAuth, kink_id: str) -> KinkSchema:
    """Get a kink by ID."""

    kink = await Kink.get_or_none(id=kink_id)

    if kink is None:
        raise NotFoundError("kink")

    rating = await KinkRating.get_or_none(kink_id=kink_id, user_id=auth.user.id)

    return KinkSchema.from_orm(kink, rating)


@router.post("/{kink_id}/rating")
async def rate_kink(
    auth: UserAuth, kink_id: str, rate_kink: RateKinkSchema
) -> KinkSchema:
    kink = await Kink.get_or_none(id=kink_id)

    if kink is None:
        raise NotFoundError("kink")

    rating = await KinkRating.get_or_none(kink_id=kink_id, user_id=auth.user.id)

    if rating is None:
        rating = await KinkRating.create(
            kink_id=kink_id,
            user_id=auth.user.id,
            rating=rate_kink.rating,
            comment=rate_kink.comment,
        )

    else:
        rating.rating = rate_kink.rating
        rating.comment = rate_kink.comment

        await rating.save()

    return KinkSchema.from_orm(kink, rating)


@router.delete("/{kink_id}/rating")
async def delete_kink_rating(auth: UserAuth, kink_id: str) -> KinkSchema:
    kink = await Kink.get_or_none(id=kink_id)

    if kink is None:
        raise NotFoundError("kink")

    await KinkRating.filter(kink_id=kink_id, user_id=auth.user.id).delete()

    return KinkSchema.from_orm(kink, None)
