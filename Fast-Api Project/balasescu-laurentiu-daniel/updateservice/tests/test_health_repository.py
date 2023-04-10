from unittest import mock

import pytest

from updateservice.repositories.healthcheck_repo import HealthcheckRepository


@pytest.mark.asyncio
async def test_db_repo_session():
    mock_cursor = mock.Mock(**{"fetchall.return_value": "Database result"})
    mock_session = mock.AsyncMock(**{"execute.return_value": mock_cursor})
    mock_async_session = mock.AsyncMock(**{"__aenter__.return_value": mock_session})

    with mock.patch(
        "updateservice.repositories.healthcheck_repo.async_session",
        return_value=mock_async_session,
    ):
        repo = HealthcheckRepository()
        result = await repo.healthcheck_repo_api()
        assert result == "Database result"
        mock_session.execute.assert_called_once_with("Select 200 as dummy")
        mock_cursor.fetchall.assert_called_once_with()
