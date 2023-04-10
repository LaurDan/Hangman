from fastapi import APIRouter, Depends, HTTPException

from updateservice.services.healthcheck_service import (ABCHealthcheckService,
                                                        HealthcheckService)

router = APIRouter(tags=["health"])


@router.get("/health")
async def healthcheck_api(
    health_check: ABCHealthcheckService = Depends(HealthcheckService),
):
    response = await health_check.healthcheck_service_api()
    if response == "Database is available":
        return {"detail": "Application is healthy!"}
    else:
        raise HTTPException(
            status_code=500,
            detail="Application is not healthy! Database is unavailable",
        )
