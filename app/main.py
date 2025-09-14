from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import cats, missions, targets

app = FastAPI(title="Spy Cat Agency API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(cats.router, prefix="/api/v1")
app.include_router(missions.router, prefix="/api/v1")
app.include_router(targets.router, prefix="/api/v1")
