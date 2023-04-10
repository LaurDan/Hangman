import hashlib
import os
import shutil
from fastapi import File, UploadFile
from sqlalchemy import select
from ..db_connection import async_session
from ..models.package_model import Package


class FileRepo:
    async def upload_file(self, file: UploadFile = File(...)):
        file_location = f"updateservice/upload_files/{file.filename}"
        try:
            with open(file_location, 'wb') as f:
                shutil.copyfileobj(file.file, f)
        except Exception:
            return {"message": "There was an error uploading the file"}

    async def collect_garbage(self):
        async with async_session() as session:
            result = await session.execute(select(Package.file_name))
            registered_files = {row[0] for row in result.fetchall()}

            all_files = os.listdir("updateservice/upload_files")

            for file_name in all_files:
                if file_name not in registered_files:
                    os.remove(os.path.join("updateservice/upload_files", file_name))

    async def hash_file(self, file: UploadFile = File(...)):
        with open(f"updateservice/upload_files/{file.filename}", "rb") as f:
            content = f.read()
            sha256 = hashlib.sha256()
            sha256.update(content)
            return sha256.hexdigest()

    async def get_size(self, file: UploadFile = File(...)):
        size = os.stat(f"updateservice/upload_files/{file.filename}")
        return size.st_size

    async def get_file_path(self, file_name: str):
        return f"updateservice/upload_files/{file_name}"
