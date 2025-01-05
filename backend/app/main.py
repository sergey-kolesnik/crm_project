from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse


from db_connection_async import db_async_session
from api import client_router
from core import (
    version,
    description,
    tags_metadata,
    title,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        yield
    finally:
        await db_async_session.dispose()

# app.add_middleware(CORSMiddleware, allow_origins=['*'])
app = FastAPI(
    lifespan=lifespan,  
    title=title,
    description=description,
    version=version,
    openapi_tags=tags_metadata,
)

app.include_router(client_router)




