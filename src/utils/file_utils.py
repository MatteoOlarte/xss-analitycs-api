import os
from uuid import uuid4
from typing import Any

from fastapi import UploadFile

from .. import config

UPLOAD_DIRECTORY = "static"


def __get_hashes_file_name(filename: str) -> str:
    unique_id = uuid4().hex[:16]
    return f'file_{unique_id}_{filename}'


def __make_dirs(dir_path: str) -> str:
    os.makedirs(dir_path, exist_ok=True)
    return dir_path


async def upload_file(
    file: UploadFile,
    *,
    sub_directories: str = 'uploads'
) -> Any | str:
    dir_path : str = __make_dirs(os.path.join(UPLOAD_DIRECTORY, sub_directories))
    file_name: str = __get_hashes_file_name(file.filename)
    file_path: str = os.path.join(dir_path, file_name)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return file_path


async def get_file(
    file_url: str,
) -> str | None:
    file_path = os.path.join(config.BASE_DIR, file_url)
    return file_path if os.path.exists(file_path) else None


async def delete_file(
    file_url: str
) -> bool:
    file_path = os.path.join(config.BASE_DIR, file_url)

    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False
