import os
import pytest
from fastapi import status

pytestmark = pytest.mark.asyncio


async def test_create_app_package(
    async_client, create_access_token_for_test, application_integration_test_data
):

    payload = {"version": "1.0.0", "description": "Test Package"}
    token = create_access_token_for_test
    response = await async_client.post(
        f"/v1/applications/{application_integration_test_data.id}/packages",
        headers={"Authorization": f"Bearer {token}"},
        json=payload,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["version"] == "1.0.0"
    assert response.json()["description"] == "Test Package"


async def test_create_app_package_with_wrong_authorization_token(
    async_client, application_integration_test_data
):

    payload = {"version": "1.0.0", "description": "Test Package"}
    token = "123 + test_create_token.tokens + wrong token"
    response = await async_client.post(
        f"/v1/applications/{application_integration_test_data.id}/packages",
        headers={"Authorization": f"Bearer {token}"},
        json=payload,
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}


async def test_create_app_package_with_wrong_application(
    async_client, create_access_token_for_test, application_integration_test_data
):

    payload = {"version": "1.0.0", "description": "Test Package"}
    token = create_access_token_for_test
    response = await async_client.post(
        f"/v1/applications/{application_integration_test_data.id + 99999}/packages",
        headers={"Authorization": f"Bearer {token}"},
        json=payload,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Application Id not found in the system"}


async def test_create_app_package_with_wrong_semantic_version(
    async_client, create_access_token_for_test, application_integration_test_data
):

    payload = {"version": "wrong_semantic_type", "description": "Test Package"}
    token = create_access_token_for_test
    response = await async_client.post(
        f"/v1/applications/{application_integration_test_data.id}/packages",
        headers={"Authorization": f"Bearer {token}"},
        json=payload,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": "Invalid version string: 'wrong_semantic_type', "
        "please use semantic version format string: <x.y.z>"
    }


async def test_delete_package(
    async_client, create_access_token_for_test, package_integration_test_data
):

    token = create_access_token_for_test
    response = await async_client.delete(
        f"/v1/applications/{package_integration_test_data.application_id}"
        f"/packages/{package_integration_test_data.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_200_OK


async def test_delete_package_with_wrong_application_id(
    async_client, create_access_token_for_test, package_integration_test_data
):

    token = create_access_token_for_test
    response = await async_client.delete(
        f"/v1/applications/{package_integration_test_data.application_id + 999999}"
        f"/packages/{package_integration_test_data.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Application Id not found in the system"}


async def test_get_application_package(
    async_client, create_access_token_for_test, package_integration_test_data
):

    token = create_access_token_for_test
    response = await async_client.get(
        f"/v1/applications/{package_integration_test_data.application_id}"
        f"/packages/{package_integration_test_data.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] is not None
    assert response.json()["version"] == package_integration_test_data.version
    assert response.json()["description"] == package_integration_test_data.description
    assert response.json()["appl"] is not None


async def test_get_application_package_with_wrong_app_id(
    async_client, create_access_token_for_test, package_integration_test_data
):
    wrong_app_id = package_integration_test_data.application_id + 999999
    token = create_access_token_for_test
    response = await async_client.get(
        f"/v1/applications/{wrong_app_id}"
        f"/packages/{package_integration_test_data.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Application id is not found in the system"}


async def test_get_application_package_with_wrong_package_id(
    async_client, create_access_token_for_test, package_integration_test_data
):
    wrong_pack_id = package_integration_test_data.id + "Wrong Id"
    token = create_access_token_for_test
    response = await async_client.get(
        f"/v1/applications/{package_integration_test_data.application_id}"
        f"/packages/{wrong_pack_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Package Id not found in the system"}


async def test_upload_file(
    async_client,
    create_access_token_for_test,
    package_integration_test_data_with_all_info,
):
    token = create_access_token_for_test
    file = f"updateservice/upload_files/{package_integration_test_data_with_all_info.file_name}"

    response = await async_client.post(
        f"/v1/applications/{package_integration_test_data_with_all_info.application_id}"
        f"/packages/{package_integration_test_data_with_all_info.id}/file",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("test.txt", file)},
    )
    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    assert response_json["id"] == package_integration_test_data_with_all_info.id
    assert response_json["file_name"] == "test.txt"
    assert response_json["hash"] is not None
    assert response_json["size"] is not None


async def test_upload_file_with_wrong_token_auth(
    async_client,
    create_access_token_for_test,
    package_integration_test_data_with_all_info,
):
    token = "definitely a wrong token here :)" + create_access_token_for_test
    file = f"updateservice/upload_files/{package_integration_test_data_with_all_info.file_name}"

    response = await async_client.post(
        f"/v1/applications/{package_integration_test_data_with_all_info.application_id}"
        f"/packages/{package_integration_test_data_with_all_info.id}/file",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("test.txt", file)},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}


async def test_upload_file_wrong_app_id(
    async_client,
    create_access_token_for_test,
    package_integration_test_data_with_all_info,
):
    token = create_access_token_for_test
    file = f"updateservice/upload_files/{package_integration_test_data_with_all_info.file_name}"

    response = await async_client.post(
        f"/v1/applications/{package_integration_test_data_with_all_info.application_id + 999999}"
        f"/packages/{package_integration_test_data_with_all_info.id}/file",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("test.txt", file)},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Application id is not found in the system"}

async def test_upload_file_wrong_package_id(
    async_client,
    create_access_token_for_test,
    package_integration_test_data_with_all_info,
):
    token = create_access_token_for_test
    file = f"updateservice/upload_files/{package_integration_test_data_with_all_info.file_name}"

    response = await async_client.post(
        f"/v1/applications/{package_integration_test_data_with_all_info.application_id}"
        f"/packages/{package_integration_test_data_with_all_info.id + 'wrong id'}/file",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("test.txt", file)},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Package Id not found in the system"}

async def test_download_file(
    async_client,
     create_access_token_for_test,
     package_integration_test_data_with_all_info,
):
    token = create_access_token_for_test

    response = await async_client.get(
    f"/v1/applications/{package_integration_test_data_with_all_info.application_id}"
    f"/packages/{package_integration_test_data_with_all_info.id}/file",
     headers={"Authorization": f"Bearer {token}"}
)
    assert response.status_code == status.HTTP_200_OK

async def test_download_file_with_wrong_auth(
    async_client,
    create_access_token_for_test,
    package_integration_test_data_with_all_info,
):
    token = "wrong token here" + create_access_token_for_test

    response = await async_client.get(
    f"/v1/applications/{package_integration_test_data_with_all_info.application_id}"
    f"/packages/{package_integration_test_data_with_all_info.id}/file",
    headers={"Authorization": f"Bearer {token}"}
)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}

async def test_download_file_with_wrong_app_id(
    async_client,
    create_access_token_for_test,
    package_integration_test_data_with_all_info,
):
    token = create_access_token_for_test

    response = await async_client.get(
    f"/v1/applications/{package_integration_test_data_with_all_info.application_id + 999999}"
    f"/packages/{package_integration_test_data_with_all_info.id}/file",
    headers={"Authorization": f"Bearer {token}"}
)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Application id is not found in the system"}

async def test_download_file_with_wrong_pack_id(
    async_client,
    create_access_token_for_test,
    package_integration_test_data_with_all_info,
):
    token = create_access_token_for_test

    response = await async_client.get(
    f"/v1/applications/{package_integration_test_data_with_all_info.application_id}"
    f"/packages/{package_integration_test_data_with_all_info.id + 'wrong pack id'}/file",
    headers={"Authorization": f"Bearer {token}"}
)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Package Id not found in the system"}

async def test_get_all_packages_for_app(
    async_client, create_access_token_for_test, package_integration_test_data
):

    token = create_access_token_for_test
    response = await async_client.get(
        f"/v1/applications/{package_integration_test_data.application_id}"
        f"/packages",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_200_OK

async def test_get_all_packages_for_app_with_wrong_auth(
    async_client, create_access_token_for_test, package_integration_test_data
):

    token = "wrong token here" + create_access_token_for_test
    response = await async_client.get(
        f"/v1/applications/{package_integration_test_data.application_id}"
        f"/packages",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}

async def test_get_all_packages_for_app_with_wrong_app_id(
    async_client, create_access_token_for_test, package_integration_test_data
):

    token = create_access_token_for_test
    wrong_app_id = package_integration_test_data.application_id + 9999999
    response = await async_client.get(
        f"/v1/applications/{wrong_app_id}"
        f"/packages",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": f"No packages found for application with ID {wrong_app_id}"}


async def test_delete_file_after_api_testing():
    os.remove('updateservice/upload_files/test.txt')
