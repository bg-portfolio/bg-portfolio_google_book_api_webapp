from fastapi import APIRouter
from . import apis
from . import page_router


router = APIRouter()
router.include_router(page_router.page_router,
                      prefix="/#", tags=["general_pages"])
router.include_router(apis.api_router, prefix="", tags=["CRUD"])
