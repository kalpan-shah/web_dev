"""
@file:          tests/conftest.py
@description:   Pytest fixtures for isolated database sessions and HTTP client setup with dynamic dependency overrides
@date:          21 April 2026
@last modified:   28 May 2026
@author:        Kalpan Shah
@version:       1.0.0
"""

from typing import AsyncGenerator

import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.main import app
from app.db.session import get_db

from app.core.config import base_settings, ENV

base_settings.Environment = ENV.TEST

# Create the async engine
test_engine = create_async_engine(
    base_settings.db_url,
    echo=False
)

# Create the async session factory
AsyncTestingSessionLocal = async_sessionmaker(
    test_engine,
    expire_on_commit=False,  # Prevents session from expiring after commit
)

# Create a default test user
test_user_data = {
    "email": "user_001@mailbox.com",
    "password": "Random@123"
}

# Todo: add fixture to create a test user in the database before tests run, and clean up after tests finish.
@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_test_user():
    """Creates a default test user before any tests run and cleans up after all tests finish."""
    # Load the session
    async with AsyncTestingSessionLocal() as session:
        from app.schema.user import UserCreate
        from app.services import user_service
        from app.core.exceptions import EmailAlreadyExistsException
        test_user = UserCreate(
            username=test_user_data["email"].split("@")[0],
            email=test_user_data["email"],
            password=test_user_data["password"]
        )
        try:
            # Create the user using the service layer (handles hashing, etc.)
            await user_service.create_new_user(session, test_user)
            print("Test user created")
        except EmailAlreadyExistsException:
            print("Test user already exists, skipping creation")


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Provides an isolated transactional database session per test."""
    # 1. Connect to the database
    async with test_engine.connect() as connection:
        # 2. Begin a root transaction
        async with connection.begin() as transaction:
            # 3. Bind the session to this specific active connection
            async with AsyncTestingSessionLocal(bind=connection) as session:
                yield session

                # 4. TEARDOWN: Force a rollback when the test finishes
                await transaction.rollback()

    # 5. Prevent asyncpg "attached to a different loop" error
    await test_engine.dispose()

@pytest_asyncio.fixture(scope="function")
async def client(db_session):
    """Overrides the app dependency dynamically and yields the HTTP client."""

    # This dependency override function now points directly to the active test session
    async def _get_test_db():
        try:
            yield db_session
        finally:
            pass # db_session fixture handles cleanup

    # Inject the override right before the test runs
    app.dependency_overrides[get_db] = _get_test_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac

    # Clean up the override after the individual test finishes
    app.dependency_overrides.clear()




@pytest_asyncio.fixture(scope="function")
async def authorized_client(client):
    """Fetches an access token for the default test user and stores it in the client headers."""

    res = await client.post("/api/v1/users/token", json=test_user_data)

    assert res.status_code == 200, f"Failed to login: {res.text}"

    header = {"Bearer": res.json()["access_token"] }

    client.headers.update(header)

    yield client

    client.headers.pop("Bearer", None)
