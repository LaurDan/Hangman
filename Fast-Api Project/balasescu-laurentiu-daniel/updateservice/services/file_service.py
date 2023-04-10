from asyncpg.exceptions import UniqueViolationError
from fastapi import Depends, File, UploadFile
from ..repositories.file_repo import FileRepo

class FileService:
    def __init__(self, repo: FileRepo = Depends(FileRepo)):
        self.repo = repo

    async def upload_file_srv(self, file: UploadFile = File(..., timeout=60)):
        try:
            result = await self.repo.upload_file(file)
        except ValueError:
            raise UniqueViolationError
        return result

    async def garbage_file_srv(self):
        try:
            result = await self.repo.collect_garbage()
        except ValueError:
            raise UniqueViolationError
        return result

    async def hash_file_srv(self,file: UploadFile = File(...)):
        try:
            result = await self.repo.hash_file(file)
        except ValueError:
            raise UniqueViolationError
        return result

    async def get_size_srv(self, file: UploadFile = File(...)):
        try:
            result = await self.repo.get_size(file)
        except ValueError:
            raise UniqueViolationError
        return result
