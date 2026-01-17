from pydantic import BaseModel, HttpUrl


class FileUrlSchema(BaseModel):
    url: HttpUrl
