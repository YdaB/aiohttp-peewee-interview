import peewee
import peewee_async


database = peewee_async.PooledPostgresqlDatabase(None, max_connections=10)


class Page(peewee.Model):
    name = peewee.CharField(max_length=200)
    slug = peewee.CharField(max_length=50)
    sort = peewee.IntegerField(default=100)

    class Meta:
        database = database


class Block(peewee.Model):
    name = peewee.CharField(max_length=200)
    video_url = peewee.CharField(max_length=200)
    sort = peewee.IntegerField(default=100)
    number_of_shows = peewee.IntegerField(default=0)

    class Meta:
        database = database


class PageHasBlocks(peewee.Model):
    page = peewee.ForeignKeyField(Page, backref='to_pages')
    block = peewee.ForeignKeyField(Block, backref='to_blocks')

    class Meta:
        database = database
