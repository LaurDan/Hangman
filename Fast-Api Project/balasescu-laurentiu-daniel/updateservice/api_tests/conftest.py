import asyncio
import hashlib
import os
import random

import string
import uuid
from datetime import datetime, timedelta

import jwt
import pytest
import pytest_asyncio

from httpx import AsyncClient
from jose import jwt

from updateservice.db_connection import async_session
from updateservice.models.application_model import Application
from updateservice.models.token_model import Token
from updateservice.models.user_teams import Team, User

from ..app import app
from ..models.package_model import Package
from ..models.schemas.team_schema import TeamCreate
from ..models.schemas.user_schema import UserCreate

from ..models.group_model import Group
from ..models.schemas.groups_schema import GroupBase
from ..models.application_groups_model import ApplicationGroups


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture()
async def async_client():
    async with AsyncClient(app=app, base_url="http://0.0.0.0:8080") as ac:
        yield ac


@pytest.fixture
def test_random_build_user():
    def random_string():
        return "".join(random.choices(string.ascii_lowercase, k=10))

    random_email = random_string()
    random_full_name = random_string()
    yield UserCreate(email=random_email, full_name=random_full_name)


@pytest.fixture
def test_random_build_team():
    def random_string():
        return "".join(random.choices(string.ascii_lowercase, k=10))

    random_name = random_string()
    random_description = random_string()
    yield TeamCreate(name=random_name, description=random_description)


@pytest_asyncio.fixture
async def team_integration_test_data():
    async with async_session() as async_session_for_test:

        def random_string():
            return "".join(random.choices(string.ascii_lowercase, k=10))

        random_id = random.randint(1, 1000000)
        random_team_name = random_string()
        random_team_description = random_string()

        team = Team(
            id=random_id, name=random_team_name, description=random_team_description
        )
        async_session_for_test.add(team)
        await async_session_for_test.commit()
        yield team
        await async_session_for_test.delete(team)
        await async_session_for_test.commit()
        await async_session_for_test.close()


@pytest_asyncio.fixture
async def application_integration_test_data(team_integration_test_data, test_group_db_build):
    async with async_session() as async_session_for_test:

        def random_string():
            return "".join(random.choices(string.ascii_lowercase, k=10))

        random_id = random.randint(1, 1000000)
        random_team_name = random_string()
        random_team_description = random_string()
        random_group_id = test_group_db_build.id

        app = Application(
            id=random_id,
            name=random_team_name,
            description=random_team_description,
            team_id=team_integration_test_data.id,
            group_id = random_group_id
        )

        async_session_for_test.add(app)
        await async_session_for_test.commit()
        yield app
        await async_session_for_test.delete(app)
        await async_session_for_test.commit()
        await async_session_for_test.close()


@pytest.fixture()
def create_access_token_for_test(expires_delta=None):
    secret_key = "my secret key for testing"
    algorithm = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    data = {"sub": "id"}
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


@pytest_asyncio.fixture
async def test_create_user_for_token():
    async with async_session() as async_session_for_test:

        def random_string():
            return "".join(random.choices(string.ascii_lowercase, k=10))

        random_id = random.randint(1, 1000000)
        random_email = random_string()
        random_full_name = random_string()

        user = User(id=random_id, email=f"test{random_email}@example.com", full_name=random_full_name)

        async_session_for_test.add(user)
        await async_session_for_test.commit()
        yield user
        await async_session_for_test.delete(user)
        await async_session_for_test.commit()
        await async_session_for_test.close()


@pytest_asyncio.fixture
async def test_create_token():
    async with async_session() as async_session_for_test:

        random_user_id = random.randint(1, 1000000)
        token_pass = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NzQ0NzI0MzJ9.cCH9ohJPbZullQjGCjJx8-5N0raI-ReYTb27BCOTtty"
        deleted = False
        user_for_token = Token(id=random_user_id, tokens=token_pass, deleted=deleted)
        async_session_for_test.add(user_for_token)
        await async_session_for_test.commit()
        yield user_for_token
        await async_session_for_test.delete(user_for_token)
        await async_session_for_test.commit()
        await async_session_for_test.close()


@pytest_asyncio.fixture
async def package_integration_test_data(application_integration_test_data):
    async with async_session() as async_session_for_test:

        def random_string():
            return "".join(random.choices(string.ascii_lowercase, k=10))

        pack_id = str(uuid.uuid4())
        pack_version = "1.0.1"
        random_team_description = random_string()

        pack = Package(
            id=pack_id,
            version=pack_version,
            description=random_team_description,
            application_id=application_integration_test_data.id,
        )
        async_session_for_test.add(pack)
        await async_session_for_test.commit()
        yield pack

        await async_session_for_test.commit()
        await async_session_for_test.close()


@pytest_asyncio.fixture
async def package_integration_test_data_with_all_info(
    application_integration_test_data,
):
    async with async_session() as async_session_for_test:

        def random_string():
            return "".join(random.choices(string.ascii_lowercase, k=10))

        pack_id = str(uuid.uuid4())
        pack_version = "1.0.1"
        random_team_description = random_string()
        file_name = "test.txt"

        file_data = b"Hello World"
        file_path = f"updateservice/upload_files/{file_name}"

        file_hash = hashlib.sha256(file_data).hexdigest()
        file_size = len(file_data)

        if not os.path.exists(file_path):
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "wb") as f:
                f.write(file_data)

        pack = Package(
            id=pack_id,
            version=pack_version,
            description=random_team_description,
            file_name=file_name,
            hash=file_hash,
            size=file_size,
            file_path=file_path,
            application_id=application_integration_test_data.id,
        )
        async_session_for_test.add(pack)
        await async_session_for_test.commit()
        yield pack

        await async_session_for_test.commit()
        await async_session_for_test.close()


@pytest.fixture
def test_group_integration():
    def random_string():
        return "".join(random.choices(string.ascii_lowercase, k=10))

    random_id = "5a4061d5-f1f5-4ae2-ba64-70e27bfff268"
    name = random_string()
    yield GroupBase(id=random_id, name=name)

@pytest_asyncio.fixture
async def test_group_db_build():
    async with async_session() as async_session_for_test:
        def random_string():
            return "".join(random.choices(string.ascii_lowercase, k=10))
        random_id = str(uuid.uuid4())
        name = random_string()

        group = Group(
            id=random_id,
            name=name,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        async_session_for_test.add(group)
        await async_session_for_test.commit()
        yield group
        await async_session_for_test.commit()
        await async_session_for_test.close()

@pytest_asyncio.fixture
async def test_apps_assigned_to_group_db_build(application_integration_test_data, test_group_db_build):
    async with async_session() as async_session_for_test:
        random_id = str(uuid.uuid4())
        app_id = application_integration_test_data.id
        group_id = test_group_db_build.id

        group = ApplicationGroups(
            id=random_id,
            application_id=app_id,
            group_id=group_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        async_session_for_test.add(group)
        await async_session_for_test.commit()
        yield group
        await async_session_for_test.commit()
        await async_session_for_test.close()
