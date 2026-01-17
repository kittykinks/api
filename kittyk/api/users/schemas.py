from pydantic import BaseModel

from kittyk.db import User


class UserSchema(BaseModel):
    id: str

    discord_id: str

    @classmethod
    def from_orm(cls, obj: User):
        return cls(
            id=obj.id,
            discord_id=obj.discord_id,
        )
