from fastapi import APIRouter, Depends
from app.auth import require_active_user

router = APIRouter(prefix="/analyze", tags=["Analyze"])

@router.get("/ping", summary="Ping analyze service")
def ping(auth=Depends(require_active_user)):
    return {"status": "analyze pong", "user": auth.username}
