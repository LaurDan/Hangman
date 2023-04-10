import pytest
from fastapi import status

pytestmark = pytest.mark.asyncio


async def test_201_status_code_for_generate_token_for_existent_user(
    async_client, test_create_user_for_token
):
    data = {
        "id": test_create_user_for_token.id,
        "email": test_create_user_for_token.email,
        "full_name": test_create_user_for_token.full_name,
    }
    response = await async_client.post(
        f"/internal/v1/users/{test_create_user_for_token.id}/token",
        headers={"accept": "application/json"},
        json=data,
    )

    assert response.status_code == status.HTTP_201_CREATED


async def test_404_status_code_for_generate_token_for_user_nonexistent(
    async_client, test_create_user_for_token
):
    data = {
        "id": test_create_user_for_token.id,
        "email": test_create_user_for_token.email,
        "full_name": test_create_user_for_token.full_name,
    }
    response = await async_client.post(
        f"/internal/v1/users/{test_create_user_for_token.id + 99999}/token",
        headers={"accept": "application/json"},
        json=data,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_201_status_code_for_generated_token(async_client, test_create_token):
    response = await async_client.delete(
        f"/internal/v1/users/token/{test_create_token.id}",
        headers={"accept": "application/json"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == "The token has been deleted"


async def test_422_status_code_for_generated_token(async_client, test_create_token):
    response = await async_client.delete(
        f"/internal/v1/users/token/{test_create_token.id + 9999999}",
        headers={"accept": "application/json"},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
