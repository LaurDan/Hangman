import pytest
from fastapi import status

pytestmark = pytest.mark.asyncio


async def test_create_group(async_client, create_access_token_for_test, test_group_integration):
    token = create_access_token_for_test
    payload = {
        "name": test_group_integration.name
    }
    response = await async_client.post(f"/v1/groups/",
                                       headers={"Authorization": f"Bearer {token}"},
                                       json=payload,
                                       )
    assert response.status_code == status.HTTP_200_OK

    response = await async_client.post(f"/v1/groups/",
                                       headers={"Authorization": f"Bearer {token}"},
                                       json=payload,
                                       )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "A group with this name already exists in the system!"}


async def test_create_group_with_wrong_auth(async_client, create_access_token_for_test, test_group_integration):
    token = "wrong auth token" + create_access_token_for_test
    payload = {
        "name": test_group_integration.name
    }
    response = await async_client.post(f"/v1/groups/",
                                       headers={"Authorization": f"Bearer {token}"},
                                       json=payload,
                                       )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}


async def test_create_group_unprocessable_entity(async_client, create_access_token_for_test):
    token = create_access_token_for_test

    response = await async_client.post(f"/v1/groups/",
                                       headers={"Authorization": f"Bearer {token}"},
                                       )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

async def test_delete_group(async_client, create_access_token_for_test, test_group_db_build):
    token = create_access_token_for_test
    group_id = test_group_db_build.id

    response = await async_client.delete(f"/v1/groups/{group_id}",
                                       headers={"Authorization": f"Bearer {token}"},
                                       )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == "Group has been deleted"

async def test_delete_group_with_wrong_auth(async_client, create_access_token_for_test, test_group_db_build):
    token = "wrong token" + create_access_token_for_test
    group_id = test_group_db_build.id

    response = await async_client.delete(f"/v1/groups/{group_id}",
                                       headers={"Authorization": f"Bearer {token}"},
                                       )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}

async def test_delete_group_with_wrong_id(async_client, create_access_token_for_test, test_group_db_build):
    token = create_access_token_for_test
    group_id = "wrong id" + test_group_db_build.id

    response = await async_client.delete(f"/v1/groups/{group_id}",
                                       headers={"Authorization": f"Bearer {token}"},
                                       )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": f"Group with id {group_id} not found in the system!"}
