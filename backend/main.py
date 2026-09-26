import os
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from prometheus_fastapi_instrumentator import Instrumentator


DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://devops_user:secure_password@db:5432/app_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI(title="Proyecto DevOps/SRE")

# Instrumentar la app para exponer /metrics
Instrumentator().instrument(app).expose(app)

@app.get("/")
def read_root():
    return {"message": "¡Hola desde el Backend de DevOps/SRE!"}

@app.get("/health")
def health_check():
    try:
        # Intentar conectar a la base de datos para el health check (SRE standard)
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    return {
        "status": "ok",
        "database": db_status
    }