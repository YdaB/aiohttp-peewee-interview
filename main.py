import argparse

from aiohttp import web

from utils.make_application import make_application
from utils.migrate import makemigrations, migrate
from utils.fixtures import export_data, import_data


class CallMethodAction(argparse.Action):

    METHODS_MAPPER = {
        'migrate': migrate,
        'makemigrations': makemigrations,
        'export_data': export_data,
        'import_data': import_data
    }

    def __init__(self, option_strings, dest, const):
        super().__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=0,
            const=const,
            default=None,
            required=False,
            help=None
        )

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, self.const)

        method = self.METHODS_MAPPER.get(self.dest, None)

        if method is not None:
            method()


cli_parser = argparse.ArgumentParser()

cli_parser.add_argument('--runserver', action='store_true')
cli_parser.add_argument('--makemigrations',
                        action=CallMethodAction, const=True)
cli_parser.add_argument('--migrate', action=CallMethodAction, const=True)
cli_parser.add_argument('--export_data', action=CallMethodAction, const=True)
cli_parser.add_argument('--import_data', action=CallMethodAction, const=True)


if __name__ == '__main__':
    cli_args = cli_parser.parse_args()

    if cli_args.runserver:
        web.run_app(make_application())
