"""
路由
"""
from fastapi import APIRouter, Depends 
from ...settings.config import INTERCEPT, API_PREFIX
from starlette.responses import RedirectResponse
router = APIRouter()

@router.get("/")
async def root():
    return RedirectResponse('/docs')
