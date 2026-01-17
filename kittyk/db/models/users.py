from datetime import datetime, timezone, timedelta

from tortoise import fields
from tortoise.models import Model

from kittyk.db.fields import IDField
from kittyk.db.models.sites import Site, KinkRating, Link


class User(Model):
    id = IDField()

    discord_id = fields.CharField(max_length=32, unique=True, null=True)

    site: fields.BackwardOneToOneRelation[Site]
    links: fields.ReverseRelation[Link]
    kink_ratings: fields.ReverseRelation[KinkRating]

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    async def create_session(self, expires_at: datetime = ...) -> "Session":
        """Creates a new session for the user.

        Args:
            expires_at (datetime, optional): The expiration date of the session.
                Defaults to 7 days from now.

        Returns:
            Session: The created session.

        Raises:
            tortoise.exceptions.BaseORMException: If the session could not be created.
        """

        if expires_at is ...:
            expires_at = datetime.now(timezone.utc) + timedelta(days=7)

        session = await Session.create(user=self, expires_at=expires_at)

        return session


class Session(Model):
    id = IDField()

    user = fields.ForeignKeyField("models.User", related_name="sessions")

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    expires_at = fields.DatetimeField()
