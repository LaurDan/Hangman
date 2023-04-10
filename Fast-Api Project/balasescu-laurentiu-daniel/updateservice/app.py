from fastapi import Depends, FastAPI

from .apis import (
    api_healthcheck,
    app_api,
    hello_api,
    package_api,
    team_api,
    token_api,
    user_api,
    groups_api,
    application_groups_api
)

from .repositories.validate_token_repo import check_access_token

PROTECTED = [Depends(check_access_token)]


def _register_api_handlers(app: FastAPI) -> FastAPI:
    app.include_router(hello_api.router)
    app.include_router(api_healthcheck.router)
    app.include_router(team_api.router)
    app.include_router(app_api.router, dependencies=PROTECTED)
    app.include_router(user_api.router)
    app.include_router(token_api.router)
    app.include_router(package_api.router, dependencies=PROTECTED)
    app.include_router(groups_api.router, dependencies=PROTECTED)
    app.include_router(application_groups_api.router, dependencies=PROTECTED)
    return app


def create_app() -> FastAPI:
    """Create and return FastAPI application."""
    app = FastAPI()
    app = _register_api_handlers(app)
    return app


app = create_app()
