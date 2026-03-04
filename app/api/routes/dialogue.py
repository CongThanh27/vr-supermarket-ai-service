from fastapi import APIRouter, Depends
from app.auth import optional_active_user

router = APIRouter(prefix="/dialogue", tags=["Dialogue"])

@router.get("/hello", summary="Say hello")
def hello(auth=Depends(optional_active_user)):
    msg = "hello anonymous"
    if auth:
        msg = f"hello {auth.username}"
    return {"message": msg}
