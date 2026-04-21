""" Runs before every test """

import pytest
from app.services import post_service


@pytest.fixture(autouse=True)
def clear_posts_db():
    post_service.POSTS_DB.clear()
