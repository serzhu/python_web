# import os
# from  pathlib import Path
# from dotenv import load_dotenv

import contextlib
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from src.conf.config import settings



class DatabaseSessionManager:
    def __init__(self, url: str):
        self._engine: AsyncEngine | None = create_async_engine(url)
        self._session_maker: async_sessionmaker = async_sessionmaker(
                                                autoflush=False, autocommit = False, bind = self._engine
                                                )
    

    @contextlib.asynccontextmanager
    async def session(self):
        if self._session_maker is None:
            raise Exception("Session is not initialized")
        session = self._session_maker()
        try:
            yield session
        # except Exception as err:
        #     print(err)
        #     session.rollback()
        finally:
            await session.close()
            
# load_dotenv(Path(__file__).resolve().parents[1].joinpath('.env'))
# URI = os.environ.get('DATABASE_URL')

URI = settings.pg_database_url

sessionmanager = DatabaseSessionManager(URI)


async def get_db():
    async with sessionmanager.session() as session:
        yield session
