import os
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.ucar_top_doer_service.models import Base
from app.config import get_database_url
from app.dao.session_maker import DatabaseSessionManager, session_manager
from app.main import app


TEST_DB_URL = os.getenv("TEST_DB_URL", get_database_url(for_tests=True))

test_engine = create_async_engine(
    TEST_DB_URL,
    future=True,
    echo=False,
    poolclass=NullPool,
)

TestingSessionLocal = DatabaseSessionManager(
    async_sessionmaker(
        bind=test_engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
        class_=AsyncSession,
    ))


async def override_db():
    async with TestingSessionLocal.create_session() as session:
        yield session


@pytest_asyncio.fixture(autouse=True, scope="function")
async def init_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def client():
    app.dependency_overrides = {}
    app.dependency_overrides[session_manager.get_session] = override_db
    app.dependency_overrides[session_manager.get_transaction_session] = override_db
    with TestClient(app) as client:
        yield client


@pytest.fixture(params=[
    {"description": "вышел из строя аккумулятор", "source": "operator", "status": "new"},
    {"description": "поставили на стоянку", "source": "monitoring", "status": "in_progress"},
    {"description": "пригласили друга", "source": "partner", "status": "resolved"},
    {"description": "ошибка 302", "source": "system", "status": "closed"},
    {"description": "ошибка 202", "source": "system", "status": "rejected"}
])
def incident_param(request):
    """Параметризованная фикстура для разных типов инцидентов"""
    return request.param


@pytest.fixture
def create_param_incident(client, incident_param):
    """Создает инцидент на основе параметров"""
    response_create = client.post('/incidents/create', json={
        "description": incident_param["description"],
        "source": incident_param["source"]
    })
    assert response_create.status_code == 200
    incident = response_create.json()
    response_update =client.patch(f'/incidents/{incident["id"]}', json={"status": "in_progress"})
    assert response_update.status_code == 200
    incident_update = response_update.json()
    return incident_update
