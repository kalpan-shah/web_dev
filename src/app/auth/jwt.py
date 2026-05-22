"""
@file:          auth/jwt.py
@description:   Handler functions to sanction and decode JWT
@date:          20 May 2026
@last updated:  20 May 2026
@author:        Kalpan Shah
@version:       1.0.0
"""
from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError
from datetime import datetime as dt
from datetime import timedelta, UTC
from app.core.config import base_settings

def sign_jwt(user_email: str) -> dict:
    """
    Signs a dictionary payload and returns a secure JWT token string.

    Args:
        user_email (str): The user email claims to embed in the token

    Returns:
        str: Encoded JSON Web Token.
    """
    # calc token expiration timestamp
    _expire = dt.now(UTC) + timedelta(minutes=base_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    _payload = {
        "email": user_email,
        "exp": int(_expire)
    }

    return encode(
        _payload,
        base_settings.JWT_SECRET_KEY,
        algorithm=base_settings.JWT_ALGORITHM
    )

def decode_jwt(token: str) -> str | None:
    """
    Decodes, verifies the signature, and checks the expiration of a JWT string.

    Args:
        token (str): The incoming JWT token from HTTP headers.

    Returns:
        str | None: The decoded user email if valid; None if expired/corrupted.
    """
    try:
        decoded_token = decode(
            token,
            base_settings.JWT_SECRET_KEY,
            algorithms=[base_settings.JWT_ALGORITHM]
        )
        return decoded_token["email"]
    except KeyError:
        # the token doesn't contain the user email
        return None
    except ExpiredSignatureError:
        # the exp value is in the past, i.e. token expired
        return None
    except InvalidTokenError:
        # unable to decode the token, signature failed to match
        return None
