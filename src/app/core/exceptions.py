"""
@file:          core/exceptions.py
@description:   Custom application-wide HTTP exceptions
@date:          24 May 2026
@author:        Kalpan Shah
"""
from fastapi import HTTPException, status
from typing import Any, Dict

class BaseAppException(HTTPException):
    """Base exception for the application to handle defaults gracefully."""
    STATUS_CODE: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    DEFAULT_DETAIL: str = "An unexpected error occurred."

    def __init__(
        self,
        detail: str | None = None,
        headers: Dict[str, Any] | None = None
    ):
        super().__init__(
            status_code=self.STATUS_CODE,
            detail=detail or self.DEFAULT_DETAIL,
            headers=headers
        )


# region USER-RELATED EXCEPTIONS

class UserNotFoundException(BaseAppException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DEFAULT_DETAIL = "User not found."

class UsernameAlreadyExistsException(BaseAppException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DEFAULT_DETAIL = "Username is already registered."

class EmailAlreadyExistsException(BaseAppException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DEFAULT_DETAIL = "Email is already registered."


# region AUTHENTICATION EXCEPTIONS

class InvalidCredentialsException(BaseAppException):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DEFAULT_DETAIL = "Incorrect username, email, or password."

    def __init__(self, detail: str | None = None):
        # TODO: Enforce the mandatory OAuth2 header for 401s automatically
        super().__init__(
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )


# region AUTHORIZATION EXCEPTIONS

class UnauthorizedException(BaseAppException):
    STATUS_CODE = status.HTTP_403_FORBIDDEN
    DEFAULT_DETAIL = "You do not have permission to perform this action."