from fastapi import FastAPI
from app.api.api import api_router

app = FastAPI(title="Distributed Food Ordering & Delivery Management System")

app.include_router(api_router, prefix="/api")