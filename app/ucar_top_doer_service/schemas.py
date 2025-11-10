from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict
from app.ucar_top_doer_service.models import IncidentSource


class IncidentBase(BaseModel):
    """Схема инцидента"""
    description: str = Field(min_length=1, max_length=1000, description="Описание инцидента")
    source: IncidentSource = Field(description="Источник инцидента")


class IncidentCreate(IncidentBase):
    """Схема создания инцидента"""
    pass


class IncidentUpdate(BaseModel):
    """Схема обновления инцидента"""
    status: str | None = Field(description="Новый статус инцидента")


class IncidentID(BaseModel):
    id: UUID = Field(description="Уникальный идентификатор инцидента")


class IncidentResponse(IncidentBase, IncidentID):
    """Схема успешного обновления инцидента"""
    status: str = Field(description="Новый статус инцидента")
    model_config = ConfigDict(validate_by_name=True)


class IncidentListResponse(BaseModel):
    """Схема успешного ответа списка инцидентов"""
    incidents: list[IncidentResponse] = Field(description="Список инцидентов")
    total: int = Field(description="Количество инцидентов")
