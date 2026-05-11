from fastapi import Depends
from fastapi import HTTPException

from app.core.auth import get_current_user


# ADMIN ONLY
def admin_required(
    current_user = Depends(get_current_user)
):

    if current_user.role != "admin":

        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    return current_user