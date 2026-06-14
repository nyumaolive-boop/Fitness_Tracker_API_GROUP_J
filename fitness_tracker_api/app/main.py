from fastapi import FastAPI
from fastapi.openapi.docs import get_redoc_html

from app.database import Base, engine
from app.routers import auth, workouts, exercises, nutrition, progress

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Fitness Tracker API",
    description="Group J FastAPI Industry-Standard Fitness Tracker Application aligned with SDG 3: Good Health and Well-being.",
    version="1.0.0",
    redoc_url=None
)

app.include_router(auth.router)
app.include_router(workouts.router)
app.include_router(exercises.router)
app.include_router(nutrition.router)
app.include_router(progress.router)

@app.get("/redoc", include_in_schema=False)
def custom_redoc():
    return get_redoc_html(
        openapi_url="/openapi.json",
        title="Fitness Tracker API - ReDoc"
    )

@app.get("/")
def home():
    return {
        "message": "Welcome to the Fitness Tracker API",
        "docs": "/docs",
        "redoc": "/redoc"
    }