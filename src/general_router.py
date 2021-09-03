from fastapi import APIRouter
from src import apis_router
from src import page_router


router = APIRouter()
router.include_router(page_router.page_router,
                      prefix="", tags=["general_pages"])
router.include_router(apis_router.api_router, prefix="/api", tags=["CRUD"])
