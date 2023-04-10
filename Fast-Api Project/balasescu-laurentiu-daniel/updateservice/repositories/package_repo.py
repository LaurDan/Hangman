import uuid

from sqlalchemy import delete, select, update
from sqlalchemy.orm import joinedload
from ..db_connection import async_session
from ..models.package_model import Package
from updateservice.repositories.file_repo import FileRepo
from ..models.schemas.package_schema import PackageCreate

class PackageNotFoundException(Exception):
    pass

class PackageRepo:
    async def create_app_package(self, app_id: int, version: str, description: str, package: PackageCreate):
        async with async_session() as session:

            new_package = Package(
                id=str(uuid.uuid4()),
                version=version,
                description=description,
                application_id=app_id
            )
            session.add(new_package)
            await session.commit()
            new_pack = await session.execute(
                select(Package)
                .options(joinedload(Package.appl))
                .filter(
                    Package.application_id == app_id,
                    Package.version == package.version,
                    Package.description == package.description,
                )
            )
            final_pack = new_pack.fetchone()
            return final_pack[0]

    async def delete_package(self, app_id: int, package_id: str):
        async with async_session() as session:
            pack_query = await session.execute(
                select(Package).filter(
                    Package.id == package_id, Package.application_id == app_id
                )
            )
            pack_check_query = pack_query.first()
            if pack_check_query is None:
                raise PackageNotFoundException("Package Id not found in the system")
            delete_query = (
                delete(Package)
                .where(Package.application_id == app_id)
                .where(Package.id == package_id)
            )
            await session.execute(delete_query)
            await session.commit()
            return "Package has been deleted!"

    async def get_app_package(self, app_id: int, package_id: str):
        async with async_session() as session:
            pack_query = await session.execute(
                select(Package).filter(
                    Package.id == package_id, Package.application_id == app_id
                )
            )
            pack_check_query = pack_query.first()
            if pack_check_query is None:
                raise PackageNotFoundException("Package Id not found in the system")
            show_pack = (
                select(Package)
                .options(joinedload(Package.appl))
                .where(Package.id == package_id, Package.application_id == app_id)
            )
            result = await session.execute(show_pack)
            package = result.scalar()
            return package


    async def package_update(
            self,
            app_id: int,
            package_id: str,
            filename: str,
            file_hash: str,
            file_size: int,
    ):
        async with async_session() as session:
            file_path = await FileRepo().get_file_path(filename)
            update_query = (
                update(Package)
                .where(Package.id == package_id, Package.application_id == app_id)
                .values(
                    size=file_size, hash=file_hash, file_name=filename, file_path=file_path
                )
            )
            update_query.application_id = app_id
            await session.execute(update_query)
            await session.commit()

            result = await session.execute(
                select(Package)
                .options(joinedload(Package.appl))
                .filter(Package.id == package_id, Package.application_id == app_id)
            )
            pack = result.scalar_one()
            return pack

    async def get_all_packages_for_app(self, app_id: int, page: int = 1, page_size: int = 20):
        async with async_session() as session:
            offset = (page - 1) * page_size
            pack_query = await session.execute(
                select(Package)
                .filter(Package.application_id == app_id)
                .order_by(Package.id)
                .offset(offset)
                .limit(page_size))
            packages = pack_query.scalars().all()

            return packages
