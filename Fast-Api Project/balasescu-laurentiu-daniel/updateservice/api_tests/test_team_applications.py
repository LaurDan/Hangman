import pytest
from fastapi import status

pytestmark = pytest.mark.asyncio


async def test_not_authenticated(async_client, team_integration_test_data):
    response = await async_client.post(
        f"/v1/teams/{team_integration_test_data.id}/applications/",
        headers={"X-Token": "hailhydra"},
        json={"id": "bazz", "title": "Bazz", "description": "Drop the bazz"},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "Not authenticated"}


async def test_not_valid_credentials(async_client, test_create_token):
    team_id = 1
    secret_key = test_create_token.tokens
    app_data = {
        "name": "asdasdaweqweqwsdasdstring",
        "description": "asdasdasdasdewqeqweqstring",
    }
    headers = {
        "Authorization": f"Bearer {secret_key}",
        "Content-Type": "application/json",
    }
    response = await async_client.post(
        f"/v1/teams/{team_id}/applications/", json=app_data, headers=headers
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Token has expired"}


async def test_create_applications_with_authorization(
    async_client, create_access_token_for_test, team_integration_test_data
):
    data = {
        "id": team_integration_test_data.id,
        "name": team_integration_test_data.name,
        "description": team_integration_test_data.description,
    }
    token = create_access_token_for_test
    response = await async_client.post(
        f"/v1/teams/{team_integration_test_data.id}/applications/",
        headers={"Authorization": f"Bearer {token}"},
        json=data,
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == data["name"]
    assert response.json()["description"] == data["description"]


async def test_application_with_token_authorization(
    async_client, create_access_token_for_test, team_integration_test_data
):
    data = {
        "id": team_integration_test_data.id,
        "name": team_integration_test_data.name,
        "description": team_integration_test_data.description,
    }
    token = create_access_token_for_test
    response = await async_client.get(
        f"/v1/teams/{team_integration_test_data.id}/applications",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    for application in response.json():
        assert application["name"] == data["name"]
        assert application["description"] == data["description"]


async def test_nonexistent_team_id_for_application(
    async_client, create_access_token_for_test, team_integration_test_data
):
    token = create_access_token_for_test
    response = await async_client.get(
        f"/v1/teams/{team_integration_test_data.id + 9999999}/applications",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {
        "detail": "The team with this id does not exist in the system"
    }


async def test_invalid_authorization_token(
    async_client, create_access_token_for_test, team_integration_test_data
):
    token = "invalid token"
    response = await async_client.get(
        f"/v1/teams/{team_integration_test_data.id}/applications",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}


async def test_update_app(
    async_client,
    create_access_token_for_test,
    team_integration_test_data,
    application_integration_test_data,
):
    token = create_access_token_for_test
    data = {
        "id": application_integration_test_data.id,
        "name": application_integration_test_data.name,
        "description": application_integration_test_data.description,
    }
    response = await async_client.patch(
        f"/v1/teams/{team_integration_test_data.id}/applications/{application_integration_test_data.id}",
        headers={"Authorization": f"Bearer {token}"},
        json=data,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == data["name"]
    assert response.json()["description"] == data["description"]


async def test_wrong_team_update_app(
    async_client,
    create_access_token_for_test,
    team_integration_test_data,
    application_integration_test_data,
):
    token = create_access_token_for_test
    data = {
        "id": application_integration_test_data.id,
        "name": application_integration_test_data.name,
        "description": application_integration_test_data.description,
    }
    response = await async_client.patch(
        f"/v1/teams/{team_integration_test_data.id + 999999}/applications/{application_integration_test_data.id}",
        headers={"Authorization": f"Bearer {token}"},
        json=data,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Team Id not found in the system"}


async def test_get_application_details(
    async_client,
    team_integration_test_data,
    application_integration_test_data,
    create_access_token_for_test,
):
    token = create_access_token_for_test
    response = await async_client.get(
        f"/v1/teams/{team_integration_test_data.id}/applications/{application_integration_test_data.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    app_data = response.json()
    assert app_data["id"] == application_integration_test_data.id
    assert app_data["name"] == application_integration_test_data.name
    assert app_data["description"] == application_integration_test_data.description
    assert app_data["team"] == team_integration_test_data.id
    assert app_data["groups"] is not None


async def test_get_application_details_with_invalid_team(
    async_client,
    team_integration_test_data,
    application_integration_test_data,
    create_access_token_for_test,
):
    token = create_access_token_for_test
    response = await async_client.get(
        f"/v1/teams/{team_integration_test_data.id + 999999}/applications/{application_integration_test_data.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Team with this id does not exists in the system"
    }


async def test_get_application_details_with_invalid_application(
    async_client,
    team_integration_test_data,
    application_integration_test_data,
    create_access_token_for_test,
):
    token = create_access_token_for_test
    response = await async_client.get(
        f"/v1/teams/{team_integration_test_data.id}/applications/{application_integration_test_data.id + 999999}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Application with this id does not exists in the system"
    }
