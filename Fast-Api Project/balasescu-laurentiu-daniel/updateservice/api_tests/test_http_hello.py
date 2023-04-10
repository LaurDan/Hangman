import pytest


@pytest.mark.parametrize(
    "test_input, expected",
    [(0, "Hello, World!"), (1, "Hello, John Doe!")],
)
@pytest.mark.asyncio
async def test_temp_hello(async_client, test_input, expected):
    response = await async_client.get(f"/temp/hello?name_id={test_input}")
    assert response.status_code == 200
    assert response.json() == expected
