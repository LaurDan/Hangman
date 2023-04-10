from asyncpg.exceptions import UniqueViolationError
from fastapi import Depends

from ..models.schemas.package_schema import PackageCreate
from ..repositories.package_repo import PackageRepo

class PackService:
    def __init__(self, repo: PackageRepo = Depends(PackageRepo)):
        self.repo = repo

    async def fetch_one_pack(self, app_id: int, package_id: str):
        try:
            result = await self.repo.get_app_package(app_id, package_id)
        except ValueError:
            raise UniqueViolationError
        return result

    async def create_pack_srv(self, app_id: int, version: str, description: str, package: PackageCreate):
        try:
            result = await self.repo.create_app_package(app_id, version, description, package)
        except ValueError:
            raise UniqueViolationError
        return result

    async def get_all_packs_serv(self, app_id: int, page: int = 1, page_size: int = 20):
        try:
            result = await self.repo.get_all_packages_for_app(app_id, page, page_size)
        except ValueError:
            raise UniqueViolationError
        return result


    async def package_update_info_srv(
        self,
        app_id: int,
        package_id: str,
        filename: str,
        file_hash: str,
        file_size: int,

    ):
        try:
            results = await self.repo.package_update(
                app_id,
                package_id,
                filename,
                file_hash,
                file_size,
            )
        except ValueError:
            raise UniqueViolationError
        return results
