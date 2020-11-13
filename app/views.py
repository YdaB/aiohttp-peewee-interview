import json

from aiohttp import web
from peewee import fn

from app.models import Page, PageHasBlocks, Block
from app.serializer import PageDetailSerializer, PageListSerialiser


class BaseView:
    @property
    def database(self):
        return self.request.config_dict['objects']


class PageListView(BaseView, web.View):

    async def get(self):
        query = Page.select(
            Page.name,
            fn.CONCAT(f'{self.request.url}').concat(Page.slug).alias('url')
        ).order_by(Page.sort)
        items = await self.database.execute(query)

        return web.json_response({
            'items': PageListSerialiser().dump(items, many=True),
        })


class PageDetailView(BaseView, web.View):
    @property
    def query(self):
        return Page.select(
            Page,
            fn.ARRAY_TO_JSON(
                fn.ARRAY_AGG(Block)
            ).alias('blocks')
        ).join(
            PageHasBlocks
        ).join(
            Block
        ).group_by(
            Page.id
        )

    async def get(self):
        slug = self.request.match_info.get('slug')

        try:
            item = await self.database.get(self.query, slug=slug)
        except Page.DoesNotExist:
            raise web.HTTPBadRequest(
                text=json.dumps({
                    'error': ['item does not exist.']
                }),
                content_type='application/json'
            )

        for block in item.blocks:
            block['number_of_shows'] += 1
            query = Block.update(
                number_of_shows=block['number_of_shows']
            ).where(Block.id == block['id'])
            await self.database.execute(query)

        return web.json_response(PageDetailSerializer().dump(item))
