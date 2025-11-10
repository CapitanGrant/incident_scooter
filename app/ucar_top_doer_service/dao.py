from app.dao.base import BaseDAO
from app.ucar_top_doer_service.models import Incident

class IncidentDAO(BaseDAO[Incident]):
    model = Incident
