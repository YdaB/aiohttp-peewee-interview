from utils.make_application import make_application


async def run_application():
    app = await make_application()
    return app
