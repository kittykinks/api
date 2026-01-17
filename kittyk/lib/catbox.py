from httpx import AsyncClient


http = AsyncClient()


async def upload(*, file: bytes = ..., url: str = ...) -> str:
    """Uploads a file to Catbox and returns the URL.

    One and only one of `file` or `url` must be provided. Passing them both or neither will raise a
    ValueError.
    
    Args:
        file (bytes): The file to upload.
        url (str): The Catbox upload URL.
    
    Returns:
        str: The URL of the uploaded file.

    Raises:
        ValueError: If neither or both of `file` and `url` are provided.
        httpx.HTTPError: If the upload fails.
    """

    if file is ... and url is ...:
        raise ValueError("Either 'file' or 'url' must be provided to catbox.upload().")
    
    if file is not ... and url is not ...:
        raise ValueError("Only one of 'file' or 'url' can be provided to catbox.upload().")
    
    if file is not ...:
        response = await http.post(
            "https://catbox.moe/user/api.php",
            data={
                "reqtype": "fileupload",
                "userhash": "",
            },
            files={"fileToUpload": file},
        )

    else:
        response = await http.post(
            "https://catbox.moe/user/api.php",
            data={
                "reqtype": "urlupload",
                "userhash": "",
                "url": url,
            },
        )

    response.raise_for_status()

    return response.text
