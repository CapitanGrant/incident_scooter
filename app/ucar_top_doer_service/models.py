import uuid
from enum import Enum
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy import String, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.dao.database import Base


class IncidentStatus(str, Enum):
    """Статусы инцидентов"""
    NEW = "new"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"
    REJECTED = "rejected"


class IncidentSource(str, Enum):
    """Источники инцидентов"""
    OPERATOR = "operator"
    MONITORING = "monitoring"
    PARTNER = "partner"
    SYSTEM = "system"


class Incident(Base):
    """Модель инцидента"""
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    description: Mapped[str] = mapped_column(String(1000), nullable=False)
    status: Mapped[Enum] = mapped_column(SQLEnum(IncidentStatus), default=IncidentStatus.NEW, nullable=False)
    source: Mapped[Enum] = mapped_column(SQLEnum(IncidentSource), nullable=False)
