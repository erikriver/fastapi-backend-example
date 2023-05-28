import pytest
from jwt import ExpiredSignatureError
from app.security import create_access_token, verify_token


@pytest.mark.asyncio
async def test_generate_token(client):
    response = await client.post("/secutiry/generate_token")
    assert response.status_code == 200
    assert type(response.json()["access_token"]) is str


@pytest.mark.freeze_time("2017-05-21")
def late_create_access_token():
    return create_access_token()


def test_expired_token(freezer):
    freezer.move_to("2022-04-30")
    token = create_access_token()

    freezer.move_to("2023-05-30")
    assert verify_token(token) == False

    # TODO with pytest.raises(ExpiredSignatureError):
