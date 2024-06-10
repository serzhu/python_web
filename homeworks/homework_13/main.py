from pathlib import Path
from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from fastapi_limiter import FastAPILimiter
import redis.asyncio as redis
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.routes import contacts, auth, users
from src.database.db import get_db
from src.conf.config import settings

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")  # TODO change to lifespan
async def startup():
    """
    The startup function is called when the application starts up.
    It's a good place to initialize things that are used by the app, such as
    connecting to databases or initializing caches.

    :return: A coroutine, so we need to call it with await
    :doc-author: Trelent
    """
    r = await redis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=0,
        encoding="utf-8",
        decode_responses=True,
    )
    await FastAPILimiter.init(r)


app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).resolve().parents[0].joinpath("src/static")),
    name="static",
)

app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(contacts.router, prefix="/api")


@app.get("/")
def index():
    """
    The index function responds to a request for /api/contacts with the complete list of contacts
        :return:        json string of list of contacts


    :return: A dictionary with the key &quot;message&quot; and value &quot;contacts&quot;
    :doc-author: Trelent
    """
    return {"message": "Contacts"}


@app.get("/api/healthchecker")
async def healthchecker(db: AsyncSession = Depends(get_db)):
    """
    The healthchecker function is a simple function that checks if the database is up and running.
    It does this by making a request to the database, and checking if it returns any results.
    If it doesn't return any results, then we know something's wrong with our connection.

    :param db: AsyncSession: Pass the database session to the function
    :return: A dict
    :doc-author: Trelent
    """
    try:
        # Make request
        result = await db.execute(text("SELECT 1"))
        result = result.fetchone()
        if result is None:
            raise HTTPException(
                status_code=500, detail="Database is not configured correctly"
            )
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")
