from fastapi import HTTPException

from fastapi import Depends

from speedrun.auth.auth import get_current_user
from speedrun.dtos.user import UserDetails


class PermissionChecker:

    def __init__(self) -> None:
        pass

    def __call__(
        self,
        user: UserDetails = Depends(get_current_user)
    ) -> UserDetails:
        if not user:
            raise HTTPException(status_code=401, detail="User not allowed to use this api")
        return user
