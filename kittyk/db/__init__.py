import json

from aerich import Command

from tortoise import Tortoise, connections

from kittyk.db.models.users import User as User, Session as Session
from kittyk.db.models.kinks import Kink as Kink
from kittyk.db.models.sites import (
    Site as Site,
    KinkRating as KinkRating,
    Link as Link,
    LinkSource as LinkSource,
)
from kittyk.lib import settings


CONFIG = {
    "connections": {"default": settings.DATABASE_URL},
    "apps": {
        "models": {
            "models": [
                "kittyk.db.models.users",
                "kittyk.db.models.kinks",
                "kittyk.db.models.sites",
                "aerich.models",
            ],
            "default_connection": "default",
        }
    },
    "use_tz": True,
    "timezone": "UTC",
}


async def on_startup():
    """Connects to the database and creates the missing schemas on FastAPI startup."""

    async with Command(
        tortoise_config=CONFIG, app="models", location="kittyk/db/migrations"
    ) as command:
        await command.upgrade()

    await Tortoise.init(config=CONFIG)

    if await Kink.all().count() == 0:
        kinks = json.load(open("kinks.json", "r"))

        for kink in kinks["entries"].values():
            await Kink.create(name=kink["name"].strip(), description=kink["content"])


async def on_shutdown():
    """Closes the database connections on FastAPI shutdown."""

    await connections.close_all()
