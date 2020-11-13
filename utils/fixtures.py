from playhouse.dataset import DataSet

from utils.load_config import load_config
from app.models import database


TABLES_TO_FIXTURE = ('page', 'block', 'pagehasblocks')


def init_db():
    settings = load_config()
    database.init(**settings['database'])
    return DataSet(database)


def export_data():
    db = init_db()
    for table in TABLES_TO_FIXTURE:
        db.freeze(
            db[table].all(),
            format='json',
            filename=f'fixtures/{table}.json'
        )


def import_data():
    db = init_db()
    for table in TABLES_TO_FIXTURE:
        db[table].thaw(format='json', filename=f'fixtures/{table}.json')
