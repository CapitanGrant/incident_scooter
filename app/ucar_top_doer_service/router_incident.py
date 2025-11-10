from uuid import UUID

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.session_maker import TransactionSessionDep, SessionDep
from app.ucar_top_doer_service.dao import IncidentDAO
from app.ucar_top_doer_service.models import IncidentStatus
from app.ucar_top_doer_service.schemas import IncidentResponse, IncidentCreate, \
    IncidentUpdate, IncidentID

router = APIRouter(prefix="", tags=["Incident Management API"])


@router.post("/incidents/create", response_model=IncidentResponse)
async def create_incident(incident: IncidentCreate, session: AsyncSession = TransactionSessionDep):
    """Создать новый инцидент"""
    try:
        db_incident = await IncidentDAO.add(session=session, values=incident)
        await session.commit()
        return db_incident
    except Exception:
        raise HTTPException(status_code=500, detail="Ошибка сервера. Повторите попытку позже")


@router.get("/incidents/all_records")
async def get_incidents(status: IncidentStatus | None = Query(None, description="Фильтр по статусу"),
                        session: AsyncSession = SessionDep):
    """Получить список инцидентов с фильтрацией"""
    try:
        result = await IncidentDAO.find_all(session=session, filters=IncidentUpdate(status=status))
        return result
    except Exception:
        raise HTTPException(status_code=500, detail="Ошибка сервера. Повторите попытку позже")


@router.patch("/incidents/{incident_id}", response_model=IncidentResponse)
async def update_incident_status(
        incident_id: UUID,
        update_data: IncidentUpdate,
        session: AsyncSession = SessionDep):
    """Обновить статус инцидента"""
    try:
        updated_count = await IncidentDAO.update(session=session, filters=IncidentID(id=incident_id),
                                                 values=update_data)
        await session.commit()
        if updated_count == 0:
            raise HTTPException(status_code=500, detail="Не удалось обновить инцидент")

        updated_incident = await IncidentDAO.find_one_or_none_by_id(
            session=session,
            data_id=incident_id
        )
        return updated_incident
    except Exception:
        raise HTTPException(status_code=500, detail="Ошибка сервера. Повторите попытку позже")
