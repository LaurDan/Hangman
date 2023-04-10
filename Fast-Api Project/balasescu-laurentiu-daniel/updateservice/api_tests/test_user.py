import pytest
from fastapi import status

@pytest.mark.asyncio
async def test_get_team_endpoint(async_client, test_random_build_user):
    team_dict = {
        "email": test_random_build_user.email,
        "full_name": test_random_build_user.full_name,
    }
    response = await async_client.post(
        "/internal/v1/users",
        headers={"accept": "application/json"},
        json=team_dict,
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["email"] == test_random_build_user.email
    assert response.json()["full_name"] == test_random_build_user.full_name
    assert response.json()["id"] is not None


@pytest.mark.asyncio
async def test_search_users(async_client, test_create_user_for_token):
    response = await async_client.get(f"/internal/v1/users?search={test_create_user_for_token.email}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert response.json()[0]["email"].startswith("test")


@pytest.mark.asyncio
async def test_search_users_with_wrong_url(async_client, test_create_user_for_token):
    response = await async_client.get(f"/wrong/v1/users?search={test_create_user_for_token.email}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
