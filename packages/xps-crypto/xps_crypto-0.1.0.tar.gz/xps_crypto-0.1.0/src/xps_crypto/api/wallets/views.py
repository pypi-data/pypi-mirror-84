from fastapi import APIRouter

from .serializers import SomeRequest, SomeResponse


router = APIRouter()


@router.post(
    "/",
    response_model=SomeResponse,
)
async def index(request_data: SomeRequest) -> SomeResponse:
    # raise RuntimeError("test error")
    print(request_data)
    return SomeResponse(success=True)
