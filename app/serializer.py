from marshmallow import fields
from marshmallow_peewee import ModelSchema

from app.models import Page, Block


class BlockSerializer(ModelSchema):
    id = fields.Integer()
    video_url = fields.String()
    sort = fields.Integer()
    number_of_shows = fields.Integer()

    class Meta:
        model = Block


class PageListSerialiser(ModelSchema):
    name = fields.String()
    url = fields.String()

    class Meta:
        model = Page
        fields = ('name', 'url')


class PageDetailSerializer(ModelSchema):
    id = fields.Integer()
    name = fields.String()
    slug = fields.String()
    sort = fields.Integer()
    blocks = fields.Nested(BlockSerializer, dump_only=True, many=True)

    class Meta:
        model = Page
