from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status, File
from semantic_version import Version
from sqlalchemy.exc import NoResultFound
from starlette.responses import FileResponse

from ..services.package_service import PackService
from ..models.schemas.package_schema import PackageBase, PackageCreate, PackageUpdate, Packages
from ..repositories.app_repo import AppRepo
from ..repositories.package_repo import PackageRepo
from ..services.application_service import AppService
from ..services.file_service import FileService
from ..repositories.package_repo import PackageNotFoundException

router = APIRouter(tags=["packages"])


@router.post("/v1/applications/{app_id}/packages", response_model=PackageBase)
async def create_app_package(
    app_id: int,
    package: PackageCreate,
    app_srv: AppService = Depends(AppService),
    pack_serv: PackService = Depends(PackService),
):
    try:
        await app_srv.fetch_one_app(app_id)
    except NoResultFound:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"Application Id not found in the system"
        )
    try:
        version_obj = Version(package.version)
    except ValueError as er:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{er}, please use semantic version format string: <x.y.z>",
        )
    pack = await pack_serv.create_pack_srv(app_id, str(version_obj), package.description, package)
    return pack


@router.delete("/v1/applications/{app_id}/packages/{package_id}")
async def delete_app_package(
    app_id: int,
    package_id: str,
    app: AppRepo = Depends(AppRepo),
    repo: PackageRepo = Depends(PackageRepo),
):
    try:
        await app.fetch_one_app(app_id)
    except NoResultFound:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"Application Id not found in the system"
        )
    try:
        delete_result = await repo.delete_package(app_id, package_id)
    except PackageNotFoundException as e:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    return delete_result


@router.get(
    "/v1/applications/{app_id}/packages/{package_id}", response_model=PackageBase
)
async def get_application_package(
    app_id: int,
    package_id: str,
    app_srv: AppService = Depends(AppService),
    pack_srv: PackService = Depends(PackService),
):
    try:
        await app_srv.fetch_one_app(app_id)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application id is not found in the system",
        )
    try:
        package = await pack_srv.fetch_one_pack(app_id, package_id)
    except PackageNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    return package


@router.post(
    "/v1/applications/{app_id}/packages/{package_id}/file", response_model=PackageUpdate
)
async def upload_file(
    app_id: int,
    package_id: str,
    file: UploadFile = File(..., timeout=60),
    app_srv: AppService = Depends(AppService),
    pack_srv: PackService = Depends(PackService),
    file_srv: FileService = Depends(FileService),
):
    try:
        await app_srv.fetch_one_app(app_id)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application id is not found in the system",
        )
    try:
        await pack_srv.fetch_one_pack(app_id, package_id)
    except PackageNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    filename = file.filename

    await file_srv.upload_file_srv(file)
    hash_file = await file_srv.hash_file_srv(file)
    file_size = await file_srv.get_size_srv(file)

    pack_upload = await pack_srv.package_update_info_srv(
        app_id, package_id, filename, hash_file, file_size)

    await file_srv.garbage_file_srv()
    return pack_upload

@router.get("/v1/applications/{app_id}/packages/{package_id}/file")
async def download_file(
    app_id: int,
    package_id: str,
    app_srv: AppService = Depends(AppService),
    pack_srv: PackService = Depends(PackService),
):
    try:
        await app_srv.fetch_one_app(app_id)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application id is not found in the system",
        )
    try:
        pack = await pack_srv.fetch_one_pack(app_id, package_id)
    except PackageNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    pack_file_path = pack.file_path
    try:
        pack_download = FileResponse(
            pack_file_path,
            headers={
                "Content-Disposition": f"attachment; filename={pack_file_path}"
            },
        )
    except TypeError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )
    return pack_download

@router.get("/v1/applications/{app_id}/packages", response_model=List[Packages], status_code=status.HTTP_200_OK)
async def get_all_packages(app_id: int,
                           page: int = 1,
                           page_size: int = 20,
                           app_srv: AppService = Depends(AppService),
                           pack_srv: PackService = Depends(PackService)):
    try:
        await app_srv.fetch_one_app(app_id)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No packages found for application with ID {app_id}",
        )
    packages = await pack_srv.get_all_packs_serv(app_id, page, page_size)
    return packages
