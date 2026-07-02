"""
@file:          core/enums.py
@description:   Enum Definitions
@date:          02 July 2026
@last modified:   02 July 2026
@author:        Kalpan Shah
@version:       1.0.0
"""
from enum import Enum


# Helper Enum
class TodoStatus(str, Enum):
    """
        Enum for Todo Status
    """
    pending = "pending"
    completed = "completed"
    skipped = "skipped"
    deleted = "deleted"