from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse


from models import db_async_session
from api import client_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        yield
    finally:
        await db_async_session.dispose()

# app.add_middleware(CORSMiddleware, allow_origins=['*'])
app = FastAPI(
    lifespan=lifespan,  
)

app.include_router(client_router)




