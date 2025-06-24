from app.auth import create_access_token, get_current_user
from jose import jwt
import pytest

def test_token_creation_and_decoding():
    data = {"sub": "medic", "role": "doctor"}
    token = create_access_token(data)
    decoded = jwt.decode(token, "secrettoken2025", algorithms=["HS256"])
    assert decoded["sub"] == "medic"
    assert decoded["role"] == "doctor"

def test_invalid_token_raises_exception():
    with pytest.raises(Exception):
        get_current_user(token="invalid.token.here")
