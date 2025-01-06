# routes/__init__.py
from fastapi import APIRouter
from .web_actions import router as web_actions_router
from .inference import router as inference_router
from .other_routes import router as other_routes_router

router = APIRouter()
router.include_router(web_actions_router, prefix="/web", tags=["web"])
router.include_router(inference_router, prefix="/inference", tags=["inference"])
router.include_router(other_routes_router, prefix="/other", tags=["other"])