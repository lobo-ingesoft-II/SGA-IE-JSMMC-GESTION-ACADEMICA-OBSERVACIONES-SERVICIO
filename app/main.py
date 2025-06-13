from fastapi import FastAPI
from app.routers import observaciones
from app.db import init_db, test_connection

app = FastAPI(title="Observaciones API")

@app.on_event("startup")
def startup_event():
    init_db()
    test_connection()

# Registrar rutas
app.include_router(observaciones.router, prefix="/observaciones", tags=["Observaciones"])