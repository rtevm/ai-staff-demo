from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.database import engine, Base
from app.api.endpoints import agents
from app.models import models

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI Staff Platform - Build and manage AI agent teams with clear roles, accountabilities, and governance"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Include API routers
app.include_router(agents.router, prefix="/api/v1/agents", tags=["agents"])

# Root endpoint - serve the landing page
@app.get("/")
async def read_root(request: Request):
    """Serve the landing page"""
    return templates.TemplateResponse("index.html", {"request": request})

# Dashboard endpoint
@app.get("/dashboard")
async def dashboard(request: Request):
    """Serve the main dashboard"""
    return templates.TemplateResponse("dashboard.html", {"request": request})

# Demo endpoint
@app.get("/demo")
async def demo(request: Request):
    """Serve the demo page"""
    return templates.TemplateResponse("dashboard.html", {"request": request, "demo_mode": True})

# CEO Interface endpoint
@app.get("/ceo-interface")
async def ceo_interface(request: Request):
    """Serve the CEO interface page"""
    return templates.TemplateResponse("ceo-interface.html", {"request": request})

# Architecture diagram endpoint
@app.get("/architecture")
async def architecture_diagram(request: Request):
    """Serve the technical architecture diagram"""
    return templates.TemplateResponse("architecture-diagram.html", {"request": request})

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.app_version,
        "app_name": settings.app_name
    }

# API info endpoint
@app.get("/api/v1/info")
async def api_info():
    """API information endpoint"""
    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "description": "AI Staff Platform API for managing AI agent teams",
        "endpoints": {
            "agents": "/api/v1/agents",
            "teams": "/api/v1/teams",
            "projects": "/api/v1/projects",
            "tasks": "/api/v1/tasks"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
