"""Peewee migrations -- 001_auto_20201111_2204.py.

Some examples (model - class or model name)::

    > Model = migrator.orm['model_name']            # Return model in current state by name

    > migrator.sql(sql)                             # Run custom SQL
    > migrator.python(func, *args, **kwargs)        # Run python code
    > migrator.create_model(Model)                  # Create a model (could be used as decorator)
    > migrator.remove_model(model, cascade=True)    # Remove a model
    > migrator.add_fields(model, **fields)          # Add fields to a model
    > migrator.change_fields(model, **fields)       # Change fields
    > migrator.remove_fields(model, *field_names, cascade=True)
    > migrator.rename_field(model, old_field_name, new_field_name)
    > migrator.rename_table(model, new_table_name)
    > migrator.add_index(model, *col_names, unique=False)
    > migrator.drop_index(model, *col_names)
    > migrator.add_not_null(model, *field_names)
    > migrator.drop_not_null(model, *field_names)
    > migrator.add_default(model, field_name, default)

"""

import datetime as dt
import peewee as pw
from decimal import ROUND_HALF_EVEN

try:
    import playhouse.postgres_ext as pw_pext
except ImportError:
    pass

SQL = pw.SQL


def migrate(migrator, database, fake=False, **kwargs):
    """Write your migrations here."""

    @migrator.create_model
    class Block(pw.Model):
        id = pw.AutoField()
        name = pw.CharField(max_length=200)
        video_url = pw.CharField(max_length=200)
        sort = pw.IntegerField(constraints=[SQL("DEFAULT 100")])
        number_of_shows = pw.IntegerField(constraints=[SQL("DEFAULT 0")])

        class Meta:
            table_name = "block"

    @migrator.create_model
    class Page(pw.Model):
        id = pw.AutoField()
        name = pw.CharField(max_length=200)
        slug = pw.CharField(max_length=50)
        sort = pw.IntegerField(constraints=[SQL("DEFAULT 100")])

        class Meta:
            table_name = "page"

    @migrator.create_model
    class PageHasBlocks(pw.Model):
        id = pw.AutoField()
        page = pw.ForeignKeyField(backref='to_pages', column_name='page_id', field='id', model=migrator.orm['page'])
        block = pw.ForeignKeyField(backref='to_blocks', column_name='block_id', field='id', model=migrator.orm['block'])

        class Meta:
            table_name = "pagehasblocks"



def rollback(migrator, database, fake=False, **kwargs):
    """Write your rollback migrations here."""

    migrator.remove_model('pagehasblocks')

    migrator.remove_model('page')

    migrator.remove_model('block')
