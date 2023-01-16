# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from word2number import w2n
from asgiref.sync import sync_to_async
from bot.models import Scraper

class ScraperPipeline(object):
    @sync_to_async
    def process_item(self, item, spider):
        try:
            checks_true = False
            product = Scraper.objects.get(name=item['name'])      
            instance = item.save(commit=False)
            instance.pk = product.pk
            try:
                a = (product.cat_1_prize)
                b = (item['cat_1_prize'])
                if int(a) > int(b):
                    item.save()
                    product = Scraper.objects.get(name=item['name'])
                    product.ticked_option = 'True'
                    checks_true = True
            except:
                a = (product.estimated_next_jackpot)
                b = (item['estimated_next_jackpot'])
                if int(a) > int(b):
                    item.save()
                    product = Scraper.objects.get(name=item['name'])
                    product.ticked_option = 'True'
                    checks_true = True
            if checks_true == True:
                item = product.save()
            else:
                item.save()            
        except:
            item.save()
        return item
