import httpx
from fastapi import File, HTTPException, Response, UploadFile, APIRouter

router = APIRouter()

async def forward_files(path: str, uploaded_files: list[UploadFile]):
    files = [
        (
            "uploaded_files",
            (
                file.filename or "file",
                await file.read(),
                file.content_type or "application/octet-stream",
            ),
        )
        for file in uploaded_files
    ]

    try:
        async with httpx.AsyncClient(
            timeout=httpx.Timeout(180.0, connect=15.0)
        ) as client:
            response = await client.post(
                f"https://yasno.up.railway.app{path}",
                files=files,
            )
    except httpx.TimeoutException:
        raise HTTPException(504, "Railway не ответил вовремя")
    except httpx.RequestError:
        raise HTTPException(502, "Не удалось подключиться к Railway")

    headers = {}
    if "content-type" in response.headers:
        headers["content-type"] = response.headers["content-type"]

    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=headers,
    )


@router.post("/free_multiple_files_upload")
async def free_multiple_files_upload(
    uploaded_files: list[UploadFile] = File(...),
):
    return await forward_files(
        "/free_multiple_files_upload", uploaded_files
    )


@router.post("/paid_multiple_files_upload")
async def paid_multiple_files_upload(
    uploaded_files: list[UploadFile] = File(...),
):
    return await forward_files(
        "/paid_multiple_files_upload", uploaded_files
    )