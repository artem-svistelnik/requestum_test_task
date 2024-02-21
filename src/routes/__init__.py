from routes.health_check import health_check_router
def include_routes(app):
    app.include_router(health_check_router)
