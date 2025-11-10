from fastapi import FastAPI
from app.ucar_top_doer_service.router_incident import router

app = FastAPI()

app.include_router(router)
