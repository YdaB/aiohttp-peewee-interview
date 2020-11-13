import asyncio

from utils.load_config import load_config

import aiohttp_autoreload
import peewee_async

from aiohttp import web

from app.models import database
from app.views import PageListView, PageDetailView


async def make_application(settings=None, loop=None):

    if settings is None:
        settings = load_config()

    if loop is None:
        loop = asyncio.get_event_loop()

    app = web.Application(debug=settings['base']['debug'])

    app.add_routes([
        web.get('/', PageListView),
        web.get('/{slug}', PageDetailView)
    ])

    database.init(**settings['database'])
    database.set_allow_sync(False)

    app['database'] = database
    app['objects'] = peewee_async.Manager(app['database'], loop=loop)
    app['settings'] = settings

    if settings['base']['debug']:
        aiohttp_autoreload.start()

    return app
