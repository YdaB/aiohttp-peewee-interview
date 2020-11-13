import datetime

import peewee_migrate

from utils.load_config import load_config
from app.models import database


def makemigrations():
    router = init_router()
    name = 'auto_{0:%Y%m%d_%H%M}'.format(datetime.datetime.now())
    router.create(name, auto=True)


def migrate():
    router = init_router()
    router.run()


def init_router():
    settings = load_config()
    database.init(**settings['database'])
    return peewee_migrate.Router(database)
