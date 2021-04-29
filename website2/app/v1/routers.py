from fastapi import APIRouter
from .endpoints import eval

router = APIRouter()
router.include_router(eval.router)
