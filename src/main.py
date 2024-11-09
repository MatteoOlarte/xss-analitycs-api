import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from . import routers
from . import config

os.makedirs('static', exist_ok=True)
app = FastAPI(title="XSS Analytics")
app.include_router(routers.xss_analytics.router)
app.include_router(routers.files.router)
app.mount('/' + config.BASE_DIR + '/static', StaticFiles(directory='static'), name='static')
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
    expose_headers=['x-error']
)