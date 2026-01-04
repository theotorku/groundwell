"""
Groundswell - Main FastAPI Application
Facilities & Property Services Execution Intelligence
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from backend.api import (
    inspections_router,
    work_orders_router,
    sites_router,
    signals_router
)

# Create FastAPI app
app = FastAPI(
    title="Groundswell API",
    description="Execution intelligence from the ground up",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # Alternative dev port
        os.getenv("FRONTEND_URL", ""),  # Production frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Groundswell API",
        "version": "0.1.0"
    }

# Register routers
app.include_router(inspections_router)
app.include_router(work_orders_router)
app.include_router(sites_router)
app.include_router(signals_router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Groundswell API",
        "tagline": "Execution intelligence from the ground up",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )
