from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class Data(BaseModel):
    name: str
    email: str


@router.get(path="/health", description="Health API", tags=["Health"])
def health_check() -> str:
    """
    Checks the health of a project.

    It returns 200 if the project is healthy.
    """
    return "healthy"


@router.post(
    path="/test",
    description="This is testing api",
    tags=["Test"],
)
def test(
    data: Data,
) -> dict:
    """
    Checks the health of a project.

    It returns 200 if the project is healthy.
    """
    return data.model_dump()
