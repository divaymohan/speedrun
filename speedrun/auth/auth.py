from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from speedrun.dtos.user import UserDetails

security = HTTPBasic()


async def get_current_user(
    credentials: HTTPBasicCredentials = Depends(security)
) -> UserDetails:
    if credentials.username == "speedrun" and credentials.password == "speedrun":
        return UserDetails(name="speedrun", email="admin@speedrun.com")
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )


