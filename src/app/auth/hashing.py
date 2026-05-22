"""
@file:          auth/hashing.py
@description:   Password hashing and verification utilities using Argon2
@date:          19 May 2026
@author:        Kalpan Shah
@version:       1.0.0
"""
from pwdlib import PaswordHash

password_hasher = PaswordHash.recommended()

def get_password_hash(password: str) -> str:
    """ Hash the clean password and return the hashed string """
    return password_hasher.hash(password)

def verify_password(password: str, hashed_password: str):
    """ Verify the raw password against the hashed pss saved in db """
    return password_hasher.verify(password, hashed_password)
