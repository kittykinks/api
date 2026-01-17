from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from kittyk import db
from kittyk.api import router
from kittyk.api.errors import BaseError, NotFoundError


@asynccontextmanager
async def lifespan(_: FastAPI):
    await db.on_startup()

    yield

    await db.on_shutdown()


app = FastAPI(
    title="KittyKinks API",
    version="0.1.0",
    description="Your kinky link in bio.",
    docs_url=None,
    redoc_url="/docs",
    lifespan=lifespan,
)


@app.get("/")
def home():
    return {"message": "Welcome to the KittyKinks API!"}


app.include_router(router)

app.add_exception_handler(404, NotFoundError.handler)
app.add_exception_handler(BaseError, BaseError.handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://kittyk.xyz", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
