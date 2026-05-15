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
