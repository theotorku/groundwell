"""
API routes package
"""

from .inspections import router as inspections_router
from .work_orders import router as work_orders_router
from .sites import router as sites_router
from .signals import router as signals_router

__all__ = [
    "inspections_router",
    "work_orders_router",
    "sites_router",
    "signals_router",
]
