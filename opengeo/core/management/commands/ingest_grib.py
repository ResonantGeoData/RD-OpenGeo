import logging
import os
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import djclick as click
from rgd.management.commands import _data_helper as helper
from rgd.models import Collection
from rgd.utility import url_file_to_local_path
from rgd_imagery.management.commands import _data_helper as imagery_helper
from rgd_imagery.models import Image

logger = logging.getLogger(__name__)

# start: 20040302/
# end: 20040331/


@click.command()
@click.option(
    '-h',
    '--host',
    default='https://www.ncei.noaa.gov/data/global-forecast-system/access/historical/analysis/200403/',
)
@click.option('-c', '--collection', default='GRIB')
@click.option('-x', '--extension', default='.grb')
def ingest_s3(
    host: str,
    collection: str,
    extension: str,
) -> None:

    collection, _ = Collection.objects.get_or_create(name=collection)

    for directory in range(20040302, 20040331 + 1):
        directory = str(directory)
        with url_file_to_local_path(urljoin(host, directory)) as path:
            with open(path, 'r') as f:
                page = f.read()
        soup = BeautifulSoup(page, 'html.parser')

        urls = [
            # NOTE: double urljoin isn't working
            urljoin(host, directory) + f'/{node.get("href")}'
            for node in soup.find_all('a')
            if node.get('href').endswith(extension)
        ]

        for url in urls:
            logger.info(url)
            name = os.path.basename(url)
            file_entry = helper._get_or_create_checksum_file_url(url, name=name)
            file_entry.description = str(path)
            file_entry.collection = collection
            file_entry.save(
                update_fields=[
                    'description',
                    'collection',
                ]
            )
            # Create Image
            image, _ = Image.objects.get_or_create(file=file_entry)

            # Create ImageSet and raster
            imagery_helper.load_raster(
                [
                    image.pk,
                ],
                {},
            )
