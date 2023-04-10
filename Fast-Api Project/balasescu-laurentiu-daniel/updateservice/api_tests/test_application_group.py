import uuid

import pytest
from fastapi import status
import random


pytestmark = pytest.mark.asyncio


async def test_application_assigned_to_group(
    async_client,
    create_access_token_for_test,
    test_group_integration,
    test_group_db_build,
    application_integration_test_data
):
    app_id = application_integration_test_data.id
    group_id = test_group_db_build.id
    token = create_access_token_for_test
    response = await async_client.post(
        f"/v1/applications/{app_id}/groups/{group_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == 'Application successfully assigned to the group'


async def test_application_assigned_to_group_with_wrong_auth(
        async_client,
        create_access_token_for_test,
):
    app_id = random.randint(1, 1000000)
    group_id = str(uuid.uuid4())
    token = "wrong token" + create_access_token_for_test
    response = await async_client.post(
        f"/v1/applications/{app_id}/groups/{group_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}


async def test_application_assigned_to_group_wrong_id(
        async_client,
        create_access_token_for_test,
):
    app_id = random.randint(1, 1000000)
    group_id = str(uuid.uuid4())
    token = create_access_token_for_test
    response = await async_client.post(
        f"/v1/applications/{app_id}/groups/{group_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Application Id not found in the system"}


async def test_application_assigned_to_group_wrong_group_id(
        async_client,
        create_access_token_for_test,
        application_integration_test_data
):
    app_id = application_integration_test_data.id
    group_id = str(uuid.uuid4())
    token = create_access_token_for_test
    response = await async_client.post(
        f"/v1/applications/{app_id}/groups/{group_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": f'Group with id {group_id} not found in the system!'}


async def test_assign_app_from_group(async_client, create_access_token_for_test, test_apps_assigned_to_group_db_build):
    token = create_access_token_for_test
    app_id = test_apps_assigned_to_group_db_build.application_id
    group_id = test_apps_assigned_to_group_db_build.group_id

    response = await async_client.post(f"/v1/applications/{app_id}/groups/{group_id}",
                                       headers={"Authorization": f"Bearer {token}"},
                                       )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == 'Application successfully assigned to the group'

async def test_unassign_app_from_group(async_client, create_access_token_for_test, test_apps_assigned_to_group_db_build):
    token = create_access_token_for_test
    app_id = test_apps_assigned_to_group_db_build.application_id
    group_id = test_apps_assigned_to_group_db_build.group_id

    response = await async_client.delete(f"/v1/applications/{app_id}/groups/{group_id}",
                                       headers={"Authorization": f"Bearer {token}"},
                                       )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == 'Application successfully unassigned from the group'


async def test_unassign_app_from_group_with_wrong_auth(async_client, create_access_token_for_test,
                                       test_apps_assigned_to_group_db_build):
    token = "wrong" + create_access_token_for_test
    app_id = test_apps_assigned_to_group_db_build.application_id
    group_id = test_apps_assigned_to_group_db_build.group_id

    response = await async_client.delete(f"/v1/applications/{app_id}/groups/{group_id}",
                                         headers={"Authorization": f"Bearer {token}"},
                                         )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}

async def test_unassign_app_from_group_with_wrong_app_id(async_client, create_access_token_for_test, test_apps_assigned_to_group_db_build):
    token = create_access_token_for_test
    app_id = test_apps_assigned_to_group_db_build.application_id
    group_id = test_apps_assigned_to_group_db_build.group_id

    response = await async_client.delete(f"/v1/applications/{app_id + 999999}/groups/{group_id}",
                                       headers={"Authorization": f"Bearer {token}"},
                                       )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Application Id not found in the system'}

async def test_unassign_app_from_group_with_wrong_group_id(async_client, create_access_token_for_test, test_apps_assigned_to_group_db_build):
    token = create_access_token_for_test
    app_id = test_apps_assigned_to_group_db_build.application_id
    group_id = "wrong" + test_apps_assigned_to_group_db_build.group_id

    response = await async_client.delete(f"/v1/applications/{app_id}/groups/{group_id}",
                                       headers={"Authorization": f"Bearer {token}"},
                                       )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': f'Group with id {group_id} not found in the system!'}
