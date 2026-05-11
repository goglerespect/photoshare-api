from fastapi import APIRouter
from fastapi import Depends

from app.core.roles import admin_required


router = APIRouter(
    prefix="/test",
    tags=["test"]
)


# ADMIN ROUTE
@router.get("/admin")
def admin_test(
    admin = Depends(admin_required)
):

    return {
        "message": "Admin access granted"
    }