from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from scraper.scraper import settings as my_settings
from scraper.scraper.spiders.scrapy import CanadaMaxLotto
import sys

class Command(BaseCommand):
    help = 'Release spider'
    def add_arguments(self, parser):#
        parser.add_argument('name', type=str)
    def handle(self, *args, **options):
        crawler_settings = Settings()
        crawler_settings.setmodule(my_settings)
        process = CrawlerProcess(settings=crawler_settings)
        name = options['name']
        process.crawl(name)
        process.start()