from routes.health_check import health_check_router
from routes.contributors import contributors_router


def include_routes(app):
    app.include_router(health_check_router)
    app.include_router(contributors_router)
