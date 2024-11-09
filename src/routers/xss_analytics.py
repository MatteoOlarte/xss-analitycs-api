import asyncio
from typing import Annotated
from enum import Enum

from fastapi import APIRouter
from fastapi import status
from fastapi import HTTPException

from ..utils import file_utils
from ..utils import xss
from ..shemas import SecurityPredictionSchema

router = APIRouter(tags=['XSS Analysis'], prefix='/xss_analysis')
__invalid_model_error = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Invalid model',
    headers={'X-Error': 'InvalidModel'}
)
__file_not_found_error = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='File not found',
    headers={'X-Error': 'FileNotFound'}
)


class __SecurityModels(str, Enum):
    MODEL_150E = 'model_150e'
    MODEL_1600E = 'model_1600e'


@router.get('/analyze_js', response_model=SecurityPredictionSchema)
async def analyze_js(
    url: str,
    model: __SecurityModels = __SecurityModels.MODEL_150E
) -> SecurityPredictionSchema:
    file = await file_utils.get_file(url)

    if not file:
        raise __file_not_found_error

    if (model is __SecurityModels.MODEL_150E):
        prediction = await asyncio.to_thread(xss.run_150epochs, file)
        return prediction
    
    if (model is __SecurityModels.MODEL_1600E):
        prediction = await asyncio.to_thread(xss.run_1600epochs, file)
        return prediction
    
    raise __invalid_model_error
