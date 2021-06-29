import os

from rgd.management.commands._data_helper import SynchronousTasksCommand
from rgd_imagery.management.commands import _data_helper as helper

SUCCESS_MSG = 'Finished loading all demo data.'


class Command(SynchronousTasksCommand):
    help = 'Populate database with Raster images at a URL.'

    def add_arguments(self, parser):
        parser.add_argument(
            '-f',
            '--footprint',
            action='store_true',
            default=False,
            help='Compute the valid data footprints',
        )

    def handle(self, *args, **options):
        footprint = options.get('footprint')

        data_file = os.path.join(os.path.dirname(__file__), 'California_Data.txt')

        with open(data_file, 'r') as f:
            raster_urls = [u.strip() for u in f.readlines()]

        self.set_synchronous()
        # Run the command
        helper.load_raster_files(
            [
                helper.make_raster_dict(
                    [
                        im,
                    ]
                )
                for im in raster_urls
            ],
            footprint=footprint,
        )
        self.stdout.write(self.style.SUCCESS(SUCCESS_MSG))
        self.reset_celery()
