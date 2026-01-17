from fastapi import APIRouter, UploadFile

from kittyk.lib import catbox
from kittyk.api.errors import ValidationError
from kittyk.api.dependencies import UserAuth
from kittyk.api.files.schemas import FileUrlSchema


router = APIRouter(tags=["Files"])


@router.post("/files/upload")
async def upload_file(auth: UserAuth, file: UploadFile):
    # No more than 10mb files
    if file.size > 10 * 1024 * 1024:
        raise ValidationError("File size exceeds the maximum limit of 10MB.")

    url = await catbox.upload(file=file.file)

    return FileUrlSchema(url=url)
