from datetime import timezone

import nanoid

from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from tortoise import transactions
from tortoise.exceptions import IntegrityError

from kittyk.db import User, Site
from kittyk.lib import discord, settings, catbox


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/discord/callback")
@transactions.atomic()
async def login_with_discord_callback(code: str) -> RedirectResponse:
    discord_user = await discord.get_user(code)

    user, is_new = await User.get_or_create(
        discord_id=discord_user.id,
    )

    if is_new:
        avatar_url = None
        banner_url = None

        if discord_user.avatar_url:
            avatar_url = await catbox.upload(url=discord_user.avatar_url)

        if discord_user.banner_url:
            banner_url = await catbox.upload(url=discord_user.banner_url)

        try:
            await Site.create(
                user_id=user.id,
                name=discord_user.name,
                slug=discord_user.username,
                avatar_url=avatar_url,
                banner_url=banner_url,
            )

        except IntegrityError:
            slug = nanoid.generate()

            await Site.create(
                user_id=user.id,
                name=discord_user.name,
                slug=slug,
                avatar_url=avatar_url,
                banner_url=banner_url,
            )

    session = await user.create_session()

    response = RedirectResponse(url=settings.LOGIN_NEXT_URL)
    response.set_cookie(
        key="session",
        value=session.id,
        httponly=True,
        expires=session.expires_at.astimezone(timezone.utc),
    )

    return response
