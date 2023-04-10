import random
import string

import pytest
from fastapi import status

random_name = "".join(random.choices(string.ascii_lowercase, k=10))
random_description = "".join(random.choices(string.ascii_lowercase, k=10))
pytestmark = pytest.mark.asyncio


async def test_read_get_listing_team(async_client, test_random_build_team):
    await async_client.post(
        "/internal/v1/teams/",
        headers={"accept": "application/json"},
        json=test_random_build_team.dict(),
    )
    response = await async_client.get("/internal/v1/teams/")
    response_payload = {"id", "name", "description", "created_at", "updated_at"}
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0].keys() == response_payload


async def test_get_wrong_router_path_404(async_client):
    response = await async_client.get("/internal/v1/wrong_path_teams/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Not Found"}


async def test_good_post_new_created_team(async_client):
    response = await async_client.post(
        "/internal/v1/teams/",
        headers={"accept": "application/json"},
        json={"name": random_name, "description": random_description},
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["id"] is not None
    assert response.json()["name"] == random_name
    assert response.json()["description"] == random_description
    assert response.json()["created_at"] is not None
    assert response.json()["updated_at"] is not None


async def test_fail_post_already_created_team(async_client):
    response = await async_client.post(
        "/internal/v1/teams/",
        headers={"accept": "application/json"},
        json={"name": random_name, "description": random_description},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {"detail": "User already registered in the system"}


async def test_read_get_one_user_team(async_client, team_integration_test_data):
    response = await async_client.get(
        f"/internal/v1/teams/{team_integration_test_data.id}"
    )
    assert response.status_code == status.HTTP_200_OK


async def test_update_post_team(async_client, test_random_build_team):
    data = {
        "id": 1,
        "name": test_random_build_team.name,
        "description": test_random_build_team.description,
    }

    response = await async_client.put(
        f"/internal/v1/teams/1", headers={"accept": "application/json"}, json=data
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == data["name"]
    assert response.json()["description"] == data["description"]


async def test_update_post_team_404_status_code(async_client, test_random_build_team):
    nonexistent_id = 9999999
    data = {
        "id": 1,
        "name": test_random_build_team.name,
        "description": test_random_build_team.description,
    }
    response = await async_client.put(
        f"/internal/v1/teams/{nonexistent_id}",
        headers={"accept": "application/json"},
        json=data,
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {
        "detail": "The team with this id does not exist in the system"
    }
