from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from updateservice.settings import setting

engine = create_async_engine(setting["db_conn"], echo=True, future=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()
# DB Utilities:
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        async with session.begin():
            yield session


# # Dependency
async def async_get_db():
    async with async_session() as db:
        yield db
        await db.commit()
