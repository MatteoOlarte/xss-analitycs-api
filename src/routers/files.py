from typing import Annotated

from fastapi import APIRouter
from fastapi import File
from fastapi import UploadFile
from fastapi import HTTPException
from fastapi import status

from ..utils import file_utils


router = APIRouter(tags=['Files'], prefix='/files')
__file_not_found_error = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='File not found',
    headers={'X-Error': 'FileNotFound'}
)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def upload_file(file: Annotated[UploadFile, File()]):
    file_url = await file_utils.upload_file(file)
    return {'file_url': file_url}


@router.get('/')
async def get_file(file_url: str):
    file_url = await file_utils.get_file(file_url)

    if not file_url:
        raise __file_not_found_error
    return {'file_url': file_url}


@router.delete('/')
async def delete_file(file_url: str):
    was_deleted = await file_utils.delete_file(file_url)

    if not was_deleted:
        raise __file_not_found_error
    return {'status': True}
