from typing import Annotated

from fastapi import Cookie, Depends

from kittyk.db import Session, User
from kittyk.api.errors import UnauthorizedError


class _Auth:
    user: User
    session: Session

    @classmethod
    def from_token(cls, session: Session) -> "_Auth":
        auth = cls()

        auth.user = session.user
        auth.session = session

        return auth


async def _authenticate_session(session: str):
    session = await Session.get_or_none(id=session).select_related("user")

    return session


async def _authentication(
    session: Annotated[str, Cookie()],
) -> _Auth:
    session = await _authenticate_session(session)

    if session is None:
        raise UnauthorizedError(
            title="Invalid Session Cookie",
            message="The session cookie provided is invalid.",
        )

    return _Auth.from_token(session)


UserAuth = Annotated[_Auth, Depends(_authentication)]
