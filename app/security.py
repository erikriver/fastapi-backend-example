from datetime import datetime, timedelta
import jwt

from app.config import get_settings

settings = get_settings()


def create_access_token() -> str:
    """Generate JWT token

    Returns:
        str: a valid JWT
    """
    expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
    expire = datetime.utcnow() + expires_delta
    token_payload = {"sub": "api_key", "exp": expire}
    access_token = jwt.encode(token_payload, settings.secret_key, algorithm=settings.algorithm)
    return access_token


def verify_token(token: str) -> bool:
    """Verify JWT token

    Args:
        token (str): a json web token

    Returns:
        bool: if it is valid or not
    """
    try:
        decoded_token = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return decoded_token["sub"] == "api_key"
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False
