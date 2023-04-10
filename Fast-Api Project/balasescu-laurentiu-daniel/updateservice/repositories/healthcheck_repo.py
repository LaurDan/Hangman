import abc

from updateservice.db_connection import async_session


class ABCHealthcheckRepo:
    @abc.abstractmethod
    async def healthcheck_repo_api(self):
        pass


class HealthcheckRepository(ABCHealthcheckRepo):
    async def healthcheck_repo_api(self):
        async with async_session() as session:
            postgres_query = "Select 200 as dummy"
            cursor = await session.execute(postgres_query)
            result = cursor.fetchall()
        return result
