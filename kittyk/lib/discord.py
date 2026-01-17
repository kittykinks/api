from dataclasses import dataclass

from httpx import AsyncClient

from kittyk.lib.settings import (
    DISCORD_CLIENT_ID,
    DISCORD_CLIENT_SECRET,
    DISCORD_REDIRECT_URI,
)


@dataclass
class DiscordUser:
    id: str
    username: str
    name: str
    avatar_hash: str | None
    banner_hash: str | None

    @property
    def avatar_url(self) -> str | None:
        if self.avatar_hash is None:
            return None

        return f"https://cdn.discordapp.com/avatars/{self.id}/{self.avatar_hash}.png"
    
    @property
    def banner_url(self) -> str | None:
        if self.banner_hash is None:
            return None

        return f"https://cdn.discordapp.com/banners/{self.id}/{self.banner_hash}.png"


DISCORD_API_ENDPOINT = "https://discord.com/api/v10"


http = AsyncClient()


async def _get_token(code: str) -> str:
    response = await http.post(
        "%s/oauth2/token" % DISCORD_API_ENDPOINT,
        data={
            "client_id": DISCORD_CLIENT_ID,
            "client_secret": DISCORD_CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": DISCORD_REDIRECT_URI,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    response.raise_for_status()

    data = response.json()
    return data["access_token"]


async def _get_user(access_token: str) -> DiscordUser:
    response = await http.get(
        "%s/users/@me" % DISCORD_API_ENDPOINT,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    response.raise_for_status()

    data = response.json()
    return DiscordUser(
        id=data["id"],
        username=data["username"],
        name=data["global_name"] or data["username"],
        avatar_hash=data["avatar"],
        banner_hash=data["banner"],
    )


async def get_user(code: str) -> DiscordUser:
    access_token = await _get_token(code)
    user = await _get_user(access_token)

    return user
