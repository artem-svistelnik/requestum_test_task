from fastapi import APIRouter

health_check_router = APIRouter(prefix="/health", tags=["Health"])


@health_check_router.get("")
async def health_check():
    return {200: "ok"}
