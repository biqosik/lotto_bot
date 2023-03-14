import random
import re
import json
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
import scrapy
from datetime import datetime
from datetime import timedelta
import requests
from scrapy.spiders import CrawlSpider
import time
import re
import locale
import pandas as pd
import math
import random
from scraper.scraper.items import *
from dateutil.relativedelta import relativedelta
from urllib.parse import urljoin

UK_proxy_lst = [
    '154.92.116.6:6318',    
    '64.43.91.158:6929',    
    '45.8.203.10:8124',     
    '154.92.114.112:5807',  
    '64.43.89.215:6474',    
    '45.8.203.154:8268',    
    '64.43.89.214:6473',    
    '64.43.90.51:6566',     
    '154.92.114.207:5902',  
    '154.92.114.4:5699',   
    '64.43.90.177:6692',  
    '84.21.188.202:8736',   
    '64.43.89.39:6298',     
    '154.92.114.97:5792', 
    '154.92.114.142:5837',  
    '45.43.64.153:6411',
]

US_proxy_lst = [
    '104.144.26.252:8782',
    '107.152.214.94:8671', 
    '209.127.127.177:7275', 
    '107.175.119.61:6589', 
    '45.72.119.89:9165', 
    '104.144.235.181:7261', 
    '144.168.140.121:8192', 
    '45.85.160.57:7149', 
    '198.46.241.155:6690', 
    '104.144.72.32:6064', 
    '194.5.153.116:7481', 
    '104.144.26.118:8648', 
    '66.151.50.40:6843', 
    '138.128.97.98:7688', 
    '69.58.9.71:7141', 
    '198.46.137.164:6368', 
    '104.227.145.172:8767', 
    '170.244.92.240:8800', 
    '45.158.185.88:8600',  
]

AUS_proxy_lst = [
    '103.139.48.97:5982',   
    '103.139.48.58:5943',  
    '103.139.48.70:5955', 
    '103.139.48.104:5989',  
    '103.139.48.115:6000',  
    '103.139.48.16:5901',  
    '103.139.48.187:6072',  
    '103.139.48.122:6007',  
    '103.139.48.121:6006',  
    '103.139.48.135:6020',  
    '103.139.48.228:6113',  
    '103.139.48.227:6112',  
    '103.139.48.178:6063',  
    '103.139.48.40:5925',  
    '103.139.48.166:6051',  
    '103.139.48.154:6039',  
    '103.139.48.169:6054',  
    '103.139.48.204:6089',  
    '103.139.48.129:6014',  
    '103.139.48.75:5960',  
    '103.139.48.146:6031',  
    '103.139.48.158:6043', 
    '103.139.48.73:5958',  
    '103.139.48.47:5932',  
    '103.139.48.179:6064',  
    '103.139.48.23:5908',  

]

Australialottoonly_proxy = [
    '103.139.48.146:6031',  
    '103.139.48.158:6043', 
    '103.139.48.73:5958',  
    '103.139.48.47:5932',  
    '103.139.48.179:6064',  
    '103.139.48.23:5908',  
]


def get_UK_proxy():
    # UK proxy rotating function to randomly select proxy per request
    random_proxy = random.choice(UK_proxy_lst)

    return {
        "http": f"http://keizzermop:WSPassword123@{random_proxy}",
        "https": f"https://keizzermop:WSPassword123@{random_proxy}",
    }


def get_US_proxy():
    # US proxy rotating function to randomly select proxy per request
    random_proxy = random.choice(US_proxy_lst)

    return {
        "http": f"http://keizzermop:WSPassword123@{random_proxy}",
        "https": f"https://keizzermop:WSPassword123@{random_proxy}",
    }


def get_AUS_proxy():
    # US proxy rotating function to randomly select proxy per request
    random_proxy = random.choice(AUS_proxy_lst)

    return {
        "http": f"http://keizzermop:WSPassword123@{random_proxy}",
        "https": f"https://keizzermop:WSPassword123@{random_proxy}",
    }

def get_AUS_data_proxy():
    # US proxy rotating function to randomly select proxy per request
    random_proxy = random.choice(Australialottoonly_proxy)

    return {
        "http": f"http://keizzermop:WSPassword123@{random_proxy}",
        "https": f"https://keizzermop:WSPassword123@{random_proxy}",
    }

def clean_date_string(element):
    # removes 'th','nd', etc. from date string
    clean = re.sub(r'(\d+)(st|nd|rd|th)', r'\g<1>', element)
    return clean


def clean_datetime(element):
    # method to remove letters and unnecessary symbols from datetime
    if "/" in element:
        digits = [s for s in element if s.isdigit() or s =='/']
        value = ''.join(digits)
    elif "." in element:
        digits = [s for s in element if s.isdigit() or s =='.']
        value = ''.join(digits)
    return value


def remove_unicode(element):
    # method to remove unicode characters
    if type(element) == str:
        if u"\xa0" in element:
            element = element.replace(u"\xa0", u" ")
        if r"\u" in element:
            element = (element.encode('ascii', 'ignore')).decode("utf-8")

    return element


def prize_to_num(element):
    if type(element) == str:
        value = "".join([s for s in str(element) if s.isdigit() or s == '.'])
        if len(value) > 0:
            if any(string in element.lower() for string in ['million', 'mil']):
                value = float(value) * 1_000_000
            return float(value)
        else:
            return 0
    else:
        return element


def swap_commas_fullstops(element):
    # method to swap commas and fullstops
    if "," and "." in element:
        return element.replace('.', '@').replace(',', '.').replace('@', ',')
    elif "," in element:
        return element.replace(',', '.')
    elif "." in element:
        return element.replace('.', ',')
    else:
        return element

class USMegaMillions(scrapy.Spider):

    name = "USMegaMillions"

    def start_requests(self):
        self.name = "USMegaMillions"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.megamillions.com/Winning-Numbers.aspx"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        LottoItem = ItemLoader(item=USMegaMillionsItem(), selector=response)
        draw_date = response.xpath(
            '//span[@class="lastestDate"]/text()').get()
        draw_date = "".join([s for s in draw_date if s.isdigit() or s=='/'])

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%m/%d/%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("ball0", response.xpath('//ul[@class="numbers"]/li[@class="ball winNum1"]/text()').get())
        LottoItem.add_value("ball1", response.xpath('//ul[@class="numbers"]/li[@class="ball winNum2"]/text()').get())
        LottoItem.add_value("ball2", response.xpath('//ul[@class="numbers"]/li[@class="ball winNum3"]/text()').get())
        LottoItem.add_value("ball3", response.xpath('//ul[@class="numbers"]/li[@class="ball winNum4"]/text()').get())
        LottoItem.add_value("ball4", response.xpath('//ul[@class="numbers"]/li[@class="ball winNum5"]/text()').get())
        LottoItem.add_value("bonus_ball", response.xpath('//ul[@class="numbers"]/li[@class="ball yellowBall winNumMB"]/text()').get())
        LottoItem.add_value("megaplier", response.xpath('//ul[@class="numbers"]/li[@class="megaplier"]/span[@class="winNumMP"]/text()').get())
        LottoItem.add_value("cat_1_winners", response.xpath(
            '//div[@class="dividerLine-small tier0 ie11-col2 ie11-row2"]/text()').get())
        LottoItem.add_value("cat_2_winners", response.xpath(
            '//div[@class="dividerLine-small tier1t ie11-col2 ie11-row3"]/text()').get())
        LottoItem.add_value("cat_3_winners", response.xpath(
            '//div[@class="dividerLine-small tier2t ie11-col2 ie11-row4"]/text()').get())
        LottoItem.add_value("cat_4_winners", response.xpath(
            '//div[@class="dividerLine-small tier3t ie11-col2 ie11-row5"]/text()').get())
        LottoItem.add_value("cat_5_winners", response.xpath(
            '//div[@class="dividerLine-small tier4t ie11-col2 ie11-row6"]/text()').get())
        LottoItem.add_value("cat_6_winners", response.xpath(
            '//div[@class="dividerLine-small tier5t ie11-col2 ie11-row7"]/text()').get())
        LottoItem.add_value("cat_7_winners", response.xpath(
            '//div[@class="dividerLine-small tier6t ie11-col2 ie11-row8"]/text()').get())
        LottoItem.add_value("cat_8_winners", response.xpath(
            '//div[@class="dividerLine-small tier7t ie11-col2 ie11-row9"]/text()').get())
        LottoItem.add_value("cat_9_winners", response.xpath(
            '//div[@class="dividerLine-small tier8t ie11-col2 ie11-row10"]/text()').get())
        LottoItem.add_value("jackpot_cash", response.xpath('//span[@class="nextCashOpt js_pastCashOpt"]/text()').get())
        # note: cat_1_prize HERE IS NOT DIVIDED BY NUM_WINNERS
        LottoItem.add_value("cat_1_prize", response.xpath('//span[@class="estJackpot js_pastJackpot"]/text()').get())
        LottoItem.add_value("cat_2_prize", response.xpath(
            '//div[@class="dividerLine-small prize1 ie11-col3 ie11-row3"]/text()').get())
        LottoItem.add_value("cat_3_prize", response.xpath(
            '//div[@class="dividerLine-small prize2 ie11-col3 ie11-row4"]/text()').get())
        LottoItem.add_value("cat_4_prize", response.xpath(
            '//div[@class="dividerLine-small prize3 ie11-col3 ie11-row5"]/text()').get())
        LottoItem.add_value("cat_5_prize", response.xpath(
            '//div[@class="dividerLine-small prize4 ie11-col3 ie11-row6"]/text()').get())
        LottoItem.add_value("cat_6_prize", response.xpath(
            '//div[@class="dividerLine-small prize5 ie11-col3 ie11-row7"]/text()').get())
        LottoItem.add_value("cat_7_prize", response.xpath(
            '//div[@class="dividerLine-small prize6 ie11-col3 ie11-row8"]/text()').get())
        LottoItem.add_value("cat_8_prize", response.xpath(
            '//div[@class="dividerLine-small prize7 ie11-col3 ie11-row9"]/text()').get())
        LottoItem.add_value("cat_9_prize", response.xpath(
            '//div[@class="dividerLine-small prize8 ie11-col3 ie11-row10"]/text()').get())
        yield LottoItem.load_item()


class USPowerball(scrapy.Spider):

    name = "USPowerball"

    def start_requests(self):
        self.name = "USPowerball"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.national-lottery.com/powerball/results/history"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        next_page = response.xpath('//table//tr/td/a/@href').get()
        url = urljoin(response.url, next_page)
        yield scrapy.Request(url, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":10})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=USPowerballItem(), selector=response)
        balls_lst = response.xpath('//ul[@class="balls"]/li/text()').getall()
        rows = response.xpath('//table//tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("bonus_ball", balls_lst[5])
        LottoItem.add_value("draw_datetime", response.url.split('/')[-1])
        LottoItem.add_value("cat_1_winners", rows[1].xpath('./td/text()').getall()[-2].strip())
        LottoItem.add_value("cat_2_winners", rows[2].xpath('./td/text()').getall()[-2].strip())
        LottoItem.add_value("cat_3_winners", rows[3].xpath('./td/text()').getall()[-2].strip())
        LottoItem.add_value("cat_4_winners", rows[4].xpath('./td/text()').getall()[-2].strip())
        LottoItem.add_value("cat_5_winners", rows[5].xpath('./td/text()').getall()[-2].strip())
        LottoItem.add_value("cat_6_winners", rows[6].xpath('./td/text()').getall()[-2].strip())
        LottoItem.add_value("cat_7_winners", rows[7].xpath('./td/text()').getall()[-2].strip())
        LottoItem.add_value("cat_8_winners", rows[8].xpath('./td/text()').getall()[-2].strip())
        LottoItem.add_value("cat_9_winners", rows[9].xpath('./td/text()').getall()[-2].strip())
        LottoItem.add_value("cat_1_prize", rows[1].xpath('./td/text()').getall()[1].strip())
        LottoItem.add_value("cat_2_prize", rows[2].xpath('./td/text()').getall()[1].strip())
        LottoItem.add_value("cat_3_prize", rows[3].xpath('./td/text()').getall()[1].strip())
        LottoItem.add_value("cat_4_prize", rows[4].xpath('./td/text()').getall()[1].strip())
        LottoItem.add_value("cat_5_prize", rows[5].xpath('./td/text()').getall()[1].strip())
        LottoItem.add_value("cat_6_prize", rows[6].xpath('./td/text()').getall()[1].strip())
        LottoItem.add_value("cat_7_prize", rows[7].xpath('./td/text()').getall()[1].strip())
        LottoItem.add_value("cat_8_prize", rows[8].xpath('./td/text()').getall()[1].strip())
        LottoItem.add_value("cat_9_prize", rows[9].xpath('./td/text()').getall()[1].strip())
        yield LottoItem.load_item()


class USLottoAmerica(scrapy.Spider):

    name = "USLottoAmerica"

    def start_requests(self):
        self.name = "USLottoAmerica"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.lottoamerica.com/numbers/"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        latest = response.xpath('//div[@class="result -lotto"]')[0]
        self.balls_lst = latest.xpath('.//ul[@class="balls"]/li/text()').getall()
        next_page = latest.xpath('./a/@href').get()
        url = urljoin(response.url, next_page)
        yield scrapy.Request(url, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":10})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=USLottoAmericaItem(), selector=response)
        rows = response.xpath('//tbody/tr')

        LottoItem.add_value("name", self.name)
        draw_date = response.xpath('//h1/span/text()').get()
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%B %d, %Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("ball0", self.balls_lst[0])
        LottoItem.add_value("ball1", self.balls_lst[1])
        LottoItem.add_value("ball2", self.balls_lst[2])
        LottoItem.add_value("ball3", self.balls_lst[3])
        LottoItem.add_value("ball4", self.balls_lst[4])
        LottoItem.add_value("bonus_ball", self.balls_lst[5])
        next_jackpot = "".join(response.xpath('//div[@class="featured-jackpot"]/div[@class="_amount"]//text()').getall())
        if "m" in next_jackpot:
            next_jackpot = next_jackpot.replace("m", "million")
        LottoItem.add_value("estimated_next_jackpot", next_jackpot)
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td[@class="-right"]/text()').getall()[1].strip())
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./td[@class="-right"]/text()').getall()[1].strip())
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./td[@class="-right"]/text()').getall()[1].strip())
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./td[@class="-right"]/text()').getall()[1].strip())
        LottoItem.add_value("cat_5_winners", rows[4].xpath('./td[@class="-right"]/text()').getall()[1].strip())
        LottoItem.add_value("cat_6_winners", rows[5].xpath('./td[@class="-right"]/text()').getall()[1].strip())
        LottoItem.add_value("cat_7_winners", rows[6].xpath('./td[@class="-right"]/text()').getall()[1].strip())
        LottoItem.add_value("cat_8_winners", rows[7].xpath('./td[@class="-right"]/text()').getall()[1].strip())
        LottoItem.add_value("cat_9_winners", rows[8].xpath('./td[@class="-right"]/text()').getall()[1].strip())
        LottoItem.add_value("cat_1_prize", rows[0].xpath('./td[@class="-right"]/text()').get().strip())
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./td[@class="-right"]/text()').get().strip())
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./td[@class="-right"]/text()').get().strip())
        LottoItem.add_value("cat_4_prize", rows[3].xpath('./td[@class="-right"]/text()').get().strip())
        LottoItem.add_value("cat_5_prize", rows[4].xpath('./td[@class="-right"]/text()').get().strip())
        LottoItem.add_value("cat_6_prize", rows[5].xpath('./td[@class="-right"]/text()').get().strip())
        LottoItem.add_value("cat_7_prize", rows[6].xpath('./td[@class="-right"]/text()').get().strip())
        LottoItem.add_value("cat_8_prize", rows[7].xpath('./td[@class="-right"]/text()').get().strip())
        LottoItem.add_value("cat_9_prize", rows[8].xpath('./td[@class="-right"]/text()').get().strip())
        yield LottoItem.load_item()


class USArizonaThePick(scrapy.Spider):

    name = "USArizonaThePick"

    # Confirmed that match_6 is 'division4' by checking on day when jackpot is won

    def start_requests(self):
        self.name = "USArizonaThePick"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://api.arizonalottery.com/v1/DrawGames/1"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=USArizonaThePickItem(), selector=response)
        latest = response.json()
        balls_lst = latest['winningNumbers'].split('-')
        if str(latest['divisionCounts']['division3']) == '0':
            pass
        else:
            LottoItem.add_value("name", self.name)
            draw_date = str(latest['drawDate'])
            LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d"))
            LottoItem.add_value("draw_number", str(latest['drawNum']))
            LottoItem.add_value("ball0", str(balls_lst[0]))
            LottoItem.add_value("ball1", str(balls_lst[1]))
            LottoItem.add_value("ball2", str(balls_lst[2]))
            LottoItem.add_value("ball3", str(balls_lst[3]))
            LottoItem.add_value("ball4", str(balls_lst[4]))
            LottoItem.add_value("ball5", str(balls_lst[5]))
            LottoItem.add_value("estimated_next_jackpot", str(latest['nextJackpotAmount']))
            cat_1_winners = prize_to_num(latest['divisionCounts']['division4'])
            if cat_1_winners > 0:
                cat_1_prize = int(latest['jackpotAmount'])/cat_1_winners
                LottoItem.add_value("cat_1_prize", str(cat_1_prize))
            else:
                LottoItem.add_value("cat_1_prize", str(latest['jackpotAmount']))
            LottoItem.add_value("cat_2_prize", '2000')
            LottoItem.add_value("cat_3_prize", '50')
            LottoItem.add_value("cat_4_prize", '3')
            LottoItem.add_value("cat_1_winners", str(latest['divisionCounts']['division4']))
            LottoItem.add_value("cat_2_winners", str(latest['divisionCounts']['division1']))
            LottoItem.add_value("cat_3_winners", str(latest['divisionCounts']['division2']))
            LottoItem.add_value("cat_4_winners", str(latest['divisionCounts']['division3']))
            yield LottoItem.load_item()


class USArizonaFantasy5(scrapy.Spider):

    name = "USArizonaFantasy5"

    # Confirmed that match_5 is 'division7' by checking on day when jackpot is won

    def start_requests(self):
        self.name = "USArizonaFantasy5"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://api.arizonalottery.com/v1/DrawGames/4"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        self.latest = response.json()
        url = 'https://www.arizonalottery.com/draw-games/fantasy-5/'
        yield scrapy.Request(url=url, callback=self.parse_next,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse_next(self, response):
        LottoItem = ItemLoader(item=USArizonaFantasy5Item(), selector=response)
        rows = response.xpath('//table[@id="winning-number-chart"]//tbody/tr')
        date1 = rows[0].xpath('.//strong//text()').get()
        date2 = rows[3].xpath('.//strong//text()').get()
        now = datetime.strftime(datetime.now() - timedelta(days=1), "%m/%d/%Y")
        date1= datetime.strptime(date1, "%m/%d/%Y").strftime("%m/%d/%Y")
        if now == date1:
            balls_lst = rows[0].xpath('.//text()').getall()[1].split()
            draw_date = datetime.strptime(date1, "%m/%d/%Y").strftime("%Y-%m-%d")
            winners_lst = rows[2].xpath('.//text()').getall()
            winners_lst = list(filter(lambda x:x.strip(), winners_lst))
        else:
            balls_lst = rows[3].xpath('.//text()').getall()[1].split()
            draw_date = datetime.strptime(date2, "%m/%d/%Y").strftime("%Y-%m-%d")
            winners_lst = rows[5].xpath('.//text()').getall()
            winners_lst = list(filter(lambda x:x.strip(), winners_lst))
        if int(winners_lst[0]) == 0:
            pass
        else:
            LottoItem.add_value("name", self.name)
            LottoItem.add_value("draw_datetime", draw_date)
            LottoItem.add_value("draw_number", str(self.latest['drawNum']))
            LottoItem.add_value("ball0", str(balls_lst[0]))
            LottoItem.add_value("ball1", str(balls_lst[1]))
            LottoItem.add_value("ball2", str(balls_lst[2]))
            LottoItem.add_value("ball3", str(balls_lst[3]))
            LottoItem.add_value("ball4", str(balls_lst[4]))
            LottoItem.add_value("estimated_next_jackpot", str(self.latest['nextJackpotAmount']))
            LottoItem.add_value("cat_1_prize", str(self.latest['jackpotAmount']))
            LottoItem.add_value("cat_2_prize", '1000')
            LottoItem.add_value("cat_3_prize", '500')
            LottoItem.add_value("cat_4_prize", '10')
            LottoItem.add_value("cat_5_prize", '5')
            LottoItem.add_value("cat_6_prize", '2')
            LottoItem.add_value("cat_7_prize", '1')
            LottoItem.add_value("cat_1_winners", winners_lst[-1])
            LottoItem.add_value("cat_2_winners", winners_lst[-2])
            LottoItem.add_value("cat_3_winners", winners_lst[-3])
            LottoItem.add_value("cat_4_winners", winners_lst[-4])
            LottoItem.add_value("cat_5_winners", winners_lst[-5])
            LottoItem.add_value("cat_6_winners", winners_lst[-6])
            LottoItem.add_value("cat_7_winners", winners_lst[-7])
            yield LottoItem.load_item()


class USArizonaTripleTwist(scrapy.Spider):

    name = "USArizonaTripleTwist"

    def start_requests(self):
        self.name = "USArizonaTripleTwist"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://api.arizonalottery.com/v1/DrawGames/15"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        self.latest = response.json()
        url = 'https://www.arizonalottery.com/draw-games/triple-twist/'
        yield scrapy.Request(url=url, callback=self.parse_next,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse_next(self, response):
        LottoItem = ItemLoader(item=USArizonaTripleTwistItem(), selector=response)
        rows = response.xpath('//table[@id="winning-number-chart"]//tbody/tr')
        date1 = rows[0].xpath('.//strong//text()').get()
        date2 = rows[3].xpath('.//strong//text()').get()
        now = datetime.strftime(datetime.now() - timedelta(days=1), "%m/%d/%Y")
        date1= datetime.strptime(date1, "%m/%d/%Y").strftime("%m/%d/%Y")
        if now == date1:
            balls_lst = rows[0].xpath('.//text()').getall()[1].split()
            draw_date = datetime.strptime(date1, "%m/%d/%Y").strftime("%Y-%m-%d")
            winners_lst = rows[2].xpath('.//text()').getall()
            winners_lst = list(filter(lambda x:x.strip(), winners_lst))
        else:
            balls_lst = rows[3].xpath('.//text()').getall()[1].split()
            draw_date = datetime.strptime(date2, "%m/%d/%Y").strftime("%Y-%m-%d")
            winners_lst = rows[5].xpath('.//text()').getall()
            winners_lst = list(filter(lambda x:x.strip(), winners_lst))
        if int(winners_lst[0]) == 0:
            pass
        else:
            LottoItem.add_value("name", self.name)
            LottoItem.add_value("draw_datetime", draw_date)
            LottoItem.add_value("draw_number", str(self.latest['drawNum']))
            LottoItem.add_value("ball0", str(balls_lst[0]))
            LottoItem.add_value("ball1", str(balls_lst[1]))
            LottoItem.add_value("ball2", str(balls_lst[2]))
            LottoItem.add_value("ball3", str(balls_lst[3]))
            LottoItem.add_value("ball4", str(balls_lst[4]))
            LottoItem.add_value("ball5", str(balls_lst[5]))
            LottoItem.add_value("estimated_next_jackpot", str(self.latest['nextJackpotAmount']))
            LottoItem.add_value("cat_1_prize", str(self.latest['jackpotAmount']))
            LottoItem.add_value("cat_2_prize", '2000')
            LottoItem.add_value("cat_3_prize", '500')
            LottoItem.add_value("cat_4_prize", '50')
            LottoItem.add_value("cat_5_prize", '10')
            LottoItem.add_value("cat_6_prize", '5')
            LottoItem.add_value("cat_7_prize", '2')
            LottoItem.add_value("cat_1_winners", winners_lst[-1])
            LottoItem.add_value("cat_2_winners", winners_lst[-2])
            LottoItem.add_value("cat_3_winners", winners_lst[-3])
            LottoItem.add_value("cat_4_winners", winners_lst[-4])
            LottoItem.add_value("cat_5_winners", winners_lst[-5])
            LottoItem.add_value("cat_6_winners", winners_lst[-6])
            LottoItem.add_value("cat_7_winners", winners_lst[-7])
            yield LottoItem.load_item()


class USArkansasLotto(scrapy.Spider):

    name = "USArkansasLotto"

    def start_requests(self):
        self.name = "USArkansasLotto"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        headers = {
            'authority': 'www.myarkansaslottery.com',
            'accept': '*/*',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'dnt': '1',
            'if-none-match': '"1663851415-0"',
            'referer': 'https://www.myarkansaslottery.com/games/lotto/past-winners',
            'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        url = 'https://www.myarkansaslottery.com/games/results-paged.json?game=lotto&offset=0&limit=10'
        yield scrapy.Request(url=url, headers=headers, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=USArkansasLottoItem(), selector=response)
        latest = response.json()[0]

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("estimated_next_jackpot", latest['prizes']['nextgpannuity'])
        LottoItem.add_value("draw_datetime", datetime.strptime(latest['drawdate'], "%A %B %d, %Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("ball0", latest['numbers']['ball_1'])
        LottoItem.add_value("ball1", latest['numbers']['ball_2'])
        LottoItem.add_value("ball2", latest['numbers']['ball_3'])
        LottoItem.add_value("ball3", latest['numbers']['ball_4'])
        LottoItem.add_value("ball4", latest['numbers']['ball_5'])
        LottoItem.add_value("ball5", latest['numbers']['ball_6'])
        LottoItem.add_value("bonus_ball", latest['numbers']['bonus_number'])
        LottoItem.add_value("cat_1_prize", latest['winners']['jackpotprize'])
        LottoItem.add_value("cat_2_prize", latest['winners']['p_1'])
        LottoItem.add_value("cat_3_prize", latest['winners']['p_2'])
        LottoItem.add_value("cat_4_prize", latest['winners']['p_3'])
        LottoItem.add_value("cat_5_prize", latest['winners']['p_4'])
        LottoItem.add_value("cat_6_prize", latest['winners']['p_5'])
        LottoItem.add_value("cat_7_prize", latest['winners']['p_6'])
        LottoItem.add_value("cat_8_prize", latest['winners']['p_7'])
        LottoItem.add_value("cat_1_winners", latest['winners']['jackpot'])
        LottoItem.add_value("cat_2_winners", latest['winners']['t_1'])
        LottoItem.add_value("cat_3_winners", latest['winners']['t_2'])
        LottoItem.add_value("cat_4_winners", latest['winners']['t_3'])
        LottoItem.add_value("cat_5_winners", latest['winners']['t_4'])
        LottoItem.add_value("cat_6_winners", latest['winners']['t_5'])
        LottoItem.add_value("cat_7_winners", latest['winners']['t_6'])
        LottoItem.add_value("cat_8_winners", latest['winners']['t_7'])
        yield LottoItem.load_item()


class USArkansasNaturalState(scrapy.Spider):

    name = "USArkansasNaturalState"

    def start_requests(self):
        self.name = "USArkansasNaturalState"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        headers = {
            'authority': 'www.myarkansaslottery.com',
            'accept': '*/*',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.myarkansaslottery.com/games/natural-state-jackpot/past-winners',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'cookie': 'has_js=1; _gcl_au=1.1.2046456470.1609360415; _scid=e37ed10d-0f8a-4c24-8b27-a92ccbb80021; wisepops=%7B%22csd%22%3A1%2C%22popups%22%3A%7B%22241345%22%3A%7B%22dc%22%3A1%2C%22d%22%3A%222020-12-30T21%3A09%3A46.743Z%22%7D%7D%2C%22sub%22%3A0%2C%22ucrn%22%3A39%2C%22cid%22%3A%2242933%22%2C%22v%22%3A4%7D; wisepops_visits=%5B%222021-01-04T17%3A28%3A05.635Z%22%2C%222021-01-04T09%3A01%3A30.660Z%22%2C%222020-12-30T20%3A33%3A34.977Z%22%5D; wisepops_session=%7B%22arrivalOnSite%22%3A%222021-01-04T17%3A28%3A05.635Z%22%2C%22mtime%22%3A%222021-01-04T17%3A28%3A05.802Z%22%2C%22pageviews%22%3A1%2C%22popups%22%3A%7B%7D%2C%22bars%22%3A%7B%7D%2C%22src%22%3Anull%2C%22utm%22%3A%7B%7D%7D; __cfduid=d7368979d51e090a2714dc5d37477e3a11613062198; _gid=GA1.2.854948341.1613062200; _dc_gtm_UA-10693725-1=1; fpestid=sco5gY7Vd3TLRURjEsBc23LmofRTqElJnG9n3jDmp4uwwNmlC_S5Rpe3PUzE0UY4OZQlFw; _ga_YVS861CXNG=GS1.1.1613062199.4.1.1613062215.0; _ga=GA1.2.1344971879.1609360415',
        }
        url = "https://www.myarkansaslottery.com/games/results-paged-ar.json?game=nsj&offset=0&limit=10"
        yield scrapy.Request(url=url, headers=headers, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=USArkansasNaturalStateItem(), selector=response)
        latest = response.json()[0]

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("estimated_next_jackpot", latest['prizes']['nextgpannuity'])
        LottoItem.add_value("draw_datetime", datetime.strptime(latest['drawdate'], "%A %B %d, %Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("ball0", latest['numbers']['ball_1'])
        LottoItem.add_value("ball1", latest['numbers']['ball_2'])
        LottoItem.add_value("ball2", latest['numbers']['ball_3'])
        LottoItem.add_value("ball3", latest['numbers']['ball_4'])
        LottoItem.add_value("ball4", latest['numbers']['ball_5'])
        LottoItem.add_value("cat_1_prize", latest['winners']['jackpotprize'])
        LottoItem.add_value("cat_2_prize", latest['winners']['p_1'])
        LottoItem.add_value("cat_3_prize", latest['winners']['p_2'])
        LottoItem.add_value("cat_4_prize", latest['winners']['p_3'])
        LottoItem.add_value("cat_1_winners", latest['winners']['jackpot'])
        LottoItem.add_value("cat_2_winners", latest['winners']['t_1'])
        LottoItem.add_value("cat_3_winners", latest['winners']['t_2'])
        LottoItem.add_value("cat_4_winners", latest['winners']['t_3'])
        yield LottoItem.load_item()


class USCaliforniaDailyDerby(scrapy.Spider):

    name = "USCaliforniaDailyDerby"

    # 1st place = ball0, 2nd place = ball1, 3rd place = ball2, racetime = ball3

    def start_requests(self):
        self.name = "USCaliforniaDailyDerby"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.calottery.com/api/DrawGameApi/DrawGamePastDrawResults/11/1/20"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=USCaliforniaDailyDerbyItem(), selector=response)
        latest = response.json()['MostRecentDraw']

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", str(latest['WinningNumbers']['1']['Number']))
        LottoItem.add_value("ball1", str(latest['WinningNumbers']['2']['Number']))
        LottoItem.add_value("ball2", str(latest['WinningNumbers']['3']['Number']))
        LottoItem.add_value("ball3", str(latest['RaceTime']))
        draw_date = str(latest['DrawDate'])
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", str(latest['DrawNumber']))
        LottoItem.add_value("cat_1_prize", str(latest['Prizes']['7']['Amount']))
        LottoItem.add_value("cat_2_prize", str(latest['Prizes']['6']['Amount']))
        LottoItem.add_value("cat_3_prize", str(latest['Prizes']['5']['Amount']))
        LottoItem.add_value("cat_4_prize", str(latest['Prizes']['4']['Amount']))
        LottoItem.add_value("cat_5_prize", str(latest['Prizes']['3']['Amount']))
        LottoItem.add_value("cat_6_prize", str(latest['Prizes']['2']['Amount']))
        LottoItem.add_value("cat_7_prize", str(latest['Prizes']['1']['Amount']))
        LottoItem.add_value("cat_1_winners", str(latest['Prizes']['7']['Count']))
        LottoItem.add_value("cat_2_winners", str(latest['Prizes']['6']['Count']))
        LottoItem.add_value("cat_3_winners", str(latest['Prizes']['5']['Count']))
        LottoItem.add_value("cat_4_winners", str(latest['Prizes']['4']['Count']))
        LottoItem.add_value("cat_5_winners", str(latest['Prizes']['3']['Count']))
        LottoItem.add_value("cat_6_winners", str(latest['Prizes']['2']['Count']))
        LottoItem.add_value("cat_7_winners", str(latest['Prizes']['1']['Count']))
        yield LottoItem.load_item()


class USCaliforniaFantasy5(scrapy.Spider):

    name = "USCaliforniaFantasy5"

    def start_requests(self):
        self.name = "USCaliforniaFantasy5"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.calottery.com/api/DrawGameApi/DrawGamePastDrawResults/10/1/20"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=USCaliforniaFantasy5Item(), selector=response)
        latest = response.json()['MostRecentDraw']

        LottoItem.add_value("name", self.name)
        draw_date = str(latest['DrawDate'])
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", str(latest['DrawNumber']))
        LottoItem.add_value("ball0", str(latest['WinningNumbers']['0']['Number']))
        LottoItem.add_value("ball1", str(latest['WinningNumbers']['1']['Number']))
        LottoItem.add_value("ball2", str(latest['WinningNumbers']['2']['Number']))
        LottoItem.add_value("ball3", str(latest['WinningNumbers']['3']['Number']))
        LottoItem.add_value("ball4", str(latest['WinningNumbers']['4']['Number']))
        LottoItem.add_value("cat_1_prize", str(latest['Prizes']['1']['Amount']))
        LottoItem.add_value("cat_2_prize", str(latest['Prizes']['2']['Amount']))
        LottoItem.add_value("cat_3_prize", str(latest['Prizes']['3']['Amount']))
        LottoItem.add_value("cat_4_prize", '1') # prize is free play
        LottoItem.add_value("cat_1_winners", str(latest['Prizes']['1']['Count']))
        LottoItem.add_value("cat_2_winners", str(latest['Prizes']['2']['Count']))
        LottoItem.add_value("cat_3_winners", str(latest['Prizes']['3']['Count']))
        LottoItem.add_value("cat_4_winners", str(latest['Prizes']['4']['Count']))
        yield LottoItem.load_item()


class USCaliforniaSuperLotto(scrapy.Spider):

    name = "USCaliforniaSuperLotto"

    def start_requests(self):
        self.name = "USCaliforniaSuperLotto"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.calottery.com/api/DrawGameApi/DrawGamePastDrawResults/8/1/20"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=USCaliforniaSuperLottoItem(), selector=response)
        latest = response.json()['MostRecentDraw']

        LottoItem.add_value("name", self.name)
        draw_date = str(latest['DrawDate'])
        LottoItem.add_value("ball0", str(latest['WinningNumbers']['0']['Number']))
        LottoItem.add_value("ball1", str(latest['WinningNumbers']['1']['Number']))
        LottoItem.add_value("ball2", str(latest['WinningNumbers']['2']['Number']))
        LottoItem.add_value("ball3", str(latest['WinningNumbers']['3']['Number']))
        LottoItem.add_value("ball4", str(latest['WinningNumbers']['4']['Number']))
        LottoItem.add_value("bonus_ball", str(latest['WinningNumbers']['5']['Number']))
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", str(latest['DrawNumber']))
        LottoItem.add_value("cat_1_prize", str(latest['Prizes']['1']['Amount']))
        LottoItem.add_value("cat_2_prize", str(latest['Prizes']['2']['Amount']))
        LottoItem.add_value("cat_3_prize", str(latest['Prizes']['3']['Amount']))
        LottoItem.add_value("cat_4_prize", str(latest['Prizes']['4']['Amount']))
        LottoItem.add_value("cat_5_prize", str(latest['Prizes']['5']['Amount']))
        LottoItem.add_value("cat_6_prize", str(latest['Prizes']['6']['Amount']))
        LottoItem.add_value("cat_7_prize", str(latest['Prizes']['7']['Amount']))
        LottoItem.add_value("cat_8_prize", str(latest['Prizes']['8']['Amount']))
        LottoItem.add_value("cat_9_prize", str(latest['Prizes']['9']['Amount']))
        LottoItem.add_value("cat_1_winners", str(latest['Prizes']['1']['Count']))
        LottoItem.add_value("cat_2_winners", str(latest['Prizes']['2']['Count']))
        LottoItem.add_value("cat_3_winners", str(latest['Prizes']['3']['Count']))
        LottoItem.add_value("cat_4_winners", str(latest['Prizes']['4']['Count']))
        LottoItem.add_value("cat_5_winners", str(latest['Prizes']['5']['Count']))
        LottoItem.add_value("cat_6_winners", str(latest['Prizes']['6']['Count']))
        LottoItem.add_value("cat_7_winners", str(latest['Prizes']['7']['Count']))
        LottoItem.add_value("cat_8_winners", str(latest['Prizes']['8']['Count']))
        LottoItem.add_value("cat_9_winners", str(latest['Prizes']['9']['Count']))
        yield LottoItem.load_item()


class USColoradoLottoPlus(scrapy.Spider):

    name = "USColoradoLottoPlus"

    def start_requests(self):
        self.name = "USColoradoLottoPlus"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.coloradolottery.com/en/games/colorado-lotto-plus/"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        next_page = response.xpath("//div[@class='winningNumbers']/a/@href").get()
        url = urljoin(response.url, next_page)
        yield scrapy.Request(url, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":10})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=USColoradoLottoPlusItem(), selector=response)
        rows = response.xpath('//tbody')[0].xpath('./tr')
        balls_lst = response.xpath('//h2/text()').get().split('-')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("draw_datetime", response.url.split('/')[-2].strip())
        LottoItem.add_value("ball0", balls_lst[0].split(':')[1].strip())
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("jackpot_cash", response.xpath('//h4/text()').get().split(':')[1])
        LottoItem.add_value("cat_1_prize", rows[0].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_2_prize", '250')
        LottoItem.add_value("cat_3_prize", '25')
        LottoItem.add_value("cat_4_prize", '3')
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td/text()').getall()[1])
        # Returns list of 4 strings of numbers that need to be summed
        match_5_lst = [rows[1].xpath('./td/text()').getall()[1], rows[2].xpath('./td/text()').getall()[1],
                        rows[3].xpath('./td/text()').getall()[1], rows[4].xpath('./td/text()').getall()[1]]
        match_4_lst = [rows[5].xpath('./td/text()').getall()[1], rows[6].xpath('./td/text()').getall()[1],
                        rows[7].xpath('./td/text()').getall()[1], rows[8].xpath('./td/text()').getall()[1]]
        match_3_lst = [rows[9].xpath('./td/text()').getall()[1], rows[10].xpath('./td/text()').getall()[1],
                        rows[11].xpath('./td/text()').getall()[1], rows[12].xpath('./td/text()').getall()[1]]
        LottoItem.add_value("cat_2_winners", str(sum([int(i.strip()) for i in match_5_lst])))
        LottoItem.add_value("cat_3_winners", str(sum([int(i.strip()) for i in match_4_lst])))
        LottoItem.add_value("cat_4_winners", str(sum([int(i.strip()) for i in match_3_lst])))
        yield LottoItem.load_item()


class USConnecticutLotto(scrapy.Spider):

    name = "USConnecticutLotto"

    def start_requests(self):
        self.name = "USConnecticutLotto"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.ctlottery.org/Lotto!"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        latest = response.xpath('//main[@id="main"]//div[@class="info-holder"]')[0]
        self.balls_lst = latest.xpath('.//ul[@class="numbers-list"]/li/text()').getall()
        self.next_jackpot = latest.xpath('.//strong[@class="price"]/text()').get()
        self.next_jackpot_cash = latest.xpath('.//div[@class="mx-auto"]/strong[@class="title"]/text()').getall()[-1]
        self.draw_date = latest.xpath('.//strong/time/@datetime').get()
        headers = {
            'Connection': 'keep-alive',
            'Accept': 'text/html, */*; q=0.01',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://www.ctlottery.org/WinningNumbers/Lotto!',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }
        draw_datetime = datetime.strptime(self.draw_date, "%Y-%m-%d")
        date_string = datetime.strftime(draw_datetime, '%m%d%Y')
        url = "https://www.ctlottery.org/ajax/getPayouts?numbers=true&game=6&ddate=" + date_string
        yield scrapy.Request(url=url, callback=self.parse_draw, headers=headers, meta={"proxy": self.req_proxy, "download_timeout":10})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=USConnecticutLottoItem(), selector=response)
        rows = response.xpath('//tbody/tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("draw_datetime", self.draw_date)
        LottoItem.add_value("ball0", self.balls_lst[0])
        LottoItem.add_value("ball1", self.balls_lst[1])
        LottoItem.add_value("ball2", self.balls_lst[2])
        LottoItem.add_value("ball3", self.balls_lst[3])
        LottoItem.add_value("ball4", self.balls_lst[4])
        LottoItem.add_value("ball5", self.balls_lst[5])
        LottoItem.add_value("estimated_next_jackpot", self.next_jackpot)
        LottoItem.add_value("estimated_next_jackpot_cash", self.next_jackpot_cash)
        LottoItem.add_value("cat_1_prize", rows[0].xpath('.//td/text()').getall()[-1])
        LottoItem.add_value("cat_2_prize", rows[1].xpath('.//td/text()').getall()[-1])
        LottoItem.add_value("cat_3_prize", rows[2].xpath('.//td/text()').getall()[-1])
        LottoItem.add_value("cat_4_prize", rows[3].xpath('.//td/text()').getall()[-1])
        LottoItem.add_value("cat_1_winners", rows[0].xpath('.//td/text()').get())
        LottoItem.add_value("cat_2_winners", rows[1].xpath('.//td/text()').get())
        LottoItem.add_value("cat_3_winners", rows[2].xpath('.//td/text()').get())
        LottoItem.add_value("cat_4_winners", rows[3].xpath('.//td/text()').get())
        yield LottoItem.load_item()


class USDelawareMultiWin(scrapy.Spider):

    name = "USDelawareMultiWin"

    def start_requests(self):
        self.name = "USDelawareMultiWin"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.delottery.com/Drawing-Games/Multi-Win-Lotto/Number-Of-Winners"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        LottoItem = ItemLoader(item=USDelawareMultiWinItem(), selector=response)
        balls_lst = response.xpath(
            '//div[@class="drawing-ball ball-size-large"]/div/text()').getall()
        rows = response.xpath('//tbody/tr')

        LottoItem.add_value("name", self.name)
        draw_date = rows[0].xpath('./td/text()').getall()[0].strip()
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%m/%d/%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("estimated_next_jackpot", response.xpath('//h1[@class="text-center"]/strong/text()').get())
        LottoItem.add_value("cat_2_prize", '500')
        LottoItem.add_value("cat_3_prize", '20')
        LottoItem.add_value("cat_4_prize", '2')
        LottoItem.add_value("cat_5_prize", '1000')
        LottoItem.add_value("cat_6_prize", '100')
        LottoItem.add_value("cat_7_prize", '20')
        LottoItem.add_value("cat_8_prize", '5')
        LottoItem.add_value("cat_9_prize", '3')
        LottoItem.add_value("cat_10_prize", '2')
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_2_winners", rows[0].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_3_winners", rows[0].xpath('./td/text()').getall()[3])
        LottoItem.add_value("cat_4_winners", rows[0].xpath('./td/text()').getall()[4])
        LottoItem.add_value("cat_5_winners", rows[0].xpath('./td/text()').getall()[5])
        LottoItem.add_value("cat_6_winners", rows[0].xpath('./td/text()').getall()[6])
        LottoItem.add_value("cat_7_winners", rows[0].xpath('./td/text()').getall()[7])
        LottoItem.add_value("cat_8_winners", rows[0].xpath('./td/text()').getall()[8])
        LottoItem.add_value("cat_9_winners", rows[0].xpath('./td/text()').getall()[9])
        LottoItem.add_value("cat_10_winners", rows[0].xpath('./td/text()').getall()[10])
        yield LottoItem.load_item()


class USFloridaLotto(scrapy.Spider):

    name = "USFloridaLotto"

    def start_requests(self):
        self.name = "USFloridaLotto"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.flalottery.com/lotto"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def sum_lst(self, num_lst):
        num_int_lst = []
        for num_str in num_lst:
            value = "".join([s for s in num_str if s.isdigit()])
            num_int_lst.append(int(value))
        summed_nums = sum(num_int_lst)
        return str(summed_nums)

    def parse(self, response):
        LottoItem = ItemLoader(item=USFloridaLottoItem(), selector=response)
        balls_lst = response.xpath('//div[@class="gamePageBalls"]//span[@class="balls"]/text()').getall()
        rows = response.xpath('//tbody/tr')
        draw_date = response.xpath('//div[@class="gamePageNumbers"]/p/text()').getall()[-1]
        draw_date = ",".join(draw_date.split(',')[1:]).strip()

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%B %d, %Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("estimated_next_jackpot", response.xpath(
            '//div[@class="nextJackpot"]/p[@class="gameJackpot"]/text()').get())
        LottoItem.add_value("cat_1_prize", rows[0].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_2_prize", '3000')
        LottoItem.add_value("cat_3_prize", '50')
        LottoItem.add_value("cat_4_prize", '5')
        LottoItem.add_value("cat_5_prize", '2')
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td[@class="column2"]/text()').get())
        LottoItem.add_value("cat_2_winners", self.sum_lst([rows[1].xpath('./td[@class="column2"]/text()').get(),
            rows[2].xpath('./td[@class="column2"]/text()').get(), rows[3].xpath('./td[@class="column2"]/text()').get(),
            rows[4].xpath('./td[@class="column2"]/text()').get(), rows[5].xpath('./td[@class="column2"]/text()').get()]))
        LottoItem.add_value("cat_3_winners", self.sum_lst([rows[6].xpath('./td[@class="column2"]/text()').get(),
            rows[7].xpath('./td[@class="column2"]/text()').get(), rows[8].xpath('./td[@class="column2"]/text()').get(),
            rows[9].xpath('./td[@class="column2"]/text()').get(), rows[10].xpath('./td[@class="column2"]/text()').get()]))
        LottoItem.add_value("cat_4_winners", self.sum_lst([rows[11].xpath('./td[@class="column2"]/text()').get(),
            rows[12].xpath('./td[@class="column2"]/text()').get(), rows[13].xpath('./td[@class="column2"]/text()').get(),
            rows[14].xpath('./td[@class="column2"]/text()').get(), rows[15].xpath('./td[@class="column2"]/text()').get()]))
        LottoItem.add_value("cat_5_winners", rows[16].xpath('./td[@class="column2"]/text()').get())
        yield LottoItem.load_item()


class USFloridaTriplePlay(scrapy.Spider):

    name = "USFloridaTriplePlay"

    def start_requests(self):
        self.name = "USFloridaTriplePlay"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.flalottery.com/jackpotTriplePlay"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=USFloridaTriplePlayItem(), selector=response)
        balls_lst = response.xpath('//div[@class="gamePageBalls"]//span[@class="balls"]/text()').getall()
        rows = response.xpath('//tbody/tr')
        draw_date = response.xpath('//div[@class="gamePageNumbers"]/p/text()').getall()[-1]
        draw_date = ",".join(draw_date.split(',')[1:]).strip()

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%B %d, %Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("estimated_next_jackpot", response.xpath(
            '//div[@class="nextJackpot"]/p[@class="gameJackpot"]/text()').get())
        LottoItem.add_value("cat_1_prize", rows[0].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_4_prize", rows[3].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./td/text()').getall()[1])
        if "rolldown" in response.xpath('//p[@class="luckyMoney rolloverOrWinners"]/text()').get().lower():
            LottoItem.add_value("rolldown", "yes")
        else:
            LottoItem.add_value("rolldown", "no")
        yield LottoItem.load_item()


class USGeorgiaFantasy5(scrapy.Spider):

    name = "USGeorgiaFantasy5"

    def start_requests(self):
        self.name = "USGeorgiaFantasy5"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        headers = {
            'Connection': 'keep-alive',
            'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-User-Agent': 'portal',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://www.galottery.com/en-us/games/draw-games/fantasy-five.html',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }
        url = 'https://www.galottery.com/api/v2/draw-games/draws/page?order=desc&previous-draws=100&game-names=FANTASY+5&size=20&status=CLOSED'
        yield scrapy.Request(url=url, headers=headers, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=USGeorgiaFantasy5Item(), selector=response)
        latest = response.json()['draws'][0]

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", str(latest['results'][0]['primary'][0]))
        LottoItem.add_value("ball1", str(latest['results'][0]['primary'][1]))
        LottoItem.add_value("ball2", str(latest['results'][0]['primary'][2]))
        LottoItem.add_value("ball3", str(latest['results'][0]['primary'][3]))
        LottoItem.add_value("ball4", str(latest['results'][0]['primary'][4]))
        # remove 1 day from draw_date timestamp to get actual draw_date
        draw_timestamp = (latest['drawTime']/1000)-(24*60*60)
        LottoItem.add_value("draw_datetime", str(int(draw_timestamp)))
        LottoItem.add_value("draw_number", str(latest['id']))

        for cat in latest['prizeTiers']:
            prize_category = cat['name']
            num_winners = int(cat['shareCount'])
            prize_value = int(cat['shareAmount'])/(100.0)

            if '5/' in prize_category:
                if num_winners == 0:
                    LottoItem.add_value("cat_1_prize", str(int(latest['estimatedJackpot'])/100.0))
                else:
                    LottoItem.add_value("cat_1_prize", str(prize_value))
                LottoItem.add_value("cat_1_winners", str(num_winners))
            elif '4/' in prize_category:
                LottoItem.add_value("cat_2_prize", str(prize_value))
                LottoItem.add_value("cat_2_winners", str(num_winners))
            elif '3/' in prize_category:
                LottoItem.add_value("cat_3_prize", str(prize_value))
                LottoItem.add_value("cat_3_winners", str(num_winners))
            elif '2/' in prize_category:
                LottoItem.add_value("cat_4_prize", '1') # prize is free ticket
                LottoItem.add_value("cat_4_winners", str(num_winners))

        yield LottoItem.load_item()


class USGeorgiaJumboBucks(scrapy.Spider):

    name = "USGeorgiaJumboBucks"

    def start_requests(self):
        self.name = "USGeorgiaJumboBucks"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        headers = {
            'Connection': 'keep-alive',
            'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-User-Agent': 'portal',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://www.galottery.com/en-us/games/draw-games/jumbo-bucks-lotto.html',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }
        url = 'https://www.galottery.com/api/v2/draw-games/draws/page?order=desc&previous-draws=100&game-names=JUMBO+LOTTO&size=20&status=CLOSED'
        yield scrapy.Request(url=url, headers=headers, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=USGeorgiaJumboBucksItem(), selector=response)
        latest = response.json()['draws'][0]

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", str(latest['results'][0]['primary'][0]))
        LottoItem.add_value("ball1", str(latest['results'][0]['primary'][1]))
        LottoItem.add_value("ball2", str(latest['results'][0]['primary'][2]))
        LottoItem.add_value("ball3", str(latest['results'][0]['primary'][3]))
        LottoItem.add_value("ball4", str(latest['results'][0]['primary'][4]))
        LottoItem.add_value("ball5", str(latest['results'][0]['primary'][5]))
        # remove 1 day from draw_date timestamp to get actual draw_date
        draw_timestamp = (latest['drawTime']/1000)-(24*60*60)
        LottoItem.add_value("draw_datetime", str(int(draw_timestamp)))
        LottoItem.add_value("draw_number", str(latest['id']))

        for cat in latest['prizeTiers']:
            prize_category = cat['name']
            num_winners = int(cat['shareCount'])
            prize_value = int(cat['shareAmount'])/100.0

            if '6/' in prize_category:
                if num_winners == 0:
                    LottoItem.add_value("cat_1_prize", str(int(latest['estimatedJackpot'])/100.0))
                else:
                    LottoItem.add_value("cat_1_prize", str(prize_value))
                LottoItem.add_value("cat_1_winners", str(num_winners))
            elif '5/' in prize_category:
                LottoItem.add_value("cat_2_prize", str(prize_value))
                LottoItem.add_value("cat_2_winners", str(num_winners))
            elif '4/' in prize_category:
                LottoItem.add_value("cat_3_prize", str(prize_value))
                LottoItem.add_value("cat_3_winners", str(num_winners))
            elif '3/' in prize_category:
                LottoItem.add_value("cat_4_prize", str(prize_value))
                LottoItem.add_value("cat_4_winners", str(num_winners))

        yield LottoItem.load_item()


class USIdaho5Star(scrapy.Spider):

    name = "USIdaho5Star"

    def start_requests(self):
        self.name = "USIdaho5Star"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = 'https://www.idaholottery.com/games/draw/5-star-draw'
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        LottoItem = ItemLoader(item=USIdaho5StarItem(), selector=response)
        balls_lst = response.xpath('//div[@id="tab4"]//tbody/tr/td[@data-title="Winning Numbers"]/ul/li/text()').getall()
        rows = response.xpath('//div[@id="tab3"]//table[@class="full-rules-and-odds prize-chart-table"]//tr')

        LottoItem.add_value("name", self.name)
        draw_date = response.xpath('//div[@id="tab4"]//tbody/tr/td[@data-title="Date"]/text()').get()
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%m/%d/%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("estimated_next_jackpot", response.xpath('//td/h5/text()').get())
        jackpot = prize_to_num(response.xpath('//div[@id="tab4"]//tbody/tr/td[@data-title="Jackpot"]/text()').get())
        cat_1_winners = prize_to_num(response.xpath('//div[@id="tab3"]//tr[@data-number="XXXXX"]/td/text()').getall()[-1])
        if cat_1_winners > 0:
            jackpot = jackpot/float(cat_1_winners)
        LottoItem.add_value("cat_1_prize", str(jackpot))
        LottoItem.add_value("cat_2_prize", response.xpath('//div[@id="tab3"]//tr[@data-number="XXXX"]/td/text()').getall()[-2])
        LottoItem.add_value("cat_3_prize", response.xpath('//div[@id="tab3"]//tr[@data-number="XXX"]/td/text()').getall()[-2])
        LottoItem.add_value("cat_4_prize", response.xpath('//div[@id="tab3"]//tr[@data-number="XX"]/td/text()').getall()[-2])
        LottoItem.add_value("cat_1_winners", str(cat_1_winners))
        LottoItem.add_value("cat_2_winners", response.xpath('//div[@id="tab3"]//tr[@data-number="XXXX"]/td/text()').getall()[-1])
        LottoItem.add_value("cat_3_winners", response.xpath('//div[@id="tab3"]//tr[@data-number="XXX"]/td/text()').getall()[-1])
        LottoItem.add_value("cat_4_winners", response.xpath('//div[@id="tab3"]//tr[@data-number="XX"]/td/text()').getall()[-1])
        yield LottoItem.load_item()


class USIdahoCash(scrapy.Spider):

    name = "USIdahoCash"

    def start_requests(self):
        self.name = "USIdahoCash"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = 'https://www.idaholottery.com/games/draw/idaho-cash'
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        LottoItem = ItemLoader(item=USIdahoCashItem(), selector=response)
        balls_lst = response.xpath('//div[@id="tab4"]//tbody/tr/td[@data-title="Winning Numbers"]/ul/li/text()').getall()
        rows = response.xpath('//div[@id="tab3"]//table[@class="full-rules-and-odds prize-chart-table"]//tr')

        LottoItem.add_value("name", self.name)
        draw_date = response.xpath('//div[@id="tab4"]//tbody/tr/td[@data-title="Date"]/text()').get()
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%m/%d/%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("estimated_next_jackpot", response.xpath('//td/h5/text()').get())
        jackpot = prize_to_num(response.xpath('//div[@id="tab4"]//tbody/tr/td[@data-title="Jackpot"]/text()').get())
        cat_1_winners = prize_to_num(response.xpath('//div[@id="tab3"]//tr[@data-number="XXXXX"]/td/text()').getall()[-1])
        if cat_1_winners > 0:
            jackpot = jackpot/float(cat_1_winners)
        LottoItem.add_value("cat_1_prize", str(jackpot))
        LottoItem.add_value("cat_2_prize", response.xpath('//div[@id="tab3"]//tr[@data-number="XXXX"]/td/text()').getall()[-2])
        LottoItem.add_value("cat_3_prize", response.xpath('//div[@id="tab3"]//tr[@data-number="XXX"]/td/text()').getall()[-2])
        LottoItem.add_value("cat_4_prize", '1') # prize is free ticket
        LottoItem.add_value("cat_1_winners", str(cat_1_winners))
        LottoItem.add_value("cat_2_winners", response.xpath('//div[@id="tab3"]//tr[@data-number="XXXX"]/td/text()').getall()[-1])
        LottoItem.add_value("cat_3_winners", response.xpath('//div[@id="tab3"]//tr[@data-number="XXX"]/td/text()').getall()[-1])
        LottoItem.add_value("cat_4_winners", response.xpath('//div[@id="tab3"]//tr[@data-number="XX"]/td/text()').getall()[-1])
        yield LottoItem.load_item()


class USIllinoisLuckyDay(scrapy.Spider):

    name = "USIllinoisLuckyDay"

    def start_requests(self):
        self.name = "USIllinoisLuckyDay"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "http://www.illinoislottery.com/dbg/results/luckydaylotto"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        next_page = response.xpath("//div[@class='exc-content']/ul/li/a/@href").get()
        url = urljoin(response.url, next_page)
        yield scrapy.Request(url, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":10})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=USIllinoisLuckyDayItem(), selector=response)
        balls_lst = response.xpath('//div[@class="result-line "]/div/div/div/text()').getall()
        rows = response.xpath('//tbody/tr')

        LottoItem.add_value("name", self.name)
        draw_date = response.xpath('//span[@class="dbg-result-details__draw-date"]/text()').get().strip()
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%b %d, %Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", str(response.url).split('/')[-1])
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("cat_1_prize", rows[0].xpath('./td/div/text()').getall()[-1])
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./td/div/text()').getall()[-1])
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./td/div/text()').getall()[-1])
        LottoItem.add_value("cat_4_prize", rows[3].xpath('./td/div/text()').getall()[-1])
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./td/text()').getall()[-1])
        yield LottoItem.load_item()


class USIllinoisLotto(scrapy.Spider):

    name = "USIllinoisLotto"

    def start_requests(self):
        self.name = "USIllinoisLotto"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "http://www.illinoislottery.com/dbg/results/lotto"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        next_page = response.xpath("//div[@class='exc-content']/ul/li/a/@href").get()
        url = urljoin(response.url, next_page)
        yield scrapy.Request(url, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":10})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=USIllinoisLottoItem(), selector=response)
        balls_lst = response.xpath('//div[@class="result-line "]/div/div/div/text()').getall()
        rows = response.xpath('//tbody/tr')

        LottoItem.add_value("name", self.name)
        draw_date = response.xpath('//span[@class="dbg-result-details__draw-date"]/text()').get().strip()
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%b %d, %Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", str(response.url).split('/')[-1])
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("bonus_ball", balls_lst[-1])
        LottoItem.add_value("cat_1_prize", rows[0].xpath('./td/div/text()').getall()[-1])
        LottoItem.add_value("cat_2_prize", rows[2].xpath('./td/div/text()').getall()[-1])
        LottoItem.add_value("cat_3_prize", rows[4].xpath('./td/div/text()').getall()[-1])
        LottoItem.add_value("cat_4_prize", rows[6].xpath('./td/div/text()').getall()[-1])
        LottoItem.add_value("cat_5_prize", rows[8].xpath('./td/div/text()').getall()[-1])
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_2_winners", rows[2].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_3_winners", rows[4].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_4_winners", rows[6].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_5_winners", rows[8].xpath('./td/text()').getall()[-1])
        yield LottoItem.load_item()


class USIndianaHoosierLotto(scrapy.Spider):

    name = "USIndianaHoosierLotto"

    # ONLY RETURNS DATA IF THERE IS A DRAW ON DAY OF SCRAPE
    # Have to fill form to get draw results; adds yesterday's date() to get url

    def start_requests(self):
        self.name = "USIndianaHoosierLotto"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.lotteryusa.com/indiana/lotto/"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        self.next_jackpot = response.xpath('//dd[@class="c-next-draw-card__prize-value"]/text()').get().strip()
        date_yesterday = str(datetime.now().date() - timedelta(days=1))
        url = f'https://hoosierlottery.com/games/draw/past-game-results/1/{date_yesterday}/'
        yield scrapy.Request(url=url, callback=self.parse_draw,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse_draw(self, response):
        LottoItem = ItemLoader(item=USIndianaHoosierLottoItem(), selector=response)
        balls = response.xpath('//tr[@class="main-row"]/td[@class="winning-numbers"]/text()').get()
        balls_lst = [i.strip() for i in balls.split('-')]
        rows = response.xpath('//td[@class="expandable-data"]/table[@data-table="results"]/tbody/tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("draw_datetime", response.xpath('//div[@class="form-group"]/input/@value').get())
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])

        LottoItem.add_value("estimated_next_jackpot", self.next_jackpot)
        jackpot = rows[0].xpath('./td/text()').getall()[-2]
        if "jackpot" in jackpot.lower():
            LottoItem.add_value("cat_1_prize", '0')
        else:
            LottoItem.add_value("cat_1_prize", jackpot)
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./td/text()').getall()[-2])
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./td/text()').getall()[-2])
        LottoItem.add_value("cat_4_prize", rows[3].xpath('./td/text()').getall()[-2])
        LottoItem.add_value("cat_5_prize", '2') # prize is free ticket
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_5_winners", rows[4].xpath('./td/text()').getall()[-1])
        yield LottoItem.load_item()


class USIndianaCash5(scrapy.Spider):

    name = "USIndianaCash5"

    # Have to fill form to get draw results; adds yesterday's date() to get url (Daily drawings)

    def start_requests(self):
        self.name = "USIndianaCash5"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://hoosierlottery.com/games/draw/"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        self.next_jackpot = response.xpath(
            '//div[@class="col-12 col-md-4 col-xl-3 mb-4 draw-game-card-col"]')[3].xpath(
                './/span[@class="d-block flip-card-jackpot-amount font-weight-bold mb-3"]/text()').get()
        date_yesterday = str(datetime.now().date() - timedelta(days=1))
        url = 'https://hoosierlottery.com/games/draw/past-game-results/11/' + date_yesterday + '/'
        yield scrapy.Request(url=url, callback=self.parse_draw,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=USIndianaCash5Item(), selector=response)
        balls = response.xpath('//td[@class="winning-numbers"]/text()').get()
        balls_lst = [i.strip() for i in balls.split('-')]
        rows = response.xpath('//td[@class="expandable-data"]/table[@data-table="results"]/tbody/tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("draw_datetime", response.xpath('//div[@class="form-group"]/input/@value').get())
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])

        LottoItem.add_value("estimated_next_jackpot", self.next_jackpot)
        jackpot = rows[0].xpath('./td/text()').getall()[-2]
        if "jackpot" in jackpot.lower():
            LottoItem.add_value("cat_1_prize", '0')
        else:
            LottoItem.add_value("cat_1_prize", jackpot)
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./td/text()').getall()[-2])
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./td/text()').getall()[-2])
        LottoItem.add_value("cat_4_prize", '1') # prize is free ticket
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./td/text()').getall()[-1])
        yield LottoItem.load_item()


class USKansasSuperCash(scrapy.Spider):

    name = "USKansasSuperCash"

    def start_requests(self):
        self.name = "USKansasSuperCash"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = 'https://www.kslottery.com/previous-numbers'
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        next_page = response.xpath("//div[@id='kansascash']//table/tr/td/a/@href").get()
        self.draw_date = response.xpath("//div[@id='kansascash']//table/tr/td/text()").getall()[0]
        self.balls_lst = response.xpath("//div[@id='kansascash']//table/tr/td/text()").getall()[1].split('-')
        self.bonus_number = response.xpath("//div[@id='kansascash']//table/tr/td/text()").getall()[2]
        self.jackpot = response.xpath("//div[@id='kansascash']//table/tr/td/text()").getall()[3]
        url = urljoin(response.url, next_page)
        yield scrapy.Request(url, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":10})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=USKansasSuperCashItem(), selector=response)
        row = response.xpath('//table/tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("draw_datetime", datetime.strptime(self.draw_date, "%m/%d/%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("ball0", self.balls_lst[0].strip())
        LottoItem.add_value("ball1", self.balls_lst[1].strip())
        LottoItem.add_value("ball2", self.balls_lst[2].strip())
        LottoItem.add_value("ball3", self.balls_lst[3].strip())
        LottoItem.add_value("ball4", self.balls_lst[4].strip())
        LottoItem.add_value("bonus_ball", self.bonus_number)
        LottoItem.add_value("estimated_next_jackpot", self.jackpot)
        LottoItem.add_value("cat_1_prize", '') # value will be previous estimated_next but need empty column
        LottoItem.add_value("cat_2_prize", row[1].xpath('./td/text()').getall()[1].strip())
        LottoItem.add_value("cat_3_prize", row[2].xpath('./td/text()').getall()[1].strip())
        LottoItem.add_value("cat_4_prize", row[3].xpath('./td/text()').getall()[1].strip())
        LottoItem.add_value("cat_5_prize", row[4].xpath('./td/text()').getall()[1].strip())
        LottoItem.add_value("cat_6_prize", row[5].xpath('./td/text()').getall()[1].strip())
        LottoItem.add_value("cat_7_prize", row[6].xpath('./td/text()').getall()[1].strip())
        LottoItem.add_value("cat_8_prize", row[7].xpath('./td/text()').getall()[1].strip())
        LottoItem.add_value("cat_1_winners", row[0].xpath('./td/text()').getall()[2].strip())
        LottoItem.add_value("cat_2_winners", row[1].xpath('./td/text()').getall()[2].strip())
        LottoItem.add_value("cat_3_winners", row[2].xpath('./td/text()').getall()[2].strip())
        LottoItem.add_value("cat_4_winners", row[3].xpath('./td/text()').getall()[2].strip())
        LottoItem.add_value("cat_5_winners", row[4].xpath('./td/text()').getall()[2].strip())
        LottoItem.add_value("cat_6_winners", row[5].xpath('./td/text()').getall()[2].strip())
        LottoItem.add_value("cat_7_winners", row[6].xpath('./td/text()').getall()[2].strip())
        LottoItem.add_value("cat_8_winners", row[7].xpath('./td/text()').getall()[2].strip())
        yield LottoItem.load_item()


class USLouisianaLotto(scrapy.Spider):

    name = "USLouisianaLotto"

    def start_requests(self):
        self.name = "USLouisianaLotto"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = 'https://louisianalottery.com/lotto/tab/winning-numbers'
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        LottoItem = ItemLoader(item=USLouisianaLottoItem(), selector=response)
        latest = response.xpath('//div[@class="accordion-inner"]')[0]
        latest_header = response.xpath('//div[@class="accordion-heading"]')[0]
        balls_lst = latest_header.xpath('//span[@class="ball small inline-block"]/text()').getall()
        rows = latest.xpath('.//tbody/tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("draw_datetime", latest.xpath('./div/@data-draw-date').get())
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        jackpot = latest_header.xpath('.//div[@class="accord-head-jp text-right"]/strong/text()').get()
        num_winners = prize_to_num(rows[0].xpath('./td/text()').getall()[-2])
        if num_winners == 0:
            LottoItem.add_value("cat_1_prize", jackpot)
        elif num_winners > 0:
            cat_1_prize = prize_to_num(jackpot)/num_winners
            LottoItem.add_value("cat_1_prize", str(cat_1_prize))
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_4_prize", rows[3].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td/text()').getall()[-2])
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./td/text()').getall()[-2])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./td/text()').getall()[-2])
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./td/text()').getall()[-2])
        yield LottoItem.load_item()


class USLouisianaEasy5(scrapy.Spider):

    name = "USLouisianaEasy5"

    def start_requests(self):
        self.name = "USLouisianaEasy5"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = 'https://louisianalottery.com/easy-5/tab/winning-numbers'
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        LottoItem = ItemLoader(item=USLouisianaEasy5Item(), selector=response)
        latest = response.xpath('//div[@class="accordion-inner"]')[0]
        latest_header = response.xpath('//div[@class="accordion-heading"]')[0]
        balls_lst = latest_header.xpath('//span[@class="ball small inline-block"]/text()').getall()
        rows = latest.xpath('.//tbody/tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("draw_datetime", latest.xpath('./div/@data-draw-date').get())
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        jackpot = latest_header.xpath('.//div[@class="accord-head-jp text-right"]/strong/text()').get()
        num_winners = prize_to_num(rows[0].xpath('./td/text()').getall()[-2])
        if num_winners == 0:
            LottoItem.add_value("cat_1_prize", jackpot)
        elif num_winners > 0:
            cat_1_prize = prize_to_num(jackpot)/num_winners
            LottoItem.add_value("cat_1_prize", str(cat_1_prize))
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_4_prize", rows[3].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td/text()').getall()[-2])
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./td/text()').getall()[-2])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./td/text()').getall()[-2])
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./td/text()').getall()[-2])
        yield LottoItem.load_item()


class USMarylandMultiMatch(scrapy.Spider):

    name = "USMarylandMultiMatch"

    def start_requests(self):
        self.name = "USMarylandMultiMatch"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = 'https://www.mdlottery.com/games/multi-match/detailed-results/'
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        all_links_lst = response.xpath("//section[@id='games']//ul/li/a/@href").getall()
        next_page = [link for link in all_links_lst if "detailed-result" in link and "www.mdlottery.com" in link][0]
        yield scrapy.Request(next_page, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":10})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=USMarylandMultiMatchItem(), selector=response)
        rows = response.xpath('//tbody')[0].xpath('./tr')
        balls_lst = rows[2].xpath('./td/text()').get().split('-')

        LottoItem.add_value("name", self.name)
        draw_date = rows[1].xpath('./td/strong/text()').get().strip()
        try:
            clean_date = datetime.strptime(draw_date, "%A, %B %d, %Y").strftime("%Y-%m-%d")
        except:
            try:
                clean_date = datetime.strptime(draw_date, "%A %B %d, %Y").strftime("%Y-%m-%d")
            except:
                draw_date = draw_date.replace(" ", "")
                draw_date = draw_date.replace(",", "")
                clean_date = datetime.strptime(draw_date, "%A%B%d%Y").strftime("%Y-%m-%d")
        LottoItem.add_value("draw_datetime", clean_date)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("estimated_next_jackpot", rows[17].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("estimated_next_jackpot_cash", rows[18].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_1_prize", rows[14].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_1_prize_cash", rows[15].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_2_prize", rows[3].xpath('./td/text()').get().split('(')[1])
        LottoItem.add_value("cat_3_prize", rows[4].xpath('./td/text()').get().split('(')[1])
        LottoItem.add_value("cat_4_prize", rows[5].xpath('./td/text()').get().split('(')[1])
        LottoItem.add_value("cat_5_prize", rows[7].xpath('./td/text()').get().split('(')[1])
        LottoItem.add_value("cat_6_prize", rows[8].xpath('./td/text()').get().split('(')[1])
        LottoItem.add_value("cat_7_prize", rows[9].xpath('./td/text()').get().split('(')[1])
        LottoItem.add_value("cat_8_prize", rows[10].xpath('./td/text()').get().split('(')[1])
        LottoItem.add_value("cat_9_prize", rows[11].xpath('./td/text()').get().split('(')[1])
        LottoItem.add_value("cat_10_prize", rows[12].xpath('./td/text()').get().split('(')[1])

        match_6 = rows[13].xpath('./td/text()').getall()[-1]
        if "no" in match_6.lower():
            LottoItem.add_value("cat_1_winners", '0')
        else:
            LottoItem.add_value("cat_1_winners", 'yes')
        LottoItem.add_value("cat_2_winners", rows[3].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_3_winners", rows[4].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_4_winners", rows[5].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_5_winners", rows[7].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_6_winners", rows[8].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_7_winners", rows[9].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_8_winners", rows[10].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_9_winners", rows[11].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_10_winners", rows[12].xpath('./td/text()').getall()[-1])
        yield LottoItem.load_item()


class USMassachusettsMegaBucks(scrapy.Spider):

    name = "USMassachusettsMegaBucks"

    # NO NUM OF WINNERS DATA

    def start_requests(self):
        self.name = "USMassachusettsMegaBucks"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = 'https://www.masslottery.com/api/v1/draw-results?cmsPreview=false'
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=USMassachusettsMegaBucksItem(), selector=response)
        game_info = response.json()['winningNumbers'][1]
        latest = response.json()['estimatedJackpot'][1]

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", str(game_info['winningNumbers'][0]))
        LottoItem.add_value("ball1", str(game_info['winningNumbers'][1]))
        LottoItem.add_value("ball2", str(game_info['winningNumbers'][2]))
        LottoItem.add_value("ball3", str(game_info['winningNumbers'][3]))
        LottoItem.add_value("ball4", str(game_info['winningNumbers'][4]))
        LottoItem.add_value("ball5", str(game_info['winningNumbers'][5]))
        LottoItem.add_value("draw_datetime", str(game_info['drawDate']))
        LottoItem.add_value("draw_number", str(game_info['drawNumber']))
        LottoItem.add_value("estimated_next_jackpot", str(latest['estimatedJackpotUSD']))
        LottoItem.add_value("estimated_next_jackpot_cash", str(latest['estimatedCashOptionUSD']))
        LottoItem.add_value("jackpot", '0') # value will be previous estimated_next, need column
        yield LottoItem.load_item()


class USMichiganLotto47(scrapy.Spider):

    name = "USMichiganLotto47"

    def start_requests(self):
        self.name = "USMichiganLotto47"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.lotto.net/michigan-lotto-47/numbers"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        next_page = response.xpath("//div[@class='results-big']/div[@class='row-3']/a/@href").get()
        url = urljoin(response.url, next_page)
        self.draw_date = response.xpath('//div[@class="date"]/span/text()').get().strip()
        yield scrapy.Request(url, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":10})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=USMichiganLotto47Item(), selector=response)
        balls_lst = response.xpath('//ul[@class="balls"]/li/span/text()').getall()
        rows = response.xpath('//table//tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("draw_datetime", datetime.strptime(self.draw_date, "%d %B %Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("cat_1_prize", rows[1].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_2_prize", rows[2].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_3_prize", rows[3].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_4_prize", rows[4].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_1_winners", rows[1].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_2_winners", rows[2].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_3_winners", rows[3].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_4_winners", rows[4].xpath('./td/text()').getall()[-1].strip())
        yield LottoItem.load_item()


class USMichiganFantasy5(scrapy.Spider):

    name = "USMichiganFantasy5"

    def start_requests(self):
        self.name = "USMichiganFantasy5"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.lotto.net/michigan-fantasy-5/numbers"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        next_page = response.xpath("//div[@class='results-big']/div[@class='row-3']/a/@href").get()
        url = urljoin(response.url, next_page)
        self.draw_date = response.xpath('//div[@class="date"]/span/text()').get().strip()
        yield scrapy.Request(url, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":10})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=USMichiganFantasy5Item(), selector=response)
        balls_lst = response.xpath('//ul[@class="balls"]/li/span/text()').getall()
        rows = response.xpath('//table//tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("draw_datetime", datetime.strptime(self.draw_date, "%d %B %Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("cat_1_prize", rows[1].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_2_prize", rows[2].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_3_prize", rows[3].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_4_prize", rows[4].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_1_winners", rows[1].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_2_winners", rows[2].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_3_winners", rows[3].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_4_winners", rows[4].xpath('./td/text()').getall()[-1].strip())
        yield LottoItem.load_item()


class USMinnesotaGopher5(scrapy.Spider):

    name = "USMinnesotaGopher5"

    # NO NUM OF WINNERS DATA

    def start_requests(self):
        self.name = "USMinnesotaGopher5"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.mnlottery.com/winning-numbers?selectedGames[]=1"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=USMinnesotaGopher5Item(), selector=response)
        latest = response.xpath('//div[@id="drawings"]/div[@class="cell new"]')[0]
        balls_lst = latest.xpath('.//ul[@class="lottery-number-list"]/li/text()').getall()

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        draw_date = clean_date_string(latest.xpath('.//p/span/text()').get())
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%B %d, %Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("jackpot", latest.xpath('.//span[@class="lottery-payout"]/text()').get())
        yield LottoItem.load_item()


class USMinnesotaNorthstarCash(scrapy.Spider):

    name = "USMinnesotaNorthstarCash"

    # NO NUM OF WINNERS DATA

    def start_requests(self):
        self.name = "USMinnesotaNorthstarCash"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.mnlottery.com/winning-numbers?selectedGames[]=5"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=USMinnesotaNorthstarCashItem(), selector=response)
        latest = response.xpath('//div[@id="drawings"]/div[@class="cell new"]')[0]
        balls_lst = latest.xpath('.//ul[@class="lottery-number-list"]/li/text()').getall()

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        draw_date = clean_date_string(latest.xpath('.//p/span/text()').get())
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%B %d, %Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("jackpot", latest.xpath('.//span[@class="lottery-payout"]/text()').get())
        yield LottoItem.load_item()


class USMissouriLotto(scrapy.Spider):

    name = "USMissouriLotto"

    def start_requests(self):
        self.name = "USMissouriLotto"
        while True:
            self.req_proxy = get_US_proxy()['http']
            if ":11000" not in self.req_proxy: #port seems to be banned
                break
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.molottery.com/lotto/winning-numbers"
        yield scrapy.Request(url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        url = "https://www.molottery.com/"
        latest = response.xpath('//div[@class="table-responsive"]//tr//@href')[0].get()
        self.jackpot = response.xpath('//div[@class="content"]//tr')
        self.next_jackpot = response.xpath('//div[@class="game-single__right"]//div[@class="game-single-calendar__bottom"]//text()').getall()
        url = urljoin(url, latest)
        yield scrapy.Request(url, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":10})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=USMissouriLottoItem(), selector=response)
        balls_lst = response.xpath('//div[@class="game-single__right"]//div[@class="game-single-calendar__num"]//text()').getall()
        draw_datetime = response.xpath('//div[@class="content"]/h2//text()').get()
        draw_datetime = draw_datetime.replace(",","")
        rows = response.xpath('//div[@class="table-responsive"]//tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_datetime, '%A %B %d %Y').strftime("%Y-%m-%d"))
        LottoItem.add_value("estimated_next_jackpot", self.next_jackpot[0])
        jackpot_winners = prize_to_num(rows[1].xpath('.//td//text()').getall()[1])
        if jackpot_winners > 0:
            LottoItem.add_value("cat_1_prize", rows[1].xpath('.//td//text()').getall()[2])
        else:
            LottoItem.add_value("cat_1_prize", self.jackpot[1].xpath('.//td/text()').getall()[3])
        LottoItem.add_value("cat_2_prize", rows[2].xpath('.//td//text()').getall()[2])
        LottoItem.add_value("cat_3_prize", rows[3].xpath('.//td//text()').getall()[2])
        LottoItem.add_value("cat_4_prize", '1') # prize is free QP ticket
        LottoItem.add_value("cat_1_winners", rows[1].xpath('.//td//text()').getall()[1])
        LottoItem.add_value("cat_2_winners", rows[2].xpath('.//td//text()').getall()[1])
        LottoItem.add_value("cat_3_winners", rows[3].xpath('.//td//text()').getall()[1])
        LottoItem.add_value("cat_4_winners", rows[4].xpath('.//td//text()').getall()[1])

        yield LottoItem.load_item()

class USMississippiMatch5(scrapy.Spider):
    name = "USMississippiMatch5"

    def start_requests(self):
        self.name = "USMississippiMatch5"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}")
        url = "https://www.mslotteryhome.com/games/mm5/"
        yield scrapy.Request(url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self,response):
        self.next_jackpot = prize_to_num(''.join(response.xpath('//div[@class="currentjackpot-number"]//text()').getall()).replace('\n', ''))
        self.balls_lst = response.xpath('//div[@class="lotto-numbers"]//span//text()').getall()
        self.draw_datetime = response.xpath('//p[@class="latestdrawdate"]//text()').get()
        self.draw_datetime = '/'.join(re.findall(r"\d+", self.draw_datetime))
        url = 'https://www.lotterycorner.com/ms/match-5'
        yield scrapy.Request(url=url, callback=self.parse_second,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse_second(self, response):
        self.jackpot = response.xpath('//div[@class="game-results-content"]//div[@class="game-jackpot"]//strong//text()').get()
        url = 'https://www.mslotteryhome.com/browse-winning-numbers/?game=mm5'
        yield scrapy.Request(url=url, callback=self.parse_next,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse_next(self, response):
        randomized = random.randint(1000,9999)
        randomized2 = random.randint(10,99)
        last_draw = response.xpath('//table[@class="numbers-table"]//tbody/tr')
        last_draw = last_draw[0].xpath('.//button').get()
        last_draw = re.search(r"\d+", last_draw)
        last_draw = int(last_draw.group())
        url = f'https://www.mslotteryhome.com/wp-content/themes/mlc22/mslot-ajax-handler.php?game=mm5&page=winning-details&cachebust={randomized2}&draw_post_id={last_draw}&_=166920101234{randomized}'
        yield scrapy.Request(url=url, callback=self.parse_last, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse_last(self, response):
        winners_lst = response.xpath('//table[@class="numbers-table"]//tbody/tr')
        LottoItem = ItemLoader(item=USMississippiMatch5Item(), selector=response)
        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", self.balls_lst[0])
        LottoItem.add_value("ball1", self.balls_lst[1])
        LottoItem.add_value("ball2", self.balls_lst[2])
        LottoItem.add_value("ball3", self.balls_lst[3])
        LottoItem.add_value("ball4", self.balls_lst[4])
        LottoItem.add_value("draw_datetime", datetime.strptime(self.draw_datetime, '%m/%d/%Y').strftime("%Y-%m-%d"))
        if self.next_jackpot <= 1000:
            LottoItem.add_value("estimated_next_jackpot", str(self.next_jackpot * 1000))
        else:
            LottoItem.add_value("estimated_next_jackpot", str(self.next_jackpot))
        LottoItem.add_value("cat_1_prize", str(self.jackpot))
        LottoItem.add_value("cat_2_prize", '200')
        LottoItem.add_value("cat_3_prize", '10')
        LottoItem.add_value("cat_4_prize", '2') # prize is free QP ticket
        LottoItem.add_value("cat_1_winners", winners_lst[0].xpath('.//td[@title="WINNERS"]//text()').get().split()[0])
        LottoItem.add_value("cat_2_winners", winners_lst[1].xpath('.//td[@title="WINNERS"]//text()').get().split()[0])
        LottoItem.add_value("cat_3_winners", winners_lst[2].xpath('.//td[@title="WINNERS"]//text()').get().split()[0])
        LottoItem.add_value("cat_4_winners", winners_lst[3].xpath('.//td[@title="WINNERS"]//text()').get().split()[0])
        yield LottoItem.load_item()


class USMissouriShowMeCash(scrapy.Spider):

    name = "USMissouriShowMeCash"

    def start_requests(self):
        self.name = "USMissouriShowMeCash"
        while True:
            self.req_proxy = get_US_proxy()['http']
            if ":11000" not in self.req_proxy: #port seems to be banned
                break
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.molottery.com/show-me-cash/winning-numbers"
        yield scrapy.Request(url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        url = "https://www.molottery.com/"
        latest = response.xpath('//div[@class="table-responsive"]//tr//@href')[0].get()
        self.jackpot = response.xpath('//div[@class="content"]//tr')
        self.next_jackpot = response.xpath('//div[@class="game-single__right"]//div[@class="game-single-calendar__bottom"]//text()').getall()
        url = urljoin(url, latest)
        yield scrapy.Request(url, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":10})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=USMissouriLottoItem(), selector=response)
        balls_lst = response.xpath('//div[@class="game-single__right"]//div[@class="game-single-calendar__num"]//text()').getall()
        draw_datetime = response.xpath('//div[@class="content"]/h2//text()').get()
        draw_datetime = draw_datetime.replace(",","")
        rows = response.xpath('//div[@class="table-responsive"]//tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_datetime, '%A %B %d %Y').strftime("%Y-%m-%d"))
        LottoItem.add_value("estimated_next_jackpot", self.next_jackpot[0])
        jackpot_winners = prize_to_num(rows[1].xpath('.//td//text()').getall()[1])
        if jackpot_winners > 0:
            LottoItem.add_value("cat_1_prize", rows[1].xpath('.//td//text()').getall()[2])
        else:
            LottoItem.add_value("cat_1_prize", self.jackpot[1].xpath('.//td/text()').getall()[3])
        LottoItem.add_value("cat_2_prize", rows[2].xpath('.//td//text()').getall()[2])
        LottoItem.add_value("cat_3_prize", rows[3].xpath('.//td//text()').getall()[2])
        LottoItem.add_value("cat_4_prize", '1') # prize is free QP ticket
        LottoItem.add_value("cat_1_winners", rows[1].xpath('.//td//text()').getall()[1])
        LottoItem.add_value("cat_2_winners", rows[2].xpath('.//td//text()').getall()[1])
        LottoItem.add_value("cat_3_winners", rows[3].xpath('.//td//text()').getall()[1])
        LottoItem.add_value("cat_4_winners", rows[4].xpath('.//td//text()').getall()[1])

        yield LottoItem.load_item()


class USMontanaBigSkyBonus(scrapy.Spider):

    name = "USMontanaBigSkyBonus"

    def start_requests(self):
        self.name = "USMontanaBigSkyBonus"
        while True:
            self.req_proxy = get_US_proxy()['http']
            if ":11000" not in self.req_proxy: #port seems to be banned
                break
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        self.headers = {
            'authority': 'www.montanalottery.com',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            'dnt': '1',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
            'content-type': 'application/json; charset=UTF-8',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'x-requested-with': 'XMLHttpRequest',
            'sec-ch-ua-platform': '"Windows"',
            'origin': 'https://www.montanalottery.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.montanalottery.com/en/view/game/big-sky-bonus',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }
        self.frmdata = {"gameId":"5269"}
        self.frmdata['currentPage'] = 1
        self.frmdata['startDate'] = datetime.strftime(datetime.now()-timedelta(days=7), "%Y-%m-%d")
        self.frmdata['endDate'] = datetime.strftime(datetime.now(), "%Y-%m-%d")
        self.url = 'https://www.montanalottery.com/en/drawresults'
        yield scrapy.Request(url=self.url, method='POST', headers=self.headers, body=json.dumps(self.frmdata),
                            callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=USMontanaBigSkyBonusItem(), selector=response)
        latest = response.json()['response']['items'][0]
        try:
            LottoItem.add_value("name", self.name)
            jackpot =  str(latest['jackpotAmount']/100)
            draw_date = str(latest['drawDate'])
            LottoItem.add_value("ball0", str(latest['results'][0]['number']))
            LottoItem.add_value("ball1", str(latest['results'][1]['number']))
            LottoItem.add_value("ball2", str(latest['results'][2]['number']))
            LottoItem.add_value("ball3", str(latest['results'][3]['number']))
            LottoItem.add_value("bonus_ball", str(latest['results'][4]['number']))
            LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%m.%d.%y").strftime("%Y-%m-%d"))
            LottoItem.add_value("draw_number", str(latest['drawNumber']))
            jackpot_winners = int(latest['prizes'][0]['winners'])+int(latest['prizes'][1]['winners'])
            jackpot_value = int(latest['jackpotAmount']/100)
            if jackpot_winners > 0:
                LottoItem.add_value("cat_1_prize", str(jackpot_value/float(jackpot_winners)))
            else:
                LottoItem.add_value("cat_1_prize", str(jackpot_value))
            LottoItem.add_value("cat_2_prize", str(latest['prizes'][2]['divident']/100))
            LottoItem.add_value("cat_3_prize", str(latest['prizes'][3]['divident']/100))
            LottoItem.add_value("cat_4_prize", str(latest['prizes'][4]['divident']/100))
            LottoItem.add_value("cat_5_prize", str(latest['prizes'][5]['divident']/100))
            LottoItem.add_value("cat_6_prize", str(latest['prizes'][6]['divident']/100))
            LottoItem.add_value("cat_7_prize", str(latest['prizes'][7]['divident']/100))
            LottoItem.add_value("cat_1_winners", str(jackpot_winners))
            LottoItem.add_value("cat_2_winners", str(latest['prizes'][2]['winners']))
            LottoItem.add_value("cat_3_winners", str(latest['prizes'][3]['winners']))
            LottoItem.add_value("cat_4_winners", str(latest['prizes'][4]['winners']))
            LottoItem.add_value("cat_5_winners", str(latest['prizes'][5]['winners']))
            LottoItem.add_value("cat_6_winners", str(latest['prizes'][6]['winners']))
            LottoItem.add_value("cat_7_winners", str(latest['prizes'][7]['winners']))
            yield LottoItem.load_item()
        except:
            try:
                latest = response.json()['response']['items'][1]
                LottoItem.add_value("name", self.name)
                jackpot =  str(latest['jackpotAmount']/100)
                draw_date = str(latest['drawDate'])
                LottoItem.add_value("ball0", str(latest['results'][0]['number']))
                LottoItem.add_value("ball1", str(latest['results'][1]['number']))
                LottoItem.add_value("ball2", str(latest['results'][2]['number']))
                LottoItem.add_value("ball3", str(latest['results'][3]['number']))
                LottoItem.add_value("bonus_ball", str(latest['results'][4]['number']))
                LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%m.%d.%y").strftime("%Y-%m-%d"))
                LottoItem.add_value("draw_number", str(latest['drawNumber']))
                jackpot_winners = int(latest['prizes'][0]['winners'])+int(latest['prizes'][1]['winners'])
                jackpot_value = int(latest['jackpotAmount']/100)
                if jackpot_winners > 0:
                    LottoItem.add_value("cat_1_prize", str(jackpot_value/float(jackpot_winners)))
                else:
                    LottoItem.add_value("cat_1_prize", str(jackpot_value))
                LottoItem.add_value("cat_2_prize", str(latest['prizes'][2]['divident']/100))
                LottoItem.add_value("cat_3_prize", str(latest['prizes'][3]['divident']/100))
                LottoItem.add_value("cat_4_prize", str(latest['prizes'][4]['divident']/100))
                LottoItem.add_value("cat_5_prize", str(latest['prizes'][5]['divident']/100))
                LottoItem.add_value("cat_6_prize", str(latest['prizes'][6]['divident']/100))
                LottoItem.add_value("cat_7_prize", str(latest['prizes'][7]['divident']/100))
                LottoItem.add_value("cat_1_winners", str(jackpot_winners))
                LottoItem.add_value("cat_2_winners", str(latest['prizes'][2]['winners']))
                LottoItem.add_value("cat_3_winners", str(latest['prizes'][3]['winners']))
                LottoItem.add_value("cat_4_winners", str(latest['prizes'][4]['winners']))
                LottoItem.add_value("cat_5_winners", str(latest['prizes'][5]['winners']))
                LottoItem.add_value("cat_6_winners", str(latest['prizes'][6]['winners']))
                LottoItem.add_value("cat_7_winners", str(latest['prizes'][7]['winners']))
                yield LottoItem.load_item()
            except:
                self.frmdata['currentPage'] = 2
                yield scrapy.Request(url=self.url, method='POST', headers=self.headers, body=json.dumps(self.frmdata),
                    callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":10})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=USMontanaBigSkyBonusItem(), selector=response)
        latest = response.json()['response']['items'][0]

        LottoItem.add_value("name", self.name)
        jackpot =  str(latest['jackpotAmount']/100)
        draw_date = str(latest['drawDate'])
        LottoItem.add_value("ball0", str(latest['results'][0]['number']))
        LottoItem.add_value("ball1", str(latest['results'][1]['number']))
        LottoItem.add_value("ball2", str(latest['results'][2]['number']))
        LottoItem.add_value("ball3", str(latest['results'][3]['number']))
        LottoItem.add_value("bonus_ball", str(latest['results'][4]['number']))
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%m.%d.%y").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", str(latest['drawNumber']))
        jackpot_winners = int(latest['prizes'][0]['winners'])+int(latest['prizes'][1]['winners'])
        jackpot_value = int(latest['jackpotAmount']/100)
        if jackpot_winners > 0:
            LottoItem.add_value("cat_1_prize", str(jackpot_value/float(jackpot_winners)))
        else:
            LottoItem.add_value("cat_1_prize", str(jackpot_value))
        LottoItem.add_value("cat_2_prize", str(latest['prizes'][2]['divident']/100))
        LottoItem.add_value("cat_3_prize", str(latest['prizes'][3]['divident']/100))
        LottoItem.add_value("cat_4_prize", str(latest['prizes'][4]['divident']/100))
        LottoItem.add_value("cat_5_prize", str(latest['prizes'][5]['divident']/100))
        LottoItem.add_value("cat_6_prize", str(latest['prizes'][6]['divident']/100))
        LottoItem.add_value("cat_7_prize", str(latest['prizes'][7]['divident']/100))
        LottoItem.add_value("cat_1_winners", str(jackpot_winners))
        LottoItem.add_value("cat_2_winners", str(latest['prizes'][2]['winners']))
        LottoItem.add_value("cat_3_winners", str(latest['prizes'][3]['winners']))
        LottoItem.add_value("cat_4_winners", str(latest['prizes'][4]['winners']))
        LottoItem.add_value("cat_5_winners", str(latest['prizes'][5]['winners']))
        LottoItem.add_value("cat_6_winners", str(latest['prizes'][6]['winners']))
        LottoItem.add_value("cat_7_winners", str(latest['prizes'][7]['winners']))
        yield LottoItem.load_item()


class USMontanaCash(scrapy.Spider):

    name = "USMontanaCash"

    # Here cat_1 = win without MaxCash

    def start_requests(self):
        self.name = "USMontanaCash"
        while True:
            self.req_proxy = get_US_proxy()['http']
            if ":11000" not in self.req_proxy: #port seems to be banned
                break
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        self.headers = {
            'authority': 'www.montanalottery.com',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            'dnt': '1',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
            'content-type': 'application/json; charset=UTF-8',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'x-requested-with': 'XMLHttpRequest',
            'sec-ch-ua-platform': '"Windows"',
            'origin': 'https://www.montanalottery.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.montanalottery.com/en/view/game/montana-cash',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }
        self.frmdata = {"gameId":"5108"}
        self.frmdata['startDate'] = datetime.strftime(datetime.now()-timedelta(days=7), "%Y-%m-%d")
        self.frmdata['endDate'] = datetime.strftime(datetime.now(), "%Y-%m-%d")
        self.url = 'https://www.montanalottery.com/en/drawresults'
        yield scrapy.Request(url=self.url, method='POST', headers=self.headers, body=json.dumps(self.frmdata),
            callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=USMontanaCashItem(), selector=response)
        estimated = response.json()['response']['items'][0]
        latest = response.json()['response']['items'][1]
        LottoItem.add_value("name", self.name)
        draw_date = str(latest['drawDate'])
        LottoItem.add_value("ball0", str(latest['results'][0]['number']))
        LottoItem.add_value("ball1", str(latest['results'][1]['number']))
        LottoItem.add_value("ball2", str(latest['results'][2]['number']))
        LottoItem.add_value("ball3", str(latest['results'][3]['number']))
        LottoItem.add_value("ball4", str(latest['results'][4]['number']))
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%m.%d.%y").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", str(latest['drawNumber']))
        LottoItem.add_value("estimated_next_jackpot", str(estimated['jackpotAmounts'][0]/100.0))
        if latest['prizes'][0]['winners'] > 0:
            cat_1 = str(latest['prizes'][0]['divident']/100.0)
        else:
            cat_1 = str(latest['prizes'][0]['jackpot']/100.0)
        LottoItem.add_value("cat_1_prize", cat_1)
        LottoItem.add_value("cat_2_prize", str(latest['prizes'][1]['divident']/100))
        LottoItem.add_value("cat_3_prize", str(latest['prizes'][2]['divident']/100))
        LottoItem.add_value("cat_4_prize", str(latest['prizes'][3]['divident']/100))
        LottoItem.add_value("cat_1_winners", str(latest['prizes'][0]['winners']))
        LottoItem.add_value("cat_2_winners", str(latest['prizes'][1]['winners']))
        LottoItem.add_value("cat_3_winners", str(latest['prizes'][2]['winners']))
        LottoItem.add_value("cat_4_winners", str(latest['prizes'][3]['winners']))
        yield LottoItem.load_item()
                



class USMontanaMaxCash(scrapy.Spider):

    name = "USMontanaMaxCash"

    # 'MaxCash' costs additional $1 to play for 2nd prog jackpot
    # cat_1 = just 2nd prog. jackpot value

    def start_requests(self):
        self.name = "USMontanaMaxCash"
        while True:
            self.req_proxy = get_US_proxy()['http']
            if ":11000" not in self.req_proxy: #port seems to be banned
                break
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        self.headers = {
            'authority': 'www.montanalottery.com',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            'dnt': '1',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
            'content-type': 'application/json; charset=UTF-8',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'x-requested-with': 'XMLHttpRequest',
            'sec-ch-ua-platform': '"Windows"',
            'origin': 'https://www.montanalottery.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.montanalottery.com/en/view/game/montana-cash',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }
        self.frmdata = {"gameId":"5108"}
        self.frmdata['startDate'] = datetime.strftime(datetime.now()-timedelta(days=7), "%Y-%m-%d")
        self.frmdata['endDate'] = datetime.strftime(datetime.now(), "%Y-%m-%d")
        self.url = 'https://www.montanalottery.com/en/drawresults'
        yield scrapy.Request(url=self.url, method='POST', headers=self.headers, body=json.dumps(self.frmdata),
            callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=USMontanaMaxCashItem(), selector=response)
        latest = response.json()['response']['items'][0]
        LottoItem.add_value("name", self.name)
        draw_date = str(latest['drawDate'])
        LottoItem.add_value("ball0", str(latest['results'][0]['number']))
        LottoItem.add_value("ball1", str(latest['results'][1]['number']))
        LottoItem.add_value("ball2", str(latest['results'][2]['number']))
        LottoItem.add_value("ball3", str(latest['results'][3]['number']))
        LottoItem.add_value("ball4", str(latest['results'][4]['number']))
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%m.%d.%y").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", str(latest['drawNumber']))
        LottoItem.add_value("estimated_next_jackpot", str(sum([latest['jackpotAmounts'][0]/100.0,
            latest['jackpotAmounts'][1]/100.0])))
        if latest['prizes'][4]['winners'] > 0:
            cat_1 = str(latest['prizes'][4]['divident']/100.0)
        else:
            cat_1 = str(latest['jackpotAmounts'][0]/100.0)
        LottoItem.add_value("cat_1_prize", cat_1)
        LottoItem.add_value("cat_1_winners", str(latest['prizes'][4]['winners']))
        yield LottoItem.load_item()

class USNebraskaPick5(scrapy.Spider):

    name = "USNebraskaPick5"

    def start_requests(self):
        self.name = "USNebraskaPick5"
        while True:
            self.req_proxy = get_US_proxy()['http']
            if ":11000" not in self.req_proxy: #port seems to be banned
                break
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://nelottery.com/homeapp/lotto/31/gamedetail"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=USNebraskaPick5Item(), selector=response)
        balls_lst = [i.strip() for i in response.xpath('//table[@class="numbertable"]//tr/td//text()').getall()[1].split(',')]
        rows = response.xpath('//table[@class="numbertable"]')[1].xpath('.//tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        draw_date = response.xpath('//table[@class="numbertable"]//tr/td/strong/text()').get().strip()
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%m/%d/%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("estimated_next_jackpot", response.xpath('//span[@class="detail_jack_large"]/text()').get())
        LottoItem.add_value("cat_1_prize", rows[1].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_2_prize", rows[2].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_3_prize", rows[3].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_4_prize", rows[4].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_1_winners", rows[1].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_2_winners", rows[2].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_3_winners", rows[3].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_4_winners", rows[4].xpath('./td/text()').getall()[-1])
        yield LottoItem.load_item()


class USNewJerseyPick6(scrapy.Spider):

    name = "USNewJerseyPick6"

    # scraped via lotto.net since API no longer gives winner data

    def start_requests(self):
        self.name = "USNewJerseyPick6"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.lotto.net/new-jersey-pick-6/numbers"
        #url = 'https://www.njlottery.com/api/v2/draw-games/draws/?previous-draws=1&next-draws=0&game-names=Pick+6'
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        self.next_jackpot = response.xpath('//div[@class="jackpot"]//span/text()').getall()[1].strip()
        self.draw_date = response.xpath('//div[@class="date"]/span/text()').get().strip()
        next_page = response.xpath("//div[@class='row-3']/a/@href").get()
        url = urljoin(response.url, next_page)
        yield scrapy.Request(url, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":10})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=USNewJerseyPick6Item(), selector=response)
        balls_lst = response.xpath('//ul[@class="balls"]/li/span/text()').getall()
        rows = response.xpath('//table//tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("draw_datetime", datetime.strptime(self.draw_date, "%d %B %Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("estimated_next_jackpot", self.next_jackpot)
        LottoItem.add_value("cat_1_prize", rows[1].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_2_prize", rows[2].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_3_prize", rows[3].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_4_prize", rows[4].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_1_winners", rows[1].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_2_winners", rows[2].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_3_winners", rows[3].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_4_winners", rows[4].xpath('./td/text()').getall()[-1].strip())
        yield LottoItem.load_item()


class USNewJerseyCash5(scrapy.Spider):

    name = "USNewJerseyCash5"

    def start_requests(self):
        self.name = "USNewJerseyCash5"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = 'https://www.njlottery.com/api/v2/draw-games/draws/?previous-draws=1&next-draws=0&game-names=Cash+5'
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=USNewJerseyCash5Item(), selector=response)
        latest = response.json()['draws'][0]

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", str(latest['results'][0]['primary'][0]))
        LottoItem.add_value("ball1", str(latest['results'][0]['primary'][1]))
        LottoItem.add_value("ball2", str(latest['results'][0]['primary'][2]))
        LottoItem.add_value("ball3", str(latest['results'][0]['primary'][3]))
        LottoItem.add_value("ball4", str(latest['results'][0]['primary'][4]))
        LottoItem.add_value("draw_datetime", str(latest['drawTime']))
        LottoItem.add_value("draw_number", str(latest['id']))
        LottoItem.add_value("jackpot_cash", str(latest['annuityCashOption']/100.0))
        if latest['prizeTiers'][0]['shareCount'] > 0:
            LottoItem.add_value("cat_1_prize", str(latest['prizeTiers'][0]['shareAmount']/100.0))
        else:
            LottoItem.add_value("cat_1_prize", str(latest['estimatedJackpot']/100.0))
        LottoItem.add_value("cat_2_prize", str(latest['prizeTiers'][1]['shareAmount']/100.0))
        LottoItem.add_value("cat_3_prize", str(latest['prizeTiers'][2]['shareAmount']/100.0))
        LottoItem.add_value("cat_1_winners", str(latest['prizeTiers'][0]['shareCount']))
        LottoItem.add_value("cat_2_winners", str(latest['prizeTiers'][1]['shareCount']))
        LottoItem.add_value("cat_3_winners", str(latest['prizeTiers'][2]['shareCount']))
        yield LottoItem.load_item()


class USNewMexicoRoadRunnerCash(scrapy.Spider):

    name = "USNewMexicoRoadRunnerCash"

    # NO NUM OF WINNERS DATA

    def start_requests(self):
        self.name = "USNewMexicoRoadRunnerCash"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://nmlotterydynamic.sks.com/rts/games/roadrunnercash/drawresults.aspx"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })


    def parse(self, response):
        LottoItem = ItemLoader(item=USNewMexicoRoadRunnerCashItem(), selector=response)
        balls_lst = response.xpath('//ul[@class="winning-numbers"]/li/text()').getall()

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        draw_date = response.xpath('//div[@class="draw-results roadrunner-cash"]//span[@class="date"]/text()').get().strip()
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%B %d, %Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("estimated_next_jackpot", response.xpath(
            '//div[@class="draw-results roadrunner-cash"]/p[@class="jackpot-amount"]/text()').get())
        yield LottoItem.load_item()


class USNewYorkLotto(scrapy.Spider):

    name = "USNewYorkLotto"

    def start_requests(self):
        self.name = "USNewYorkLotto"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://nylottery.ny.gov/drupal-api/api/v2/winning_numbers?_format=json&nid=26&page=0"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=USNewYorkLottoItem(), selector=response)

        try:
            latest = response.json()['rows'][0]
            jackpot = str(latest['jackpot'])
            cat_1_prize = str(latest['local_winners'][0]['prize_amount'])
        except:
            latest = response.json()['rows'][1]
            jackpot = str(latest['jackpot'])
            cat_1_prize = str(latest['local_winners'][0]['prize_amount'])
        LottoItem.add_value("name", self.name)
        LottoItem.add_value("draw_datetime", str(latest['date']))
        LottoItem.add_value("ball0", str(latest['winning_numbers'][0]))
        LottoItem.add_value("ball1", str(latest['winning_numbers'][1]))
        LottoItem.add_value("ball2", str(latest['winning_numbers'][2]))
        LottoItem.add_value("ball3", str(latest['winning_numbers'][3]))
        LottoItem.add_value("ball4", str(latest['winning_numbers'][4]))
        LottoItem.add_value("ball5", str(latest['winning_numbers'][5]))
        LottoItem.add_value("bonus_ball", str(latest['bonus_number']))
        if int(latest['local_winners'][0]['prize_winners']) == 0:
            LottoItem.add_value("cat_1_prize", jackpot)
        else:
            LottoItem.add_value("cat_1_prize", cat_1_prize)
        LottoItem.add_value("cat_2_prize", str(latest['local_winners'][1]['prize_amount']))
        LottoItem.add_value("cat_3_prize", str(latest['local_winners'][2]['prize_amount']))
        LottoItem.add_value("cat_4_prize", str(latest['local_winners'][3]['prize_amount']))
        LottoItem.add_value("cat_5_prize", str(latest['local_winners'][4]['prize_amount']))
        LottoItem.add_value("cat_1_winners", str(latest['local_winners'][0]['prize_winners']))
        LottoItem.add_value("cat_2_winners", str(latest['local_winners'][1]['prize_winners']))
        LottoItem.add_value("cat_3_winners", str(latest['local_winners'][2]['prize_winners']))
        LottoItem.add_value("cat_4_winners", str(latest['local_winners'][3]['prize_winners']))
        LottoItem.add_value("cat_5_winners", str(latest['local_winners'][4]['prize_winners']))
        yield LottoItem.load_item()


class USNorthCarolinaCash5(scrapy.Spider):

    name = "USNorthCarolinaCash5"

    def start_requests(self):
        self.name = "USNorthCarolinaCash5"
        while True:
            self.req_proxy = get_US_proxy()['http']
            if ":11000" not in self.req_proxy: #port seems to be banned
                break
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = 'https://nclottery.com/Cash5Past'
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        latest = response.xpath('//tbody/tr')[0]
        self.date = latest.xpath('./td/text()').get()
        self.advertised_jackpot = latest.xpath('./td')[2].xpath('./text()').get()
        next_page = latest.xpath('.//a/@href').getall()[-1]
        url = urljoin(response.url, next_page)
        yield scrapy.Request(url=url, callback=self.parse_draw,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=USNorthCarolinaCash5Item(), selector=response)
        balls_lst = response.xpath('//div[@class="ball-row"]/span[@class="ball"]/text()').getall()
        rows = response.xpath('//table[@class="datatable payout_results"]/tbody/tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        try:
            draw_date = datetime.strptime(self.date, "%Y %b %d").strftime("%Y-%m-%d")
        except:
            draw_date = datetime.strptime(self.date, "%b %d, %Y").strftime("%Y-%m-%d")
        LottoItem.add_value("draw_datetime", draw_date)
        LottoItem.add_value("estimated_next_jackpot", response.xpath(
            '//div[@class="box JackpotCash5"]/span[@class="prize"]/text()').get())
        jackpot = rows[0].xpath('./td/span/text()').get()
        if "rollover" in jackpot.lower():
            LottoItem.add_value("cat_1_prize", self.advertised_jackpot)
        else:
            LottoItem.add_value("cat_1_prize", jackpot)
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./td/span/text()').get())
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./td/span/text()').get())
        LottoItem.add_value("cat_4_prize", rows[3].xpath('./td/span/text()').get())
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td/span/text()').getall()[-1])
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./td/span/text()').getall()[-1])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./td/span/text()').getall()[-1])
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./td/span/text()').getall()[-1])
        yield LottoItem.load_item()


class USOhioLotto(scrapy.Spider):

    name = "USOhioLotto"

    # NO NUM OF WINNERS DATA
    # Using lotteryusa since Ohio website requires selenium to scrape

    def start_requests(self):
        self.name = "USOhioLotto"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.lotteryusa.com/ohio/classic-lotto/"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        self.latest = response.xpath('//table[@class="c-results-table"]/tbody/tr')[0]
        self.balls_lst = self.latest.xpath('.//ul/li/text()').getall()
        date_now = self.latest.xpath('.//time/@datetime').get()
        url = f'https://www.lottonumbers.com/ohio-classic-lotto/results/{date_now}'
        yield scrapy.Request(url=url, callback=self.parse_next, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse_next(self, response):
        LottoItem = ItemLoader(item=USOhioLottoItem(), selector=response)
        rows = response.xpath('//div[@class="box-container"]//tbody[1]/tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", self.balls_lst[0])
        LottoItem.add_value("ball1", self.balls_lst[1])
        LottoItem.add_value("ball2", self.balls_lst[2])
        LottoItem.add_value("ball3", self.balls_lst[3])
        LottoItem.add_value("ball4", self.balls_lst[4])
        LottoItem.add_value("ball5", self.balls_lst[5])
        LottoItem.add_value("cat_2_prize", rows[2].xpath('./td//text()').getall()[1].strip())
        LottoItem.add_value("cat_3_prize", rows[3].xpath('./td//text()').getall()[1].strip())
        LottoItem.add_value("cat_4_prize", rows[4].xpath('./td//text()').getall()[1].strip())
        LottoItem.add_value("draw_datetime", self.latest.xpath('.//time/@datetime').get())
        LottoItem.add_value("jackpot", self.latest.xpath('.//dd/text()').get().strip())
        LottoItem.add_value("estimated_next_jackpot", response.xpath(
            '//div[@class="estimated-jackpot"]//text()').get())
        LottoItem.add_value("total_winnings", response.xpath('//tr[@class="totals"]/td[@class="righty"]//text()').getall()[2].strip())
        yield LottoItem.load_item()


class USOhioRollingCash5(scrapy.Spider):

    name = "USOhioRollingCash5"

    # NO NUM OF WINNERS DATA
    # Using lotteryusa since Ohio website requires selenium to scrape

    def start_requests(self):
        self.name = "USOhioRollingCash5"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.lotteryusa.com/ohio/rolling-cash-5/"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=USOhioRollingCash5Item(), selector=response)
        latest = response.xpath('//table[@class="c-results-table"]/tbody/tr')[0]
        balls_lst = latest.xpath('.//ul/li/text()').getall()

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("draw_datetime", latest.xpath('.//time/@datetime').get())
        LottoItem.add_value("jackpot", latest.xpath('.//dd/text()').get().strip())
        LottoItem.add_value("estimated_next_jackpot", response.xpath(
            '//div[@class="c-next-draw-box__game-prize"]/dd/text()').get())
        yield LottoItem.load_item()


class USOregonMegaBucks(scrapy.Spider):

    name = "USOregonMegaBucks"

    def start_requests(self):
        self.name = "USOregonMegaBucks"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        headers = {
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
            'Ocp-Apim-Subscription-Key': '683ab88d339c4b22b2b276e3c2713809',
            'Origin': 'https://www.oregonlottery.org',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://www.oregonlottery.org/megabucks/winning-numbers/',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }
        date_end = datetime.strftime(datetime.now().date(), "%m/%d/%y")
        date_start = datetime.strftime(datetime.now().date()-timedelta(days=30), "%m/%d/%y")
        base_url = 'https://api2.oregonlottery.org/drawresults/ByDrawDate?gameSelector=mb&startingDate=xxxxx&endingDate=yyyyy&pageSize=1000&includeOpen=False'
        url = base_url.replace('yyyyy', date_end)
        url = url.replace('xxxxx', date_start)
        yield scrapy.Request(url=url, callback=self.parse, headers=headers, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=USOregonMegaBucksItem(), selector=response)
        latest = response.json()[0]

        LottoItem.add_value("name", self.name)
        draw_date = str(latest['DrawDateTime'])
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", str(latest['DrawNumber']))
        LottoItem.add_value("ball0", str(latest['WinningNumbers'][0]))
        LottoItem.add_value("ball1", str(latest['WinningNumbers'][1]))
        LottoItem.add_value("ball2", str(latest['WinningNumbers'][2]))
        LottoItem.add_value("ball3", str(latest['WinningNumbers'][3]))
        LottoItem.add_value("ball4", str(latest['WinningNumbers'][4]))
        LottoItem.add_value("ball5", str(latest['WinningNumbers'][5]))
        LottoItem.add_value("cat_1_prize", str(latest['JackpotShareAmount']))
        # prize values will be '0' unless won
        LottoItem.add_value("cat_2_prize", str(latest['ShareAmounts'][1]))
        LottoItem.add_value("cat_3_prize", str(latest['ShareAmounts'][3]))
        LottoItem.add_value("cat_4_prize", str(latest['ShareAmounts'][5]))
        LottoItem.add_value("cat_1_winners", str(latest['OregonJackpotWinners']))
        LottoItem.add_value("cat_2_winners", str(latest['OregonShareCounts'][1]))
        LottoItem.add_value("cat_3_winners", str(latest['OregonShareCounts'][3]))
        LottoItem.add_value("cat_4_winners", str(latest['OregonShareCounts'][5]))
        yield LottoItem.load_item()


class USOregonLuckyLines(scrapy.Spider):

    name = "USOregonLuckyLines"

    def start_requests(self):
        self.name = "USOregonLuckyLines"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        headers = {
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
            'Ocp-Apim-Subscription-Key': '683ab88d339c4b22b2b276e3c2713809',
            'Origin': 'https://www.oregonlottery.org',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://www.oregonlottery.org/lucky-lines/winning-numbers/',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }
        date_end = datetime.strftime(datetime.now().date(), "%m/%d/%y")
        date_start = datetime.strftime(datetime.now().date()-timedelta(days=30), "%m/%d/%y")
        base_url = 'https://api2.oregonlottery.org/drawresults/ByDrawDate?gameSelector=ll&startingDate=xxxxx&endingDate=yyyyy&pageSize=1000&includeOpen=False'
        url = base_url.replace('yyyyy', date_end)
        url = url.replace('xxxxx', date_start)
        yield scrapy.Request(url=url, callback=self.parse, headers=headers, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=USOregonLuckyLinesItem(), selector=response)
        latest = response.json()[0]

        LottoItem.add_value("name", self.name)
        draw_date = str(latest['DrawDateTime'])
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", str(latest['DrawNumber']))
        LottoItem.add_value("ball0", str(latest['WinningNumbers'][0]))
        LottoItem.add_value("ball1", str(latest['WinningNumbers'][1]))
        LottoItem.add_value("ball2", str(latest['WinningNumbers'][2]))
        LottoItem.add_value("ball3", str(latest['WinningNumbers'][3]))
        LottoItem.add_value("ball4", str(latest['WinningNumbers'][4]))
        LottoItem.add_value("ball5", str(latest['WinningNumbers'][5]))
        LottoItem.add_value("ball6", str(latest['WinningNumbers'][6]))
        LottoItem.add_value("ball7", str(latest['WinningNumbers'][7]))
        if int(latest['OregonJackpotWinners']) == 0:
            LottoItem.add_value("cat_1_prize", str(latest['EstimatedJackpot']))
        else:
            LottoItem.add_value("cat_1_prize", str(latest['JackpotShareAmount']))
        LottoItem.add_value("cat_2_prize", str(latest['ShareAmounts'][0]))
        LottoItem.add_value("cat_3_prize", str(latest['ShareAmounts'][1]))
        LottoItem.add_value("cat_4_prize", str(latest['ShareAmounts'][2]))
        LottoItem.add_value("cat_5_prize", str(latest['ShareAmounts'][3]))
        LottoItem.add_value("cat_6_prize", str(latest['ShareAmounts'][4]))
        LottoItem.add_value("cat_7_prize", str(latest['ShareAmounts'][5]))
        LottoItem.add_value("cat_1_winners", str(latest['OregonJackpotWinners']))
        LottoItem.add_value("cat_2_winners", str(latest['OregonShareCounts'][0]))
        LottoItem.add_value("cat_3_winners", str(latest['OregonShareCounts'][1]))
        LottoItem.add_value("cat_4_winners", str(latest['OregonShareCounts'][2]))
        LottoItem.add_value("cat_5_winners", str(latest['OregonShareCounts'][3]))
        LottoItem.add_value("cat_6_winners", str(latest['OregonShareCounts'][4]))
        LottoItem.add_value("cat_7_winners", str(latest['OregonShareCounts'][5]))
        yield LottoItem.load_item()


class USPennsylvaniaCash5(scrapy.Spider):

    name = "USPennsylvaniaCash5"

    def start_requests(self):
        self.name = "USPennsylvaniaCash5"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        year = datetime.strftime(datetime.now()-timedelta(days=1), "%Y")
        base_url = 'https://www.palottery.state.pa.us/Custom/uploadedfiles/winning-numbers-history/PastWinningNumbers.ashx?g=8&y=xxxxx'
        url = base_url.replace('xxxxx', year)
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=USPennsylvaniaCash5Item(), selector=response)
        latest = response.json()[0]

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("draw_datetime", str(latest['drawingNumberDate']))
        LottoItem.add_value("draw_number", str(latest['drawingNumberID']))
        LottoItem.add_value("ball0", str(latest['drawingNumber1']))
        LottoItem.add_value("ball1", str(latest['drawingNumber2']))
        LottoItem.add_value("ball2", str(latest['drawingNumber3']))
        LottoItem.add_value("ball3", str(latest['drawingNumber4']))
        LottoItem.add_value("ball4", str(latest['drawingNumber5']))
        if prize_to_num(latest['drawingNumberPayoutData'].split('5>')[1].split('<')[0]) == 0:
            LottoItem.add_value("estimated_next_jackpot", str(latest['drawingNumberPayoutData'].split('5>')[3].split('<')[0]))
            LottoItem.add_value("cat_1_prize", '0')
        else:
            LottoItem.add_value("estimated_next_jackpot", '0')
            LottoItem.add_value("cat_1_prize", str(latest['drawingNumberPayoutData'].split('5>')[3].split('<')[0]))
        LottoItem.add_value("cat_2_prize", str(latest['drawingNumberPayoutData'].split('4>')[3].split('<')[0]))
        LottoItem.add_value("cat_3_prize", str(latest['drawingNumberPayoutData'].split('3>')[3].split('<')[0]))
        LottoItem.add_value("cat_4_prize", str(latest['drawingNumberPayoutData'].split('2>')[3].split('<')[0]))
        LottoItem.add_value("cat_1_winners", str(latest['drawingNumberPayoutData'].split('5>')[1].split('<')[0]))
        LottoItem.add_value("cat_2_winners", str(latest['drawingNumberPayoutData'].split('4>')[1].split('<')[0]))
        LottoItem.add_value("cat_3_winners", str(latest['drawingNumberPayoutData'].split('3>')[1].split('<')[0]))
        LottoItem.add_value("cat_4_winners", str(latest['drawingNumberPayoutData'].split('2>')[1].split('<')[0]))
        yield LottoItem.load_item()


class USPennsylvaniaMatch6(scrapy.Spider):

    name = "USPennsylvaniaMatch6"

    def start_requests(self):
        self.name = "USPennsylvaniaMatch6"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        year = datetime.strftime(datetime.now()-timedelta(days=1), "%Y")
        base_url = 'https://www.palottery.state.pa.us/Custom/uploadedfiles/winning-numbers-history/PastWinningNumbers.ashx?g=11&y=xxxxx'
        url = base_url.replace('xxxxx', year)
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=USPennsylvaniaMatch6Item(), selector=response)
        latest = response.json()[0]

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("draw_datetime", str(latest['drawingNumberDate']))
        LottoItem.add_value("draw_number", str(latest['drawingNumberID']))
        LottoItem.add_value("ball0", str(latest['drawingNumber1']))
        LottoItem.add_value("ball1", str(latest['drawingNumber2']))
        LottoItem.add_value("ball2", str(latest['drawingNumber3']))
        LottoItem.add_value("ball3", str(latest['drawingNumber4']))
        LottoItem.add_value("ball4", str(latest['drawingNumber5']))
        LottoItem.add_value("ball5", str(latest['drawingNumber6']))
        if prize_to_num(latest['drawingNumberPayoutData'].split('numberofWinners66>')[1].split('<')[0]) == 0:
            LottoItem.add_value("estimated_next_jackpot", str(latest['drawingNumberPayoutData'].split('AmountReceived66>')[1].split('<')[0]))
            LottoItem.add_value("cat_1_prize", '0')
        else: # i.e. someone has won and jackpot will reset to $500k next draw
            LottoItem.add_value("estimated_next_jackpot", '$500,000')
            LottoItem.add_value("cat_1_prize", str(latest['drawingNumberPayoutData'].split('AmountReceived66>')[1].split('<')[0]))
        LottoItem.add_value("cat_2_prize", str(latest['drawingNumberPayoutData'].split('AmountReceived56>')[1].split('<')[0]))
        LottoItem.add_value("cat_3_prize", str(latest['drawingNumberPayoutData'].split('AmountReceived46>')[1].split('<')[0]))
        LottoItem.add_value("cat_4_prize", str(latest['drawingNumberPayoutData'].split('AmountReceived36>')[1].split('<')[0]))
        LottoItem.add_value("cat_5_prize", str(latest['drawingNumberPayoutData'].split('AmountReceived1018>')[1].split('<')[0]))
        LottoItem.add_value("cat_6_prize", str(latest['drawingNumberPayoutData'].split('AmountReceived918>')[1].split('<')[0]))
        LottoItem.add_value("cat_7_prize", str(latest['drawingNumberPayoutData'].split('AmountReceived818>')[1].split('<')[0]))
        LottoItem.add_value("cat_8_prize", str(latest['drawingNumberPayoutData'].split('AmountReceived718>')[1].split('<')[0]))
        LottoItem.add_value("cat_9_prize", str(latest['drawingNumberPayoutData'].split('AmountReceived618>')[1].split('<')[0]))
        LottoItem.add_value("cat_10_prize", str(latest['drawingNumberPayoutData'].split('AmountReceived518>')[1].split('<')[0]))
        LottoItem.add_value("cat_11_prize", str(latest['drawingNumberPayoutData'].split('AmountReceived418>')[1].split('<')[0]))
        LottoItem.add_value("cat_1_winners", str(latest['drawingNumberPayoutData'].split('numberofWinners66>')[1].split('<')[0]))
        LottoItem.add_value("cat_2_winners", str(latest['drawingNumberPayoutData'].split('numberofWinners56>')[1].split('<')[0]))
        LottoItem.add_value("cat_3_winners", str(latest['drawingNumberPayoutData'].split('numberofWinners46>')[1].split('<')[0]))
        LottoItem.add_value("cat_4_winners", str(latest['drawingNumberPayoutData'].split('numberofWinners36>')[1].split('<')[0]))
        LottoItem.add_value("cat_5_winners", str(latest['drawingNumberPayoutData'].split('numberofWinners1018>')[1].split('<')[0]))
        LottoItem.add_value("cat_6_winners", str(latest['drawingNumberPayoutData'].split('numberofWinners918>')[1].split('<')[0]))
        LottoItem.add_value("cat_7_winners", str(latest['drawingNumberPayoutData'].split('numberofWinners818>')[1].split('<')[0]))
        LottoItem.add_value("cat_8_winners", str(latest['drawingNumberPayoutData'].split('numberofWinners718>')[1].split('<')[0]))
        LottoItem.add_value("cat_9_winners", str(latest['drawingNumberPayoutData'].split('numberofWinners618>')[1].split('<')[0]))
        LottoItem.add_value("cat_10_winners", str(latest['drawingNumberPayoutData'].split('numberofWinners518>')[1].split('<')[0]))
        LottoItem.add_value("cat_11_winners", str(latest['drawingNumberPayoutData'].split('numberofWinners418>')[1].split('<')[0]))
        yield LottoItem.load_item()


class USPennsylvaniaTreasureHunt(scrapy.Spider):

    name = "USPennsylvaniaTreasureHunt"

    def start_requests(self):
        self.name = "USPennsylvaniaTreasureHunt"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        year = datetime.strftime(datetime.now()-timedelta(days=1), "%Y")
        base_url = 'https://www.palottery.state.pa.us/Custom/uploadedfiles/winning-numbers-history/PastWinningNumbers.ashx?g=7&y=xxxxx'
        url = base_url.replace('xxxxx', year)
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=USPennsylvaniaTreasureHuntItem(), selector=response)
        latest = response.json()[0]

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("draw_datetime", str(latest['drawingNumberDate']))
        LottoItem.add_value("draw_number", str(latest['drawingNumberID']))
        LottoItem.add_value("ball0", str(latest['drawingNumber1']))
        LottoItem.add_value("ball1", str(latest['drawingNumber2']))
        LottoItem.add_value("ball2", str(latest['drawingNumber3']))
        LottoItem.add_value("ball3", str(latest['drawingNumber4']))
        LottoItem.add_value("ball4", str(latest['drawingNumber5']))
        if prize_to_num(latest['drawingNumberPayoutData'].split('numberofWinners5>')[1].split('<')[0]) == 0:
            LottoItem.add_value("estimated_next_jackpot", str(latest['drawingNumberPayoutData'].split('AmountReceived5>')[1].split('<')[0]))
            LottoItem.add_value("cat_1_prize", '0')
        else:
            LottoItem.add_value("estimated_next_jackpot", '0')
            LottoItem.add_value("cat_1_prize", str(latest['drawingNumberPayoutData'].split('AmountReceived5>')[1].split('<')[0]))
        LottoItem.add_value("cat_2_prize", str(latest['drawingNumberPayoutData'].split('AmountReceived4>')[1].split('<')[0]))
        LottoItem.add_value("cat_3_prize", str(latest['drawingNumberPayoutData'].split('AmountReceived3>')[1].split('<')[0]))
        LottoItem.add_value("cat_4_prize", str(latest['drawingNumberPayoutData'].split('AmountReceived2>')[1].split('<')[0]))
        LottoItem.add_value("cat_1_winners", str(latest['drawingNumberPayoutData'].split('numberofWinners5>')[1].split('<')[0]))
        LottoItem.add_value("cat_2_winners", str(latest['drawingNumberPayoutData'].split('numberofWinners4>')[1].split('<')[0]))
        LottoItem.add_value("cat_3_winners", str(latest['drawingNumberPayoutData'].split('numberofWinners3>')[1].split('<')[0]))
        LottoItem.add_value("cat_4_winners", str(latest['drawingNumberPayoutData'].split('numberofWinners2>')[1].split('<')[0]))
        yield LottoItem.load_item()


class USPuertoRicoLoto(scrapy.Spider):

    name = "USPuertoRicoLoto"

    def start_requests(self):
        self.name = "USPuertoRicoLoto"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.lotteryusa.com/puerto-rico/lotto/"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=USPuertoRicoLotoItem(), selector=response)
        latest = response.xpath('//tbody/tr')[0]
        balls_lst = latest.xpath('.//ul/li/text()').getall()

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("bonus_ball", latest.xpath('.//ul/li/span/text()').get())
        LottoItem.add_value("multiplier", balls_lst[-1])
        LottoItem.add_value("draw_datetime", latest.xpath('.//time/@datetime').get())
        next_jackpot = response.xpath('//div[@class="c-next-draw-card__body"]//dd/text()').get()
        LottoItem.add_value("estimated_next_jackpot", next_jackpot)
        LottoItem.add_value("jackpot", latest.xpath('.//dd/text()').get().strip())
        yield LottoItem.load_item()


class USPuertoRicoRevancha(scrapy.Spider):

    name = "USPuertoRicoRevancha"

    def start_requests(self):
        self.name = "USPuertoRicoRevancha"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.lotteryusa.com/puerto-rico/revancha/"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=USPuertoRicoRevanchaItem(), selector=response)
        latest = response.xpath('//tbody/tr')[0]
        balls_lst = latest.xpath('.//ul/li/text()').getall()

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("bonus_ball", latest.xpath('.//ul/li/span/text()').get())
        LottoItem.add_value("draw_datetime", latest.xpath('.//time/@datetime').get())
        next_jackpot = response.xpath('//div[@class="c-next-draw-card__body"]//dd/text()').get()
        LottoItem.add_value("estimated_next_jackpot", next_jackpot)
        LottoItem.add_value("jackpot", latest.xpath('.//dd/text()').get().strip())
        yield LottoItem.load_item()


class USRhodeIslandWildMoney(scrapy.Spider):

    name = "USRhodeIslandWildMoney"

    def start_requests(self):
        self.name = "USRhodeIslandWildMoney"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        headers = {
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-User-Agent': 'portal',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://www.rilot.com/en-us/winning-numbers/wild-money.html',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }
        date_to = str(round(datetime.timestamp(datetime.now()) * 1000))
        date_from = str(round(datetime.timestamp(datetime.now()-timedelta(days=30)) * 1000))
        base_url = 'https://www.rilot.com/api/v2/draw-games/draws/page?order=DESC&previous-draws=100&next-draws=0&date-from=xxxxx&date-to=yyyyy&game-names=WILD&status=PAYABLE&status=RESULTS_AVAILABLE&size=30&page=0'
        url = base_url.replace('yyyyy', date_to)
        url = url.replace('xxxxx', date_from)
        yield scrapy.Request(url=url, callback=self.parse, headers=headers, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=USRhodeIslandWildMoneyItem(), selector=response)
        latest = response.json()['draws'][0]

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("draw_datetime", str(latest['drawTime']))
        LottoItem.add_value("draw_number", str(latest['id']))
        LottoItem.add_value("ball0", str(latest['results'][0]['primary'][0]))
        LottoItem.add_value("ball1", str(latest['results'][0]['primary'][1]))
        LottoItem.add_value("ball2", str(latest['results'][0]['primary'][2]))
        LottoItem.add_value("ball3", str(latest['results'][0]['primary'][3]))
        LottoItem.add_value("ball4", str(latest['results'][0]['primary'][4]))
        LottoItem.add_value("bonus_ball", str(latest['results'][0]['secondary'][0]))
        LottoItem.add_value("cat_1_prize", str(latest['prizeTiers'][0]['shareAmount']))
        LottoItem.add_value("cat_2_prize", str(latest['prizeTiers'][1]['shareAmount']))
        LottoItem.add_value("cat_3_prize", str(latest['prizeTiers'][2]['shareAmount']))
        LottoItem.add_value("cat_4_prize", str(latest['prizeTiers'][3]['shareAmount']))
        LottoItem.add_value("cat_5_prize", str(latest['prizeTiers'][4]['shareAmount']))
        LottoItem.add_value("cat_6_prize", str(latest['prizeTiers'][5]['shareAmount']))
        LottoItem.add_value("cat_7_prize", str(latest['prizeTiers'][6]['shareAmount']))
        LottoItem.add_value("cat_1_winners", str(latest['prizeTiers'][0]['shareCount']))
        LottoItem.add_value("cat_2_winners", str(latest['prizeTiers'][1]['shareCount']))
        LottoItem.add_value("cat_3_winners", str(latest['prizeTiers'][2]['shareCount']))
        LottoItem.add_value("cat_4_winners", str(latest['prizeTiers'][3]['shareCount']))
        LottoItem.add_value("cat_5_winners", str(latest['prizeTiers'][4]['shareCount']))
        LottoItem.add_value("cat_6_winners", str(latest['prizeTiers'][5]['shareCount']))
        LottoItem.add_value("cat_7_winners", str(latest['prizeTiers'][6]['shareCount']))
        yield LottoItem.load_item()


class USSouthDakotaCash(scrapy.Spider):

    name = "USSouthDakotaCash"

    # ONLY RETURNS DATA IF THERE IS A DRAW ON DAY OF SCRAPE

    def start_requests(self):
        self.name = "USSouthDakotaCash"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://lottery.sd.gov/winners/lottogames/"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        LottoItem = ItemLoader(item=USSouthDakotaCashItem(), selector=response)
        game_ids = response.xpath('//article[@class="pastdrawgame"]/@id').getall()
        games = response.xpath('//article[@class="pastdrawgame"]')
        for game, game_id in zip(games, game_ids):
            if "dakotacash" in game_id.lower():
                balls_lst = [i.strip() for i in game.xpath('.//span[@class="winningnumbers"]/span/text()').get().split('-')]
                rows = game.xpath('.//tbody/tr')[1:]

                LottoItem.add_value("name", self.name)
                LottoItem.add_value("ball0", balls_lst[0])
                LottoItem.add_value("ball1", balls_lst[1])
                LottoItem.add_value("ball2", balls_lst[2])
                LottoItem.add_value("ball3", balls_lst[3])
                LottoItem.add_value("ball4", balls_lst[4])
                draw_date = game.xpath('.//span[@class="drawingdate"]/span/text()').get().strip()
                LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%m/%d/%Y").strftime("%Y-%m-%d"))
                LottoItem.add_value("cat_1_prize", rows[0].xpath('./td/text()').getall()[1])
                LottoItem.add_value("cat_2_prize", rows[1].xpath('./td/text()').getall()[1])
                LottoItem.add_value("cat_3_prize", rows[2].xpath('./td/text()').getall()[1])
                LottoItem.add_value("cat_4_prize", rows[3].xpath('./td/text()').getall()[1])
                LottoItem.add_value("cat_1_winners", rows[0].xpath('./td/text()').getall()[-1])
                LottoItem.add_value("cat_2_winners", rows[1].xpath('./td/text()').getall()[-1])
                LottoItem.add_value("cat_3_winners", rows[2].xpath('./td/text()').getall()[-1])
                LottoItem.add_value("cat_4_winners", rows[3].xpath('./td/text()').getall()[-1])
                yield LottoItem.load_item()
            else:
            # i.e. If no draw today/day of scrape
                pass


class USTennesseeCash(scrapy.Spider):

    name = "USTennesseeCash"

    def start_requests(self):
        self.name = "USTennesseeCash"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)
        url = "https://www.lotteryusa.com/tennessee/tennessee-cash/"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        jackpot = response.xpath('//div[@class="c-next-draw-card__body"]//dd[@class="c-next-draw-card__prize-value"]//text()').get()
        draw_datetime = response.xpath('//tbody[@class="c-results-table__items"]//time[@class="c-result-card__title"]//text()').get()
        LottoItem = ItemLoader(item=USTennesseeCashItem(), selector=response)

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("estimated_next_jackpot", jackpot)
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_datetime, "%A, %b %d, %Y").strftime("%Y-%m-%d"))
        yield LottoItem.load_item()

class USTennesseeDailyCash(scrapy.Spider):

    name = "USTennesseeDailyCash"

    def start_requests(self):
        self.name = "USTennesseeDailyCash"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)
        
        url = "https://www.lotteryusa.com/tennessee/daily-tennessee-jackpot/"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        jackpot = response.xpath('//div[@class="c-next-draw-card__body"]//dd[@class="c-next-draw-card__prize-value"]//text()').get()
        draw_datetime = response.xpath('//tbody[@class="c-results-table__items"]//time[@class="c-result-card__title"]//text()').get()
        
        LottoItem = ItemLoader(item=USTennesseeDailyCashItem(), selector=response)
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_datetime, "%A, %b %d, %Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("name", self.name)
        LottoItem.add_value("estimated_next_jackpot", jackpot)
        yield LottoItem.load_item()

class USTexasLotto(scrapy.Spider):

    name = "USTexasLotto"

    def start_requests(self):
        self.name = "USTexasLotto"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.txlottery.org/export/sites/lottery/Games/Lotto_Texas/index.html"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=USTexasLottoItem(), selector=response)
        balls_lst = response.xpath(
            '//div[@class="large-12 cell"]/ol[@class="winningNumberBalls"]/li/span/text()').getall()
        rows = response.xpath('//div[@class="large-12 cell"]//tbody/tr')
        draw_date = clean_datetime(response.xpath('//div[@class="large-12 cell"]/h2/text()').get())

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%m/%d/%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("estimated_next_jackpot", response.xpath('//h1[@class="sans"]/text()').get())
        LottoItem.add_value("estimated_next_jackpot_cash", response.xpath('//h2[@class="sans"]/text()').get())
        LottoItem.add_value("cat_1_prize", rows[0].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_4_prize", rows[3].xpath('./td/text()').getall()[1])
        match_6 = rows[0].xpath('./td/text()').getall()[2]
        if "roll" in match_6.lower():
            LottoItem.add_value("cat_1_winners", '0')
        else:
            LottoItem.add_value("cat_1_winners", match_6)
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./td/text()').getall()[2])
        yield LottoItem.load_item()


class USTexasTwoStep(scrapy.Spider):

    name = "USTexasTwoStep"

    def start_requests(self):
        self.name = "USTexasTwoStep"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.txlottery.org/export/sites/lottery/Games/Texas_Two_Step/index.html"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=USTexasTwoStepItem(), selector=response)
        balls_lst = response.xpath(
            '//div[@class="large-12 cell"]/ol[@class="winningNumberBalls"]/li/span/text()').getall()
        rows = response.xpath('//div[@class="large-12 cell"]//tbody/tr')
        draw_date = clean_datetime(response.xpath('//div[@class="large-12 cell"]/h2/text()').get())

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("bonus_ball", balls_lst[4])
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%m/%d/%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("estimated_next_jackpot", response.xpath(
            '//div[@class="large-12 cell"]//h1[@class="sans"]/text()').get())
        LottoItem.add_value("cat_1_prize", rows[0].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_4_prize", rows[3].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_5_prize", rows[4].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_6_prize", rows[5].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_7_prize", rows[6].xpath('./td/text()').getall()[1])
        match_4_bonus = rows[0].xpath('./td/text()').getall()[-1]
        if "roll" in match_4_bonus.lower():
            LottoItem.add_value("cat_1_winners", '0')
        else:
            LottoItem.add_value("cat_1_winners", match_4_bonus)
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_5_winners", rows[4].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_6_winners", rows[5].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_7_winners", rows[6].xpath('./td/text()').getall()[-1])
        yield LottoItem.load_item()


class USTristateMegaBucks(scrapy.Spider):

    name = "USTristateMegaBucks"

    # Played in Maine, New Hampshire & Vermont
    # Scraped from VT website to atleast get VT winners data (other states don't publish)

    def start_requests(self):
        self.name = "USTristateMegaBucks"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://vtlottery.com/games/megabucks"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        LottoItem = ItemLoader(item=USTristateMegaBucksItem(), selector=response)
        balls_lst = response.xpath('//div[@class="ballWrapper"]/div[@class="ball"]/text()').getall()
        bonus_ball = response.xpath('//div[@class="ballWrapper"]/div[@class="ball coloredball"]/text()').get()
        rows = response.xpath('//div[@class="tableWrapper megabucksOdds"]//tbody/tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("bonus_ball", bonus_ball)
        draw_date = response.xpath('//div[@class="winningNumebrsDate"]//span/text()').get().strip()
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%A, %B %d, %Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("estimated_next_jackpot", response.xpath(
            '//div[@class="estimatedJackpot"]/div[@class="field-items"]/text()').get())
        # Jackpot prize will be '0' if not won
        LottoItem.add_value("cat_1_prize", rows[0].xpath('./td/text()').getall()[-2])
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./td/text()').getall()[-2])
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./td/text()').getall()[-2])
        LottoItem.add_value("cat_4_prize", rows[3].xpath('./td/text()').getall()[-2])
        LottoItem.add_value("cat_5_prize", rows[4].xpath('./td/text()').getall()[-2])
        LottoItem.add_value("cat_6_prize", rows[5].xpath('./td/text()').getall()[-2])
        LottoItem.add_value("cat_7_prize", rows[6].xpath('./td/text()').getall()[-2])
        LottoItem.add_value("cat_8_prize", rows[7].xpath('./td/text()').getall()[-2])
        LottoItem.add_value("cat_9_prize", rows[8].xpath('./td/text()').getall()[-2])
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_5_winners", rows[4].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_6_winners", rows[5].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_7_winners", rows[6].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_8_winners", rows[7].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_9_winners", rows[8].xpath('./td/text()').getall()[-1])
        yield LottoItem.load_item()


class USVirginiaCash5(scrapy.Spider):

    name = "USVirginiaCash5"

    def start_requests(self):
        self.name = "USVirginiaCash5"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.lotteryusa.com/virginia/cash-5/"
        yield scrapy.Request(url=url, callback=self.parse_next_estimated, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse_next_estimated(self, response):
        self.next_jackpot = response.xpath('//dd[@class="c-next-draw-card__prize-value"]/text()').get().strip()
        url = 'https://www.valottery.com/api/v1/drawnumbers?page=0&totalPages=0&pageSize=6&gameId=1030'
        yield scrapy.Request(url=url, method='POST', callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=USVirginiaCash5Item(), selector=response)
        latest = response.json()['data'][0]

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", str(latest['DailyDraws'][0]['SelectedNumbers']['Value'][0]))
        LottoItem.add_value("ball1", str(latest['DailyDraws'][0]['SelectedNumbers']['Value'][1]))
        LottoItem.add_value("ball2", str(latest['DailyDraws'][0]['SelectedNumbers']['Value'][2]))
        LottoItem.add_value("ball3", str(latest['DailyDraws'][0]['SelectedNumbers']['Value'][3]))
        LottoItem.add_value("ball4", str(latest['DailyDraws'][0]['SelectedNumbers']['Value'][4]))
        draw_date = str(latest['DrawDateFormatted'])
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%B %d, %Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("estimated_next_jackpot", self.next_jackpot)
        LottoItem.add_value("cat_1_prize", str(latest['DailyDrawDetails'][0]['Prize1']).lower().split('paying')[1])
        LottoItem.add_value("cat_2_prize", str(latest['DailyDrawDetails'][0]['Prize2']).lower().split('paying')[1])
        LottoItem.add_value("cat_3_prize", str(latest['DailyDrawDetails'][0]['Prize3']).lower().split('paying')[1])
        LottoItem.add_value("cat_4_prize", str(latest['DailyDrawDetails'][0]['Prize4']).lower().split('paying')[1])
        LottoItem.add_value("cat_1_winners", str(latest['DailyDrawDetails'][0]['Prize1']).lower().split('plays')[0])
        LottoItem.add_value("cat_2_winners", str(latest['DailyDrawDetails'][0]['Prize2']).lower().split('plays')[0])
        LottoItem.add_value("cat_3_winners", str(latest['DailyDrawDetails'][0]['Prize3']).lower().split('plays')[0])
        LottoItem.add_value("cat_4_winners", str(latest['DailyDrawDetails'][0]['Prize4']).lower().split('plays')[0])
        yield LottoItem.load_item()


class USWashingtonLotto(scrapy.Spider):

    name = "USWashingtonLotto"

    def start_requests(self):
        self.name = "USWashingtonLotto"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.walottery.com/JackpotGames/Lotto.aspx"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        self.next_jackpot = response.xpath('//h1/text()').get()
        url = "https://www.walottery.com/WinningNumbers/PastDrawings.aspx?gamename=lotto"
        yield scrapy.Request(url=url, callback=self.parse_draw,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=USWashingtonLottoItem(), selector=response)
        latest = response.xpath('//table[@class="table-viewport-large"]')
        balls_lst = latest.xpath('.//td[@class="game-balls"]/ul/li/text()').getall()
        rows = latest.xpath('./tbody/tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        draw_date = "".join(latest.xpath('//th/h2/text()').get().split(',')[1:]).strip()
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%b %d %Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("estimated_next_jackpot", self.next_jackpot)
        cat_1_winners = prize_to_num(rows[0].xpath('./td/text()').getall()[-2])
        cat_1_prize = prize_to_num(rows[0].xpath('./td/text()').getall()[-3])
        if cat_1_winners > 0:
            LottoItem.add_value("cat_1_prize", str(cat_1_prize/cat_1_winners))
        else:
            LottoItem.add_value("cat_1_prize", str(cat_1_prize))
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./td/text()').getall()[-3])
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./td/text()').getall()[-3])
        LottoItem.add_value("cat_4_prize", rows[3].xpath('./td/text()').getall()[-3])
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td/text()').getall()[-2])
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./td/text()').getall()[-2])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./td/text()').getall()[-2])
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./td/text()').getall()[-2])
        yield LottoItem.load_item()


class USWashingtonHit5(scrapy.Spider):

    name = "USWashingtonHit5"

    def start_requests(self):
        self.name = "USWashingtonHit5"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.walottery.com/JackpotGames/Hit5.aspx"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        self.next_jackpot = response.xpath('//h1/text()').get()
        url = "https://www.walottery.com/WinningNumbers/PastDrawings.aspx?gamename=hit5"
        yield scrapy.Request(url=url, callback=self.parse_draw,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=USWashingtonHit5Item(), selector=response)
        latest = response.xpath('//table[@class="table-viewport-large"]')
        balls_lst = latest.xpath('.//td[@class="game-balls"]/ul/li/text()').getall()
        rows = latest.xpath('./tbody/tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        draw_date = "".join(latest.xpath('//th/h2/text()').get().split(',')[1:]).strip()
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%b %d %Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("estimated_next_jackpot", self.next_jackpot)
        cat_1_winners = prize_to_num(rows[0].xpath('./td/text()').getall()[-2])
        cat_1_prize = prize_to_num(rows[0].xpath('./td/text()').getall()[-3])
        if cat_1_winners > 0:
            LottoItem.add_value("cat_1_prize", str(cat_1_prize/cat_1_winners))
        else:
            LottoItem.add_value("cat_1_prize", str(cat_1_prize))
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./td/text()').getall()[-3])
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./td/text()').getall()[-3])
        LottoItem.add_value("cat_4_prize", '1') # prize is a free ticket
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td/text()').getall()[-2])
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./td/text()').getall()[-2])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./td/text()').getall()[-2])
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./td/text()').getall()[-2])
        yield LottoItem.load_item()


class USWisconsinMegaBucks(scrapy.Spider):

    name = "USWisconsinMegaBucks"

    def start_requests(self):
        self.name = "USWisconsinMegaBucks"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://wilottery.com/games/megabucks"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    },
            })

    def parse(self, response):
        LottoItem = ItemLoader(item=USWisconsinMegaBucksItem(), selector=response)
        balls_lst = response.xpath('//div[@class="latest-drawing"]//ul/li/div/span/text()').getall()
        rows = response.xpath('//div[@id="tab-content-0"]//tbody/tr')
        megabucks_winner_date = response.xpath('//div[@class="interior lowTopBottom number-of-winners-top"]//p[@class="note"]//text()').get()
        megabucks_winner_date = re.findall(r"(?:0[1-9]|1[012])[-/.](?:0[1-9]|[12][0-9]|3[01])[-/.](?:19\d{2}|20[01][0-9]|202[1-9])", megabucks_winner_date)
        megabucks_winner_date = datetime.strptime(megabucks_winner_date[0], "%m/%d/%Y").strftime("%Y-%m-%d")
        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        draw_date = ",".join(response.xpath('//div[@class="latest-drawing"]//div[@class="draw-date"]/text()').get().split(',')[1:]).strip()
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%B %d, %Y").strftime("%Y-%m-%d"))
        checking_time = datetime.strptime(draw_date, "%B %d, %Y").strftime("%Y-%m-%d")
        LottoItem.add_value("estimated_next_jackpot", "".join(response.xpath(
            '//div[@class="current-jackpot"]//div[@class="jackpot-amount"]')[0].xpath('.//text()').getall()[:-1]))
        LottoItem.add_value("estimated_next_jackpot_cash", "".join(response.xpath(
            '//div[@class="current-jackpot"]//div[@class="jackpot-amount"]')[1].xpath('.//text()').getall()[:-1]))
        LottoItem.add_value("cat_1_prize", rows[0].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_4_prize", rows[3].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./td/text()').getall()[1])
        if megabucks_winner_date == checking_time:
            yield LottoItem.load_item()
        else:
            print("Something oddd")
            pass


class USWisconsinBadger5(scrapy.Spider):

    name = "USWisconsinBadger5"

    def start_requests(self):
        self.name = "USWisconsinBadger5"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://wilottery.com/games/badger-5"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                },
            })

    def parse(self, response):
        LottoItem = ItemLoader(item=USWisconsinBadger5Item(), selector=response)
        balls_lst = response.xpath('//div[@class="latest-drawing"]//ul/li/div/span/text()').getall()
        rows = response.xpath('//div[@id="tab-content-0"]//tbody/tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        draw_date = ",".join(response.xpath('//div[@class="latest-drawing"]//div[@class="draw-date"]/text()').get().split(',')[1:]).strip()
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%B %d, %Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("estimated_next_jackpot", response.xpath(
            '//div[@class="current-jackpot"]//div[@class="jackpot-amount"]//text()').get())
        LottoItem.add_value("cat_1_prize", rows[0].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_4_prize", rows[3].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./td/text()').getall()[1])
        yield LottoItem.load_item()


class USWyomingCowboyDraw(scrapy.Spider):

    name = "USWyomingCowboyDraw"

    def start_requests(self):
        self.name = "USWyomingCowboyDraw"
        self.req_proxy = get_UK_proxy()['http']
        url = "https://www.lotteryusa.com/wyoming/"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=USWyomingCowboyDrawItem(), selector=response)
        x = response.xpath('//td[@class="c-result-card__next-draw "]//dd[@class="c-result-card__prize-value"]//text()').get()

        LottoItem.add_value("name", self.name)
        #LottoItem.add_value("estimated_next_jackpot", self.next_jackpot)
        LottoItem.add_value("cat_1_prize", x)
        yield LottoItem.load_item()


"""
REST OF THE WORLD LOTTOS
"""

class AntiguaSuperLotto(scrapy.Spider):

    name = "AntiguaSuperLotto"

    # Played in Barbados, Anguilla, Jamaica, Antigua and Barbuda, St. Kitts and Nevis, St. Maarten, US Virgin Islands

    def start_requests(self):
        self.name = "AntiguaSuperLotto"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.thecaribbeanlottery.com/games/super-lotto"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=AntiguaSuperLottoItem(), selector=response)
        balls_lst = response.xpath('//div[@class="ball-results"]/ul/li/text()').getall()
        bonus_ball = response.xpath('//div[@class="ball-results alt"]/ul/li/text()').get()

        # Note: Jackpot is in USD
        LottoItem.add_value("name", self.name)
        draw_date = ",".join(response.xpath('//div[@class="panel-result"]//time/text()').get().split(',')[1:]).strip()
        LottoItem.add_value("draw_datetime", datetime.strptime(clean_date_string(draw_date), "%B %d, %Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("bonus_ball", bonus_ball)
        LottoItem.add_value("estimated_next_jackpot", response.xpath('//h2/span[@id="gameJackpot"]/text()').get())
        LottoItem.add_value("jackpot", '0') # value will be previous estimated_next, need column
        yield LottoItem.load_item()


# class ArgentinaLoto(scrapy.Spider):

#     name = "ArgentinaLoto"
#     custom_settings = {
#         "PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT" : 90*1000 # over-ride usual 60s
#     }

#     def start_requests(self):
#         self.name = "ArgentinaLoto"
#         self.req_proxy = get_UK_proxy()['http']
#         print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)
# 
#         url = "https://loto.loteriadelaciudad.gob.ar"
#         yield scrapy.Request(url=url, callback=self.parse,
#             meta={'playwright': True, "playwright_context": "new",
#                 "playwright_context_kwargs": {
#                     "java_script_enabled": True,
#                     "ignore_https_errors": True,
#                     "proxy": {
#                         "server": self.req_proxy,
#                         "username": "keizzermop",
#                         "password": "WSPassword123",
#                     },
#                 },
#             })

#     def parse(self, response):
#         LottoItem = ItemLoader(item=ArgentinaLotoItem(), selector=response)
#         game = response.xpath('//div[@class="grilla"]')[0]
#         date_info = response.xpath('//span/span[@class="ui-selectmenu-text"]/text()').get()
#         balls_lst = game.xpath('.//div[@class="item-loto"]/p/text()').getall()
#         winner_values = game.xpath('.//div[@class="infoJuego alto"]/div[@class="item-info"]')[1]
#         prize_values = game.xpath('.//div[@class="infoJuego alto"]/div[@class="item-info"]')[2]

#         LottoItem.add_value("name", self.name)
#         LottoItem.add_value("ball0", balls_lst[0])
#         LottoItem.add_value("ball1", balls_lst[1])
#         LottoItem.add_value("ball2", balls_lst[2])
#         LottoItem.add_value("ball3", balls_lst[3])
#         LottoItem.add_value("ball4", balls_lst[4])
#         LottoItem.add_value("ball5", balls_lst[5])
#         LottoItem.add_value("bonus_ball", response.xpath(
#             '//div[@class="multiplicador"]/span[@class="circle"]/text()').get())

#         draw_date = date_info.split('-')[0].split(':')[1].strip()
#         LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d/%m/%Y").strftime("%Y-%m-%d"))
#         LottoItem.add_value("draw_number", date_info.split('-')[1].split(':')[1])
#         next_jackpot = response.xpath('//div[@class="noticias"]/fieldset/b/text()').get()
#         LottoItem.add_value("estimated_next_jackpot", next_jackpot)
#         LottoItem.add_value("cat_1_prize", prize_values.xpath('./p/text()').getall()[1])
#         LottoItem.add_value("cat_2_prize", prize_values.xpath('./p/text()').getall()[2])
#         LottoItem.add_value("cat_3_prize", prize_values.xpath('./p/text()').getall()[3])
#         LottoItem.add_value("cat_1_winners", winner_values.xpath('./p/text()').getall()[1])
#         LottoItem.add_value("cat_2_winners", winner_values.xpath('./p/text()').getall()[2])
#         LottoItem.add_value("cat_3_winners", winner_values.xpath('./p/text()').getall()[3])
#         yield LottoItem.load_item()


# class ArgentinaLotoPlus(scrapy.Spider):

#     name = "ArgentinaLotoPlus"
#     custom_settings = {
#         "PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT" : 90*1000 # over-ride usual 60s
#     }

#     def start_requests(self):
#         self.name = "ArgentinaLotoPlus"
#         self.req_proxy = get_UK_proxy()['http']
#         print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)
# 
#         url = "https://loto.loteriadelaciudad.gob.ar"
#         yield scrapy.Request(url=url, callback=self.parse,
#             meta={'playwright': True, "playwright_context": "new",
#                 "playwright_context_kwargs": {
#                     "java_script_enabled": True,
#                     "ignore_https_errors": True,
#                     "proxy": {
#                         "server": self.req_proxy,
#                         "username": "keizzermop",
#                         "password": "WSPassword123",
#                     },
#                 },
#             })

#     def parse(self, response):
#         LottoItem = ItemLoader(item=ArgentinaLotoPlusItem(), selector=response)
#         game = response.xpath('//div[@class="grilla"]')[1]
#         date_info = response.xpath('//span/span[@class="ui-selectmenu-text"]/text()').get()
#         balls_lst = game.xpath('.//div[@class="item-loto"]/p/text()').getall()
#         winner_values = game.xpath('.//div[@class="infoJuego alto"]/div[@class="item-info"]')[1]
#         prize_values = game.xpath('.//div[@class="infoJuego alto"]/div[@class="item-info"]')[2]

#         LottoItem.add_value("name", self.name)
#         LottoItem.add_value("ball0", balls_lst[0])
#         LottoItem.add_value("ball1", balls_lst[1])
#         LottoItem.add_value("ball2", balls_lst[2])
#         LottoItem.add_value("ball3", balls_lst[3])
#         LottoItem.add_value("ball4", balls_lst[4])
#         LottoItem.add_value("ball5", balls_lst[5])
#         LottoItem.add_value("bonus_ball", response.xpath(
#             '//div[@class="multiplicador"]/span[@class="circle"]/text()').get())

#         draw_date = date_info.split('-')[0].split(':')[1].strip()
#         LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d/%m/%Y").strftime("%Y-%m-%d"))
#         LottoItem.add_value("draw_number", date_info.split('-')[1].split(':')[1])
#         next_jackpot = response.xpath('//div[@class="noticias"]/fieldset/b/text()').get()
#         LottoItem.add_value("estimated_next_jackpot", next_jackpot)
#         LottoItem.add_value("cat_1_prize", prize_values.xpath('./p/text()').getall()[1])
#         LottoItem.add_value("cat_2_prize", prize_values.xpath('./p/text()').getall()[2])
#         LottoItem.add_value("cat_3_prize", prize_values.xpath('./p/text()').getall()[3])
#         LottoItem.add_value("cat_1_winners", winner_values.xpath('./p/text()').getall()[1])
#         LottoItem.add_value("cat_2_winners", winner_values.xpath('./p/text()').getall()[2])
#         LottoItem.add_value("cat_3_winners", winner_values.xpath('./p/text()').getall()[3])
#         yield LottoItem.load_item()


class ArgentinaLoto5(scrapy.Spider):

    name = "ArgentinaLoto5"
    custom_settings = {
        "PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT" : 120*1000 # over-ride usual 60s
    }

    def start_requests(self):
        self.name = "ArgentinaLoto5"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://loto5.loteriadelaciudad.gob.ar"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        LottoItem = ItemLoader(item=ArgentinaLoto5Item(), selector=response)
        balls_lst = response.xpath('//div[@class="grilla"]//div[@class="item-loto"]/p/text()').getall()
        rows = response.xpath('//div[@class="grilla"]//div[@class="infoJuego"]//tr')[1:]

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])

        date_info = response.xpath('//span/span[@class="ui-selectmenu-text"]/text()').get()
        draw_date = date_info.split('-')[0].split(':')[1].strip()
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d/%m/%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", date_info.split('-')[1].split(':')[1])
        next_jackpot = response.xpath('//div[@class="noticias"]/fieldset/b/text()').get()
        LottoItem.add_value("estimated_next_jackpot", next_jackpot)
        LottoItem.add_value("cat_1_prize", rows[0].xpath('./td/text()').getall()[-3])
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./td/text()').getall()[-3])
        LottoItem.add_value("cat_3_prize", '35') # prize is value of ticket
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./td/text()').getall()[-1])
        yield LottoItem.load_item()


class ArgentinaLotoTradicional(scrapy.Spider):

    name = "ArgentinaLotoTradicional"
    def start_requests(self):
        self.name = "ArgentinaLotoTradicional"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://loto.loteriadelaciudad.gob.ar/"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        LottoItem = ItemLoader(item=ArgentinaLotoTradicionalItem(), selector=response)
        rows = response.xpath('//div[@class="multiplica"]//div[@class="content-loto"]')
        balls_lst = rows[0].xpath('.//div[@class="resultado"]//p//text()').getall()
        row_winner = rows[0].xpath('.//div[@class="infoJuego alto"]//p//text()').getall()
        row_winner = [f.replace('Vacante', '0').replace('.-', '') for f in row_winner]
        date_info = response.xpath('//div[@id="form"]//div[@id="combo"]//option//text()').get()
        draw_date = re.search('(\d+/\d+/\d+)', date_info)
        draw_number = re.sub('.*?: ', '', date_info)

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("cat_1_prize", row_winner[9])
        LottoItem.add_value("cat_2_prize", row_winner[10])
        LottoItem.add_value("cat_3_prize", row_winner[11])
        LottoItem.add_value("cat_1_winners", row_winner[5])
        LottoItem.add_value("cat_2_winners", row_winner[6])
        LottoItem.add_value("cat_3_winners", row_winner[7])
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date.group(0), "%d/%m/%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", draw_number)
        yield LottoItem.load_item()

class ArgentinaLotoMatch(scrapy.Spider):

    name = "ArgentinaLotoMatch"
    def start_requests(self):
        self.name = "ArgentinaLotoMatch"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://loto.loteriadelaciudad.gob.ar/"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        LottoItem = ItemLoader(item=ArgentinaLotoMatchItem(), selector=response)
        rows = response.xpath('//div[@class="multiplica"]//div[@class="content-loto"]')
        balls_lst = rows[1].xpath('.//div[@class="resultado"]//p//text()').getall()
        row_winner = rows[1].xpath('.//div[@class="infoJuego alto"]//p//text()').getall()
        row_winner = [f.replace('Vacante', '0').replace('.-', '') for f in row_winner]
        date_info = response.xpath('//div[@id="form"]//div[@id="combo"]//option//text()').get()
        draw_date = re.search('(\d+/\d+/\d+)', date_info)
        draw_number = re.sub('.*?: ', '', date_info)

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("cat_1_prize", row_winner[9])
        LottoItem.add_value("cat_2_prize", row_winner[10])
        LottoItem.add_value("cat_3_prize", row_winner[11])
        LottoItem.add_value("cat_1_winners", row_winner[5])
        LottoItem.add_value("cat_2_winners", row_winner[6])
        LottoItem.add_value("cat_3_winners", row_winner[7])
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date.group(0), "%d/%m/%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", draw_number)
        yield LottoItem.load_item()

class ArgentinaLotoDesquite(scrapy.Spider):

    name = "ArgentinaLotoDesquite"
    def start_requests(self):
        self.name = "ArgentinaLotoDesquite"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://loto.loteriadelaciudad.gob.ar/"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        LottoItem = ItemLoader(item=ArgentinaLotoDesquiteItem(), selector=response)
        rows = response.xpath('//div[@class="multiplica"]//div[@class="content-loto"]')
        balls_lst = rows[2].xpath('.//div[@class="resultado"]//p//text()').getall()
        row_winner = rows[2].xpath('.//div[@class="infoJuego"]//p//text()').getall()
        row_winner = [f.replace('Vacante', '0').replace('.-', '') for f in row_winner]
        date_info = response.xpath('//div[@id="form"]//div[@id="combo"]//option//text()').get()
        draw_date = re.search('(\d+/\d+/\d+)', date_info)
        draw_number = re.sub('.*?: ', '', date_info)

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("cat_1_prize", row_winner[5])
        LottoItem.add_value("cat_1_winners", row_winner[3])
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date.group(0), "%d/%m/%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", draw_number)
        yield LottoItem.load_item()

class ArgentinaLotoSale(scrapy.Spider):

    name = "ArgentinaLotoSale"
    def start_requests(self):
        self.name = "ArgentinaLotoSale"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://loto.loteriadelaciudad.gob.ar/"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        LottoItem = ItemLoader(item=ArgentinaLotoSaleItem(), selector=response)
        rows = response.xpath('//div[@class="multiplica"]//div[@class="content-loto"]')
        balls_lst = rows[3].xpath('.//div[@class="resultado"]//p//text()').getall()
        row_winner = rows[3].xpath('.//div[@class="infoJuego"]//p//text()').getall()
        row_winner = [f.replace('Vacante', '0').replace('.-', '') for f in row_winner]
        date_info = response.xpath('//div[@id="form"]//div[@id="combo"]//option//text()').get()
        draw_date = re.search('(\d+/\d+/\d+)', date_info)
        draw_number = re.sub('.*?: ', '', date_info)

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("cat_1_prize", row_winner[5])
        LottoItem.add_value("cat_1_winners", row_winner[3])
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date.group(0), "%d/%m/%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", draw_number)
        yield LottoItem.load_item()

class ArgentinaQuini6(scrapy.Spider):

    name = "ArgentinaQuini6"

    def start_requests(self):
        self.name = "ArgentinaQuini6"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = 'https://apps.loteriasantafe.gov.ar:8443/Extractos/paginas/mostrarQuini6.xhtml'
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=ArgentinaQuini6Item(), selector=response)
        latest = response.xpath('//div[@class="contenedorquini1"]')[0]
        balls_lst = latest.xpath('.//b/text()').getall()
        rows = latest.xpath('.//tbody/tr')

        date = response.xpath('//div[@class="menu1"]//ul/li/text()').get().strip()
        date2 = response.xpath('//div[@class="menu2"]//ul/li/text()').get().strip()
        draw_num = date2.split('-')[1].strip()
        draw_date = f"{date} {date2.split('-')[0].strip()}"

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        locale.setlocale(locale.LC_TIME, "es_AR.ISO8859-1")
        clean = datetime.strptime(draw_date, "%B %Y %A %d")
        locale.setlocale(locale.LC_TIME, "en_GB.ISO8859-1")
        LottoItem.add_value("draw_datetime", clean.strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", draw_num)

        jackpot_winners = rows[0].xpath('./td/text()').getall()[2]
        if prize_to_num(jackpot_winners) > 0:
            LottoItem.add_value("cat_1_prize", rows[0].xpath('./td/text()').getall()[-1])
        else:
            LottoItem.add_value("cat_1_prize", rows[0].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_1_winners", jackpot_winners)
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./td/text()').getall()[2])
        yield LottoItem.load_item()


class AustraliaTattsLotto(scrapy.Spider):

    name = "AustraliaTattsLotto"

    def start_requests(self):
        self.name = "AustraliaTattsLotto"
        self.req_proxy = get_AUS_data_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        headers = {
            'authority': 'data.api.thelott.com',
            'accept': '*/*',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'dnt': '1',
            'origin': 'https://www.thelott.com',
            'referer': 'https://www.thelott.com/',
            'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        }
        url = 'https://data.api.thelott.com/sales/vmax/web/data/lotto/latestresults'
        frmdata = {"CompanyId":"NTLotteries","MaxDrawCountPerProduct":10,"OptionalProductFilter":["TattsLotto"]}
        yield scrapy.Request(url=url, headers=headers, method='POST', body=json.dumps(frmdata), callback=self.parse,
            meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=AustraliaTattsLottoItem(), selector=response)
        latest = response.json()['DrawResults'][0]

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", str(latest['PrimaryNumbers'][0]))
        LottoItem.add_value("ball1", str(latest['PrimaryNumbers'][1]))
        LottoItem.add_value("ball2", str(latest['PrimaryNumbers'][2]))
        LottoItem.add_value("ball3", str(latest['PrimaryNumbers'][3]))
        LottoItem.add_value("ball4", str(latest['PrimaryNumbers'][4]))
        LottoItem.add_value("ball5", str(latest['PrimaryNumbers'][5]))
        LottoItem.add_value("bonus_ball0", str(latest['SecondaryNumbers'][0]))
        LottoItem.add_value("bonus_ball1", str(latest['SecondaryNumbers'][1]))
        draw_date = str(latest['DrawDate'])
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", str(latest['DrawNumber']))
        LottoItem.add_value("cat_1_prize", str(latest['Dividends'][0]['BlocDividend']))
        LottoItem.add_value("cat_2_prize", str(latest['Dividends'][1]['BlocDividend']))
        LottoItem.add_value("cat_3_prize", str(latest['Dividends'][2]['BlocDividend']))
        LottoItem.add_value("cat_4_prize", str(latest['Dividends'][3]['BlocDividend']))
        LottoItem.add_value("cat_5_prize", str(latest['Dividends'][4]['BlocDividend']))
        LottoItem.add_value("cat_6_prize", str(latest['Dividends'][5]['BlocDividend']))
        LottoItem.add_value("cat_1_winners", str(latest['Dividends'][0]['BlocNumberOfWinners']))
        LottoItem.add_value("cat_2_winners", str(latest['Dividends'][1]['BlocNumberOfWinners']))
        LottoItem.add_value("cat_3_winners", str(latest['Dividends'][2]['BlocNumberOfWinners']))
        LottoItem.add_value("cat_4_winners", str(latest['Dividends'][3]['BlocNumberOfWinners']))
        LottoItem.add_value("cat_5_winners", str(latest['Dividends'][4]['BlocNumberOfWinners']))
        LottoItem.add_value("cat_6_winners", str(latest['Dividends'][5]['BlocNumberOfWinners']))
        yield LottoItem.load_item()


class AustraliaOzLotto(scrapy.Spider):

    name = "AustraliaOzLotto"

    # scraped via lotto.net since Aus API doesn't give cat_1_prize values unless won

    def start_requests(self):
        self.name = "AustraliaOzLotto"
        self.req_proxy = get_AUS_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = 'https://www.lotto.net/oz-lotto/results'
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        self.next_jackpot = response.xpath('//div[@class="jackpot"]//span/text()').getall()[1].strip()
        self.draw_date = response.xpath('//div[@class="date"]/span/text()').get().strip()
        next_page = response.xpath("//div[@class='row-3']/a/@href").get()
        url = urljoin(response.url, next_page)
        yield scrapy.Request(url, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":10})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=AustraliaOzLottoItem(), selector=response)
        balls_lst = response.xpath('//ul[@class="balls"]/li/span/text()').getall()
        rows = response.xpath('//table//tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("ball6", balls_lst[6])
        LottoItem.add_value("bonus_ball0", balls_lst[7])
        LottoItem.add_value("bonus_ball1", balls_lst[8])
        LottoItem.add_value("draw_datetime", datetime.strptime(self.draw_date, "%d %B %Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("estimated_next_jackpot", self.next_jackpot)
        LottoItem.add_value("cat_1_prize", rows[1].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_2_prize", rows[2].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_3_prize", rows[3].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_4_prize", rows[4].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_5_prize", rows[5].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_6_prize", rows[6].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_7_prize", rows[7].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_1_winners", rows[1].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_2_winners", rows[2].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_3_winners", rows[3].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_4_winners", rows[4].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_5_winners", rows[5].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_6_winners", rows[6].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_7_winners", rows[7].xpath('./td/text()').getall()[-1].strip())
        yield LottoItem.load_item()


class AustraliaPowerball(scrapy.Spider):

    name = "AustraliaPowerball"

    # scraped via lotto.net since Aus API doesn't give cat_1_prize values unless won

    def start_requests(self):
        self.name = "AustraliaPowerball"
        self.req_proxy = get_AUS_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = 'https://www.lotto.net/australia-powerball/results'
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        self.next_jackpot = response.xpath('//div[@class="jackpot"]//span/text()').getall()[1].strip()
        self.draw_date = response.xpath('//div[@class="date"]/span/text()').get().strip()
        next_page = response.xpath("//div[@class='row-3']/a/@href").get()
        url = urljoin(response.url, next_page)
        yield scrapy.Request(url, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":10})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=AustraliaPowerballItem(), selector=response)
        balls_lst = response.xpath('//ul[@class="balls"]/li/span/text()').getall()
        rows = response.xpath('//table//tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("ball6", balls_lst[6])
        LottoItem.add_value("bonus_ball", balls_lst[7])
        LottoItem.add_value("draw_datetime", datetime.strptime(self.draw_date, "%d %B %Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("estimated_next_jackpot", self.next_jackpot)
        LottoItem.add_value("cat_1_prize", rows[1].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_2_prize", rows[2].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_3_prize", rows[3].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_4_prize", rows[4].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_5_prize", rows[5].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_6_prize", rows[6].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_7_prize", rows[7].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_8_prize", rows[8].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_9_prize", rows[9].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_1_winners", rows[1].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_2_winners", rows[2].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_3_winners", rows[3].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_4_winners", rows[4].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_5_winners", rows[5].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_6_winners", rows[6].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_7_winners", rows[7].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_8_winners", rows[8].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_9_winners", rows[9].xpath('./td/text()').getall()[-1].strip())
        yield LottoItem.load_item()


class AustraliaSuper66(scrapy.Spider):

    name = "AustraliaSuper66"

    # 'Joker' style game, prog. jackpot, so match_6 is effectively matching a 6 digit number
    # match_5 is either matching the first or last 5 digits, etc.

    def start_requests(self):
        self.name = "AustraliaSuper66"
        self.req_proxy = get_AUS_data_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        headers = {
            'authority': 'data.api.thelott.com',
            'accept': '*/*',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'dnt': '1',
            'origin': 'https://www.thelott.com',
            'referer': 'https://www.thelott.com/',
            'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        }
        url = 'https://data.api.thelott.com/sales/vmax/web/data/lotto/latestresults'
        frmdata = {"CompanyId":"NTLotteries","MaxDrawCountPerProduct":10,"OptionalProductFilter":["Super66"]}
        yield scrapy.Request(url=url, headers=headers, method='POST', body=json.dumps(frmdata), callback=self.parse,
            meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=AustraliaSuper66Item(), selector=response)
        latest = response.json()['DrawResults'][0]

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", str(latest['PrimaryNumbers'][0]))
        LottoItem.add_value("ball1", str(latest['PrimaryNumbers'][1]))
        LottoItem.add_value("ball2", str(latest['PrimaryNumbers'][2]))
        LottoItem.add_value("ball3", str(latest['PrimaryNumbers'][3]))
        LottoItem.add_value("ball4", str(latest['PrimaryNumbers'][4]))
        LottoItem.add_value("ball5", str(latest['PrimaryNumbers'][5]))
        draw_date = str(latest['DrawDate'])
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", str(latest['DrawNumber']))
        LottoItem.add_value("cat_1_prize", str(latest['Dividends'][0]['BlocDividend']))
        LottoItem.add_value("cat_2_prize", str(latest['Dividends'][1]['BlocDividend']))
        LottoItem.add_value("cat_3_prize", str(latest['Dividends'][2]['BlocDividend']))
        LottoItem.add_value("cat_4_prize", str(latest['Dividends'][3]['BlocDividend']))
        LottoItem.add_value("cat_5_prize", str(latest['Dividends'][4]['BlocDividend']))
        LottoItem.add_value("cat_1_winners", str(latest['Dividends'][0]['BlocNumberOfWinners']))
        LottoItem.add_value("cat_2_winners", str(latest['Dividends'][1]['BlocNumberOfWinners']))
        LottoItem.add_value("cat_3_winners", str(latest['Dividends'][2]['BlocNumberOfWinners']))
        LottoItem.add_value("cat_4_winners", str(latest['Dividends'][3]['BlocNumberOfWinners']))
        LottoItem.add_value("cat_5_winners", str(latest['Dividends'][4]['BlocNumberOfWinners']))
        yield LottoItem.load_item()


class AustraliaSuperJackpot(scrapy.Spider):

    name = "AustraliaSuperJackpot"

    # Raffle style game; only need to track jackpot value

    def start_requests(self):
        self.name = "AustraliaSuperJackpot"
        self.req_proxy = get_AUS_data_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        headers = {
            'authority': 'data.api.thelott.com',
            'accept': '*/*',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'dnt': '1',
            'origin': 'https://www.thelott.com',
            'referer': 'https://www.thelott.com/',
            'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        }
        url = 'https://data.api.thelott.com/sales/vmax/web/data/lotto/latestresults'
        frmdata = {"CompanyId":"NTLotteries","MaxDrawCountPerProduct":10,"OptionalProductFilter":["LuckyLotteries2"]}
        yield scrapy.Request(url=url, headers=headers, method='POST', body=json.dumps(frmdata), callback=self.parse,
            meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=AustraliaSuperJackpotItem(), selector=response)
        latest = response.json()['DrawResults'][0]

        LottoItem.add_value("name", self.name)
        draw_date = str(latest['DrawDate'])
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", str(latest['DrawNumber']))
        LottoItem.add_value("cat_1_prize", str(latest['Dividends'][10]['BlocDividend']))
        LottoItem.add_value("cat_1_winners", str(latest['Dividends'][10]['BlocNumberOfWinners']))
        yield LottoItem.load_item()


class AustraliaMegaJackpot(scrapy.Spider):

    name = "AustraliaMegaJackpot"

    # Raffle style game; only need to track jackpot value

    def start_requests(self):
        self.name = "AustraliaMegaJackpot"
        self.req_proxy = get_AUS_data_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        headers = {
            'authority': 'data.api.thelott.com',
            'accept': '*/*',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            # Already added when you pass json=
            # 'content-type': 'application/json',
            'origin': 'https://www.thelott.com',
            'referer': 'https://www.thelott.com/',
            'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        }
        url = 'https://data.api.thelott.com/sales/vmax/web/data/lotto/latestresults'
        frmdata = {"CompanyId":"NTLotteries","MaxDrawCountPerProduct":10,"OptionalProductFilter":["LuckyLotteries5"]}
        yield scrapy.Request(url=url, headers=headers, method='POST', body=json.dumps(frmdata), callback=self.parse,
            meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=AustraliaMegaJackpotItem(), selector=response)
        latest = response.json()['DrawResults'][0]

        LottoItem.add_value("name", self.name)
        draw_date = str(latest['DrawDate'])
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", str(latest['DrawNumber']))
        LottoItem.add_value("cat_1_prize", str(latest['Dividends'][10]['BlocDividend']))
        LottoItem.add_value("cat_1_winners", str(latest['Dividends'][10]['BlocNumberOfWinners']))
        yield LottoItem.load_item()


class AustriaLotto(scrapy.Spider):

    name = "AustriaLotto"

    def start_requests(self):
        self.name = "AustriaLotto"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)
        url = "https://lotteryguru.com/austria-lottery-results"

        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=AustriaLottoItem(), selector=response)
        rows = response.xpath('//div[@class="lg-card lg-link"]')
        draw_date = rows[1].xpath('.//div[@class="lg-card-row"]//div[@class="lg-time"]//span[@class="lg-date"]//text()').get()
        jackpot = rows[1].xpath('.//div[@class="lg-card-row lg-jackpot-info"]//div[@class="lg-sum"]//text()').get()
        LottoItem.add_value("name", self.name)
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d %b %Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("cat_1_prize", jackpot)
        yield LottoItem.load_item()


class AustriaJoker(scrapy.Spider):

    name = "AustriaJoker"

    def start_requests(self):
        self.name = "AustriaJoker"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.win2day.at/lotterie/joker/joker-ziehungen?apID=LOAT&seglo=true&oID=2"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        LottoItem = ItemLoader(item=AustriaJokerItem(), selector=response)
        latest = response.xpath('//div[@class="accordion-body"]')[0]
        balls_lst = latest.xpath(
            './/div[@class="win-numbers"]//span[@class="ball joker"]/strong/text()').getall()
        rows = latest.xpath('.//table[@class="drawresult-table"]/tbody/tr')
        datetime_info = response.xpath('//div[@class="accordion"]//h3//span/text()').getall()
        draw_date = [i for i in datetime_info if any(string in i for string in ['.20'])]
        draw_date = draw_date[0].split(',')[1].strip()

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d.%m.%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("cat_1_prize", rows[1].xpath('./td[@class="drawresult-td-right strong"]/text()').get())
        LottoItem.add_value("cat_2_prize", rows[2].xpath('./td[@class="drawresult-td-right strong"]/text()').get())
        LottoItem.add_value("cat_3_prize", rows[3].xpath('./td[@class="drawresult-td-right strong"]/text()').get())
        LottoItem.add_value("cat_4_prize", rows[4].xpath('./td[@class="drawresult-td-right strong"]/text()').get())
        LottoItem.add_value("cat_5_prize", rows[5].xpath('./td[@class="drawresult-td-right strong"]/text()').get())
        LottoItem.add_value("cat_6_prize", rows[6].xpath('./td[@class="drawresult-td-right strong"]/text()').get())
        match_6_lst = rows[1].xpath('./td[@class="drawresult-td-left strong"]//text()').getall()
        if "jackpot" in "".join(match_6_lst).lower():
            LottoItem.add_value("cat_1_winners", '0')
        else:
            LottoItem.add_value("cat_1_winners", match_6_lst[-1])
        match_5_lst = rows[2].xpath('./td[@class="drawresult-td-left strong"]//text()').getall()
        if "jackpot" in "".join(match_5_lst).lower():
            LottoItem.add_value("cat_2_winners", '0')
        else:
            LottoItem.add_value("cat_2_winners", match_5_lst[-1])
        LottoItem.add_value("cat_3_winners", rows[3].xpath('./td[@class="drawresult-td-left strong"]/text()').get())
        LottoItem.add_value("cat_4_winners", rows[4].xpath('./td[@class="drawresult-td-left strong"]/text()').get())
        LottoItem.add_value("cat_5_winners", rows[5].xpath('./td[@class="drawresult-td-left strong"]/text()').get())
        LottoItem.add_value("cat_6_winners", rows[6].xpath('./td[@class="drawresult-td-left strong"]/text()').get())
        yield LottoItem.load_item()


class AzerbaijanLotto5x36(scrapy.Spider):

    name = "AzerbaijanLotto5x36"

    # NO NUM WINNERS DATA

    def start_requests(self):
        self.name = "AzerbaijanLotto5x36"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://azerlotereya.com/az"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        game_tile = response.xpath('//div[@class="partgame__inside"]')
        for game in game_tile:
            if "5/36" in game.xpath('.//img/@title').get():
                self.jackpot = game.xpath('.//span[@class="cekpotprice"]/text()').get()

        url = "https://azerlotereya.com/az/gameresult/meqa536"
        yield scrapy.Request(url=url, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":10})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=AzerbaijanLotto5x36Item(), selector=response)
        balls_lst = response.xpath('//div[@class="load_gameresult"]//div[@class="fs"]/span/text()').getall()
        draw_details = response.xpath('//select[@class="change_draw"]/option/text()').get()

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        draw_date = draw_details.split('-')[1].strip()
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d.%m.%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", draw_details.split('-')[0].strip())
        LottoItem.add_value("jackpot", self.jackpot)
        yield LottoItem.load_item()


class AzerbaijanLotto6x40(scrapy.Spider):

    name = "AzerbaijanLotto6x40"

    # NO NUM WINNERS DATA

    def start_requests(self):
        self.name = "AzerbaijanLotto6x40"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://azerlotereya.com/az"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        self.jackpot = '' # if no 6/40 jackpot being advertised
        game_tile = response.xpath('//div[@class="partgame__inside"]')
        for game in game_tile:
            if "6/40" in game.xpath('.//img/@title').get():
                self.jackpot = game.xpath('.//span[@class="cekpotprice"]/text()').get()

        url = "https://azerlotereya.com/az/gameresult/640"
        yield scrapy.Request(url=url, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":10})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=AzerbaijanLotto6x40Item(), selector=response)
        balls_lst = response.xpath('//div[@class="load_gameresult"]//div[@class="fs"]/span/text()').getall()
        draw_details = response.xpath('//select[@class="change_draw"]/option/text()').get()

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        draw_date = draw_details.split('-')[1].strip()
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d.%m.%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", draw_details.split('-')[0].strip())
        LottoItem.add_value("jackpot", self.jackpot)
        yield LottoItem.load_item()


class BarbadosMega6(scrapy.Spider):

    name = "BarbadosMega6"

    # CHECK ON DAY OF DRAW WHEN JACKPOT IS WON TO SEE IF 'match_6' IS ADDED TO TABLE

    def start_requests(self):
        self.name = "BarbadosMega6"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.mybarbadoslottery.com/games/mega-6"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=BarbadosMega6Item(), selector=response)
        balls_lst = response.xpath('//div[@class="ball-results"]/ul/li/text()').getall()
        rows = response.xpath('//table[@class="winners-table"]/tbody/tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        draw_date = ",".join(response.xpath('//div[@class="panel-result"]//time/text()').get().split(',')[1:]).strip()
        LottoItem.add_value("draw_datetime", datetime.strptime(clean_date_string(draw_date), "%B %d, %Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("estimated_next_jackpot", response.xpath('//div[@class="jackpot"]/h2/text()').get())
        match_6, match_5, match_4, match_3 = '0','0','0','0'
        prize_6, prize_5, prize_4, prize_3 = '0','0','0','0'
        for row in rows:
            match_category = row.xpath('./td/text()').getall()[0]
            if "6 of" in match_category:
                prize_6 = row.xpath('./td/text()').getall()[2]
                match_6 = row.xpath('./td/text()').getall()[1]
            elif "5 of" in match_category:
                prize_5 = row.xpath('./td/text()').getall()[2]
                match_5 = row.xpath('./td/text()').getall()[1]
            elif "4 of" in match_category:
                prize_4 = row.xpath('./td/text()').getall()[2]
                match_4 = row.xpath('./td/text()').getall()[1]
            elif "3 of" in match_category:
                prize_3 = row.xpath('./td/text()').getall()[2]
                match_3 = row.xpath('./td/text()').getall()[1]
        LottoItem.add_value("cat_1_prize", prize_6)
        LottoItem.add_value("cat_2_prize", prize_5)
        LottoItem.add_value("cat_3_prize", prize_4)
        LottoItem.add_value("cat_4_prize", prize_3)
        LottoItem.add_value("cat_1_winners", match_6)
        LottoItem.add_value("cat_2_winners", match_5)
        LottoItem.add_value("cat_3_winners", match_4)
        LottoItem.add_value("cat_4_winners", match_3)
        yield LottoItem.load_item()


class BelarusLotto(scrapy.Spider):

    name = "BelarusSportLotto5x36"
    name2 = "BelarusSportLotto6x49"

    # NUMBERS ARE IMAGES AND NOT TEXT; CAN'T SCRAPE RESULTS

    urls = [
        "https://sportloto.by/archive",
        "https://6x49.sportloto.by/arkhivtirazhej"
    ]


class BelgiumLotto(scrapy.Spider):

    name = "BelgiumLotto"

    def start_requests(self):
        self.name = "BelgiumLotto"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        headers = {
            'authority': 'apim.prd.natlot.be',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'dnt': '1',
            'origin': 'https://www.loterie-nationale.be',
            'referer': 'https://www.loterie-nationale.be/nos-jeux/lotto/resultats-tirage/11-06-2022?',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36',
        }
        url = 'https://apim.prd.natlot.be/api/v4/draw-games/draws?status=PAYABLE&previous-draws=5&game-names=Lotto'
        yield scrapy.Request(url=url, headers=headers, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=BelgiumLottoItem(), selector=response)
        latest = response.json()['draws'][-1]
        balls_lst = latest['results'][0]['primary']
        bonus_ball = latest['results'][1]['primary'][0]

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", str(balls_lst[0]))
        LottoItem.add_value("ball1", str(balls_lst[1]))
        LottoItem.add_value("ball2", str(balls_lst[2]))
        LottoItem.add_value("ball3", str(balls_lst[3]))
        LottoItem.add_value("ball4", str(balls_lst[4]))
        LottoItem.add_value("ball5", str(balls_lst[5]))
        LottoItem.add_value("bonus_ball", str(bonus_ball))
        LottoItem.add_value("draw_datetime", str(latest['drawTime']))
        LottoItem.add_value("draw_number", str(latest['id']))
        if int(latest['prizeTiers'][0]['shareCount']) == 0:
            LottoItem.add_value("cat_1_prize", str(int(latest['jackpots'][0]['amount'])/100.0))
        else:
            LottoItem.add_value("cat_1_prize", str(int(latest['prizeTiers'][0]['shareAmount'])/100.0))
        LottoItem.add_value("cat_2_prize", str(int(latest['prizeTiers'][1]['shareAmount'])/100.0))
        LottoItem.add_value("cat_3_prize", str(int(latest['prizeTiers'][2]['shareAmount'])/100.0))
        LottoItem.add_value("cat_4_prize", str(int(latest['prizeTiers'][3]['shareAmount'])/100.0))
        LottoItem.add_value("cat_5_prize", str(int(latest['prizeTiers'][4]['shareAmount'])/100.0))
        LottoItem.add_value("cat_6_prize", str(int(latest['prizeTiers'][5]['shareAmount'])/100.0))
        LottoItem.add_value("cat_7_prize", str(int(latest['prizeTiers'][6]['shareAmount'])/100.0))
        LottoItem.add_value("cat_8_prize", str(int(latest['prizeTiers'][7]['shareAmount'])/100.0))
        LottoItem.add_value("cat_9_prize", str(int(latest['prizeTiers'][8]['shareAmount'])/100.0))
        LottoItem.add_value("cat_1_winners", str(latest['prizeTiers'][0]['shareCount']))
        LottoItem.add_value("cat_2_winners", str(latest['prizeTiers'][1]['shareCount']))
        LottoItem.add_value("cat_3_winners", str(latest['prizeTiers'][2]['shareCount']))
        LottoItem.add_value("cat_4_winners", str(latest['prizeTiers'][3]['shareCount']))
        LottoItem.add_value("cat_5_winners", str(latest['prizeTiers'][4]['shareCount']))
        LottoItem.add_value("cat_6_winners", str(latest['prizeTiers'][5]['shareCount']))
        LottoItem.add_value("cat_7_winners", str(latest['prizeTiers'][6]['shareCount']))
        LottoItem.add_value("cat_8_winners", str(latest['prizeTiers'][7]['shareCount']))
        LottoItem.add_value("cat_9_winners", str(latest['prizeTiers'][8]['shareCount']))
        yield LottoItem.load_item()


class BosniaSuperLoto(scrapy.Spider):

    name = "BosniaSuperLoto"

    # Note: Number of winners is a decimal/non-integer (not sure why?)
    # Can play with/without bonus_colour; either black or red
    # Loto combination price is 0.5 KM, an extra 0.2 KM for bonus_colour (req. for Superjackpot)

    def start_requests(self):
        self.name = "BosniaSuperLoto"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.lutrijabih.ba/"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        self.next_jackpot = response.xpath('//div[@class="nagrade"]/span[@class="nagradni-iznos-head"]/text()').getall()[-1]
        url = "https://www.lutrijabih.ba/igre/super-loto/privremeni-izvjestaj/"
        yield scrapy.Request(url=url, callback=self.parse_draw,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=BosniaSuperLotoItem(), selector=response)
        balls_lst = response.xpath('//div[@id="lotoIzvestaj"]//ul/li/span/text()').getall()
        bonus_colour = response.xpath('//div[@class="detalji-izvlacenja"]/p/span/text()').get()
        rows = response.xpath('//tbody/tr')[1:]
        draw_info = response.xpath('//div[@id="subtitle"]/text()').get().lower().split('kolo')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("bonus_colour", bonus_colour)
        LottoItem.add_value("draw_datetime", datetime.strptime(clean_datetime(draw_info[1]), "%d.%m.%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", "".join([s for s in draw_info[0] if s.isdigit()]))
        LottoItem.add_value("sales", response.xpath('//div[@class="detalji-izvlacenja"]/p/strong/text()').getall()[1])
        LottoItem.add_value("draw_bonus_colour_sales", response.xpath(
            '//div[@class="detalji-izvlacenja"]/p/strong/text()').getall()[4])
        LottoItem.add_value("estimated_next_jackpot", self.next_jackpot)
        # note: Jackpot will be '0' unless won
        LottoItem.add_value("cat_1_prize", rows[0].xpath('./td/text()').getall()[-1]) #superjackpot
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./td/text()').getall()[-1]) #jackpot
        LottoItem.add_value("cat_3_prize", rows[3].xpath('./td/text()').getall()[-1]) #5
        LottoItem.add_value("cat_4_prize", rows[5].xpath('./td/text()').getall()[-1]) #4
        LottoItem.add_value("cat_5_prize", rows[7].xpath('./td/text()').getall()[-1]) #3
        LottoItem.add_value("cat_2_bonus_prize", rows[2].xpath('./td/text()').getall()[-1]) #5+colour
        LottoItem.add_value("cat_3_bonus_prize", rows[4].xpath('./td/text()').getall()[-1]) #4+colour
        LottoItem.add_value("cat_4_bonus_prize", rows[6].xpath('./td/text()').getall()[-1]) #3+colour
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td/text()').getall()[-2]) #superjackpot
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./td/text()').getall()[-2]) #jackpot
        LottoItem.add_value("cat_3_winners", rows[3].xpath('./td/text()').getall()[-2]) #5 (prev. cat_4)
        LottoItem.add_value("cat_4_winners", rows[5].xpath('./td/text()').getall()[-2]) #4 (prev. cat_6)
        LottoItem.add_value("cat_5_winners", rows[7].xpath('./td/text()').getall()[-2]) #3 (prev. cat_8)
        LottoItem.add_value("cat_2_bonus_winners", rows[2].xpath('./td/text()').getall()[-2]) #5+colour (prev. cat_3)
        LottoItem.add_value("cat_3_bonus_winners", rows[4].xpath('./td/text()').getall()[-2]) #4+colour (prev. cat_5)
        LottoItem.add_value("cat_4_bonus_winners", rows[6].xpath('./td/text()').getall()[-2]) #3+colour (prev. cat_7)

        yield LottoItem.load_item()


class BrazilTimeMania(scrapy.Spider):

    name = "BrazilTimeMania"

    def start_requests(self):
        self.name = "BrazilTimeMania"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        #url = "http://loterias.caixa.gov.br/wps/portal/loterias/landing/timemania"
        root_url = 'https://servicebus2.caixa.gov.br/portaldeloterias/api/timemania/'
        yield scrapy.Request(url=root_url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        LottoItem = ItemLoader(item=BrazilTimeManiaItem(), selector=response)
        temp = response.body.decode('utf-8', 'ignore').encode('ascii', 'replace').decode()
        temp = re.sub(r"[^a-zA-Z]'", '"', temp)
        clean_text = BeautifulSoup(temp, 'lxml').text
        latest = json.loads(clean_text)
        balls_lst = latest['listaDezenas']

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", str(int(balls_lst[0])))
        LottoItem.add_value("ball1", str(int(balls_lst[1])))
        LottoItem.add_value("ball2", str(int(balls_lst[2])))
        LottoItem.add_value("ball3", str(int(balls_lst[3])))
        LottoItem.add_value("ball4", str(int(balls_lst[4])))
        LottoItem.add_value("ball5", str(int(balls_lst[5])))
        LottoItem.add_value("ball6", str(int(balls_lst[6])))
        draw_date = str(latest['dataApuracao'])
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d/%m/%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", str(latest['numero']))
        LottoItem.add_value("sales", str(latest['valorArrecadado']))
        LottoItem.add_value("estimated_next_jackpot", str(latest['valorEstimadoProximoConcurso']))
        # note: 'cat_1_prize' == 0 unless won
        LottoItem.add_value("cat_1_prize", str(latest['listaRateioPremio'][0]['valorPremio']))
        LottoItem.add_value("cat_2_prize", str(latest['listaRateioPremio'][1]['valorPremio']))
        LottoItem.add_value("cat_3_prize", str(latest['listaRateioPremio'][2]['valorPremio']))
        LottoItem.add_value("cat_4_prize", str(latest['listaRateioPremio'][3]['valorPremio']))
        LottoItem.add_value("cat_5_prize", str(latest['listaRateioPremio'][4]['valorPremio']))
        LottoItem.add_value("cat_6_prize", str(latest['listaRateioPremio'][5]['valorPremio']))
        LottoItem.add_value("cat_1_winners", str(latest['listaRateioPremio'][0]['numeroDeGanhadores']))
        LottoItem.add_value("cat_2_winners", str(latest['listaRateioPremio'][1]['numeroDeGanhadores']))
        LottoItem.add_value("cat_3_winners", str(latest['listaRateioPremio'][2]['numeroDeGanhadores']))
        LottoItem.add_value("cat_4_winners", str(latest['listaRateioPremio'][3]['numeroDeGanhadores']))
        LottoItem.add_value("cat_5_winners", str(latest['listaRateioPremio'][4]['numeroDeGanhadores']))
        LottoItem.add_value("cat_6_winners", str(latest['listaRateioPremio'][5]['numeroDeGanhadores']))
        yield LottoItem.load_item()


class BrazilMegaSena(scrapy.Spider):

    name = "BrazilMegaSena"

    def start_requests(self):
        self.name = "BrazilMegaSena"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        #url = "http://loterias.caixa.gov.br/wps/portal/loterias/landing/megasena"
        root_url = 'https://servicebus2.caixa.gov.br/portaldeloterias/api/megasena/'
        yield scrapy.Request(url=root_url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        LottoItem = ItemLoader(item=BrazilMegaSenaItem(), selector=response)
        temp = response.body.decode('utf-8', 'ignore').encode('ascii', 'replace').decode()
        temp = re.sub(r"[^a-zA-Z]'", '"', temp)
        clean_text = BeautifulSoup(temp, 'lxml').text
        latest = json.loads(clean_text)
        balls_lst = latest['listaDezenas']

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", str(int(balls_lst[0])))
        LottoItem.add_value("ball1", str(int(balls_lst[1])))
        LottoItem.add_value("ball2", str(int(balls_lst[2])))
        LottoItem.add_value("ball3", str(int(balls_lst[3])))
        LottoItem.add_value("ball4", str(int(balls_lst[4])))
        LottoItem.add_value("ball5", str(int(balls_lst[5])))
        draw_date = str(latest['dataApuracao'])
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d/%m/%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", str(latest['numero']))
        LottoItem.add_value("sales", str(latest['valorArrecadado']))
        LottoItem.add_value("estimated_next_jackpot", str(latest['valorEstimadoProximoConcurso']))
        # note: 'cat_1_prize' == 0 unless won
        LottoItem.add_value("cat_1_prize", str(latest['listaRateioPremio'][0]['valorPremio']))
        LottoItem.add_value("cat_2_prize", str(latest['listaRateioPremio'][1]['valorPremio']))
        LottoItem.add_value("cat_3_prize", str(latest['listaRateioPremio'][2]['valorPremio']))
        LottoItem.add_value("cat_1_winners", str(latest['listaRateioPremio'][0]['numeroDeGanhadores']))
        LottoItem.add_value("cat_2_winners", str(latest['listaRateioPremio'][1]['numeroDeGanhadores']))
        LottoItem.add_value("cat_3_winners", str(latest['listaRateioPremio'][2]['numeroDeGanhadores']))
        yield LottoItem.load_item()


class BrazilLotoMania(scrapy.Spider):

    name = "BrazilLotoMania"

    def start_requests(self):
        self.name = "BrazilLotoMania"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        #url = "http://loterias.caixa.gov.br/wps/portal/loterias/landing/lotomania"
        root_url = 'https://servicebus2.caixa.gov.br/portaldeloterias/api/lotomania/'
        yield scrapy.Request(url=root_url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        LottoItem = ItemLoader(item=BrazilLotoManiaItem(), selector=response)
        temp = response.body.decode('utf-8', 'ignore').encode('ascii', 'replace').decode()
        temp = re.sub(r"[^a-zA-Z]'", '"', temp)
        clean_text = BeautifulSoup(temp, 'lxml').text
        latest = json.loads(clean_text)
        balls_lst = latest['listaDezenas']

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", str(int(balls_lst[0])))
        LottoItem.add_value("ball1", str(int(balls_lst[1])))
        LottoItem.add_value("ball2", str(int(balls_lst[2])))
        LottoItem.add_value("ball3", str(int(balls_lst[3])))
        LottoItem.add_value("ball4", str(int(balls_lst[4])))
        LottoItem.add_value("ball5", str(int(balls_lst[5])))
        LottoItem.add_value("ball6", str(int(balls_lst[6])))
        LottoItem.add_value("ball7", str(int(balls_lst[7])))
        LottoItem.add_value("ball8", str(int(balls_lst[8])))
        LottoItem.add_value("ball9", str(int(balls_lst[9])))
        LottoItem.add_value("ball10", str(int(balls_lst[10])))
        LottoItem.add_value("ball11", str(int(balls_lst[11])))
        LottoItem.add_value("ball12", str(int(balls_lst[12])))
        LottoItem.add_value("ball13", str(int(balls_lst[13])))
        LottoItem.add_value("ball14", str(int(balls_lst[14])))
        LottoItem.add_value("ball15", str(int(balls_lst[15])))
        LottoItem.add_value("ball16", str(int(balls_lst[16])))
        LottoItem.add_value("ball17", str(int(balls_lst[17])))
        LottoItem.add_value("ball18", str(int(balls_lst[18])))
        LottoItem.add_value("ball19", str(int(balls_lst[19])))
        draw_date = str(latest['dataApuracao'])
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d/%m/%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", str(latest['numero']))
        LottoItem.add_value("sales", str(latest['valorArrecadado']))
        LottoItem.add_value("estimated_next_jackpot", str(latest['valorEstimadoProximoConcurso']))
        # note: 'cat_1_prize' == 0 unless won
        LottoItem.add_value("cat_1_prize", str(latest['listaRateioPremio'][0]['valorPremio']))
        LottoItem.add_value("cat_2_prize", str(latest['listaRateioPremio'][6]['valorPremio']))
        LottoItem.add_value("cat_3_prize", str(latest['listaRateioPremio'][1]['valorPremio']))
        LottoItem.add_value("cat_4_prize", str(latest['listaRateioPremio'][2]['valorPremio']))
        LottoItem.add_value("cat_5_prize", str(latest['listaRateioPremio'][3]['valorPremio']))
        LottoItem.add_value("cat_6_prize", str(latest['listaRateioPremio'][4]['valorPremio']))
        LottoItem.add_value("cat_7_prize", str(latest['listaRateioPremio'][5]['valorPremio']))
        LottoItem.add_value("cat_1_winners", str(latest['listaRateioPremio'][0]['numeroDeGanhadores']))
        LottoItem.add_value("cat_2_winners", str(latest['listaRateioPremio'][6]['numeroDeGanhadores']))
        LottoItem.add_value("cat_3_winners", str(latest['listaRateioPremio'][1]['numeroDeGanhadores']))
        LottoItem.add_value("cat_4_winners", str(latest['listaRateioPremio'][2]['numeroDeGanhadores']))
        LottoItem.add_value("cat_5_winners", str(latest['listaRateioPremio'][3]['numeroDeGanhadores']))
        LottoItem.add_value("cat_6_winners", str(latest['listaRateioPremio'][4]['numeroDeGanhadores']))
        LottoItem.add_value("cat_7_winners", str(latest['listaRateioPremio'][5]['numeroDeGanhadores']))
        yield LottoItem.load_item()


class BrazilLotoFacil(scrapy.Spider):

    name = "BrazilLotoFacil"

    def start_requests(self):
        self.name = "BrazilLotoFacil"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        #url = "http://loterias.caixa.gov.br/wps/portal/loterias/landing/lotofacil"
        root_url = 'https://servicebus2.caixa.gov.br/portaldeloterias/api/lotofacil/'
        yield scrapy.Request(url=root_url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        LottoItem = ItemLoader(item=BrazilLotoFacilItem(), selector=response)
        temp = response.body.decode('utf-8', 'ignore').encode('ascii', 'replace').decode()
        temp = re.sub(r"[^a-zA-Z]'", '"', temp)
        clean_text = BeautifulSoup(temp, 'lxml').text
        latest = json.loads(clean_text)
        balls_lst = latest['listaDezenas']

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", str(int(balls_lst[0])))
        LottoItem.add_value("ball1", str(int(balls_lst[1])))
        LottoItem.add_value("ball2", str(int(balls_lst[2])))
        LottoItem.add_value("ball3", str(int(balls_lst[3])))
        LottoItem.add_value("ball4", str(int(balls_lst[4])))
        LottoItem.add_value("ball5", str(int(balls_lst[5])))
        LottoItem.add_value("ball6", str(int(balls_lst[6])))
        LottoItem.add_value("ball7", str(int(balls_lst[7])))
        LottoItem.add_value("ball8", str(int(balls_lst[8])))
        LottoItem.add_value("ball9", str(int(balls_lst[9])))
        LottoItem.add_value("ball10", str(int(balls_lst[10])))
        LottoItem.add_value("ball11", str(int(balls_lst[11])))
        LottoItem.add_value("ball12", str(int(balls_lst[12])))
        LottoItem.add_value("ball13", str(int(balls_lst[13])))
        LottoItem.add_value("ball14", str(int(balls_lst[14])))
        draw_date = str(latest['dataApuracao'])
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d/%m/%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", str(latest['numero']))
        LottoItem.add_value("sales", str(latest['valorArrecadado']))
        LottoItem.add_value("estimated_next_jackpot", str(latest['valorEstimadoProximoConcurso']))
        # note: 'cat_1_prize' == 0 unless won
        LottoItem.add_value("cat_1_prize", str(latest['listaRateioPremio'][0]['valorPremio']))
        LottoItem.add_value("cat_2_prize", str(latest['listaRateioPremio'][1]['valorPremio']))
        LottoItem.add_value("cat_3_prize", str(latest['listaRateioPremio'][2]['valorPremio']))
        LottoItem.add_value("cat_4_prize", str(latest['listaRateioPremio'][3]['valorPremio']))
        LottoItem.add_value("cat_5_prize", str(latest['listaRateioPremio'][4]['valorPremio']))
        LottoItem.add_value("cat_1_winners", str(latest['listaRateioPremio'][0]['numeroDeGanhadores']))
        LottoItem.add_value("cat_2_winners", str(latest['listaRateioPremio'][1]['numeroDeGanhadores']))
        LottoItem.add_value("cat_3_winners", str(latest['listaRateioPremio'][2]['numeroDeGanhadores']))
        LottoItem.add_value("cat_4_winners", str(latest['listaRateioPremio'][3]['numeroDeGanhadores']))
        LottoItem.add_value("cat_5_winners", str(latest['listaRateioPremio'][4]['numeroDeGanhadores']))
        yield LottoItem.load_item()


class BrazilQuina(scrapy.Spider):

    name = "BrazilQuina"

    def start_requests(self):
        self.name = "BrazilQuina"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        #url = "http://loterias.caixa.gov.br/wps/portal/loterias/landing/quina"
        self.headers = {
            'Connection': 'keep-alive',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
            'Accept': 'application/json, text/plain, */*',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
            'sec-ch-ua-platform': '"Windows"',
            'Origin': 'https://loterias.caixa.gov.br',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://loterias.caixa.gov.br/',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }
        root_url = 'https://servicebus2.caixa.gov.br/portaldeloterias/api/quina/'
        yield scrapy.Request(url=root_url, callback=self.parse, headers=self.headers,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        LottoItem = ItemLoader(item=BrazilQuinaItem(), selector=response)
        temp = response.body.decode('utf-8', 'ignore').encode('ascii', 'replace').decode()
        temp = re.sub(r"[^a-zA-Z]'", '"', temp)
        clean_text = BeautifulSoup(temp, 'lxml').text
        latest = json.loads(clean_text)
        balls_lst = latest['listaDezenas']

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", str(int(balls_lst[0])))
        LottoItem.add_value("ball1", str(int(balls_lst[1])))
        LottoItem.add_value("ball2", str(int(balls_lst[2])))
        LottoItem.add_value("ball3", str(int(balls_lst[3])))
        LottoItem.add_value("ball4", str(int(balls_lst[4])))
        draw_date = str(latest['dataApuracao'])
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d/%m/%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", str(latest['numero']))
        LottoItem.add_value("sales", str(latest['valorArrecadado']))
        LottoItem.add_value("estimated_next_jackpot", str(latest['valorEstimadoProximoConcurso']))
        # note: 'cat_1_prize' == 0 unless won
        LottoItem.add_value("cat_1_prize", str(latest['listaRateioPremio'][0]['valorPremio']))
        LottoItem.add_value("cat_2_prize", str(latest['listaRateioPremio'][1]['valorPremio']))
        LottoItem.add_value("cat_3_prize", str(latest['listaRateioPremio'][2]['valorPremio']))
        LottoItem.add_value("cat_4_prize", str(latest['listaRateioPremio'][3]['valorPremio']))
        LottoItem.add_value("cat_1_winners", str(latest['listaRateioPremio'][0]['numeroDeGanhadores']))
        LottoItem.add_value("cat_2_winners", str(latest['listaRateioPremio'][1]['numeroDeGanhadores']))
        LottoItem.add_value("cat_3_winners", str(latest['listaRateioPremio'][2]['numeroDeGanhadores']))
        LottoItem.add_value("cat_4_winners", str(latest['listaRateioPremio'][3]['numeroDeGanhadores']))
        yield LottoItem.load_item()


class BrazilDuplaSena(scrapy.Spider):

    name = "BrazilDuplaSena"

    def start_requests(self):
        self.name = "BrazilDuplaSena"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        #url = "http://loterias.caixa.gov.br/wps/portal/loterias/landing/duplasena"
        self.headers = {
            'Connection': 'keep-alive',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
            'Accept': 'application/json, text/plain, */*',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
            'sec-ch-ua-platform': '"Windows"',
            'Origin': 'https://loterias.caixa.gov.br',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://loterias.caixa.gov.br/',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }
        root_url = 'https://servicebus2.caixa.gov.br/portaldeloterias/api/duplasena/'
        yield scrapy.Request(url=root_url, callback=self.parse, headers=self.headers,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        LottoItem = ItemLoader(item=BrazilDuplaSenaItem(), selector=response)
        temp = response.body.decode('utf-8', 'ignore').encode('ascii', 'replace').decode()
        temp = re.sub(r"[^a-zA-Z]'", '"', temp)
        clean_text = BeautifulSoup(temp, 'lxml').text
        latest = json.loads(clean_text)
        draw_1_balls_lst = latest['listaDezenas']
        draw_2_balls_lst = latest['listaDezenasSegundoSorteio']

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("draw1_ball0", str(int(draw_1_balls_lst[0])))
        LottoItem.add_value("draw1_ball1", str(int(draw_1_balls_lst[1])))
        LottoItem.add_value("draw1_ball2", str(int(draw_1_balls_lst[2])))
        LottoItem.add_value("draw1_ball3", str(int(draw_1_balls_lst[3])))
        LottoItem.add_value("draw1_ball4", str(int(draw_1_balls_lst[4])))
        LottoItem.add_value("draw1_ball5", str(int(draw_1_balls_lst[5])))
        LottoItem.add_value("draw2_ball0", str(int(draw_2_balls_lst[0])))
        LottoItem.add_value("draw2_ball1", str(int(draw_2_balls_lst[1])))
        LottoItem.add_value("draw2_ball2", str(int(draw_2_balls_lst[2])))
        LottoItem.add_value("draw2_ball3", str(int(draw_2_balls_lst[3])))
        LottoItem.add_value("draw2_ball4", str(int(draw_2_balls_lst[4])))
        LottoItem.add_value("draw2_ball5", str(int(draw_2_balls_lst[5])))
        draw_date = str(latest['dataApuracao'])
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d/%m/%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", str(latest['numero']))
        LottoItem.add_value("sales", str(latest['valorArrecadado']))
        LottoItem.add_value("estimated_next_jackpot", str(latest['valorEstimadoProximoConcurso']))
        # note: 'jackpot' == 0 unless won
        LottoItem.add_value("draw1_cat_1_prize", str(latest['listaRateioPremio'][0]['valorPremio']))
        LottoItem.add_value("draw1_cat_2_prize", str(latest['listaRateioPremio'][1]['valorPremio']))
        LottoItem.add_value("draw1_cat_3_prize", str(latest['listaRateioPremio'][2]['valorPremio']))
        LottoItem.add_value("draw1_cat_4_prize", str(latest['listaRateioPremio'][3]['valorPremio']))
        LottoItem.add_value("draw2_cat_1_prize", str(latest['listaRateioPremio'][4]['valorPremio']))
        LottoItem.add_value("draw2_cat_2_prize", str(latest['listaRateioPremio'][5]['valorPremio']))
        LottoItem.add_value("draw2_cat_3_prize", str(latest['listaRateioPremio'][6]['valorPremio']))
        LottoItem.add_value("draw2_cat_4_prize", str(latest['listaRateioPremio'][7]['valorPremio']))
        LottoItem.add_value("draw1_cat_1_winners", str(latest['listaRateioPremio'][0]['numeroDeGanhadores']))
        LottoItem.add_value("draw1_cat_2_winners", str(latest['listaRateioPremio'][1]['numeroDeGanhadores']))
        LottoItem.add_value("draw1_cat_3_winners", str(latest['listaRateioPremio'][2]['numeroDeGanhadores']))
        LottoItem.add_value("draw1_cat_4_winners", str(latest['listaRateioPremio'][3]['numeroDeGanhadores']))
        LottoItem.add_value("draw2_cat_1_winners", str(latest['listaRateioPremio'][4]['numeroDeGanhadores']))
        LottoItem.add_value("draw2_cat_2_winners", str(latest['listaRateioPremio'][5]['numeroDeGanhadores']))
        LottoItem.add_value("draw2_cat_3_winners", str(latest['listaRateioPremio'][6]['numeroDeGanhadores']))
        LottoItem.add_value("draw2_cat_4_winners", str(latest['listaRateioPremio'][7]['numeroDeGanhadores']))
        yield LottoItem.load_item()


class BulgariaLotto6x49(scrapy.Spider):

    name = "BulgariaLotto6x49"

    def start_requests(self):
        self.name = "BulgariaLotto6x49"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "http://toto.bg/results/6x49"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=BulgariaLotto6x49Item(), selector=response)
        balls_lst = response.xpath('//div[@class="tir_numbers"]//span[@class="ball-white"]/text()').getall()
        rows = response.xpath('//table//tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        draw_date = response.xpath('//h2[@class="tir_title"]/text()').get().split('-')[1].strip()
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d.%m.%Y").strftime("%Y-%m-%d"))
        draw_number = response.xpath('//h2[@class="tir_title"]/text()').get().split('-')[0].strip().split(' ')[-1].strip()
        LottoItem.add_value("draw_number", draw_date.split('.')[-1] + "-" + draw_number)
        if prize_to_num(rows[1].xpath('./td/text()').getall()[1].strip()) == 0:
            LottoItem.add_value("cat_1_prize", response.xpath(
                '//div[@class="tir_jackpot"]//div[@class="col-sm-6 sum text-right"]/text()').get().strip())
        else:
            LottoItem.add_value("cat_1_prize", rows[1].xpath('./td[@align="right"]/text()').get())
        LottoItem.add_value("cat_2_prize", rows[2].xpath('./td[@align="right"]/text()').get())
        LottoItem.add_value("cat_3_prize", rows[3].xpath('./td[@align="right"]/text()').get())
        LottoItem.add_value("cat_4_prize", rows[4].xpath('./td[@align="right"]/text()').get())
        LottoItem.add_value("cat_1_winners", rows[1].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_2_winners", rows[2].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_3_winners", rows[3].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_4_winners", rows[4].xpath('./td/text()').getall()[1])
        yield LottoItem.load_item()


class BulgariaLotto6x42(scrapy.Spider):

    name = "BulgariaLotto6x42"

    def start_requests(self):
        self.name = "BulgariaLotto6x42"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "http://toto.bg/results/6x42"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=BulgariaLotto6x42Item(), selector=response)
        balls_lst = response.xpath('//div[@class="tir_numbers"]//span[@class="ball-white"]/text()').getall()
        rows = response.xpath('//table//tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        draw_date = response.xpath('//h2[@class="tir_title"]/text()').get().split('-')[1].strip()
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d.%m.%Y").strftime("%Y-%m-%d"))
        draw_number = response.xpath('//h2[@class="tir_title"]/text()').get().split('-')[0].strip().split(' ')[-1].strip()
        LottoItem.add_value("draw_number", draw_date.split('.')[-1] + "-" + draw_number)
        if prize_to_num(rows[1].xpath('./td/text()').getall()[1].strip()) == 0:
            LottoItem.add_value("cat_1_prize", response.xpath(
                '//div[@class="tir_jackpot"]//div[@class="col-sm-6 sum text-right"]/text()').get().strip())
        else:
            LottoItem.add_value("cat_1_prize", rows[1].xpath('./td[@align="right"]/text()').get())
        LottoItem.add_value("cat_2_prize", rows[2].xpath('./td[@align="right"]/text()').get())
        LottoItem.add_value("cat_3_prize", rows[3].xpath('./td[@align="right"]/text()').get())
        LottoItem.add_value("cat_4_prize", rows[4].xpath('./td[@align="right"]/text()').get())
        LottoItem.add_value("cat_1_winners", rows[1].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_2_winners", rows[2].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_3_winners", rows[3].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_4_winners", rows[4].xpath('./td/text()').getall()[1])
        yield LottoItem.load_item()


class BulgariaLotto5x35(scrapy.Spider):

    name = "BulgariaLotto5x35"

    def start_requests(self):
        self.name = "BulgariaLotto5x35"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "http://toto.bg/results/5x35"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=BulgariaLotto5x35Item(), selector=response)
        balls_lst = response.xpath('//div[@class="tir_numbers"]//span[@class="ball-white"]/text()').getall()
        rows = response.xpath('//table//tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("draw1_ball0", balls_lst[0])
        LottoItem.add_value("draw1_ball1", balls_lst[1])
        LottoItem.add_value("draw1_ball2", balls_lst[2])
        LottoItem.add_value("draw1_ball3", balls_lst[3])
        LottoItem.add_value("draw1_ball4", balls_lst[4])
        LottoItem.add_value("draw2_ball0", balls_lst[5])
        LottoItem.add_value("draw2_ball1", balls_lst[6])
        LottoItem.add_value("draw2_ball2", balls_lst[7])
        LottoItem.add_value("draw2_ball3", balls_lst[8])
        LottoItem.add_value("draw2_ball4", balls_lst[9])
        draw_date = response.xpath('//h2[@class="tir_title"]/text()').get().split('-')[1].strip()
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d.%m.%Y").strftime("%Y-%m-%d"))
        draw_number = response.xpath('//h2[@class="tir_title"]/text()').get().split('-')[0].strip().split(' ')[-1].strip()
        LottoItem.add_value("draw_number", draw_date.split('.')[-1] + "-" + draw_number)
        LottoItem.add_value("draw1_cat_1_prize", rows[1].xpath('./td[@align="right"]/text()').get())
        LottoItem.add_value("draw1_cat_2_prize", rows[2].xpath('./td[@align="right"]/text()').get())
        LottoItem.add_value("draw1_cat_3_prize", rows[3].xpath('./td[@align="right"]/text()').get())
        LottoItem.add_value("draw2_cat_1_prize", rows[5].xpath('./td[@align="right"]/text()').get())
        LottoItem.add_value("draw2_cat_2_prize", rows[6].xpath('./td[@align="right"]/text()').get())
        LottoItem.add_value("draw2_cat_3_prize", rows[7].xpath('./td[@align="right"]/text()').get())
        LottoItem.add_value("draw1_cat_1_winners", rows[1].xpath('./td/text()').getall()[1])
        LottoItem.add_value("draw1_cat_2_winners", rows[2].xpath('./td/text()').getall()[1])
        LottoItem.add_value("draw1_cat_3_winners", rows[3].xpath('./td/text()').getall()[1])
        LottoItem.add_value("draw2_cat_1_winners", rows[5].xpath('./td/text()').getall()[1])
        LottoItem.add_value("draw2_cat_2_winners", rows[6].xpath('./td/text()').getall()[1])
        LottoItem.add_value("draw2_cat_3_winners", rows[7].xpath('./td/text()').getall()[1])
        yield LottoItem.load_item()


class CanadaMaxLotto(scrapy.Spider):

    name = "CanadaMaxLotto"

    # National lotto; easiest scrape via ontario site

    def start_requests(self):
        self.name = "CanadaMaxLotto"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        headers = {
            'authority': 'gateway.wma.bedegaming.com',
            'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            'accept': 'application/json, text/plain, */*',
            'x-correlation-token': 'bbed4432-aebc-4584-8897-e7d601178511',
            'x-client-id': 'aRhX7dCdHgaS578f6XK5FyCU60aF58lLEzfWOEE+ipsa1RDiY5HyaOnqpP8JwfoJIkW3nQ8Jhaz8jm4PZwKLSg+Zfqo/GiDJG7LdOvK9YcF8cMSBAbrvVQ==',
            'x-site-code': 'playolg.ca',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
            'origin': 'https://www.olg.ca',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.olg.ca/',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }
        url = 'https://gateway.wma.bedegaming.com/feeds/past-winning-numbers?game=lottomax&startDate=XXXX&endDate=YYYY'
        url = url.replace("XXXX", (datetime.now()-timedelta(days=10)).strftime("%Y-%m-%d"))
        url = url.replace("YYYY", (datetime.now()+timedelta(days=1)).strftime("%Y-%m-%d"))
        yield scrapy.Request(url=url, headers=headers, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        self.latest = response.json()['response']['winnings']['lottomax']['draw'][0]
        self.balls_lst = [i.strip() for i in self.latest['main']['regular'].split(',')]
        url = "http://www.wclc.com/winning-numbers/lotto-max-extra.htm"
        yield scrapy.Request(url=url, callback=self.parse_next,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse_next(self, response):
        rows = response.xpath('//div[@id="pastWinNumContent"]//div[@class="pastWinNumMaxmillions pastWinNumGroupDivider"]')
        maxmillions = rows[0].xpath('.//ul//text()').getall()
        if len(maxmillions) == 0:
            self.n_maxmillions = 0
        else:
            self.n_maxmillions = [x.replace('\n','').replace('\t','') for x in maxmillions if x.split()]
            self.n_maxmillions = len(self.n_maxmillions) // 7
        url = "https://www.lotterycanada.com/lotto-max"
        yield scrapy.Request(url=url, callback=self.parse_next_after, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse_next_after(self, response):
        LottoItem = ItemLoader(item=CanadaMaxLottoItem(), selector=response)
        total_sales = response.xpath('//div[@class="card my-2"]//tr')
        total_sales = total_sales[10].xpath('.//td//text()').getall()[1].strip()
        jackpot = self.latest['main']['prizeShares']['prize'][0]['amount']
        jackpot = prize_to_num(jackpot)
        jackpot = jackpot + (self.n_maxmillions * 1000000)

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("sales", total_sales)
        LottoItem.add_value("ball0", str(self.balls_lst[0]))
        LottoItem.add_value("ball1", str(self.balls_lst[1]))
        LottoItem.add_value("ball2", str(self.balls_lst[2]))
        LottoItem.add_value("ball3", str(self.balls_lst[3]))
        LottoItem.add_value("ball4", str(self.balls_lst[4]))
        LottoItem.add_value("ball5", str(self.balls_lst[5]))
        LottoItem.add_value("ball6", str(self.balls_lst[6]))
        LottoItem.add_value("bonus_ball", str(self.latest['main']['bonus']))
        LottoItem.add_value("draw_datetime", self.latest['date'])
        LottoItem.add_value("cat_1_prize", str(jackpot))
        LottoItem.add_value("cat_2_prize", self.latest['main']['prizeShares']['prize'][1]['amount'])
        LottoItem.add_value("cat_3_prize", self.latest['main']['prizeShares']['prize'][2]['amount'])
        LottoItem.add_value("cat_4_prize", self.latest['main']['prizeShares']['prize'][3]['amount'])
        LottoItem.add_value("cat_5_prize", self.latest['main']['prizeShares']['prize'][4]['amount'])
        LottoItem.add_value("cat_6_prize", self.latest['main']['prizeShares']['prize'][5]['amount'])
        LottoItem.add_value("cat_7_prize", self.latest['main']['prizeShares']['prize'][6]['amount'])
        LottoItem.add_value("cat_8_prize", self.latest['main']['prizeShares']['prize'][7]['amount'])
        LottoItem.add_value("cat_9_prize", '5') # prize is free play
        LottoItem.add_value("cat_1_winners", str(self.latest['main']['prizeShares']['prize'][0]['winningTickets']))
        LottoItem.add_value("cat_2_winners", str(self.latest['main']['prizeShares']['prize'][1]['winningTickets']))
        LottoItem.add_value("cat_3_winners", str(self.latest['main']['prizeShares']['prize'][2]['winningTickets']))
        LottoItem.add_value("cat_4_winners", str(self.latest['main']['prizeShares']['prize'][3]['winningTickets']))
        LottoItem.add_value("cat_5_winners", str(self.latest['main']['prizeShares']['prize'][4]['winningTickets']))
        LottoItem.add_value("cat_6_winners", str(self.latest['main']['prizeShares']['prize'][5]['winningTickets']))
        LottoItem.add_value("cat_7_winners", str(self.latest['main']['prizeShares']['prize'][6]['winningTickets']))
        LottoItem.add_value("cat_8_winners", str(self.latest['main']['prizeShares']['prize'][7]['winningTickets']))
        LottoItem.add_value("cat_9_winners", str(self.latest['main']['prizeShares']['prize'][8]['winningTickets']))
        LottoItem.add_value("n_MaxMillions", str(self.n_maxmillions))
        yield LottoItem.load_item()


class CanadaLotto649(scrapy.Spider):

    name = "CanadaLotto649"

    # National lotto; easiest scrape via ontario site

    def start_requests(self):
        self.name = "CanadaLotto649"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "http://www.wclc.com/winning-numbers/lotto-649-extra.htm"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        gold_info = response.xpath('//div[@class="nextJackpotDetails"]//div[@class="nextJackpotDetailsL649gold nextJackpotAd"]')
        self.gold_ball_jackpot = gold_info.xpath('.//div[@class="nextJackpotPrizeAmount"]//text()').get()
        self.gold_ball_jackpot = int(self.gold_ball_jackpot) * 1000000
        headers = {
            'authority': 'gateway.wma.bedegaming.com',
            'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            'accept': 'application/json, text/plain, */*',
            'x-correlation-token': 'bbed4432-aebc-4584-8897-e7d601178511',
            'x-client-id': 'aRhX7dCdHgaS578f6XK5FyCU60aF58lLEzfWOEE+ipsa1RDiY5HyaOnqpP8JwfoJIkW3nQ8Jhaz8jm4PZwKLSg+Zfqo/GiDJG7LdOvK9YcF8cMSBAbrvVQ==',
            'x-site-code': 'playolg.ca',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
            'origin': 'https://www.olg.ca',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.olg.ca/',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }
        url = 'https://gateway.wma.bedegaming.com/feeds/past-winning-numbers?game=lotto649&startDate=XXXX&endDate=YYYY'
        url = url.replace("XXXX", (datetime.now()-timedelta(days=10)).strftime("%Y-%m-%d"))
        url = url.replace("YYYY", (datetime.now()+timedelta(days=1)).strftime("%Y-%m-%d"))
        yield scrapy.Request(url=url, headers=headers, callback=self.parse_next, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse_next(self, response):
        LottoItem = ItemLoader(item=CanadaLotto649Item(), selector=response)
        latest = response.json()['response']['winnings']['lotto649']['draw'][0]
        balls_lst = [i.strip() for i in latest['main']['regular'].split(',')]

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("draw_datetime", latest['date'])
        LottoItem.add_value("estimated_next_jackpot", str(self.gold_ball_jackpot))
        yield LottoItem.load_item()


class CanadaLottario(scrapy.Spider):

    name = "CanadaLottario"

    def start_requests(self):
        self.name = "CanadaLottario"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        headers = {
            'authority': 'gateway.wma.bedegaming.com',
            'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            'accept': 'application/json, text/plain, */*',
            'x-correlation-token': 'bbed4432-aebc-4584-8897-e7d601178511',
            'x-client-id': 'aRhX7dCdHgaS578f6XK5FyCU60aF58lLEzfWOEE+ipsa1RDiY5HyaOnqpP8JwfoJIkW3nQ8Jhaz8jm4PZwKLSg+Zfqo/GiDJG7LdOvK9YcF8cMSBAbrvVQ==',
            'x-site-code': 'playolg.ca',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
            'origin': 'https://www.olg.ca',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.olg.ca/',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }
        url = 'https://gateway.wma.bedegaming.com/feeds/past-winning-numbers?game=lottario&startDate=XXXX&endDate=YYYY'
        url = url.replace("XXXX", (datetime.now()-timedelta(days=10)).strftime("%Y-%m-%d"))
        url = url.replace("YYYY", (datetime.now()+timedelta(days=1)).strftime("%Y-%m-%d"))
        yield scrapy.Request(url=url, headers=headers, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=CanadaLottarioItem(), selector=response)
        try:
            latest = response.json()['response']['winnings']['lottario']['draw'][0]
        except:
            latest = response.json()['response']['winnings']['lottario']['draw']
        balls_lst = [i.strip() for i in latest['main']['regular'].split(',')]
        eb_balls_lst = [i.strip() for i in latest['main']['earlyBird'].split(',')]

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", str(balls_lst[0]))
        LottoItem.add_value("ball1", str(balls_lst[1]))
        LottoItem.add_value("ball2", str(balls_lst[2]))
        LottoItem.add_value("ball3", str(balls_lst[3]))
        LottoItem.add_value("ball4", str(balls_lst[4]))
        LottoItem.add_value("ball5", str(balls_lst[5]))
        LottoItem.add_value("bonus_ball", str(latest['main']['bonus']))
        LottoItem.add_value("eb_ball0", eb_balls_lst[0])
        LottoItem.add_value("eb_ball1", eb_balls_lst[1])
        LottoItem.add_value("eb_ball2", eb_balls_lst[2])
        LottoItem.add_value("eb_ball3", eb_balls_lst[3])
        LottoItem.add_value("draw_datetime", latest['date'])
        LottoItem.add_value("cat_1_prize", latest['main']['prizeShares']['prize'][0]['amount'])
        LottoItem.add_value("cat_2_prize", latest['main']['prizeShares']['prize'][1]['amount'])
        LottoItem.add_value("cat_3_prize", latest['main']['prizeShares']['prize'][2]['amount'])
        LottoItem.add_value("cat_4_prize", latest['main']['prizeShares']['prize'][3]['amount'])
        LottoItem.add_value("cat_5_prize", latest['main']['prizeShares']['prize'][4]['amount'])
        LottoItem.add_value("cat_6_prize", latest['main']['prizeShares']['prize'][5]['amount'])
        LottoItem.add_value("cat_7_prize", latest['main']['prizeShares']['prize'][6]['amount'])
        LottoItem.add_value("cat_8_prize", '1') # prize is free ticket
        LottoItem.add_value("cat_9_prize", latest['main']['prizeShares']['prize'][8]['amount'])
        LottoItem.add_value("cat_1_winners", str(latest['main']['prizeShares']['prize'][0]['winningTickets']))
        LottoItem.add_value("cat_2_winners", str(latest['main']['prizeShares']['prize'][1]['winningTickets']))
        LottoItem.add_value("cat_3_winners", str(latest['main']['prizeShares']['prize'][2]['winningTickets']))
        LottoItem.add_value("cat_4_winners", str(latest['main']['prizeShares']['prize'][3]['winningTickets']))
        LottoItem.add_value("cat_5_winners", str(latest['main']['prizeShares']['prize'][4]['winningTickets']))
        LottoItem.add_value("cat_6_winners", str(latest['main']['prizeShares']['prize'][5]['winningTickets']))
        LottoItem.add_value("cat_7_winners", str(latest['main']['prizeShares']['prize'][6]['winningTickets']))
        LottoItem.add_value("cat_8_winners", str(latest['main']['prizeShares']['prize'][7]['winningTickets']))
        LottoItem.add_value("cat_9_winners", str(latest['main']['prizeShares']['prize'][8]['winningTickets']))
        yield LottoItem.load_item()


class ChileLoto(scrapy.Spider):

    name = "ChileLoto"

    def start_requests(self):
        self.name = "ChileLoto"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.polla.cl/es/view/resultados/5271"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        headers = {
            'authority': 'www.polla.cl',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
            'content-type': 'application/json; charset=UTF-8',
            'origin': 'https://www.polla.cl',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.polla.cl/es/view/resultados/5271',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'cookie': 'edge_production=b038eupuam6klkvfc7edjq5l81; language=es; visid_incap_1960734=sUyHD8RHTs+vAV/clZpPuWh3bF8AAAAAQUIPAAAAAADMtscrnBA4yUjmQmFWo5LH; nlbi_1960734=3+6VbGiMtTIx309VvIDR4wAAAABbSdbGimWUM77TWBKQ/sCM; incap_ses_375_1960734=/tVfZv+6kksRy8yloUQ0BWt3bF8AAAAA+bXjJK1ilfqiH3T2wGQy9g==; _ga=GA1.2.95850302.1600943982; _gid=GA1.2.10019280.1600943982; _gat_UA-87866605-2=1; _gat_Tracker_0=1',
        }
        frmdata = {"gameId":"5271"}
        rows = response.xpath('//tbody/tr')
        row_one_check = rows[0].xpath('.//div[@class="tinl"]/text()').getall()[-1]
        if "result" in row_one_check.lower():
            draw_id = rows[2].xpath('.//div[@class="tinl"]/text()').getall()[1].strip()
        else:
            draw_id = rows[0].xpath('.//div[@class="tinl"]/text()').getall()[1].strip()
        frmdata['drawId'] = draw_id
        url = "https://www.polla.cl/es/get/draw/results"
        yield scrapy.Request(url=url, method='POST', body=json.dumps(frmdata), headers=headers, callback=self.parse_draw,
            meta={"proxy": self.req_proxy, "download_timeout":10})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=ChileLotoItem(), selector=response)
        latest = response.json()

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", str(latest['results'][0]['number']))
        LottoItem.add_value("ball1", str(latest['results'][1]['number']))
        LottoItem.add_value("ball2", str(latest['results'][2]['number']))
        LottoItem.add_value("ball3", str(latest['results'][3]['number']))
        LottoItem.add_value("ball4", str(latest['results'][4]['number']))
        LottoItem.add_value("ball5", str(latest['results'][5]['number']))
        LottoItem.add_value("bonus_ball", str(latest['results'][6]['number']))
        LottoItem.add_value("draw_datetime", str(latest['drawDate']))
        LottoItem.add_value("draw_number", str(latest['drawNumber']))
        if int(latest['prizes'][0]['winners']) == 0:
            LottoItem.add_value("cat_1_prize", str(latest['jackpotAmount']))
        else:
            LottoItem.add_value("cat_1_prize", str(latest['prizes'][0]['divident']))
        LottoItem.add_value("cat_2_prize", str(latest['prizes'][1]['divident']))
        LottoItem.add_value("cat_3_prize", str(latest['prizes'][2]['divident']))
        LottoItem.add_value("cat_4_prize", str(latest['prizes'][3]['divident']))
        LottoItem.add_value("cat_5_prize", str(latest['prizes'][4]['divident']))
        LottoItem.add_value("cat_6_prize", str(latest['prizes'][5]['divident']))
        LottoItem.add_value("cat_7_prize", str(latest['prizes'][6]['divident']))
        LottoItem.add_value("cat_8_prize", str(latest['prizes'][7]['divident']))
        LottoItem.add_value("cat_1_winners", str(latest['prizes'][0]['winners']))
        LottoItem.add_value("cat_2_winners", str(latest['prizes'][1]['winners']))
        LottoItem.add_value("cat_3_winners", str(latest['prizes'][2]['winners']))
        LottoItem.add_value("cat_4_winners", str(latest['prizes'][3]['winners']))
        LottoItem.add_value("cat_5_winners", str(latest['prizes'][4]['winners']))
        LottoItem.add_value("cat_6_winners", str(latest['prizes'][5]['winners']))
        LottoItem.add_value("cat_7_winners", str(latest['prizes'][6]['winners']))
        LottoItem.add_value("cat_8_winners", str(latest['prizes'][7]['winners']))
        yield LottoItem.load_item()


class ChinaHappy8Lotto(scrapy.Spider):

    name = "ChinaHappy8Lotto"

    # note: Only scraping perms that are a choose-10 perm

    def start_requests(self):
        self.name = "ChinaHappy8Lotto"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = 'http://www.cwl.gov.cn/ygkj/wqkjgg/kl8/'
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        self.latest = response.xpath('//div[@class="table kl8"]//tbody/tr/td/a/@href').get()
        url = "http://www.cwl.gov.cn" + self.latest
        yield scrapy.Request(url=url, callback=self.parse_draw,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })


    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=ChinaHappy8LottoItem(), selector=response)
        balls_lst = [i.strip() for i in response.xpath('//div[@class="lotteryNumContainer"]/div/text()').getall()]
        rows = response.xpath('//tbody/tr')[1:]

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("ball6", balls_lst[6])
        LottoItem.add_value("ball7", balls_lst[7])
        LottoItem.add_value("ball8", balls_lst[8])
        LottoItem.add_value("ball9", balls_lst[9])
        LottoItem.add_value("ball10", balls_lst[10])
        LottoItem.add_value("ball11", balls_lst[11])
        LottoItem.add_value("ball12", balls_lst[12])
        LottoItem.add_value("ball13", balls_lst[13])
        LottoItem.add_value("ball14", balls_lst[14])
        LottoItem.add_value("ball15", balls_lst[15])
        LottoItem.add_value("ball16", balls_lst[16])
        LottoItem.add_value("ball17", balls_lst[17])
        LottoItem.add_value("ball18", balls_lst[18])
        LottoItem.add_value("ball19", balls_lst[19])
        draw_date = remove_unicode(response.xpath('//p[@class="lotteryDate"]/text()').get())
        draw_date = "".join([i for i in draw_date if i.isdigit() or i=='-'])
        sales = remove_unicode(response.xpath('//p[@class="saleAmount"]/text()').get())
        sales = "".join([i for i in sales if i.isdigit()])
        prize_pool = remove_unicode(response.xpath('//p[@class="choiceTen"]/text()').get())
        prize_pool = "".join([i for i in prize_pool if i.isdigit()])
        LottoItem.add_value("draw_datetime", draw_date)
        LottoItem.add_value("sales", sales)
        LottoItem.add_value("prize_pool", prize_pool)
        LottoItem.add_value("cat_1_prize", rows[0].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_4_prize", rows[3].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_5_prize", rows[4].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_6_prize", rows[5].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_7_prize", rows[6].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_5_winners", rows[4].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_6_winners", rows[5].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_7_winners", rows[6].xpath('./td/text()').getall()[1])
        yield LottoItem.load_item()


class ChinaSevenLotto(scrapy.Spider):

    name = "ChinaSevenLotto"

    def start_requests(self):
        self.name = "ChinaSevenLotto"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "http://www.cwl.gov.cn/ygkj/wqkjgg/qlc/"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        self.latest = response.xpath('//div[@class="table qlc"]//tbody/tr/td/a/@href').get()
        url = "http://www.cwl.gov.cn" + self.latest
        yield scrapy.Request(url=url, callback=self.parse_draw,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })


    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=ChinaSevenLottoItem(), selector=response)
        balls_lst = [i.strip() for i in response.xpath('//div[@class="lotteryNumContainer"]/div/text()').getall()]
        rows = response.xpath('//tbody/tr')[1:]

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("ball6", balls_lst[6])
        LottoItem.add_value("bonus_ball", balls_lst[7])
        draw_date = remove_unicode(response.xpath('//p[@class="lotteryDate"]/text()').get())
        draw_date = "".join([i for i in draw_date if i.isdigit() or i=='-'])
        sales = remove_unicode(response.xpath('//p[@class="saleAmount"]/text()').get())
        sales = "".join([i for i in sales if i.isdigit()])
        prize_pool = remove_unicode(response.xpath('//div[@class="nexAmount"]/text()').get())
        prize_pool = "".join([i for i in prize_pool if i.isdigit()])
        LottoItem.add_value("draw_datetime", draw_date)
        LottoItem.add_value("sales", sales)
        LottoItem.add_value("prize_pool", prize_pool)
        LottoItem.add_value("cat_1_prize", rows[0].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_4_prize", rows[3].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_5_prize", rows[4].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_6_prize", rows[5].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_7_prize", rows[6].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_5_winners", rows[4].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_6_winners", rows[5].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_7_winners", rows[6].xpath('./td/text()').getall()[1])
        yield LottoItem.load_item()


class ChinaTwoColor(scrapy.Spider):

    name = "ChinaTwoColor"

    def start_requests(self):
        self.name = "ChinaTwoColor"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "http://www.cwl.gov.cn/ygkj/wqkjgg/ssq/"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        self.latest = response.xpath('//div[@class="table ssq"]//tbody/tr/td/a/@href').get()
        url = "http://www.cwl.gov.cn" + self.latest
        yield scrapy.Request(url=url, callback=self.parse_draw,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=ChinaTwoColorItem(), selector=response)
        balls_lst = [i.strip() for i in response.xpath('//div[@class="lotteryNumContainer"]/div/text()').getall()]
        rows = response.xpath('//tbody/tr')[1:]

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("bonus_ball", balls_lst[6])
        draw_date = remove_unicode(response.xpath('//p[@class="lotteryDate"]/text()').get())
        draw_date = "".join([i for i in draw_date if i.isdigit() or i=='-'])
        sales = remove_unicode(response.xpath('//p[@class="saleAmount"]/text()').get())
        sales = "".join([i for i in sales if i.isdigit()])
        prize_pool = remove_unicode(response.xpath('//div[@class="nexAmount"]/text()').get())
        prize_pool = "".join([i for i in prize_pool if i.isdigit()])
        LottoItem.add_value("draw_datetime", draw_date)
        LottoItem.add_value("sales", sales)
        LottoItem.add_value("prize_pool", prize_pool)
        LottoItem.add_value("cat_1_prize", rows[0].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_4_prize", rows[3].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_5_prize", rows[4].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_6_prize", rows[5].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_5_winners", rows[4].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_6_winners", rows[5].xpath('./td/text()').getall()[1])
        yield LottoItem.load_item()


class ColombiaBaloto(scrapy.Spider):

    name = "ColombiaBaloto"

    # note: Will 'fail' at the beginning of the month until there is a draw in that month

    def start_requests(self):
        self.name = "ColombiaBaloto"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        # headers = {
        #     'Connection': 'keep-alive',
        #     'Accept': 'application/json, text/javascript, */*; q=0.01',
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
        #     'Content-Type': 'application/json',
        #     'Origin': 'https://www.baloto.com',
        #     'Sec-Fetch-Site': 'same-site',
        #     'Sec-Fetch-Mode': 'cors',
        #     'Sec-Fetch-Dest': 'empty',
        #     'Referer': 'https://www.baloto.com/',
        #     'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        # }
        # frmdata = {"type":"/GameResultByDate"}
        # input_date = datetime.strftime(datetime.now()-timedelta(days=1), "%Y/%m")
        #frmdata["parameters"] = {"gameDate":input_date}
        url = "https://www.baloto.com/resultados/"
        #url = "https://api-baloto-prod.baloto.com/petition"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})


    def parse(self, response):
        rows = response.xpath('//div[@class="table-responsive"]//tbody[@class="text-center"]')
        self.lottery_number = rows.xpath('.//tr//td//text()').get()
        self.jackpot = rows.xpath('.//tr//td//text()').getall()[4]
        url = f"https://www.baloto.com/resultados-baloto/{self.lottery_number}"
        yield scrapy.Request(url=url, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":10})


    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=ColombiaBalotoItem(), selector=response)
        rows = response.xpath('//div[@class="table-responsive"]//tbody')
        row = [x.replace('\n ', '').replace(' ', '') for x in rows.xpath('./tr//td/text()').getall() if x.strip()]
        balls_lst = response.xpath('//div[@class="text-center bg-baloto-balls p-3"]//div[@class="row"]//text()').getall()
        balls_lst = [x.replace('\n', '').replace(' ', '') for x in balls_lst if x.strip()]
        draw_date = response.xpath('//div[@class="text-center mt-5 mb-5 mobile-without-margin"]//div[@class="gotham-medium white-color"]//text()').get()
        locale.setlocale(locale.LC_TIME, "es_CO.ISO8859-1")
        clean = datetime.strptime(draw_date, "%d de %B de %Y")
        locale.setlocale(locale.LC_TIME, "en_GB.ISO8859-1")
        #latest = response.json()[-1] If api will be working

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("bonus_ball", balls_lst[5])
        LottoItem.add_value("draw_datetime", clean.strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", self.lottery_number)
        if int(row[0].replace('$', '')) == 0:
            LottoItem.add_value("cat_1_prize", self.jackpot)
            LottoItem.add_value("cat_1_winners", row[1])
        else:
            LottoItem.add_value("cat_1_prize", row[0])
            LottoItem.add_value("cat_1_winners", row[1])
        for count, i in enumerate(range(8,len(row), 3), 2):
            LottoItem.add_value(f'cat_{count}_prize', row[i])
        for count, i in enumerate(range(7, len(row), 3), 2):
            LottoItem.add_value(f'cat_{count}_winners', row[i])
        yield LottoItem.load_item()


class ColombiaRevancha(scrapy.Spider):

    name = "ColombiaRevancha"

    # note: Will 'fail' at the beginning of the month until there is a draw in that month
    # 'Revancha' is add-on to main game (Baloto) for 2nd prog. jackpot

    def start_requests(self):
        self.name = "ColombiaRevancha"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.baloto.com/resultados/"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        rows = response.xpath('//div[@class="table-responsive"]//tbody[@class="text-center"]')
        self.lottery_number = rows.xpath('.//tr//td//text()').get()
        self.jackpot = rows.xpath('.//tr//td//text()').getall()[13]
        url = f"https://www.baloto.com/resultados-revancha/{self.lottery_number}"
        yield scrapy.Request(url=url, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":10})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=ColombiaRevanchaItem(), selector=response)
        rows = response.xpath('//div[@class="table-responsive"]//tbody')
        row = [x.replace('\n ', '').replace(' ', '') for x in rows.xpath('./tr//td/text()').getall() if x.strip()]
        balls_lst = response.xpath('//div[@class="text-center bg-revancha-balls p-3"]//div[@class="row"]//text()').getall()
        balls_lst = [x.replace('\n', '').replace(' ', '') for x in balls_lst if x.strip()]
        draw_date = response.xpath('//div[@class="text-center mt-5 mb-5 mobile-without-margin"]//div[@class="gotham-medium white-color"]//text()').get()
        locale.setlocale(locale.LC_TIME, "es_CO.ISO8859-1")
        clean = datetime.strptime(draw_date, "%d de %B de %Y")
        locale.setlocale(locale.LC_TIME, "en_GB.ISO8859-1")
        #latest = response.json()[-1] If api will be working

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("bonus_ball", balls_lst[5])
        LottoItem.add_value("draw_datetime", clean.strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", self.lottery_number)
        if int(row[0].replace('$', '')) == 0:
            LottoItem.add_value("cat_1_prize", self.jackpot)
            LottoItem.add_value("cat_1_winners", row[1])
        else:
            LottoItem.add_value("cat_1_prize", row[0])
            LottoItem.add_value("cat_1_winners", row[1])
        for count, i in enumerate(range(8,len(row), 3), 2):
            LottoItem.add_value(f'cat_{count}_prize', row[i])
        for count, i in enumerate(range(7, len(row), 3), 2):
            LottoItem.add_value(f'cat_{count}_winners', row[i])
        yield LottoItem.load_item()


class CostaRicaLotto(scrapy.Spider):

    name = "CostaRicaLotto"

    def start_requests(self):
        self.name = "CostaRicaLotto"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = 'https://integration.jps.go.cr//api/App/lotto/last'
        headers = {
        'Accept': '*/*',
        'Referer': 'https://jps.go.cr/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
        'Authorization': 'Bearer null',
        }
        yield scrapy.Request(url=url, callback=self.parse, headers=headers, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=CostaRicaLottoItem(), selector=response)
        latest = response.json()

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", str(latest['numeros'][0]))
        LottoItem.add_value("ball1", str(latest['numeros'][1]))
        LottoItem.add_value("ball2", str(latest['numeros'][2]))
        LottoItem.add_value("ball3", str(latest['numeros'][3]))
        LottoItem.add_value("ball4", str(latest['numeros'][4]))
        LottoItem.add_value("draw_datetime", str(latest['fecha']).split('T')[0])
        LottoItem.add_value("draw_number", str(latest['numeroSorteo']))
        LottoItem.add_value("estimated_next_jackpot", str(latest['premiosLotto']['acumulado']))
        LottoItem.add_value("cat_1_prize", str(latest['premiosLotto']['cincoAciertos']))
        LottoItem.add_value("cat_2_prize", str(latest['premiosLotto']['cuatroAciertos']))
        LottoItem.add_value("cat_3_prize", str(latest['premiosLotto']['tresAciertos']))
        LottoItem.add_value("cat_4_prize", str(latest['premiosLotto']['dosAciertos']))
        yield LottoItem.load_item()


class CostaRicaRevancha(scrapy.Spider):

    name = "CostaRicaRevancha"

    # Add-on game to the main lotto for an extra 400c

    def start_requests(self):
        self.name = "CostaRicaRevancha"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = 'https://integration.jps.go.cr//api/App/lotto/last'
        headers = {
        'Accept': '*/*',
        'Referer': 'https://jps.go.cr/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
        'Authorization': 'Bearer null',
        }
        yield scrapy.Request(url=url, callback=self.parse, headers=headers, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=CostaRicaRevanchaItem(), selector=response)
        latest = response.json()

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", str(latest['numerosRevancha'][0]))
        LottoItem.add_value("ball1", str(latest['numerosRevancha'][1]))
        LottoItem.add_value("ball2", str(latest['numerosRevancha'][2]))
        LottoItem.add_value("ball3", str(latest['numerosRevancha'][3]))
        LottoItem.add_value("ball4", str(latest['numerosRevancha'][4]))
        LottoItem.add_value("draw_datetime", str(latest['fecha']).split('T')[0])
        LottoItem.add_value("draw_number", str(latest['numeroSorteo']))
        LottoItem.add_value("estimated_next_jackpot", str(latest['premiosLotto']['acumuladoRevancha']))
        LottoItem.add_value("cat_1_prize", str(latest['premiosLotto']['cincoAciertosRevancha']))
        LottoItem.add_value("cat_2_prize", str(latest['premiosLotto']['cuatroAciertosRevancha']))
        LottoItem.add_value("cat_3_prize", str(latest['premiosLotto']['tresAciertosRevancha']))
        LottoItem.add_value("cat_4_prize", str(latest['premiosLotto']['dosAciertosRevancha']))
        yield LottoItem.load_item()


class CroatiaLoto7(scrapy.Spider):

    name = "CroatiaLoto7"

    def start_requests(self):
        self.name = "CroatiaLoto7"
        self.req_proxy = get_UK_proxy()['http']
        url = "https://www.lutrija.hr/hl/loto-igra/loto-7"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        self.next_jackpot = response.xpath('//div[@class="jackpot-primary"]/span/text()').getall()[1]
        self.next_secondary_jackpot = response.xpath('//div[@class="jackpot-secondary"]/span/text()').get()
        guaranteed_check = response.xpath('//div[@class="jackpot-primary"]/span/text()').getall()[0].lower()
        if "jam" in guaranteed_check:
            self.guaranteed_jackpot = "TRUE"
        else:
            self.guaranteed_jackpot = "FALSE"
        url = "https://www.lutrija.hr/hl/rezultati/loto-7"
        yield scrapy.Request(url=url, callback=self.parse_draw,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=CroatiaLoto7Item(), selector=response)
        latest = response.xpath('//div[@class="results-body"]/div')[0]
        balls_lst = latest.xpath('.//ul/li/span/text()').getall()
        rows = latest.xpath('.//div[@class="result-details-table"]/div')[1:]

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("ball6", balls_lst[6])
        LottoItem.add_value("bonus_ball", balls_lst[7])
        draw_date = latest.xpath('.//span[@class="date-time"]/span/text()').get().split(',')[1].split('\n')[0].strip()
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d.%m.%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("sales", latest.xpath('.//div[@class="footer-info"]/div/span/text()').getall()[0])
        LottoItem.add_value("estimated_next_jackpot", self.next_jackpot)
        LottoItem.add_value("estimated_next_secondary_jackpot", self.next_secondary_jackpot)
        LottoItem.add_value("guaranteed_jackpot", self.guaranteed_jackpot)
        LottoItem.add_value("cat_1_prize", rows[0].xpath('.//span/text()').getall()[-1].lower().split('kn')[0])
        LottoItem.add_value("cat_2_prize", rows[1].xpath('.//span/text()').getall()[-1].lower().split('kn')[0])
        LottoItem.add_value("cat_3_prize", rows[2].xpath('.//span/text()').getall()[-1].lower().split('kn')[0])
        LottoItem.add_value("cat_4_prize", rows[3].xpath('.//span/text()').getall()[-1].lower().split('kn')[0])
        LottoItem.add_value("cat_5_prize", rows[4].xpath('.//span/text()').getall()[-1].lower().split('kn')[0])
        LottoItem.add_value("cat_6_prize", rows[5].xpath('.//span/text()').getall()[-1].lower().split('kn')[0])
        LottoItem.add_value("cat_7_prize", rows[6].xpath('.//span/text()').getall()[-1].lower().split('kn')[0])
        LottoItem.add_value("cat_8_prize", rows[7].xpath('.//span/text()').getall()[-1].lower().split('kn')[0])
        LottoItem.add_value("cat_9_prize", rows[8].xpath('.//span/text()').getall()[-1].lower().split('kn')[0])
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./div/text()').getall()[2])
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./div/text()').getall()[2])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./div/text()').getall()[2])
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./div/text()').getall()[2])
        LottoItem.add_value("cat_5_winners", rows[4].xpath('./div/text()').getall()[2])
        LottoItem.add_value("cat_6_winners", rows[5].xpath('./div/text()').getall()[2])
        LottoItem.add_value("cat_7_winners", rows[6].xpath('./div/text()').getall()[2])
        LottoItem.add_value("cat_8_winners", rows[7].xpath('./div/text()').getall()[2])
        LottoItem.add_value("cat_9_winners", rows[8].xpath('./div/text()').getall()[2])
        yield LottoItem.load_item()


class CroatiaLoto6(scrapy.Spider):

    name = "CroatiaLoto6"

    def start_requests(self):
        self.name = "CroatiaLoto6"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.lutrija.hr/hl/loto-igra/loto-6"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        self.next_jackpot = response.xpath('//div[@class="jackpot-primary"]/span/text()').getall()[1]
        self.next_secondary_jackpot = response.xpath('//div[@class="jackpot-secondary"]/span/text()').get()
        guaranteed_check = response.xpath('//div[@class="jackpot-primary"]/span/text()').getall()[0].lower()
        if "jam" in guaranteed_check:
            self.guaranteed_jackpot = "TRUE"
        else:
            self.guaranteed_jackpot = "FALSE"
        url = "https://www.lutrija.hr/hl/rezultati/loto-6"
        yield scrapy.Request(url=url, callback=self.parse_draw,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=CroatiaLoto6Item(), selector=response)
        latest = response.xpath('//div[@class="results-body"]/div')[0]
        balls_lst = latest.xpath('.//ul/li/span/text()').getall()
        rows = latest.xpath('.//div[@class="result-details-table"]/div')[1:]

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("bonus_ball", balls_lst[6])
        draw_date = latest.xpath('.//span[@class="date-time"]/span/text()').get().split(',')[1].split('\n')[0].strip()
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d.%m.%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("sales", latest.xpath('.//div[@class="footer-info"]/div/span/text()').getall()[0])
        LottoItem.add_value("estimated_next_jackpot", self.next_jackpot)
        LottoItem.add_value("estimated_next_secondary_jackpot", self.next_secondary_jackpot)
        LottoItem.add_value("guaranteed_jackpot", self.guaranteed_jackpot)
        LottoItem.add_value("cat_1_prize", rows[0].xpath('.//span/text()').getall()[-1].lower().split('kn')[0])
        LottoItem.add_value("cat_2_prize", rows[1].xpath('.//span/text()').getall()[-1].lower().split('kn')[0])
        LottoItem.add_value("cat_3_prize", rows[2].xpath('.//span/text()').getall()[-1].lower().split('kn')[0])
        LottoItem.add_value("cat_4_prize", rows[3].xpath('.//span/text()').getall()[-1].lower().split('kn')[0])
        LottoItem.add_value("cat_5_prize", rows[4].xpath('.//span/text()').getall()[-1].lower().split('kn')[0])
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./div/text()').getall()[2])
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./div/text()').getall()[2])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./div/text()').getall()[2])
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./div/text()').getall()[2])
        LottoItem.add_value("cat_5_winners", rows[4].xpath('./div/text()').getall()[2])
        yield LottoItem.load_item()


class CroatiaJoker(scrapy.Spider):

    name = "CroatiaJoker"

    def start_requests(self):
        self.name = "CroatiaJoker"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.lutrija.hr/hl/loto-igra/loto-7"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        self.next_jackpot = response.xpath('//div[@class="subGame-jackpot-amount"]//span/text()').getall()[-1]
        url = "https://www.lutrija.hr/hl/rezultati/joker"
        yield scrapy.Request(url=url, callback=self.parse_draw,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=CroatiaJokerItem(), selector=response)
        latest = response.xpath('//div[@class="results-body"]/div')[0]
        numbers_lst = latest.xpath('.//ul/li/span/text()').getall()
        rows = latest.xpath('.//div[@class="result-details-table"]/div')[1:]

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", numbers_lst[0])
        LottoItem.add_value("ball1", numbers_lst[1])
        LottoItem.add_value("ball2", numbers_lst[2])
        LottoItem.add_value("ball3", numbers_lst[3])
        LottoItem.add_value("ball4", numbers_lst[4])
        LottoItem.add_value("ball5", numbers_lst[5])
        draw_date = latest.xpath('.//span[@class="date-time"]/span/text()').get().split(',')[1].split('\n')[0].strip()
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d.%m.%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("sales", latest.xpath('.//div[@class="footer-info"]/div/span/text()').getall()[0])
        LottoItem.add_value("estimated_next_jackpot", self.next_jackpot)
        LottoItem.add_value("cat_1_prize", rows[0].xpath('.//span/text()').getall()[-1].lower().split('kn')[0])
        LottoItem.add_value("cat_2_prize", rows[1].xpath('.//span/text()').getall()[-1].lower().split('kn')[0])
        LottoItem.add_value("cat_3_prize", rows[2].xpath('.//span/text()').getall()[-1].lower().split('kn')[0])
        LottoItem.add_value("cat_4_prize", rows[3].xpath('.//span/text()').getall()[-1].lower().split('kn')[0])
        LottoItem.add_value("cat_5_prize", rows[4].xpath('.//span/text()').getall()[-1].lower().split('kn')[0])
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./div/text()').getall()[2])
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./div/text()').getall()[2])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./div/text()').getall()[2])
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./div/text()').getall()[2])
        LottoItem.add_value("cat_5_winners", rows[4].xpath('./div/text()').getall()[2])
        yield LottoItem.load_item()


class CzechiaSportka(scrapy.Spider):

    name = "CzechiaSportka"

    # Superjackpot is won by matching 6 and the "chance" number printed on the ticket (i.e. Joker-style 6 digit num)
    # i.e. must buy "full bet" to play for superjackpot: 220 CZK for 10 perms + "chance" number

    def start_requests(self):
        self.name = "CzechiaSportka"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = 'https://www.sazka.cz/loterie/sportka/sazky-a-vysledky'
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        LottoItem = ItemLoader(item=CzechiaSportkaItem(), selector=response)
        balls_lst = response.xpath('//div[@class="number-row mb-5"]/div[@class="numbers"]/div//text()').getall()
        winner_rows = response.xpath('//div[@id="tabPrizes"]/div')[0].xpath('.//div[@class="bs-row"]')[1:]
        jackpot_row = response.xpath('//div[@id="tabPrizes"]//div[@class="number-result-item"]')[0].xpath('.//div[@class="bs-row"]')[1]

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("draw1_ball0", balls_lst[0])
        LottoItem.add_value("draw1_ball1", balls_lst[1])
        LottoItem.add_value("draw1_ball2", balls_lst[2])
        LottoItem.add_value("draw1_ball3", balls_lst[3])
        LottoItem.add_value("draw1_ball4", balls_lst[4])
        LottoItem.add_value("draw1_ball5", balls_lst[5])
        LottoItem.add_value("draw1_bonus_ball", balls_lst[6])
        LottoItem.add_value("draw2_ball0", balls_lst[7])
        LottoItem.add_value("draw2_ball1", balls_lst[8])
        LottoItem.add_value("draw2_ball2", balls_lst[9])
        LottoItem.add_value("draw2_ball3", balls_lst[10])
        LottoItem.add_value("draw2_ball4", balls_lst[11])
        LottoItem.add_value("draw2_ball5", balls_lst[12])
        LottoItem.add_value("draw2_bonus_ball", balls_lst[13])
        draw_date = remove_unicode(response.xpath('//div[@class="c-12 col-sm date-wrapper"]//ul/li/a/text()').get().split(',')[0])
        LottoItem.add_value("draw_datetime", datetime.strptime(clean_datetime(draw_date), "%d.%m.%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("estimated_next_draw1_jackpot", jackpot_row.xpath('./div[@class="c"]')[1].xpath('./strong//text()').get())
        LottoItem.add_value("estimated_next_draw2_jackpot", jackpot_row.xpath('./div[@class="c"]')[2].xpath('./strong//text()').get())
        LottoItem.add_value("estimated_next_superjackpot", response.xpath('//h1[@class="prize"]/strong//text()').get())
        # prize values will be '0' unless won
        for i in range(1,7):
            prize_value = winner_rows[i-1].xpath('./div[@class="c"]')[1].xpath('./strong/text()').get()
            try:
                check_length = len(prize_value)
            except TypeError: # if no winners prize_value will be NoneType so raises error
                prize_value = '0'
            LottoItem.add_value(f"draw1_cat_{i}_prize", prize_value)
        for i in range(1,7):
            prize_value = winner_rows[i-1].xpath('./div[@class="c"]')[2].xpath('./strong/text()').get()
            try:
                check_length = len(prize_value)
            except TypeError: # if no winners prize_value will be NoneType so raises error
                prize_value = '0'
            LottoItem.add_value(f"draw2_cat_{i}_prize", prize_value)

        LottoItem.add_value("draw1_cat_1_winners", winner_rows[0].xpath('./div[@class="c"]')[1].xpath('.//text()').getall()[-1])
        LottoItem.add_value("draw1_cat_2_winners", winner_rows[1].xpath('./div[@class="c"]')[1].xpath('.//text()').getall()[-1])
        LottoItem.add_value("draw1_cat_3_winners", winner_rows[2].xpath('./div[@class="c"]')[1].xpath('.//text()').getall()[-1])
        LottoItem.add_value("draw1_cat_4_winners", winner_rows[3].xpath('./div[@class="c"]')[1].xpath('.//text()').getall()[-1])
        LottoItem.add_value("draw1_cat_5_winners", winner_rows[4].xpath('./div[@class="c"]')[1].xpath('.//text()').getall()[-1])
        LottoItem.add_value("draw1_cat_6_winners", winner_rows[5].xpath('./div[@class="c"]')[1].xpath('.//text()').getall()[-1])
        LottoItem.add_value("draw2_cat_1_winners", winner_rows[0].xpath('./div[@class="c"]')[2].xpath('.//text()').getall()[-1])
        LottoItem.add_value("draw2_cat_2_winners", winner_rows[1].xpath('./div[@class="c"]')[2].xpath('.//text()').getall()[-1])
        LottoItem.add_value("draw2_cat_3_winners", winner_rows[2].xpath('./div[@class="c"]')[2].xpath('.//text()').getall()[-1])
        LottoItem.add_value("draw2_cat_4_winners", winner_rows[3].xpath('./div[@class="c"]')[2].xpath('.//text()').getall()[-1])
        LottoItem.add_value("draw2_cat_5_winners", winner_rows[4].xpath('./div[@class="c"]')[2].xpath('.//text()').getall()[-1])
        LottoItem.add_value("draw2_cat_6_winners", winner_rows[5].xpath('./div[@class="c"]')[2].xpath('.//text()').getall()[-1])
        yield LottoItem.load_item()


class DenmarkLotto(scrapy.Spider):

    name = "DenmarkLotto"

    def start_requests(self):
        self.name = "DenmarkLotto"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = 'https://danskelotto.com/en/lotto/past-results'
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        next_page = response.xpath("//div[@class='mainResult']//div/a/@href").get()
        url = urljoin(response.url, next_page)
        yield scrapy.Request(url, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":10})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=DenmarkLottoItem(), selector=response)
        balls_lst = response.xpath('//ul[@class="balls"]/li/text()').getall()
        rows = response.xpath('//table/tbody/tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("ball6", balls_lst[6])
        LottoItem.add_value("bonus_ball", balls_lst[7])
        date_str = response.url.split('/')[-1]
        LottoItem.add_value("draw_datetime", datetime.strptime(date_str, "%d-%B-%Y").strftime("%Y-%m-%d"))
        for j in range(5):
            row_values = [i.strip() for i in rows[j].xpath('./td/text()').getall() if len(i.strip())>0]
            LottoItem.add_value(f"cat_{j+1}_prize", row_values[0].split('kr.')[1])
            LottoItem.add_value(f"cat_{j+1}_winners", row_values[1])
        yield LottoItem.load_item()


class DominicaSuper6(scrapy.Spider):

    name = "DominicaSuper6"

    # NO NUM OF WINNERS DATA
    # Played in Grenada, St. Vincent and the Grenadines, Dominica & St. Lucia

    def start_requests(self):
        self.name = "DominicaSuper6"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "http://domlottery.com/dnl/super6.php"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=DominicaSuper6Item(), selector=response)
        balls_lst = response.xpath('//div[@class="game_results"]/ul/li/text()').getall()

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        draw_date = response.xpath('//div[@class="tdraw"]/div[@class="header"]/text()').get().strip().split(' ')[-1]
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d-%b-%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("estimated_next_jackpot", response.xpath(
            '//div[@class="next_prize"]/div[@class="desc"]/text()').get().strip())
        yield LottoItem.load_item()


class DominicaPowerball(scrapy.Spider):

    name = "DominicaPowerball"

    # NO NUM OF WINNERS DATA

    def start_requests(self):
        self.name = "DominicaPowerball"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "http://domlottery.com/dnl/powerball.php"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=DominicaPowerballItem(), selector=response)
        balls_lst = response.xpath('//div[@class="game_results"]/ul/li/text()').getall()

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("bonus_ball", balls_lst[4])
        draw_date = response.xpath('//div[@class="tdraw"]/div[@class="header"]/text()').get().strip().split(' ')[-1]
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d-%b-%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("estimated_next_jackpot", response.xpath(
            '//div[@class="next_prize"]/div[@class="desc"]/text()').get().strip())
        yield LottoItem.load_item()


class DominicanLoto(scrapy.Spider):

    name = "DominicanLoto"

    # NO NUM OF WINNERS DATA
    # Unclear prize structure/game rules
    # Is loto=match_6, lotomas=match_6_bonus_1 and supermas=match_6_bonus_2 ??

    def start_requests(self):
        self.name = "DominicanLoto"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://leidsa.com/"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=DominicanLotoItem(), selector=response)
        balls_lst = response.xpath('//div[@class="form-group numeros-ganadores-pc"]//span/text()').getall()
        jackpot_rows = response.xpath('//div[@class="panel-body panel-body-millones-acumulados"]/div')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        draw_date = response.xpath('//p[@class="resultados-del-dia"]/text()').get().split('tados del')[1].strip()
        locale.setlocale(locale.LC_TIME, "es_DO.ISO8859-1")
        clean = datetime.strptime(draw_date, "%d de %B del %Y")
        locale.setlocale(locale.LC_TIME, "en_GB.ISO8859-1")
        LottoItem.add_value("draw_datetime", clean.strftime("%Y-%m-%d"))
        LottoItem.add_value("jackpot", " ".join(jackpot_rows[0].xpath('./p/text()').getall()))
        yield LottoItem.load_item()


class DominicanLotomas(scrapy.Spider):

    name = "DominicanLotomas"

    # Add-on game to main Loto
    # NO NUM OF WINNERS DATA
    # Unclear prize structure/game rules
    # Is loto=match_6, lotomas=match_6_bonus_1 and supermas=match_6_bonus_2 ??

    def start_requests(self):
        self.name = "DominicanLotomas"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://leidsa.com/"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=DominicanLotomasItem(), selector=response)
        balls_lst = response.xpath('//div[@class="form-group numeros-ganadores-pc"]//span/text()').getall()
        jackpot_rows = response.xpath('//div[@class="panel-body panel-body-millones-acumulados"]/div')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("bonus_ball", balls_lst[6])
        draw_date = response.xpath('//p[@class="resultados-del-dia"]/text()').get().split('tados del')[1].strip()
        locale.setlocale(locale.LC_TIME, "es_DO.ISO8859-1")
        clean = datetime.strptime(draw_date, "%d de %B del %Y")
        locale.setlocale(locale.LC_TIME, "en_GB.ISO8859-1")
        LottoItem.add_value("draw_datetime", clean.strftime("%Y-%m-%d"))
        LottoItem.add_value("jackpot", " ".join(jackpot_rows[2].xpath('./p/text()').getall()))
        yield LottoItem.load_item()


class DominicanSuperomas(scrapy.Spider):

    name = "DominicanSuperomas"

    # Add-on game to Loto+Lotomas
    # NO NUM OF WINNERS DATA
    # Unclear prize structure/game rules
    # Is loto=match_6, lotomas=match_6_bonus_1 and supermas=match_6_bonus_2 ??

    def start_requests(self):
        self.name = "DominicanSuperomas"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://leidsa.com/"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=DominicanSuperomasItem(), selector=response)
        balls_lst = response.xpath('//div[@class="form-group numeros-ganadores-pc"]//span/text()').getall()
        jackpot_rows = response.xpath('//div[@class="panel-body panel-body-millones-acumulados"]/div')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("bonus_ball0", balls_lst[6])
        LottoItem.add_value("bonus_ball1", balls_lst[7])
        draw_date = response.xpath('//p[@class="resultados-del-dia"]/text()').get().split('tados del')[1].strip()
        locale.setlocale(locale.LC_TIME, "es_DO.ISO8859-1")
        clean = datetime.strptime(draw_date, "%d de %B del %Y")
        locale.setlocale(locale.LC_TIME, "en_GB.ISO8859-1")
        LottoItem.add_value("draw_datetime", clean.strftime("%Y-%m-%d"))
        LottoItem.add_value("jackpot", " ".join(jackpot_rows[-1].xpath('./p/text()').getall()))
        yield LottoItem.load_item()


class EuroJackpot(scrapy.Spider):

    name = "EuroJackpot"

    def start_requests(self):
        self.name = "EuroJackpot"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        #url = "https://www.eurojackpot.org/en/results/"
        url = "https://www.lotto-hessen.de/eurojackpot/gewinnzahlen-quoten/gewinnzahlen?gbn=5"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        self.balls_lst = response.xpath('//div[@class="drawing-wrapper"]/ul/li/span/text()').getall()
        self.draw_date = response.xpath('//div[@class="form-row date"]//select/option/text()').get().split(',')[1].strip()
        url = "https://www.lotto-hessen.de/eurojackpot/gewinnzahlen-quoten/quoten?gbn=5"
        yield scrapy.Request(url=url, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":10})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=EuroJackpotItem(), selector=response)
        rows = response.xpath('//div[@class="quoten-wrapper"]//tbody/tr')
        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", self.balls_lst[0])
        LottoItem.add_value("ball1", self.balls_lst[1])
        LottoItem.add_value("ball2", self.balls_lst[2])
        LottoItem.add_value("ball3", self.balls_lst[3])
        LottoItem.add_value("ball4", self.balls_lst[4])
        LottoItem.add_value("bonus_ball0", self.balls_lst[5])
        LottoItem.add_value("bonus_ball1", self.balls_lst[6])
        LottoItem.add_value("draw_datetime", datetime.strptime(self.draw_date, "%d.%m.%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("estimated_next_jackpot", " ".join(response.xpath('//div[@class="ticket-header-group"]//strong/span/text()').getall()))
        sales = "".join(response.xpath('//div[@class="mm"]//div[@class="quoten-head"]/p/strong/text()').get()).encode('utf-8').decode('utf-8')
        hessen_sales = "".join(response.xpath('//div[@class="mm"]//div[@class="quoten-head"]')[0].xpath('./p/text()').getall()).encode('utf-8').decode('utf-8')
        LottoItem.add_value("sales", sales)
        LottoItem.add_value("hessen_sales", hessen_sales)
        LottoItem.add_value("cat_1_prize", "".join(rows[0].xpath('./td')[-1].xpath('./text()').getall()))
        LottoItem.add_value("cat_2_prize", "".join(rows[1].xpath('./td')[-1].xpath('./text()').getall()))
        LottoItem.add_value("cat_3_prize", "".join(rows[2].xpath('./td')[-1].xpath('./text()').getall()))
        LottoItem.add_value("cat_4_prize", "".join(rows[3].xpath('./td')[-1].xpath('./text()').getall()))
        LottoItem.add_value("cat_5_prize", "".join(rows[4].xpath('./td')[-1].xpath('./text()').getall()))
        LottoItem.add_value("cat_6_prize", "".join(rows[5].xpath('./td')[-1].xpath('./text()').getall()))
        LottoItem.add_value("cat_7_prize", "".join(rows[6].xpath('./td')[-1].xpath('./text()').getall()))
        LottoItem.add_value("cat_8_prize", "".join(rows[7].xpath('./td')[-1].xpath('./text()').getall()))
        LottoItem.add_value("cat_9_prize", "".join(rows[8].xpath('./td')[-1].xpath('./text()').getall()))
        LottoItem.add_value("cat_10_prize", "".join(rows[9].xpath('./td')[-1].xpath('./text()').getall()))
        LottoItem.add_value("cat_11_prize", "".join(rows[10].xpath('./td')[-1].xpath('./text()').getall()))
        LottoItem.add_value("cat_12_prize", "".join(rows[11].xpath('./td')[-1].xpath('./text()').getall()))
        LottoItem.add_value("cat_1_winners", "".join(rows[0].xpath('./td')[2].xpath('./text()').getall()))
        LottoItem.add_value("cat_2_winners", "".join(rows[1].xpath('./td')[2].xpath('./text()').getall()))
        LottoItem.add_value("cat_3_winners", "".join(rows[2].xpath('./td')[2].xpath('./text()').getall()))
        LottoItem.add_value("cat_4_winners", "".join(rows[3].xpath('./td')[2].xpath('./text()').getall()))
        LottoItem.add_value("cat_5_winners", "".join(rows[4].xpath('./td')[2].xpath('./text()').getall()))
        LottoItem.add_value("cat_6_winners", "".join(rows[5].xpath('./td')[2].xpath('./text()').getall()))
        LottoItem.add_value("cat_7_winners", "".join(rows[6].xpath('./td')[2].xpath('./text()').getall()))
        LottoItem.add_value("cat_8_winners", "".join(rows[7].xpath('./td')[2].xpath('./text()').getall()))
        LottoItem.add_value("cat_9_winners", "".join(rows[8].xpath('./td')[2].xpath('./text()').getall()))
        LottoItem.add_value("cat_10_winners", "".join(rows[9].xpath('./td')[2].xpath('./text()').getall()))
        LottoItem.add_value("cat_11_winners", "".join(rows[10].xpath('./td')[2].xpath('./text()').getall()))
        LottoItem.add_value("cat_12_winners", "".join(rows[11].xpath('./td')[2].xpath('./text()').getall()))
        LottoItem.add_value("cat_1_hessen_winners", "".join(rows[0].xpath('./td')[3].xpath('./text()').getall()))
        LottoItem.add_value("cat_2_hessen_winners", "".join(rows[1].xpath('./td')[3].xpath('./text()').getall()))
        LottoItem.add_value("cat_3_hessen_winners", "".join(rows[2].xpath('./td')[3].xpath('./text()').getall()))
        LottoItem.add_value("cat_4_hessen_winners", "".join(rows[3].xpath('./td')[3].xpath('./text()').getall()))
        LottoItem.add_value("cat_5_hessen_winners", "".join(rows[4].xpath('./td')[3].xpath('./text()').getall()))
        LottoItem.add_value("cat_6_hessen_winners", "".join(rows[5].xpath('./td')[3].xpath('./text()').getall()))
        LottoItem.add_value("cat_7_hessen_winners", "".join(rows[6].xpath('./td')[3].xpath('./text()').getall()))
        LottoItem.add_value("cat_8_hessen_winners", "".join(rows[7].xpath('./td')[3].xpath('./text()').getall()))
        LottoItem.add_value("cat_9_hessen_winners", "".join(rows[8].xpath('./td')[3].xpath('./text()').getall()))
        LottoItem.add_value("cat_10_hessen_winners", "".join(rows[9].xpath('./td')[3].xpath('./text()').getall()))
        LottoItem.add_value("cat_11_hessen_winners", "".join(rows[10].xpath('./td')[3].xpath('./text()').getall()))
        LottoItem.add_value("cat_12_hessen_winners", "".join(rows[11].xpath('./td')[3].xpath('./text()').getall()))
        yield LottoItem.load_item()


class EuroMillions(scrapy.Spider):

    name = "EuroMillions"

    def start_requests(self):
        self.name = "EuroMillions"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        #url = "https://www.fdj.fr/jeux-de-tirage/euromillions-my-million#/"
        #headers = {
        #    'Connection': 'keep-alive',
        #    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        #    'sec-ch-ua-mobile': '?0',
        #    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        #    'sec-ch-ua-platform': '"Windows"',
        #    'Content-Type': 'application/json',
        #    'Accept': '*/*',
        #    'Sec-Fetch-Site': 'same-origin',
        #    'Sec-Fetch-Mode': 'cors',
        #    'Sec-Fetch-Dest': 'empty',
        #    'Referer': 'https://www.fdj.fr/jeux-de-tirage/euromillions-my-million',
        #    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        #}
        #url = 'https://www.fdj.fr/api/service-draws/v1/games/euromillions/announces'
        #yield scrapy.Request(url, headers=headers, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":15})

    #def parse(self, response):
        #latest = response.json()[-1]
        #self.next_jackpot = str(latest['amount']/100.0)
        #self.check_guaranteed = str(latest['amount_guarantee'])
        """
        FDJ is blocking all the UK/US proxies, so just skip estimated_next_jackpot scrape
        """
        url = "https://www.euro-millions.com/results"
        yield scrapy.Request(url=url, callback=self.parse_jackpot, meta={"proxy": self.req_proxy, "download_timeout":15})

    def parse_jackpot(self, response):
        ball_drawn = response.xpath("//tbody/tr/td/ul/li/text()").get()
        if "-" in ball_drawn:
            next_page = response.xpath("//tbody/tr/td/a/@href").getall()[1]
        else:
            next_page = response.xpath("//tbody/tr/td/a/@href").get()
        url = urljoin(response.url, next_page)
        yield scrapy.Request(url, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":10})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=EuroMillionsItem(), selector=response)
        balls_lst = response.xpath('//div[@id="ballsAscending"]/ul/li/text()').getall()
        rows = response.xpath('//div[@id="PrizeIE"]//tbody/tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("bonus_ball0", balls_lst[5])
        LottoItem.add_value("bonus_ball1", balls_lst[6])
        LottoItem.add_value("draw_datetime", datetime.strptime(response.url.split('/')[-1].strip(), "%d-%m-%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("tickets", response.xpath('//div[@class="box entries"]/div[@class="big"]/text()').get())
        #LottoItem.add_value("estimated_next_jackpot", self.next_jackpot)
        LottoItem.add_value("cat_1_prize", [i for i in rows[0].xpath('./td/text()').getall() if len(i.strip())>0][1])
        LottoItem.add_value("cat_2_prize", [i for i in rows[1].xpath('./td/text()').getall() if len(i.strip())>0][1])
        LottoItem.add_value("cat_3_prize", [i for i in rows[2].xpath('./td/text()').getall() if len(i.strip())>0][1])
        LottoItem.add_value("cat_4_prize", [i for i in rows[3].xpath('./td/text()').getall() if len(i.strip())>0][1])
        LottoItem.add_value("cat_5_prize", [i for i in rows[4].xpath('./td/text()').getall() if len(i.strip())>0][1])
        LottoItem.add_value("cat_6_prize", [i for i in rows[5].xpath('./td/text()').getall() if len(i.strip())>0][1])
        LottoItem.add_value("cat_7_prize", [i for i in rows[6].xpath('./td/text()').getall() if len(i.strip())>0][1])
        LottoItem.add_value("cat_8_prize", [i for i in rows[7].xpath('./td/text()').getall() if len(i.strip())>0][1])
        LottoItem.add_value("cat_9_prize", [i for i in rows[8].xpath('./td/text()').getall() if len(i.strip())>0][1])
        LottoItem.add_value("cat_10_prize", [i for i in rows[9].xpath('./td/text()').getall() if len(i.strip())>0][1])
        LottoItem.add_value("cat_11_prize", [i for i in rows[10].xpath('./td/text()').getall() if len(i.strip())>0][1])
        LottoItem.add_value("cat_12_prize", [i for i in rows[11].xpath('./td/text()').getall() if len(i.strip())>0][1])
        LottoItem.add_value("cat_13_prize", [i for i in rows[12].xpath('./td/text()').getall() if len(i.strip())>0][1])
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_5_winners", rows[4].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_6_winners", rows[5].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_7_winners", rows[6].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_8_winners", rows[7].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_9_winners", rows[8].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_10_winners", rows[9].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_11_winners", rows[10].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_12_winners", rows[11].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_13_winners", rows[12].xpath('./td/text()').getall()[-1])
        try:
            rolldown_check = rows[0].xpath('./td/strong/text()').getall()[-1].lower()
            if "rolldown" in rolldown_check:
                LottoItem.add_value("rolldown", "yes")
            else:
                LottoItem.add_value("rolldown", "no")
        except:
            LottoItem.add_value("rolldown", "no")
        #if "false" in self.check_guaranteed.lower():
        #    LottoItem.add_value("special_draw", "FALSE")
        #else:
        #    LottoItem.add_value("special_draw", "TRUE")
        yield LottoItem.load_item()


class EuroMillionsAll(scrapy.Spider):

    name = "EuroMillionsAll"

    def start_requests(self):
        self.name = "EuroMillionsAll"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        headers = {
            'authority': 'www.euro-millions.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'cache-control': 'max-age=0',
            'dnt': '1',
            'if-modified-since': 'Tue,03 May 2022 21:45:51 GMT',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
        }
        url = "https://www.euro-millions.com/results"
        yield scrapy.Request(url, headers=headers, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":15})

    def parse(self, response):
        ball_drawn = response.xpath("//tbody/tr/td/ul/li/text()").get()
        if "-" in ball_drawn:
            next_page = response.xpath("//tbody/tr/td/a/@href").getall()[1]
        else:
            next_page = response.xpath("//tbody/tr/td/a/@href").get()
        url = urljoin(response.url, next_page)
        yield scrapy.Request(url=url, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":15})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=EuroMillionsAllItem(), selector=response)
        balls_lst = response.xpath('//div[@id="ballsAscending"]/ul/li/text()').getall()

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("bonus_ball0", balls_lst[5])
        LottoItem.add_value("bonus_ball1", balls_lst[6])
        LottoItem.add_value("draw_datetime", datetime.strptime(response.url.split('/')[-1].strip(), "%d-%m-%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("tickets", response.xpath('//div[@class="box entries"]/div[@class="big"]/text()').get())

        for country_code in ['GB','FR','ES','IE','PT','CH','BE','AT','LU']:
            if country_code == "IE":
                try:
                    rolldown_check = rows[0].xpath('./td/strong/text()').getall()[-1].lower()
                    if "rolldown" in rolldown_check:
                        LottoItem.add_value("rolldown", "yes")
                    else:
                        LottoItem.add_value("rolldown", "no")
                except:
                    LottoItem.add_value("rolldown", "no")

            rows = response.xpath(f'//div[@id="Prize{country_code}"]')[0].xpath('.//tbody/tr')
            for row_num in range(1, len(rows)): # last row is a footer
                LottoItem.add_value(f"{country_code}_cat_{row_num}_prize", [i for i in rows[row_num-1].xpath('./td/text()').getall() if len(i.strip())>0][1])
                LottoItem.add_value(f"{country_code}_cat_{row_num}_winners", [i for i in rows[row_num-1].xpath('./td/text()').getall() if len(i.strip())>0][2])

        yield LottoItem.load_item()


class FinlandLotto(scrapy.Spider):

    name = "FinlandLotto"

    def start_requests(self):
        self.name = "FinlandLotto"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        self.year = datetime.strftime(datetime.now(), "%Y")
        self.week_num = datetime.strftime(datetime.now(), "%V")
        self.last_week_num = datetime.strftime(datetime.now()-timedelta(days=7), "%V")
        self.last_year_num = datetime.strftime(datetime.now()-timedelta(days=7), "%Y")
        url = 'https://www.veikkaus.fi/api/draw-results/v1/games/LOTTO/draws/by-week/'+str(self.year)+'-W'+str(self.week_num)
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        try:
            latest = response.json()[0]
            LottoItem = ItemLoader(item=FinlandLottoItem(), selector=response)

            LottoItem.add_value("name", self.name)
            LottoItem.add_value("ball0", str(latest['results'][0]['primary'][0]))
            LottoItem.add_value("ball1", str(latest['results'][0]['primary'][1]))
            LottoItem.add_value("ball2", str(latest['results'][0]['primary'][2]))
            LottoItem.add_value("ball3", str(latest['results'][0]['primary'][3]))
            LottoItem.add_value("ball4", str(latest['results'][0]['primary'][4]))
            LottoItem.add_value("ball5", str(latest['results'][0]['primary'][5]))
            LottoItem.add_value("ball6", str(latest['results'][0]['primary'][6]))
            LottoItem.add_value("bonus_ball", str(latest['results'][0]['secondary'][0]))
            LottoItem.add_value("draw_datetime", str(latest['drawTime']))
            LottoItem.add_value("draw_number", str(latest['id']))
            if int(latest['prizeTiers'][0]['shareCount']) == 0:
                LottoItem.add_value("cat_1_prize", str(latest['jackpots'][0]['amount']/100.0))
            else:
                LottoItem.add_value("cat_1_prize", str(latest['prizeTiers'][0]['shareAmount']/100.0))
            LottoItem.add_value("cat_2_prize", str(latest['prizeTiers'][1]['shareAmount']/100.0))
            LottoItem.add_value("cat_3_prize", str(latest['prizeTiers'][2]['shareAmount']/100.0))
            LottoItem.add_value("cat_4_prize", str(latest['prizeTiers'][3]['shareAmount']/100.0))
            LottoItem.add_value("cat_5_prize", str(latest['prizeTiers'][4]['shareAmount']/100.0))
            LottoItem.add_value("cat_6_prize", str(latest['prizeTiers'][5]['shareAmount']/100.0))
            LottoItem.add_value("cat_1_winners", str(latest['prizeTiers'][0]['shareCount']))
            LottoItem.add_value("cat_2_winners", str(latest['prizeTiers'][1]['shareCount']))
            LottoItem.add_value("cat_3_winners", str(latest['prizeTiers'][2]['shareCount']))
            LottoItem.add_value("cat_4_winners", str(latest['prizeTiers'][3]['shareCount']))
            LottoItem.add_value("cat_5_winners", str(latest['prizeTiers'][4]['shareCount']))
            LottoItem.add_value("cat_6_winners", str(latest['prizeTiers'][5]['shareCount']))
            yield LottoItem.load_item()
        except:
            url = 'https://www.veikkaus.fi/api/draw-results/v1/games/LOTTO/draws/by-week/'+str(self.last_year_num)+'-W'+str(self.last_week_num)
            yield scrapy.Request(url=url, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":10})

    async def parse_draw(self, response):
        latest = response.json()[0]
        LottoItem = ItemLoader(item=FinlandLottoItem(), selector=response)

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", str(latest['results'][0]['primary'][0]))
        LottoItem.add_value("ball1", str(latest['results'][0]['primary'][1]))
        LottoItem.add_value("ball2", str(latest['results'][0]['primary'][2]))
        LottoItem.add_value("ball3", str(latest['results'][0]['primary'][3]))
        LottoItem.add_value("ball4", str(latest['results'][0]['primary'][4]))
        LottoItem.add_value("ball5", str(latest['results'][0]['primary'][5]))
        LottoItem.add_value("ball6", str(latest['results'][0]['primary'][6]))
        LottoItem.add_value("bonus_ball", str(latest['results'][0]['secondary'][0]))
        LottoItem.add_value("draw_datetime", str(latest['drawTime']))
        LottoItem.add_value("draw_number", str(latest['id']))
        if int(latest['prizeTiers'][0]['shareCount']) == 0:
            LottoItem.add_value("cat_1_prize", str(latest['jackpots'][0]['amount']/100.0))
        else:
            LottoItem.add_value("cat_1_prize", str(latest['prizeTiers'][0]['shareAmount']/100.0))
        LottoItem.add_value("cat_1_prize", str(latest['prizeTiers'][0]['shareAmount']/100.0))
        LottoItem.add_value("cat_2_prize", str(latest['prizeTiers'][1]['shareAmount']/100.0))
        LottoItem.add_value("cat_3_prize", str(latest['prizeTiers'][2]['shareAmount']/100.0))
        LottoItem.add_value("cat_4_prize", str(latest['prizeTiers'][3]['shareAmount']/100.0))
        LottoItem.add_value("cat_5_prize", str(latest['prizeTiers'][4]['shareAmount']/100.0))
        LottoItem.add_value("cat_6_prize", str(latest['prizeTiers'][5]['shareAmount']/100.0))
        LottoItem.add_value("cat_1_winners", str(latest['prizeTiers'][0]['shareCount']))
        LottoItem.add_value("cat_2_winners", str(latest['prizeTiers'][1]['shareCount']))
        LottoItem.add_value("cat_3_winners", str(latest['prizeTiers'][2]['shareCount']))
        LottoItem.add_value("cat_4_winners", str(latest['prizeTiers'][3]['shareCount']))
        LottoItem.add_value("cat_5_winners", str(latest['prizeTiers'][4]['shareCount']))
        LottoItem.add_value("cat_6_winners", str(latest['prizeTiers'][5]['shareCount']))
        yield LottoItem.load_item()


class FranceLotto(scrapy.Spider):

    name = "FranceLotto"

    def start_requests(self):
        self.name = "FranceLotto"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.lotto.net/french-loto/results"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        self.next_jackpot = response.xpath('//div[@class="jackpot"]//span/text()').getall()[1].strip()
        self.draw_date = response.xpath('//div[@class="date"]/span/text()').get().strip()
        next_page = response.xpath("//div[@class='results-big']/div[@class='row-3']/a/@href").get()
        url = urljoin(response.url, next_page)
        yield scrapy.Request(url, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":10})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=FranceLottoItem(), selector=response)
        balls_lst = response.xpath('//ul[@class="balls"]/li/span/text()').getall()
        rows = response.xpath('//table//tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("bonus_ball", balls_lst[5])
        LottoItem.add_value("draw_datetime", datetime.strptime(self.draw_date, "%d %B %Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("estimated_next_jackpot", self.next_jackpot)
        LottoItem.add_value("cat_1_prize", rows[1].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_2_prize", rows[2].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_3_prize", rows[3].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_4_prize", rows[4].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_5_prize", rows[5].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_6_prize", rows[6].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_7_prize", rows[7].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_8_prize", rows[8].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_9_prize", rows[9].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_1_winners", rows[1].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_2_winners", rows[2].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_3_winners", rows[3].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_4_winners", rows[4].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_5_winners", rows[5].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_6_winners", rows[6].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_7_winners", rows[7].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_8_winners", rows[8].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_9_winners", rows[9].xpath('./td/text()').getall()[-1].strip())
        try:
            rolldown_check = rows[1].xpath('./td[@align="right"]/span/text()').getall()[-1].lower()
            if "rolldown" in rolldown_check:
                LottoItem.add_value("rolldown", "yes")
            else:
                LottoItem.add_value("rolldown", "no")
        except:
            LottoItem.add_value("rolldown", "no")
        yield LottoItem.load_item()


class GeorgiaLotto6x42(scrapy.Spider):

    name = "GeorgiaLotto6x42"

    def start_requests(self):
        self.name = "GeorgiaLotto6x42"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = 'https://lotto.ge/games/lotto-6-42/results'
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        LottoItem = ItemLoader(item=GeorgiaLotto6x42Item(), selector=response)
        balls_lst = response.xpath('//div[@class="balls"]/span//text()').getall()
        rows = response.xpath('//div[@class="col-12"]//tbody/tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("bonus_ball", balls_lst[6])
        LottoItem.add_value("draw_datetime", response.xpath('//form[@class="mb-4"]//input/@value').get())
        LottoItem.add_value("draw_number", response.xpath('//form[@class="mb-4"]//select/option/@value').get())
        if prize_to_num(rows[0].xpath('./td/span//text()').get().strip()) == 0:
            LottoItem.add_value("cat_1_prize", rows[0].xpath('./td/div/text()').getall()[-2])
        else:
            LottoItem.add_value("cat_1_prize", rows[0].xpath('./td/span//text()').getall()[-1])
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./td/span//text()').getall()[-1])
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./td/span//text()').getall()[-1])
        LottoItem.add_value("cat_4_prize", rows[3].xpath('./td/span//text()').getall()[-1])
        LottoItem.add_value("cat_5_prize", rows[4].xpath('./td/span//text()').getall()[-1])
        LottoItem.add_value("cat_6_prize", rows[5].xpath('./td/span//text()').getall()[-1])
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td/span//text()').get())
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./td/span//text()').get())
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./td/span//text()').get())
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./td/span//text()').get())
        LottoItem.add_value("cat_5_winners", rows[4].xpath('./td/span//text()').get())
        LottoItem.add_value("cat_6_winners", rows[5].xpath('./td/span//text()').get())
        yield LottoItem.load_item()


class GeorgiaLotto5x35(scrapy.Spider):

    name = "GeorgiaLotto5x35"

    def start_requests(self):
        self.name = "GeorgiaLotto5x35"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = 'https://lotto.ge/games/golden-ball/results'
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        LottoItem = ItemLoader(item=GeorgiaLotto5x35Item(), selector=response)
        balls_lst = response.xpath('//div[@class="balls"]/span//text()').getall()
        try:
            golden_ball = response.xpath('//div[@class="balls"]/span[@class="ball extra variant-gb"]').getall()[0]
            # Checks whether golden ball image is present; otherwise fails and hence wasn't drawn
            golden_ball = "yes"
        except:
            golden_ball = "no"
        rows = response.xpath('//div[@class="col-12"]//tbody/tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("golden_ball", golden_ball)
        LottoItem.add_value("draw_datetime", response.xpath('//form[@class="mb-4"]//input/@value').get())
        LottoItem.add_value("draw_number", response.xpath('//form[@class="mb-4"]//select/option/@value').get())
        if prize_to_num(rows[0].xpath('./td/span//text()').get().strip()) == 0:
            LottoItem.add_value("cat_1_prize", rows[0].xpath('./td/div/text()').getall()[-2])
        else:
            LottoItem.add_value("cat_1_prize", rows[0].xpath('./td/span//text()').getall()[-1])
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./td/span//text()').getall()[-1])
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./td/span//text()').getall()[-1])
        LottoItem.add_value("cat_4_prize", rows[3].xpath('./td/span//text()').getall()[-1])
        LottoItem.add_value("cat_5_prize", rows[4].xpath('./td/span//text()').getall()[-1])
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td/span//text()').get())
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./td/span//text()').get())
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./td/span//text()').get())
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./td/span//text()').get())
        LottoItem.add_value("cat_5_winners", rows[4].xpath('./td/span//text()').get())
        yield LottoItem.load_item()


class Germany6aus49(scrapy.Spider):

    name = "Germany6aus49"

    def start_requests(self):
        self.name = "Germany6aus49"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)


        url = "https://lotteryguru.com/germany-lottery-results"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        rows = response.xpath('//div[@class="lg-card lg-link"]')
        next_jackpot = rows[1].xpath('.//div[@class="lg-card-row lg-jackpot-info"]//div[@class="lg-sum"]//text()').get()
        draw_date = rows[1].xpath('.//div[@class="lg-card-row"]//div[@class="lg-time"]//span[@class="lg-date"]//text()').get()
        
        LottoItem = ItemLoader(item=Germany6aus49Item(), selector=response)
        LottoItem.add_value("name", self.name)
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d %b %Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("estimated_next_jackpot", next_jackpot)
        yield LottoItem.load_item()


class GermanySpiel77(scrapy.Spider):

    # Will fail if there is no draw from 1/2 days ago

    name = "GermanySpiel77"

    def start_requests(self):
        self.name = "GermanySpiel77"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.lotto.de/lotto-6aus49"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        self.next_jackpot = response.xpath(
            '//header[@class="TilesGameTeaserHeader TilesGameTeaserHeader--spiel77"]//strong[@class="TilesGameTeaserHeader__jackpot"]/text()').get()
        self.headers = {
            'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
            'Accept': 'application/json',
            'Referer': '',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
            'sec-ch-ua-platform': '"Windows"',
        }
        timestamp_today = int(datetime.strptime((datetime.now()-timedelta(days=1)).strftime("%Y-%m-%d"), "%Y-%m-%d").timestamp())*1000
        url = f'https://www.lotto.de/api/stats/entities.lotto/draws/{timestamp_today}'
        yield scrapy.Request(url=url, headers=self.headers, callback=self.parse_yesterday, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse_yesterday(self, response):
        LottoItem = ItemLoader(item=GermanySpiel77Item(), selector=response)
        try:
            latest = response.json()[0]['game77']
        except:
            timestamp_today = int(datetime.strptime((datetime.now()-timedelta(days=2)).strftime("%Y-%m-%d"), "%Y-%m-%d").timestamp())*1000
            url = f'https://www.lotto.de/api/stats/entities.lotto/draws/{timestamp_today}'
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse_day_before, meta={"proxy": self.req_proxy, "download_timeout":10})
        balls_lst = [i for i in str(latest['numbers'])]

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("ball6", balls_lst[6])
        # passing timestamp to itemloader; adding 43200 sec * 1000 since API timestamp is in ms (12 hours) to get correct draw_date
        LottoItem.add_value("draw_datetime", str(int(latest['drawDate'])+(43200*1000)))
        LottoItem.add_value("sales", str(latest['gameAmount']))
        if int(latest['oddsCollection'][0]['numberOfWinners']) > 0:
            LottoItem.add_value("cat_1_prize", str(latest['oddsCollection'][0]['odds']))
        else:
            LottoItem.add_value("cat_1_prize", str(latest['jackpotCurrently']))
        LottoItem.add_value("cat_2_prize", str(latest['oddsCollection'][1]['odds']))
        LottoItem.add_value("cat_3_prize", str(latest['oddsCollection'][2]['odds']))
        LottoItem.add_value("cat_4_prize", str(latest['oddsCollection'][3]['odds']))
        LottoItem.add_value("cat_5_prize", str(latest['oddsCollection'][4]['odds']))
        LottoItem.add_value("cat_6_prize", str(latest['oddsCollection'][5]['odds']))
        LottoItem.add_value("cat_7_prize", str(latest['oddsCollection'][6]['odds']))
        LottoItem.add_value("cat_1_winners", str(latest['oddsCollection'][0]['numberOfWinners']))
        LottoItem.add_value("cat_2_winners", str(latest['oddsCollection'][1]['numberOfWinners']))
        LottoItem.add_value("cat_3_winners", str(latest['oddsCollection'][2]['numberOfWinners']))
        LottoItem.add_value("cat_4_winners", str(latest['oddsCollection'][3]['numberOfWinners']))
        LottoItem.add_value("cat_5_winners", str(latest['oddsCollection'][4]['numberOfWinners']))
        LottoItem.add_value("cat_6_winners", str(latest['oddsCollection'][5]['numberOfWinners']))
        LottoItem.add_value("cat_7_winners", str(latest['oddsCollection'][6]['numberOfWinners']))
        rolldown_check_cat2 = int(latest['oddsCollection'][1]['numberOfWinners'])
        rolldown_check_cat3 = int(latest['oddsCollection'][2]['numberOfWinners'])
        if rolldown_check_cat2 > 77_777 or rolldown_check_cat3 > 7777:
            LottoItem.add_value("rolldown", "yes")
        else:
            LottoItem.add_value("rolldown", "no")
        yield LottoItem.load_item()

    # Over the weekend winner data can sometimes take 2 days to upload so if yesterday fails try 2 days ago
    def parse_day_before(self, response):
        LottoItem = ItemLoader(item=GermanySpiel77Item(), selector=response)
        latest = response.json()[0]['game77']
        balls_lst = [i for i in str(latest['numbers'])]

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("ball6", balls_lst[6])
        # passing timestamp to itemloader; adding 43200 sec * 1000 since API timestamp is in ms (12 hours) to get correct draw_date
        LottoItem.add_value("draw_datetime", str(int(latest['drawDate'])+(43200*1000)))
        LottoItem.add_value("sales", str(latest['gameAmount']))
        if int(latest['oddsCollection'][0]['numberOfWinners']) > 0:
            LottoItem.add_value("cat_1_prize", str(latest['oddsCollection'][0]['odds']))
        else:
            LottoItem.add_value("cat_1_prize", str(latest['jackpotCurrently']))
        LottoItem.add_value("cat_2_prize", str(latest['oddsCollection'][1]['odds']))
        LottoItem.add_value("cat_3_prize", str(latest['oddsCollection'][2]['odds']))
        LottoItem.add_value("cat_4_prize", str(latest['oddsCollection'][3]['odds']))
        LottoItem.add_value("cat_5_prize", str(latest['oddsCollection'][4]['odds']))
        LottoItem.add_value("cat_6_prize", str(latest['oddsCollection'][5]['odds']))
        LottoItem.add_value("cat_7_prize", str(latest['oddsCollection'][6]['odds']))
        LottoItem.add_value("cat_1_winners", str(latest['oddsCollection'][0]['numberOfWinners']))
        LottoItem.add_value("cat_2_winners", str(latest['oddsCollection'][1]['numberOfWinners']))
        LottoItem.add_value("cat_3_winners", str(latest['oddsCollection'][2]['numberOfWinners']))
        LottoItem.add_value("cat_4_winners", str(latest['oddsCollection'][3]['numberOfWinners']))
        LottoItem.add_value("cat_5_winners", str(latest['oddsCollection'][4]['numberOfWinners']))
        LottoItem.add_value("cat_6_winners", str(latest['oddsCollection'][5]['numberOfWinners']))
        LottoItem.add_value("cat_7_winners", str(latest['oddsCollection'][6]['numberOfWinners']))
        rolldown_check_cat2 = int(latest['oddsCollection'][1]['numberOfWinners'])
        rolldown_check_cat3 = int(latest['oddsCollection'][2]['numberOfWinners'])
        if rolldown_check_cat2 > 77_777 or rolldown_check_cat3 > 7777:
            LottoItem.add_value("rolldown", "yes")
        else:
            LottoItem.add_value("rolldown", "no")
        yield LottoItem.load_item()


class GreeceLotto(scrapy.Spider):

    name = "GreeceLotto"

    def start_requests(self):
        self.name = "GreeceLotto"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        headers = {
            'Connection': 'keep-alive',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'DNT': '1',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36',
            'sec-ch-ua-platform': '"Windows"',
            'Origin': 'https://www.opap.gr',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://www.opap.gr/',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }
        url = 'https://api.opap.gr/draws/v3.0/5103/last-result-and-active?status=results'
        yield scrapy.Request(url=url, headers=headers, callback=self.parse,
            meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=GreeceLottoItem(), selector=response)
        latest = response.json()['last']
        balls_lst = latest['winningNumbers']['list']
        bonus_ball = latest['winningNumbers']['bonus'][0]

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", str(balls_lst[0]))
        LottoItem.add_value("ball1", str(balls_lst[1]))
        LottoItem.add_value("ball2", str(balls_lst[2]))
        LottoItem.add_value("ball3", str(balls_lst[3]))
        LottoItem.add_value("ball4", str(balls_lst[4]))
        LottoItem.add_value("ball5", str(balls_lst[5]))
        LottoItem.add_value("bonus_ball", str(bonus_ball))
        LottoItem.add_value("draw_datetime", str(latest['drawTime']))
        LottoItem.add_value("draw_number", str(latest['drawId']))
        LottoItem.add_value("tickets", str(latest['wagerStatistics']['wagers']))
        LottoItem.add_value("perms", str(latest['wagerStatistics']['columns']))
        if int(latest['prizeCategories'][0]['winners']) == 0:
            LottoItem.add_value("cat_1_prize", str(latest['prizeCategories'][0]['jackpot']))
        else:
            LottoItem.add_value("cat_1_prize", str(latest['prizeCategories'][0]['divident']))
        LottoItem.add_value("cat_2_prize", str(latest['prizeCategories'][1]['divident']))
        LottoItem.add_value("cat_3_prize", str(latest['prizeCategories'][2]['divident']))
        LottoItem.add_value("cat_4_prize", str(latest['prizeCategories'][3]['divident']))
        LottoItem.add_value("cat_5_prize", str(latest['prizeCategories'][4]['divident']))
        LottoItem.add_value("cat_1_winners", str(latest['prizeCategories'][0]['winners']))
        LottoItem.add_value("cat_2_winners", str(latest['prizeCategories'][1]['winners']))
        LottoItem.add_value("cat_3_winners", str(latest['prizeCategories'][2]['winners']))
        LottoItem.add_value("cat_4_winners", str(latest['prizeCategories'][3]['winners']))
        LottoItem.add_value("cat_5_winners", str(latest['prizeCategories'][4]['winners']))
        yield LottoItem.load_item()


class GreeceJoker(scrapy.Spider):

    name = "GreeceJoker"

    # Not actually a "joker"-style game; 45C5 + 20C1 with prog. jackpot

    def start_requests(self):
        self.name = "GreeceJoker"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        headers = {
            'Connection': 'keep-alive',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'DNT': '1',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36',
            'sec-ch-ua-platform': '"Windows"',
            'Origin': 'https://www.opap.gr',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://www.opap.gr/',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }
        url = 'https://api.opap.gr/draws/v3.0/5104/last-result-and-active?status=results'
        yield scrapy.Request(url=url, headers=headers, callback=self.parse,
            meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=GreeceJokerItem(), selector=response)
        latest = response.json()['last']
        balls_lst = latest['winningNumbers']['list']
        bonus_ball = latest['winningNumbers']['bonus'][0]

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", str(balls_lst[0]))
        LottoItem.add_value("ball1", str(balls_lst[1]))
        LottoItem.add_value("ball2", str(balls_lst[2]))
        LottoItem.add_value("ball3", str(balls_lst[3]))
        LottoItem.add_value("ball4", str(balls_lst[4]))
        LottoItem.add_value("bonus_ball", str(bonus_ball))
        LottoItem.add_value("draw_datetime", str(latest['drawTime']))
        LottoItem.add_value("draw_number", str(latest['drawId']))
        LottoItem.add_value("tickets", str(latest['wagerStatistics']['wagers']))
        LottoItem.add_value("perms", str(latest['wagerStatistics']['columns']))
        if int(latest['prizeCategories'][0]['winners']) == 0:
            LottoItem.add_value("cat_1_prize", str(latest['prizeCategories'][0]['jackpot']))
        else:
            LottoItem.add_value("cat_1_prize", str(latest['prizeCategories'][0]['divident']))
        LottoItem.add_value("cat_2_prize", str(latest['prizeCategories'][1]['divident']))
        LottoItem.add_value("cat_3_prize", str(latest['prizeCategories'][2]['divident']))
        LottoItem.add_value("cat_4_prize", str(latest['prizeCategories'][3]['divident']))
        LottoItem.add_value("cat_5_prize", str(latest['prizeCategories'][4]['divident']))
        LottoItem.add_value("cat_6_prize", str(latest['prizeCategories'][5]['divident']))
        LottoItem.add_value("cat_7_prize", str(latest['prizeCategories'][6]['divident']))
        LottoItem.add_value("cat_8_prize", str(latest['prizeCategories'][7]['divident']))
        LottoItem.add_value("cat_1_winners", str(latest['prizeCategories'][0]['winners']))
        LottoItem.add_value("cat_2_winners", str(latest['prizeCategories'][1]['winners']))
        LottoItem.add_value("cat_3_winners", str(latest['prizeCategories'][2]['winners']))
        LottoItem.add_value("cat_4_winners", str(latest['prizeCategories'][3]['winners']))
        LottoItem.add_value("cat_5_winners", str(latest['prizeCategories'][4]['winners']))
        LottoItem.add_value("cat_6_winners", str(latest['prizeCategories'][5]['winners']))
        LottoItem.add_value("cat_7_winners", str(latest['prizeCategories'][6]['winners']))
        LottoItem.add_value("cat_8_winners", str(latest['prizeCategories'][7]['winners']))
        yield LottoItem.load_item()


class GreeceProto(scrapy.Spider):

    name = "GreeceProto"

    # 7 digit joker-style game; prog. jackpot

    def start_requests(self):
        self.name = "GreeceProto"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        headers = {
            'Connection': 'keep-alive',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'DNT': '1',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36',
            'sec-ch-ua-platform': '"Windows"',
            'Origin': 'https://www.opap.gr',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://www.opap.gr/',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }
        url = 'https://api.opap.gr/draws/v3.0/2101/last-result-and-active?status=results'
        yield scrapy.Request(url=url, headers=headers, callback=self.parse,
            meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=GreeceProtoItem(), selector=response)
        latest = response.json()['last']
        balls_lst = latest['winningNumbers']['list']

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", str(balls_lst[0]))
        LottoItem.add_value("ball1", str(balls_lst[1]))
        LottoItem.add_value("ball2", str(balls_lst[2]))
        LottoItem.add_value("ball3", str(balls_lst[3]))
        LottoItem.add_value("ball4", str(balls_lst[4]))
        LottoItem.add_value("ball5", str(balls_lst[5]))
        LottoItem.add_value("ball6", str(balls_lst[6]))
        LottoItem.add_value("draw_datetime", str(latest['drawTime']))
        LottoItem.add_value("draw_number", str(latest['drawId']))
        LottoItem.add_value("tickets", str(latest['wagerStatistics']['wagers']))
        LottoItem.add_value("perms", str(latest['wagerStatistics']['columns']))
        if int(latest['prizeCategories'][0]['winners']) == 0:
            LottoItem.add_value("cat_1_prize", str(latest['prizeCategories'][0]['jackpot']))
        else:
            LottoItem.add_value("cat_1_prize", str(latest['prizeCategories'][0]['divident']))
        LottoItem.add_value("cat_2_prize", str(latest['prizeCategories'][1]['fixed']))
        LottoItem.add_value("cat_3_prize", str(latest['prizeCategories'][2]['fixed']))
        LottoItem.add_value("cat_4_prize", str(latest['prizeCategories'][3]['fixed']))
        LottoItem.add_value("cat_5_prize", str(latest['prizeCategories'][4]['fixed']))
        LottoItem.add_value("cat_6_prize", str(latest['prizeCategories'][5]['fixed']))
        LottoItem.add_value("cat_1_winners", str(latest['prizeCategories'][0]['winners']))
        LottoItem.add_value("cat_2_winners", str(latest['prizeCategories'][1]['winners']))
        LottoItem.add_value("cat_3_winners", str(latest['prizeCategories'][2]['winners']))
        LottoItem.add_value("cat_4_winners", str(latest['prizeCategories'][3]['winners']))
        LottoItem.add_value("cat_5_winners", str(latest['prizeCategories'][4]['winners']))
        LottoItem.add_value("cat_6_winners", str(latest['prizeCategories'][5]['winners']))
        yield LottoItem.load_item()


class GrenadaLotto(scrapy.Spider):

    name = "GrenadaLotto"

    # NO NUM OF WINNERS DATA

    def start_requests(self):
        self.name = "GrenadaLotto"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.nla.gd/lotto/"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        LottoItem = ItemLoader(item=GrenadaLottoItem(), selector=response)
        latest = response.xpath('//table')
        balls_lst = latest.xpath('.//tr//td//strong//text()').get().split(',')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("draw_datetime", latest.xpath('.//tr//td/text()').get())
        LottoItem.add_value("draw_number", latest.xpath('.//tr//td//text()').getall()[2])
        LottoItem.add_value("estimated_next_jackpot", response.xpath('//div[@class="the_content_wrapper"]//span//text()').getall()[-1])
        yield LottoItem.load_item()


class GuyanaSupa6(scrapy.Spider):

    name = "GuyanaSupa6"

    # NO WINNERS DATA

    def start_requests(self):
        self.name = "GuyanaSupa6"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://guyana-lottery.com/lottery/"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=GuyanaSupa6Item(), selector=response)
        latest = response.xpath('//div[@class="container"]//div[@class="col-md-3"]')[0]
        balls_lst = [i.strip() for i in latest.xpath('//div[@class="winning-numbers"]/text()').getall()]
        bonus_ball = latest.xpath('//div[@class="bonus-number"]/text()').get()

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("bonus_ball", bonus_ball.strip())
        draw_date = ",".join(latest.xpath('//span[@class="post-date"]/span/text()').get().split(',')[1:]).strip()
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%B %d, %Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("estimated_next_jackpot", ''.join(response.xpath('//span[@class="jackpot-value"]//text()').getall()))
        yield LottoItem.load_item()


class HongKongMarkSix(scrapy.Spider):

    name = "HongKongMarkSix"

    # note: number of winners can be decimals (due to partial investments i.e. fractional bets/tickets)

    def start_requests(self):
        self.name = "HongKongMarkSix"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "http://lottery.hk/en/mark-six/results/"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        self.draw_number = response.xpath('//table//tr/td/text()').get()
        self.draw_date = response.xpath('//table/tr/td/span[@class="date"]//text()').get().strip()
        self.balls_lst = [i for i in response.xpath(
            '//table//td/ul[@class="balls"]')[0].xpath('//li/text()').getall() if i.isdigit()]
        latest_draw_href = response.xpath('//table//td/a/@href').get()
        url = "http://lottery.hk" + latest_draw_href
        yield scrapy.Request(url=url, callback=self.parse_draw)

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=HongKongMarkSixItem(), selector=response)
        rows = response.xpath('//tbody/tr')

        if rows[6].xpath('./td/text()').getall()[4].strip() == 0 or rows[6].xpath('./td/text()').getall()[4].strip() == '0':
            pass
        else:
            LottoItem.add_value("name", self.name)
            LottoItem.add_value("ball0", self.balls_lst[0])
            LottoItem.add_value("ball1", self.balls_lst[1])
            LottoItem.add_value("ball2", self.balls_lst[2])
            LottoItem.add_value("ball3", self.balls_lst[3])
            LottoItem.add_value("ball4", self.balls_lst[4])
            LottoItem.add_value("ball5", self.balls_lst[5])
            LottoItem.add_value("bonus_ball", self.balls_lst[6])
            LottoItem.add_value("draw_datetime", datetime.strptime(self.draw_date, "%d/%m/%Y").strftime("%Y-%m-%d"))
            LottoItem.add_value("draw_number", self.draw_number)
            LottoItem.add_value("cat_1_prize", rows[0].xpath('./td/text()').getall()[3].strip())
            LottoItem.add_value("cat_2_prize", rows[1].xpath('./td/text()').getall()[3].strip())
            LottoItem.add_value("cat_3_prize", rows[2].xpath('./td/text()').getall()[3].strip())
            LottoItem.add_value("cat_4_prize", rows[3].xpath('./td/text()').getall()[3].strip())
            LottoItem.add_value("cat_5_prize", rows[4].xpath('./td/text()').getall()[3].strip())
            LottoItem.add_value("cat_6_prize", rows[5].xpath('./td/text()').getall()[3].strip())
            LottoItem.add_value("cat_7_prize", rows[6].xpath('./td/text()').getall()[3].strip())
            LottoItem.add_value("cat_1_winners", rows[0].xpath('./td/text()').getall()[4].strip())
            LottoItem.add_value("cat_2_winners", rows[1].xpath('./td/text()').getall()[4].strip())
            LottoItem.add_value("cat_3_winners", rows[2].xpath('./td/text()').getall()[4].strip())
            LottoItem.add_value("cat_4_winners", rows[3].xpath('./td/text()').getall()[4].strip())
            LottoItem.add_value("cat_5_winners", rows[4].xpath('./td/text()').getall()[4].strip())
            LottoItem.add_value("cat_6_winners", rows[5].xpath('./td/text()').getall()[4].strip())
            LottoItem.add_value("cat_7_winners", rows[6].xpath('./td/text()').getall()[4].strip())
            yield LottoItem.load_item()


class HungaryOtosLotto(scrapy.Spider):

    name = "HungaryOtosLotto"

    def start_requests(self):
        self.name = "HungaryOtosLotto"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://bet.szerencsejatek.hu/jatekok/otoslotto/sorsolasok"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=HungaryOtosLottoItem(), selector=response)
        balls_lst = response.xpath('//div[@class="numbers clear"]//span/text()').getall()
        rows = response.xpath('//tbody/tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        draw_day = response.xpath('//li[@class="current"]/div[@class="day"]/text()').get().split('.')[0].strip()
        draw_year = response.xpath('//li[@class="current"]/div[@class="week"]/text()').get().split('.')[0].strip()
        draw_date = draw_day + " " + draw_year
        locale.setlocale(locale.LC_TIME, "hu_HU.ISO8859-2")
        clean = datetime.strptime(draw_date, "%B %d %Y")
        locale.setlocale(locale.LC_TIME, "en_GB.ISO8859-1")
        LottoItem.add_value("draw_datetime", clean.strftime("%Y-%m-%d"))
        LottoItem.add_value("estimated_next_jackpot", response.xpath('//div[@class="prediction clear"]/h3/text()').get().strip())
        # Note: jackpot will be '0' if not won
        LottoItem.add_value("cat_1_prize", rows[0].xpath('./td/div[@class="price"]/text()').get().strip())
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./td/div[@class="price"]/text()').get().strip())
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./td/div[@class="price"]/text()').get().strip())
        LottoItem.add_value("cat_4_prize", rows[3].xpath('./td/div[@class="price"]/text()').get().strip())
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td//text()').getall()[4])
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./td//text()').getall()[4])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./td//text()').getall()[4])
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./td//text()').getall()[4])
        yield LottoItem.load_item()


class HungaryHatosLotto(scrapy.Spider):

    name = "HungaryHatosLotto"

    def start_requests(self):
        self.name = "HungaryHatosLotto"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://bet.szerencsejatek.hu/jatekok/hatoslotto/sorsolasok"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=HungaryHatosLottoItem(), selector=response)
        balls_lst = response.xpath('//div[@class="numbers clear"]//span/text()').getall()
        rows = response.xpath('//tbody/tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        draw_day = response.xpath('//li[@class="current"]/div[@class="day"]/text()').get().split('.')[0].strip()
        draw_year = response.xpath('//li[@class="current"]/div[@class="week"]/text()').get().split('.')[0].strip()
        draw_date = draw_day + " " + draw_year
        locale.setlocale(locale.LC_TIME, "hu_HU.ISO8859-2")
        clean = datetime.strptime(draw_date, "%B %d %Y")
        locale.setlocale(locale.LC_TIME, "en_GB.ISO8859-1")
        LottoItem.add_value("draw_datetime", clean.strftime("%Y-%m-%d"))
        LottoItem.add_value("estimated_next_jackpot", response.xpath('//div[@class="prediction clear"]/h3/text()').get().strip())
        # Note: jackpot will be '0' if not won
        LottoItem.add_value("cat_1_prize", rows[0].xpath('./td/div[@class="price"]/text()').get().strip())
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./td/div[@class="price"]/text()').get().strip())
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./td/div[@class="price"]/text()').get().strip())
        LottoItem.add_value("cat_4_prize", rows[3].xpath('./td/div[@class="price"]/text()').get().strip())
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td//text()').getall()[4])
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./td//text()').getall()[4])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./td//text()').getall()[4])
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./td//text()').getall()[4])
        yield LottoItem.load_item()


class HungarySkandinavLotto(scrapy.Spider):

    name = "HungarySkandinavLotto"

    def start_requests(self):
        self.name = "HungarySkandinavLotto"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://bet.szerencsejatek.hu/jatekok/skandinavlotto/sorsolasok/"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=HungarySkandinavLottoItem(), selector=response)
        balls_lst = response.xpath('//div[@class="numbers clear"]//span/text()').getall()
        rows = response.xpath('//tbody/tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("draw1_ball0", balls_lst[0])
        LottoItem.add_value("draw1_ball1", balls_lst[1])
        LottoItem.add_value("draw1_ball2", balls_lst[2])
        LottoItem.add_value("draw1_ball3", balls_lst[3])
        LottoItem.add_value("draw1_ball4", balls_lst[4])
        LottoItem.add_value("draw1_ball5", balls_lst[5])
        LottoItem.add_value("draw1_ball6", balls_lst[6])
        LottoItem.add_value("draw2_ball0", balls_lst[7])
        LottoItem.add_value("draw2_ball1", balls_lst[8])
        LottoItem.add_value("draw2_ball2", balls_lst[9])
        LottoItem.add_value("draw2_ball3", balls_lst[10])
        LottoItem.add_value("draw2_ball4", balls_lst[11])
        LottoItem.add_value("draw2_ball5", balls_lst[12])
        LottoItem.add_value("draw2_ball6", balls_lst[13])
        draw_day = response.xpath('//li[@class="current"]/div[@class="day"]/text()').get().split('.')[0].strip()
        draw_year = response.xpath('//li[@class="current"]/div[@class="week"]/text()').get().split('.')[0].strip()
        draw_date = draw_day + " " + draw_year
        locale.setlocale(locale.LC_TIME, "hu_HU.ISO8859-2")
        clean = datetime.strptime(draw_date, "%B %d %Y")
        locale.setlocale(locale.LC_TIME, "en_GB.ISO8859-1")
        LottoItem.add_value("draw_datetime", clean.strftime("%Y-%m-%d"))
        LottoItem.add_value("estimated_next_jackpot", response.xpath('//div[@class="prediction clear"]/h3/text()').get().strip())
        # Note: jackpot will be '0' if not won
        LottoItem.add_value("cat_1_prize", rows[0].xpath('./td/div[@class="price"]/text()').get().strip())
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./td/div[@class="price"]/text()').get().strip())
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./td/div[@class="price"]/text()').get().strip())
        LottoItem.add_value("cat_4_prize", rows[3].xpath('./td/div[@class="price"]/text()').get().strip())
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td//text()').getall()[4])
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./td//text()').getall()[4])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./td//text()').getall()[4])
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./td//text()').getall()[4])
        yield LottoItem.load_item()


class HungaryJoker(scrapy.Spider):

    name = "HungaryJoker"

    def start_requests(self):
        self.name = "HungaryJoker"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://bet.szerencsejatek.hu/jatekok/joker/sorsolasok"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=HungaryJokerItem(), selector=response)
        balls_lst = response.xpath('//div[@class="numbers clear"]//span/text()').getall()
        rows = response.xpath('//tbody/tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        draw_day = response.xpath('//li[@class="current"]/div[@class="day"]/text()').get().split('.')[0].strip()
        draw_year = response.xpath('//li[@class="current"]/div[@class="week"]/text()').get().split('.')[0].strip()
        draw_date = draw_day + " " + draw_year
        locale.setlocale(locale.LC_TIME, "hu_HU.ISO8859-2")
        clean = datetime.strptime(draw_date, "%B %d %Y")
        locale.setlocale(locale.LC_TIME, "en_GB.ISO8859-1")
        LottoItem.add_value("draw_datetime", clean.strftime("%Y-%m-%d"))
        LottoItem.add_value("estimated_next_jackpot", response.xpath('//div[@class="prediction clear"]/h3/text()').get().strip())
        LottoItem.add_value("cat_1_prize", rows[0].xpath('./td/div[@class="price"]/text()').get().strip())
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./td/div[@class="price"]/text()').get().strip())
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./td/div[@class="price"]/text()').get().strip())
        LottoItem.add_value("cat_4_prize", rows[3].xpath('./td/div[@class="price"]/text()').get().strip())
        LottoItem.add_value("cat_5_prize", rows[4].xpath('./td/div[@class="price"]/text()').get().strip())
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td//text()').getall()[4])
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./td//text()').getall()[4])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./td//text()').getall()[4])
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./td//text()').getall()[4])
        LottoItem.add_value("cat_5_winners", rows[4].xpath('./td//text()').getall()[4])
        yield LottoItem.load_item()


class IcelandLotto(scrapy.Spider):

    name = "IcelandLotto"

    def start_requests(self):
        self.name = "IcelandLotto"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Referer': 'https://games.lotto.is/result/lotto?productId=1',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
            'X-CSRF-Token': 'E-7ok_cmP28VLsTg4hhreqvOb3Ufc10pWjYBhxDizzdxg4fnpEdQKCVvqJigd1ov2IUdH1s4KH04UDPmRNT9Rw==',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        current_week = (datetime.now()-timedelta(days=1)).strftime("%W")
        current_year = (datetime.now()-timedelta(days=1)).strftime("%Y")
        url = f'https://games.lotto.is/game/lotto-results?productId=1&week={current_week}&year={current_year}'
        yield scrapy.Request(url=url, headers=self.headers, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=IcelandLottoItem(), selector=response)
        if response.json()['hasResults'] == False:
            prev_week = (datetime.now()-timedelta(days=8)).strftime("%W")
            prev_year = (datetime.now()-timedelta(days=8)).strftime("%Y")
            url = f'https://games.lotto.is/game/lotto-results?productId=1&week={prev_week}&year={prev_year}'
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":10})

        latest = response.json()['results'][0]
        balls_lst = latest['result']['lottoNumbers']

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", str(balls_lst[0]))
        LottoItem.add_value("ball1", str(balls_lst[1]))
        LottoItem.add_value("ball2", str(balls_lst[2]))
        LottoItem.add_value("ball3", str(balls_lst[3]))
        LottoItem.add_value("ball4", str(balls_lst[4]))
        LottoItem.add_value("bonus_ball", str(latest['result']['bonusNumbers'][0]))
        LottoItem.add_value("draw_datetime", latest['dateDraw'])
        LottoItem.add_value("cat_1_prize", latest['result']['lottoWin'][4]['amountWinner'])
        LottoItem.add_value("cat_2_prize", latest['result']['lottoWin'][3]['amountWinner'])
        LottoItem.add_value("cat_3_prize", latest['result']['lottoWin'][2]['amountWinner'])
        LottoItem.add_value("cat_4_prize", latest['result']['lottoWin'][1]['amountWinner'])
        LottoItem.add_value("cat_5_prize", latest['result']['lottoWin'][0]['amountWinner'])
        LottoItem.add_value("cat_1_winners", latest['result']['lottoWin'][4]['winnerCnt'])
        LottoItem.add_value("cat_2_winners", latest['result']['lottoWin'][3]['winnerCnt'])
        LottoItem.add_value("cat_3_winners", latest['result']['lottoWin'][2]['winnerCnt'])
        LottoItem.add_value("cat_4_winners", latest['result']['lottoWin'][1]['winnerCnt'])
        LottoItem.add_value("cat_5_winners", latest['result']['lottoWin'][0]['winnerCnt'])
        yield LottoItem.load_item()

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=IcelandLottoItem(), selector=response)
        latest = response.json()['results'][0]
        balls_lst = latest['result']['lottoNumbers']

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", str(balls_lst[0]))
        LottoItem.add_value("ball1", str(balls_lst[1]))
        LottoItem.add_value("ball2", str(balls_lst[2]))
        LottoItem.add_value("ball3", str(balls_lst[3]))
        LottoItem.add_value("ball4", str(balls_lst[4]))
        LottoItem.add_value("bonus_ball", str(latest['result']['bonusNumbers'][0]))
        LottoItem.add_value("draw_datetime", latest['dateDraw'])
        LottoItem.add_value("cat_1_prize", latest['result']['lottoWin'][4]['amountWinner'])
        LottoItem.add_value("cat_2_prize", latest['result']['lottoWin'][3]['amountWinner'])
        LottoItem.add_value("cat_3_prize", latest['result']['lottoWin'][2]['amountWinner'])
        LottoItem.add_value("cat_4_prize", latest['result']['lottoWin'][1]['amountWinner'])
        LottoItem.add_value("cat_5_prize", latest['result']['lottoWin'][0]['amountWinner'])
        LottoItem.add_value("cat_1_winners", latest['result']['lottoWin'][4]['winnerCnt'])
        LottoItem.add_value("cat_2_winners", latest['result']['lottoWin'][3]['winnerCnt'])
        LottoItem.add_value("cat_3_winners", latest['result']['lottoWin'][2]['winnerCnt'])
        LottoItem.add_value("cat_4_winners", latest['result']['lottoWin'][1]['winnerCnt'])
        LottoItem.add_value("cat_5_winners", latest['result']['lottoWin'][0]['winnerCnt'])
        yield LottoItem.load_item()


class IrelandLotto(scrapy.Spider):

    name = "IrelandLotto"

    def start_requests(self):
        self.name = "IrelandLotto"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        url = "https://www.lottery.ie/draw-games/lotto"
        yield scrapy.Request(url=url, callback=self.parse, headers=self.headers,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        self.next_jackpot = response.xpath('//div[@class="countdown-banner__prize prizeamount"]/span/text()').get()
        url = "https://www.lottery.ie/results/lotto/history"
        yield scrapy.Request(url=url, headers=self.headers, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":10})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=IrelandLottoItem(), selector=response)
        latest = response.xpath('//div[@data-testid="result-hub-card"]')[0]
        balls_lst = latest.xpath('.//div[@data-testid="lotto-ball"]/text()').getall()
        rows = latest.xpath('.//tr')[1:]

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("bonus_ball", balls_lst[6])
        draw_date = response.xpath('//div[@class="my-4"]/h4/text()').get().split(' ')[1].strip()
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d/%m/%y").strftime("%Y-%m-%d"))
        LottoItem.add_value("estimated_next_jackpot", self.next_jackpot)
        jackpot = rows[0].xpath('./td/text()').getall()[2]
        LottoItem.add_value("cat_1_prize", jackpot)
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_4_prize", rows[3].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_5_prize", rows[4].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_6_prize", rows[5].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_7_prize", rows[6].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_8_prize", rows[7].xpath('./td/text()').getall()[2].lower().split('daily')[0])
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_5_winners", rows[4].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_6_winners", rows[5].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_7_winners", rows[6].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_8_winners", rows[7].xpath('./td/text()').getall()[1])
        if prize_to_num(jackpot) >= 19_060_000:
            LottoItem.add_value("rolldown", "yes")
        else:
            LottoItem.add_value("rolldown", "no")
        yield LottoItem.load_item()


class IsraelDoubleLotto(scrapy.Spider):

    name = "IsraelDoubleLotto"

    # REQUIRES ISRAELI PROXY
    # Can play 'double' i.e. ticket price is doubled for doubled winnings

    def start_requests(self):
        self.name = "IsraelDoubleLotto"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.pais.co.il/lotto/archive.aspx"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        self.latest_draw_id = response.xpath(
            '//div[@id="changeGameDiv"]/ol/li/div[@class="archive_list_block lotto_number"]')[0].xpath('./div/text()').getall()[-1].strip()
        url = "https://www.pais.co.il/lotto/currentlotto.aspx?lotteryId=" + str(self.latest_draw_id)
        yield scrapy.Request(url=url, callback=self.parse_draw)

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=IsraelDoubleLottoItem(), selector=response)
        balls_lst = [i for i in response.xpath('//li[@class="loto_info_num"]//text()').getall() if len(i.strip())>0]
        bonus_ball = [i for i in response.xpath('//div[@class="loto_info_num strong"]//text()').getall() if len(i.strip())>0]
        rows = response.xpath('//ol[@id="regularLottoList"]/li')
        double_rows = response.xpath('//ol[@id="doubleLottoList"]/li')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("bonus_ball", bonus_ball[0])
        LottoItem.add_value("draw_datetime", response.xpath('//div[@class="cat_archive_txt open"]/@aria-label').get())
        LottoItem.add_value("draw_number", self.latest_draw_id)
        LottoItem.add_value("double_jackpot", response.xpath(
            '//div[@class="archive_open_dates current_info w-clearfix"]')[0].xpath('.//strong//text()').getall()[-1])
        LottoItem.add_value("double_match_6_bonus", double_rows[0].xpath(
            './/div[@class="archive_list_block lotto_current"]')[1].xpath('.//div[@tabindex="0"]//text()').get())
        LottoItem.add_value("double_match_6", double_rows[1].xpath(
            './/div[@class="archive_list_block lotto_current"]')[1].xpath('.//div[@tabindex="0"]//text()').get())
        LottoItem.add_value("double_match_5_bonus", double_rows[2].xpath(
            './/div[@class="archive_list_block lotto_current"]')[1].xpath('.//div[@tabindex="0"]//text()').get())
        LottoItem.add_value("double_match_5", double_rows[3].xpath(
            './/div[@class="archive_list_block lotto_current"]')[1].xpath('.//div[@tabindex="0"]//text()').get())
        LottoItem.add_value("double_match_4_bonus", double_rows[4].xpath(
            './/div[@class="archive_list_block lotto_current"]')[1].xpath('.//div[@tabindex="0"]//text()').get())
        LottoItem.add_value("double_match_4", double_rows[5].xpath(
            './/div[@class="archive_list_block lotto_current"]')[1].xpath('.//div[@tabindex="0"]//text()').get())
        LottoItem.add_value("double_match_3_bonus", double_rows[6].xpath(
            './/div[@class="archive_list_block lotto_current"]')[1].xpath('.//div[@tabindex="0"]//text()').get())
        LottoItem.add_value("double_match_3", double_rows[7].xpath(
            './/div[@class="archive_list_block lotto_current"]')[1].xpath('.//div[@tabindex="0"]//text()').get())
        LottoItem.add_value("jackpot", response.xpath(
            '//div[@class="archive_open_dates current_info w-clearfix"]')[0].xpath('.//strong//text()').get())
        LottoItem.add_value("match_6_bonus", rows[0].xpath(
            './/div[@class="archive_list_block lotto_current"]')[1].xpath('.//div[@tabindex="0"]//text()').get())
        LottoItem.add_value("match_6", rows[1].xpath(
            './/div[@class="archive_list_block lotto_current"]')[1].xpath('.//div[@tabindex="0"]//text()').get())
        LottoItem.add_value("match_5_bonus", rows[2].xpath(
            './/div[@class="archive_list_block lotto_current"]')[1].xpath('.//div[@tabindex="0"]//text()').get())
        LottoItem.add_value("match_5", rows[3].xpath(
            './/div[@class="archive_list_block lotto_current"]')[1].xpath('.//div[@tabindex="0"]//text()').get())
        LottoItem.add_value("match_4_bonus", rows[4].xpath(
            './/div[@class="archive_list_block lotto_current"]')[1].xpath('.//div[@tabindex="0"]//text()').get())
        LottoItem.add_value("match_4", rows[5].xpath(
            './/div[@class="archive_list_block lotto_current"]')[1].xpath('.//div[@tabindex="0"]//text()').get())
        LottoItem.add_value("match_3_bonus", rows[6].xpath(
            './/div[@class="archive_list_block lotto_current"]')[1].xpath('.//div[@tabindex="0"]//text()').get())
        LottoItem.add_value("match_3", rows[7].xpath(
            './/div[@class="archive_list_block lotto_current"]')[1].xpath('.//div[@tabindex="0"]//text()').get())
        yield LottoItem.load_item()


class ItalySuperEnaLotto(scrapy.Spider):

    name = "ItalySuperEnaLotto"

    # lottomatica.it = DIFFICULT/SHIT HTML TO PARSE
    # Scrape directly via SuperEna website

    def start_requests(self):
        self.name = "ItalySuperEnaLotto"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.superenalotto.com/risultati"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        next_page = response.xpath('//table//th/a/@href').get()
        url = urljoin(response.url, next_page)
        self.next_jackpot = response.xpath('//div[@class="next-jackpot"]/span//text()').get().strip()
        yield scrapy.Request(url=url, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":10})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=ItalySuperEnaLottoItem(), selector=response)
        balls_lst = response.xpath('//td[@class="ball-46px"]/text()').getall()
        bonus_ball = response.xpath('//td[@class="jolly-46px"]/text()').get()
        rows = response.xpath('//table[@class="tbl3"]/tbody')[1].xpath('./tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("bonus_ball", bonus_ball)
        LottoItem.add_value("draw_datetime", response.xpath('//th/time/@datetime').get())
        LottoItem.add_value("draw_number", response.xpath('//p[@itemprop="description"]/strong/text()').get())
        LottoItem.add_value("estimated_next_jackpot", self.next_jackpot)
        LottoItem.add_value("cat_1_prize", rows[0].xpath('./td/text()').getall()[-2].strip())
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./td/text()').getall()[-2].strip())
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./td/text()').getall()[-2].strip())
        LottoItem.add_value("cat_4_prize", rows[3].xpath('./td/text()').getall()[-2].strip())
        LottoItem.add_value("cat_5_prize", rows[4].xpath('./td/text()').getall()[-2].strip())
        LottoItem.add_value("cat_6_prize", rows[5].xpath('./td/text()').getall()[-2].strip())
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_5_winners", rows[4].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_6_winners", rows[5].xpath('./td/text()').getall()[-1].strip())
        yield LottoItem.load_item()


class JamaicaLotto(scrapy.Spider):

    name = "JamaicaLotto"

    def start_requests(self):
        self.name = "JamaicaLotto"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://supremeventures.com/game-results/?action=lotto"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=JamaicaLottoItem(), selector=response)
        latest = response.xpath('//div[@class="game lotto"]')[0]
        balls_lst = latest.xpath('.//span[@class="result-number"]/text()').getall()
        bonus_ball = latest.xpath('.//span[@class="result-number bonusball"]/text()').get()
        raw_info = [i.strip().lower() for i in latest.xpath('.//div[@class="game-result"]/p/text()').getall() if len(i.strip())>1]
        match_info = [i.split('-')[1].split('win')[0].strip() for i in raw_info if "winner" in i]
        prize_info = [i.split('-')[1].split('win')[1].strip() for i in raw_info if "winner" in i]
        draw_num = [i for i in raw_info if "draw number" in i][0]

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("bonus_ball", bonus_ball)
        draw_date = latest.xpath('.//h5/text()').get().strip().lower()
        if "december" in draw_date:
            full_date = draw_date + " " + (datetime.now()-timedelta(days=10)).strftime("%Y")
        else:
            full_date = draw_date + " " + datetime.now().strftime("%Y")
        LottoItem.add_value("draw_datetime", datetime.strptime(full_date, "%A, %B %d %Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", draw_num)
        if prize_to_num(match_info[0]) == 0:
            LottoItem.add_value("cat_1_prize", latest.xpath('.//h4/span[@class="jackpot"]/text()').get())
        else:
            LottoItem.add_value("cat_1_prize", prize_info[0])
        LottoItem.add_value("cat_2_prize", prize_info[1])
        LottoItem.add_value("cat_3_prize", prize_info[2])
        LottoItem.add_value("cat_4_prize", prize_info[3])
        LottoItem.add_value("cat_5_prize", prize_info[4])
        LottoItem.add_value("cat_6_prize", prize_info[5])
        LottoItem.add_value("cat_1_winners", match_info[0])
        LottoItem.add_value("cat_2_winners", match_info[1])
        LottoItem.add_value("cat_3_winners", match_info[2])
        LottoItem.add_value("cat_4_winners", match_info[3])
        LottoItem.add_value("cat_5_winners", match_info[4])
        LottoItem.add_value("cat_6_winners", match_info[5])
        yield LottoItem.load_item()


class JapanLoto7(scrapy.Spider):

    name = "JapanLoto7"

    def start_requests(self):
        self.name = "JapanLoto7"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.mizuhobank.co.jp/retail/takarakuji/loto/loto7/index.html"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        LottoItem = ItemLoader(item=JapanLoto7Item(), selector=response)
        latest = response.xpath('//table[@class="typeTK"]')[0]
        balls_lst = latest.xpath('.//strong[@class="js-lottery-number-pc"]//text()').getall()
        bonus_balls = latest.xpath('.//strong[@class="js-lottery-bonus-pc"]//text()').getall()
        rows = latest.xpath('.//tr[@class="js-lottery-prize-pc"]')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("ball6", balls_lst[6])
        LottoItem.add_value("bonus_ball0", bonus_balls[0])
        LottoItem.add_value("bonus_ball1", bonus_balls[1])
        draw_date = response.xpath('//table[@class="typeTK"]')[0].xpath('.//tbody/tr/td[@colspan="7"]//text()').getall()[0]
        date_str = []
        for i in draw_date[:-1]:
            if i.isdigit() == True:
                date_str.append(i)
            else:
                date_str.append('/')
        LottoItem.add_value("draw_datetime", datetime.strptime("".join(date_str), "%Y/%m/%d").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", response.xpath('//table[@class="typeTK"]')[0].xpath('.//thead//th//text()').getall()[-1])
        LottoItem.add_value("sales", response.xpath(
            '//table[@class="typeTK"]')[0].xpath('.//tbody/tr/td[@colspan="7"]//text()').getall()[1])
        LottoItem.add_value("carryover", response.xpath(
            '//table[@class="typeTK"]')[0].xpath('.//tbody/tr/td[@colspan="7"]//text()').getall()[-1])
        for i in range(6):
            prize_value = rows[i].xpath('./td//text()').getall()[-1]
            if len([s for s in prize_value if s.isdigit()]) > 0:
                LottoItem.add_value(f"cat_{i+1}_prize", prize_value)
            else:
                LottoItem.add_value(f"cat_{i+1}_prize", '0')
        for i in range(6):
            winner_value = rows[i].xpath('./td//text()').get()
            if len([s for s in winner_value if s.isdigit()]) > 0:
                LottoItem.add_value(f"cat_{i+1}_winners", winner_value)
            else:
                LottoItem.add_value(f"cat_{i+1}_winners", '0')
        yield LottoItem.load_item()


class JapanLoto6(scrapy.Spider):

    name = "JapanLoto6"

    def start_requests(self):
        self.name = "JapanLoto6"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.mizuhobank.co.jp/retail/takarakuji/loto/loto6/index.html"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        LottoItem = ItemLoader(item=JapanLoto6Item(), selector=response)
        latest = response.xpath('//table[@class="typeTK"]')[0]
        balls_lst = latest.xpath('.//strong[@class="js-lottery-number-pc"]//text()').getall()
        bonus_ball = latest.xpath('.//strong[@class="js-lottery-bonus-pc"]//text()').get()
        rows = latest.xpath('.//tr[@class="js-lottery-prize-pc"]')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("bonus_ball", bonus_ball)
        draw_date = response.xpath('//table[@class="typeTK"]')[0].xpath('.//tbody/tr/td[@colspan="6"]//text()').getall()[0]
        date_str = []
        for i in draw_date[:-1]:
            if i.isdigit() == True:
                date_str.append(i)
            else:
                date_str.append('/')
        LottoItem.add_value("draw_datetime", datetime.strptime("".join(date_str), "%Y/%m/%d").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", response.xpath('//table[@class="typeTK"]')[0].xpath('.//thead//th//text()').getall()[-1])
        LottoItem.add_value("sales", response.xpath(
            '//table[@class="typeTK"]')[0].xpath('.//tbody/tr/td[@colspan="6"]//text()').getall()[1])
        LottoItem.add_value("carryover", response.xpath(
            '//table[@class="typeTK"]')[0].xpath('.//tbody/tr/td[@colspan="6"]//text()').getall()[-1])
        for i in range(5):
            prize_value = rows[i].xpath('./td//text()').getall()[-1]
            if len([s for s in prize_value if s.isdigit()]) > 0:
                LottoItem.add_value(f"cat_{i+1}_prize", prize_value)
            else:
                LottoItem.add_value(f"cat_{i+1}_prize", '0')
        for i in range(5):
            winner_value = rows[i].xpath('./td//text()').get()
            if len([s for s in winner_value if s.isdigit()]) > 0:
                LottoItem.add_value(f"cat_{i+1}_winners", winner_value)
            else:
                LottoItem.add_value(f"cat_{i+1}_winners", '0')
        yield LottoItem.load_item()


class KazakhstanLoto6x49(scrapy.Spider):

    name = "KazakhstanLoto6x49"

    def start_requests(self):
        self.name = "KazakhstanLoto6x49"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        headers = {
            'authority': 'sz.kz',
            'accept': '*/*',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'dnt': '1',
            'origin': 'https://sz.kz',
            'referer': 'https://sz.kz/resultsGame?gAlias=bet_cl_649',
            'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        }
        url = f'https://sz.kz/srv?srv=drawResultsEx&gameId=10&intervalID={(datetime.now()-timedelta(days=21)).strftime("%d.%m.%Y")}'
        yield scrapy.Request(url=url, headers=headers, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=KazakhstanLoto6x49Item(), selector=response)
        response = response.text
        if isinstance(response, bytes):
            response = response.decode('utf-8')
        response = json.loads(response.split('msg=')[1])
        latest = response['draws'][0]
        balls_lst = [latest['balls'][i] for i in range(6)]
        bonus_ball = latest['bonusBalls'][0]

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", str(balls_lst[0]))
        LottoItem.add_value("ball1", str(balls_lst[1]))
        LottoItem.add_value("ball2", str(balls_lst[2]))
        LottoItem.add_value("ball3", str(balls_lst[3]))
        LottoItem.add_value("ball4", str(balls_lst[4]))
        LottoItem.add_value("ball5", str(balls_lst[5]))
        LottoItem.add_value("bonus_ball", str(bonus_ball))
        draw_date = latest['makeDate'].split(' ')[0].strip()
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d.%m.%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", str(latest['drawId']))
        LottoItem.add_value("estimated_next_jackpot", str(latest['drawPrize']))
        # note: Jackpot will be '0' if  there are no winners
        LottoItem.add_value("cat_1_prize", str(latest['winData'][0]['summ']))
        LottoItem.add_value("cat_2_prize", str(latest['winData'][1]['summ']))
        LottoItem.add_value("cat_3_prize", str(latest['winData'][2]['summ']))
        LottoItem.add_value("cat_4_prize", str(latest['winData'][3]['summ']))
        LottoItem.add_value("cat_5_prize", str(latest['winData'][4]['summ']))
        LottoItem.add_value("cat_6_prize", str(latest['winData'][5]['summ']))
        LottoItem.add_value("cat_1_winners", str(latest['winData'][0]['quantity']))
        LottoItem.add_value("cat_2_winners", str(latest['winData'][1]['quantity']))
        LottoItem.add_value("cat_3_winners", str(latest['winData'][2]['quantity']))
        LottoItem.add_value("cat_4_winners", str(latest['winData'][3]['quantity']))
        LottoItem.add_value("cat_5_winners", str(latest['winData'][4]['quantity']))
        LottoItem.add_value("cat_6_winners", str(latest['winData'][5]['quantity']))
        yield LottoItem.load_item()


class KazakhstanLoto5x36(scrapy.Spider):

    # No longer publish winner data on new website

    name = "KazakhstanLoto5x36"

    def start_requests(self):
        self.name = "KazakhstanLoto5x36"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        headers = {
            'authority': 'sz.kz',
            'accept': '*/*',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'dnt': '1',
            'origin': 'https://sz.kz',
            'referer': 'https://sz.kz/resultsGame?gAlias=bet_cl_536',
            'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        }
        url = f'https://sz.kz/srv?srv=drawResultsEx&gameId=23&intervalID={(datetime.now()-timedelta(days=21)).strftime("%d.%m.%Y")}'
        yield scrapy.Request(url=url, headers=headers, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=KazakhstanLoto5x36Item(), selector=response)
        response = response.text
        if isinstance(response, bytes):
            response = response.decode('utf-8')
        response = json.loads(response.split('msg=')[1])
        latest = response['draws'][0]
        balls_lst = [latest['balls'][i] for i in range(5)]

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", str(balls_lst[0]))
        LottoItem.add_value("ball1", str(balls_lst[1]))
        LottoItem.add_value("ball2", str(balls_lst[2]))
        LottoItem.add_value("ball3", str(balls_lst[3]))
        LottoItem.add_value("ball4", str(balls_lst[4]))
        draw_date = latest['makeDate'].split(' ')[0].strip()
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d.%m.%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", str(latest['drawId']))
        LottoItem.add_value("estimated_next_jackpot", str(latest['drawPrize']))
        # New website doesn't publish winner data as of 8/11/21
        LottoItem.add_value("cat_1_prize", str(latest['winData'][0]['summ']))
        LottoItem.add_value("cat_2_prize", str(latest['winData'][1]['summ']))
        LottoItem.add_value("cat_3_prize", str(latest['winData'][2]['summ']))
        LottoItem.add_value("cat_4_prize", str(latest['winData'][3]['summ']))
        LottoItem.add_value("cat_1_winners", str(latest['winData'][0]['quantity']))
        LottoItem.add_value("cat_2_winners", str(latest['winData'][1]['quantity']))
        LottoItem.add_value("cat_3_winners", str(latest['winData'][2]['quantity']))
        LottoItem.add_value("cat_4_winners", str(latest['winData'][3]['quantity']))
        yield LottoItem.load_item()


# class KosovoLotto(scrapy.Spider):

#     name = "KosovoLotto"

#     urls = [
#         "http://www.lotaria-ks.com/loto-739/",
#         "http://www.lotaria-ks.com/joker/",
#     ]

#     # INACTIVE
#     # LAST LOTTO DRAW: 08.05.2019


class LatviaLotto5x35(scrapy.Spider):

    name = "LatviaLotto5x35"

    def start_requests(self):
        self.name = "LatviaLotto5x35"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://viking-lotto.net/en/latloto-5-35"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        self.next_jackpot = response.xpath('//main//div[@class="_amount"]/text()').get()
        url = "https://www.latloto.lv/lv/rezultati/latloto"
        yield scrapy.Request(url=url, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":10})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=LatviaLotto5x35Item(), selector=response)
        rows = response.xpath('//div[@class="col-sm-8"]//tbody/tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", response.xpath('//div[@class="col-sm-8"]//span[@class="pos1"]/text()').get())
        LottoItem.add_value("ball1", response.xpath('//div[@class="col-sm-8"]//span[@class="pos2"]/text()').get())
        LottoItem.add_value("ball2", response.xpath('//div[@class="col-sm-8"]//span[@class="pos3"]/text()').get())
        LottoItem.add_value("ball3", response.xpath('//div[@class="col-sm-8"]//span[@class="pos4"]/text()').get())
        LottoItem.add_value("ball4", response.xpath('//div[@class="col-sm-8"]//span[@class="pos5"]/text()').get())
        LottoItem.add_value("bonus_ball", response.xpath('//div[@class="col-sm-8"]//span[@class="pos6 darker"]/text()').get())
        draw_date = clean_datetime(response.xpath('//div[@class="lotto-table"]/span/p/text()').getall()[-1])
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d.%m.%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", response.xpath('//div[@class="lotto-table"]/span/p/text()').getall()[0])
        LottoItem.add_value("estimated_next_jackpot", self.next_jackpot)
        LottoItem.add_value("cat_1_prize", rows[0].xpath('./td/text()').getall()[-2])
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./td/text()').getall()[-2])
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./td/text()').getall()[-2])
        LottoItem.add_value("cat_4_prize", rows[3].xpath('./td/text()').getall()[-2])
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./td/text()').getall()[-1])
        yield LottoItem.load_item()


class LebanonLoto(scrapy.Spider):

    name = "LebanonLoto"

    def start_requests(self):
        self.name = "LebanonLoto"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.lldj.com/en/LatestResults/Loto"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        LottoItem = ItemLoader(item=LebanonLotoItem(), selector=response)
        rows = response.xpath('//ul/li[@class="row data"]')
        balls_lst = [i.strip() for i in response.xpath(
            '//ul[@class="list ballslist pseudoclear"]/li/text()').getall() if len(i.strip())>0]

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("bonus_ball", balls_lst[6])
        draw_info = response.xpath('//div[@class="drawinfobox"]/span[@class="draw"]/span[@class="yellow"]/text()').get().lower().strip()
        draw_date = draw_info.split('on')[1].strip()
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d/%m/%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", draw_info.split('on')[0])
        LottoItem.add_value("estimated_next_jackpot", response.xpath('//div[@class="estimation"]/span[@class="prize "]/text()').get())

        match_6 = rows[0].xpath('./span/span[@class="float"]/text()').getall()[-2]
        if prize_to_num(match_6) == 0:
            jackpot = response.xpath('//div[@class="drawinfobox"]/span[@class="jackpot"]/span[@class="yellow"]/text()').get().strip()
        else:
            # jackpot will be '0' unless won
            jackpot = rows[0].xpath('./span/span[@class="float"]/text()').getall()[-1]
        LottoItem.add_value("cat_1_prize", jackpot)
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./span/span[@class="float"]/text()').getall()[-1])
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./span/span[@class="float"]/text()').getall()[-1])
        LottoItem.add_value("cat_4_prize", rows[3].xpath('./span/span[@class="float"]/text()').getall()[-1])
        LottoItem.add_value("cat_5_prize", rows[4].xpath('./span/span[@class="float"]/text()').getall()[-1])
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./span/span[@class="float"]/text()').getall()[-2])
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./span/span[@class="float"]/text()').getall()[-2])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./span/span[@class="float"]/text()').getall()[-2])
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./span/span[@class="float"]/text()').getall()[-2])
        LottoItem.add_value("cat_5_winners", rows[4].xpath('./span/span[@class="float"]/text()').getall()[-2])
        yield LottoItem.load_item()


# class MacedoniaLoto7(scrapy.Spider):

#     name = "MacedoniaLoto7"

#     # INACTIVE SINCE OCTOBER 2019
#     # (would req. pdf scrape to get winner results + jackpot info)

#     def start_requests(self):
#         self.name = "MacedoniaLoto7"
#         self.req_proxy = get_UK_proxy()['http']
#         print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)
# 
#         url = "http://old.lotarija.mk/%D0%9B%D0%BE%D1%82%D0%BE-7"
#         yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

#     def parse(self, response):
#         LottoItem = ItemLoader(item=MacedoniaLoto7Item(), selector=response)
#         latest = response.xpath('//table[@id="reportsloto"]//tr')[1]
#         balls_lst = latest.xpath('./td[@class="t"]/text()').getall()[1:]

#         LottoItem.add_value("name", self.name)
#         LottoItem.add_value("draw_datetime", latest.xpath('./td/text()').getall()[1])
#         LottoItem.add_value("draw_number", latest.xpath('./td/text()').get())
#         LottoItem.add_value("ball0", balls_lst[0])
#         LottoItem.add_value("ball1", balls_lst[1])
#         LottoItem.add_value("ball2", balls_lst[2])
#         LottoItem.add_value("ball3", balls_lst[3])
#         LottoItem.add_value("ball4", balls_lst[4])
#         LottoItem.add_value("ball5", balls_lst[5])
#         LottoItem.add_value("ball6", balls_lst[6])
#         if "ДА" in balls_lst[7]:
#             LottoItem.add_value("bonus_ball", '1') # binary i.e. if present == '1'
#         else:
#             LottoItem.add_value("bonus_ball", '0') # if absent then '0'
#         yield LottoItem.load_item()


class MalaysiaJackpot(scrapy.Spider):

    name = "MalaysiaJackpot"

    def start_requests(self):
        self.name = "MalaysiaJackpot"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        headers = {
            'Connection': 'keep-alive',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'Accept': '*/*',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
            'sec-ch-ua-platform': '"Windows"',
            'Origin': 'https://www.magnum4d.my',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://www.magnum4d.my/',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }
        input_date = datetime.now().strftime("%d-%m-%Y")
        url = f"https://app-apdapi-prod-southeastasia-01.azurewebsites.net/results/past/latest-before/{input_date}/9"
        yield scrapy.Request(url=url, headers=headers, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        latest = response.json()['PastResultsRange']['PastResults'][0]
        self.draw_id = latest['DrawID']
        self.cat_1_winners = str(latest['Jackpot1Winner'])
        self.cat_2_winners = str(latest['Jackpot2Winner'])
        self.cat_1_prize = str(latest['Jackpot1Amount'])
        self.cat_2_prize = str(latest['Jackpot2Amount'])
        url = "https://www.magnum4d.my/en/results"
        yield scrapy.Request(url=url, callback=self.parse_draw,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=MalaysiaJackpotItem(), selector=response)
        latest = response.xpath('//div[@id="result-list"]/div')[0]
        draw_info = latest.xpath('.//div[@class="result-card blue"]')[0]
        balls_lst = draw_info.xpath('.//div[@class="col-xs-12 col-p-0"]')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", "+".join(balls_lst[0].xpath(
            './/span[@class="result-number btn-number-details-jp"]/text()').getall()))
        LottoItem.add_value("ball1", "+".join(balls_lst[1].xpath(
            './/span[@class="result-number btn-number-details-jp"]/text()').getall()))
        LottoItem.add_value("ball2", "+".join(balls_lst[2].xpath(
            './/span[@class="result-number btn-number-details-jp"]/text()').getall()))
        LottoItem.add_value("ball3", "+".join(balls_lst[3].xpath(
            './/span[@class="result-number btn-number-details-jp"]/text()').getall()))
        LottoItem.add_value("ball4", "+".join(balls_lst[4].xpath(
            './/span[@class="result-number btn-number-details-jp"]/text()').getall()))
        LottoItem.add_value("ball5", "+".join(balls_lst[5].xpath(
            './/span[@class="result-number btn-number-details-jp"]/text()').getall()))
        draw_date = clean_datetime(latest.xpath('.//h3/span/text()').getall()[2].strip())
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d/%m/%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", self.draw_id)
        LottoItem.add_value("estimated_next_jackpot", draw_info.xpath('.//span[@class="result-price-lg red jackpot-1"]/text()').get())
        LottoItem.add_value("cat_1_prize", self.cat_1_prize)
        LottoItem.add_value("cat_2_prize", self.cat_2_prize)
        LottoItem.add_value("cat_1_winners", self.cat_1_winners)
        LottoItem.add_value("cat_2_winners", self.cat_2_winners)
        yield LottoItem.load_item()


class MalaysiaJackpotGold(scrapy.Spider):

    name = "MalaysiaJackpotGold"

    def start_requests(self):
        self.name = "MalaysiaJackpotGold"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        headers = {
            'Connection': 'keep-alive',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'Accept': '*/*',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
            'sec-ch-ua-platform': '"Windows"',
            'Origin': 'https://www.magnum4d.my',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://www.magnum4d.my/',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }
        input_date = datetime.now().strftime("%d-%m-%Y")
        url = f"https://app-apdapi-prod-southeastasia-01.azurewebsites.net/results/past/latest-before/{input_date}/9"
        yield scrapy.Request(url=url, headers=headers, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        latest = response.json()['PastResultsRange']['PastResults'][0]
        self.draw_id = latest['DrawID']
        self.cat_1_winners = str(latest['GoldJackpot1Winner'])
        self.cat_2_winners = str(latest['GoldJackpot2Winner'])
        self.cat_1_prize = str(latest['GoldJackpot1Amount'])
        self.cat_2_prize = str(latest['GoldJackpot2Amount'])
        url = "https://www.magnum4d.my/en/results"
        yield scrapy.Request(url=url, callback=self.parse_draw,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=MalaysiaJackpotGoldItem(), selector=response)
        latest = response.xpath('//div[@id="result-list"]/div')[0]
        draw_info = latest.xpath('.//div[@class="result-card red"]')[0]
        balls_lst = draw_info.xpath('.//div/b/text()').getall()

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("bonus_ball", "".join(draw_info.xpath('.//b[@class="label-square label-square-lg"]/text()').getall()))
        draw_date = clean_datetime(latest.xpath('.//h3/span/text()').getall()[2].strip())
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d/%m/%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", self.draw_id)
        LottoItem.add_value("estimated_next_jackpot", draw_info.xpath('.//span[@class="result-price-lg red jackpot-1"]/text()').get())
        LottoItem.add_value("cat_1_prize", self.cat_1_prize)
        LottoItem.add_value("cat_2_prize", self.cat_2_prize)
        LottoItem.add_value("cat_1_winners", self.cat_1_winners)
        LottoItem.add_value("cat_2_winners", self.cat_2_winners)
        yield LottoItem.load_item()


class MaltaSuper5(scrapy.Spider):

    name = "MaltaSuper5"

    # draw_datetime too fiddly to scrape

    def start_requests(self):
        self.name = "MaltaSuper5"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.maltco.com/super/results/"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        LottoItem = ItemLoader(item=MaltaSuper5Item(), selector=response)
        balls_lst = response.xpath('//div[@id="div_desktop_result_number_area"]//div[@id="number_style"]/text()').getall()

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("draw_number", response.xpath('//div[@id="div_draw_number"]/text()').get())
        LottoItem.add_value("estimated_next_jackpot", response.xpath(
            '//div[@id="slides"]//div[@id="div_image_2_right_jackpot"]/text()').get())
        match_5 = response.xpath('//div[@id="div_winning_info_area_5_winning_number"]/text()').get()
        if "-" in match_5:
            LottoItem.add_value("cat_1_prize", response.xpath('//div[@id="div_desktop_result_right_area_jackpot"]/text()').get())
        else:
            LottoItem.add_value("cat_1_prize", response.xpath('//div[@id="div_winning_info_area_5_winning_amount"]/text()').get())
        LottoItem.add_value("cat_2_prize", response.xpath('//div[@id="div_winning_info_area_4_winning_amount"]/text()').get())
        LottoItem.add_value("cat_3_prize", response.xpath('//div[@id="div_winning_info_area_3_winning_amount"]/text()').get())
        LottoItem.add_value("cat_1_winners", response.xpath('//div[@id="div_winning_info_area_5_winning_number"]/text()').get())
        LottoItem.add_value("cat_2_winners", response.xpath('//div[@id="div_winning_info_area_4_winning_number"]/text()').get())
        LottoItem.add_value("cat_3_winners", response.xpath('//div[@id="div_winning_info_area_3_winning_number"]/text()').get())
        yield LottoItem.load_item()


class MaltaSuperstar(scrapy.Spider):

    name = "MaltaSuperstar"

    # draw_datetime too fiddly to scrape

    def start_requests(self):
        self.name = "MaltaSuperstar"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.maltco.com/superstar/results/"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        LottoItem = ItemLoader(item=MaltaSuperstarItem(), selector=response)
        balls_lst = response.xpath('//div[@id="div_desktop_result_number_area"]//div[@id="number_style"]/text()').getall()
        winners_lst = response.xpath(
            '//div[@id="div_winning_info_area_text"]//div[@id="div_winning_info_area_winning_number_section"]/text()').getall()
        prizes_lst = response.xpath(
            '//div[@id="div_winning_info_area_text"]//div[@id="div_winning_info_area_winning_amount_section"]/text()').getall()

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("bonus_ball", balls_lst[5])
        LottoItem.add_value("draw_number", response.xpath('//div[@id="div_draw_number"]/text()').get())
        LottoItem.add_value("estimated_next_jackpot", response.xpath(
            '//div[@id="slides"]//div[@id="div_image_2_right_jackpot"]/text()').get())
        if "-" in winners_lst[0]:
            LottoItem.add_value("cat_1_prize", response.xpath('//div[@id="div_desktop_result_right_area_jackpot"]/text()').get())
        else:
            LottoItem.add_value("cat_1_prize", prizes_lst[0])
        LottoItem.add_value("cat_2_prize", prizes_lst[1])
        LottoItem.add_value("cat_3_prize", prizes_lst[2])
        LottoItem.add_value("cat_4_prize", prizes_lst[3])
        LottoItem.add_value("cat_5_prize", prizes_lst[4])
        LottoItem.add_value("cat_6_prize", prizes_lst[5])
        LottoItem.add_value("cat_7_prize", prizes_lst[6])
        LottoItem.add_value("cat_1_winners", winners_lst[0])
        LottoItem.add_value("cat_2_winners", winners_lst[1])
        LottoItem.add_value("cat_3_winners", winners_lst[2])
        LottoItem.add_value("cat_4_winners", winners_lst[3])
        LottoItem.add_value("cat_5_winners", winners_lst[4])
        LottoItem.add_value("cat_6_winners", winners_lst[5])
        LottoItem.add_value("cat_7_winners", winners_lst[6])
        yield LottoItem.load_item()


class MaltaLotto(scrapy.Spider):

    name = "MaltaLotto"

    # NO GAME WINNERS DATA
    # draw_datetime too fiddly to scrape

    def start_requests(self):
        self.name = "MaltaLotto"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.maltco.com/lotto/results/"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        LottoItem = ItemLoader(item=MaltaLottoItem(), selector=response)
        balls_lst = response.xpath('//div[@id="div_desktop_result_number_area"]//div[@id="number_style"]/text()').getall()

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("ball6", balls_lst[6])
        LottoItem.add_value("ball7", balls_lst[7])
        LottoItem.add_value("draw_number", response.xpath('//div[@id="div_draw_number"]/text()').get())
        LottoItem.add_value("estimated_next_jackpot", response.xpath(
            '//div[@id="slides"]//div[@id="div_image_2_right_jackpot"]/text()').get())
        jackpot_winners = response.xpath(
            '//div[@id="div_winning_info_area_text"]//div[@id="div_winning_info_area_winning_number_section"]/text()').get()
        jackpot_prize = response.xpath(
            '//div[@id="div_winning_info_area_text"]//div[@id="div_winning_info_area_winning_amount_section"]/text()').get()
        if "-" in jackpot_winners:
            LottoItem.add_value("cat_1_prize", response.xpath('//div[@id="div_desktop_result_right_area_jackpot"]/text()').get())
        else:
            LottoItem.add_value("cat_1_prize", jackpot_prize)
        LottoItem.add_value("cat_1_winners", jackpot_winners)
        yield LottoItem.load_item()


class MauritiusLoto(scrapy.Spider):

    name = "MauritiusLoto"

    def start_requests(self):
        self.name = "MauritiusLoto"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://loterienationale.mu/fr/tirages-et-archives"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=MauritiusLotoItem(), selector=response)
        balls_lst = [i.strip() for i in response.xpath('//div[@id="num-gagnants"]/text()').get().split(',')]
        rows = response.xpath('//tbody/tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0].strip())
        LottoItem.add_value("ball1", balls_lst[1].strip())
        LottoItem.add_value("ball2", balls_lst[2].strip())
        LottoItem.add_value("ball3", balls_lst[3].strip())
        LottoItem.add_value("ball4", balls_lst[4].strip())
        LottoItem.add_value("ball5", balls_lst[5].strip())
        draw_date = response.xpath('//h3/span[@class="date-display-single"]/@content').get().split('T')[0]
        LottoItem.add_value("draw_datetime", draw_date)
        LottoItem.add_value("sales", response.xpath(
            '//div[@class="views-field views-field-field-montant-total-des-ventes"]/div/text()').get())

        match_6 = rows[0].xpath('./td/text()').getall()[1]
        # jackpot will be '0' unless won, hence use rollover value
        if prize_to_num(match_6) == 0:
            LottoItem.add_value("cat_1_prize", response.xpath(
                '//div[@class="views-field views-field-field-montant-roll-over"]/div/text()').get())
        else:
            LottoItem.add_value("cat_1_prize", rows[0].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_4_prize", rows[3].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./td/text()').getall()[1])
        yield LottoItem.load_item()


class MexicoMelate(scrapy.Spider):

    name = "MexicoMelate"

    def start_requests(self):
        self.name = "MexicoMelate"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "http://www.pronosticos.gob.mx/Melate/Resultados"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy,"download_timeout": 10})

    def parse(self, response):
        self.latest = response.xpath('//table')[0]
        self.balls = self.latest.xpath('.//td[@colspan="8"]/h3/text()').get()
        if "-" in self.balls:
            self.balls = self.balls.replace("-", " ")
        self.balls_lst = [i for i in self.balls.split(' ') if len(i.strip())>0]
        self.rows = self.latest.xpath('.//tr')[3:]
        self.draw_info = self.latest.xpath('.//td[@colspan="8"]/text()').getall()
        url = "https://lotteryguru.com/mexico-lottery-results/mx-melate"
        yield scrapy.Request(url=url, callback=self.parse_next, meta={"proxy": self.req_proxy,"download_timeout": 10})

    def parse_next(self, response):
        LottoItem = ItemLoader(item=MexicoMelateItem(), selector=response)
        jackpot = response.xpath('//div[@class="lg-block lg-lottery-older-results lg-lottery-latest-results"]//div[@class="column is-12 lg-jackpot"]//strong//text()').get()
        check_date = response.xpath('//div[@class="column is-6-tablet is-4-fullhd"]//div[@class="lg-time"]//span[@class="lg-date"]//text()').get()
        check_date = datetime.strptime(check_date, "%d %b %Y").strftime("%Y-%m-%d")
        proj_jackpot = response.xpath('//div[@class="hero-body"]//div[@class="lg-sum"]//text()').get()

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", self.balls_lst[0])
        LottoItem.add_value("ball1", self.balls_lst[1])
        LottoItem.add_value("ball2", self.balls_lst[2])
        LottoItem.add_value("ball3", self.balls_lst[3])
        LottoItem.add_value("ball4", self.balls_lst[4])
        LottoItem.add_value("ball5", self.balls_lst[5])
        LottoItem.add_value("bonus_ball", self.balls_lst[6])
        self.draw_date = clean_datetime(self.draw_info[1].strip())
        self.draw_date = datetime.strptime(self.draw_date, "%d/%m/%Y").strftime("%Y-%m-%d")
        LottoItem.add_value("draw_datetime", self.draw_date)
        LottoItem.add_value("draw_number", self.draw_info[0].strip())
        LottoItem.add_value("estimated_next_jackpot", proj_jackpot)
        LottoItem.add_value("cat_1_prize", jackpot)
        LottoItem.add_value("cat_2_prize", self.rows[1].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_3_prize", self.rows[2].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_4_prize", self.rows[3].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_5_prize", self.rows[4].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_6_prize", self.rows[5].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_7_prize", self.rows[6].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_8_prize", self.rows[7].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_9_prize", self.rows[8].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_1_winners", self.rows[0].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_2_winners", self.rows[1].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_3_winners", self.rows[2].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_4_winners", self.rows[3].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_5_winners", self.rows[4].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_6_winners", self.rows[5].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_7_winners", self.rows[6].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_8_winners", self.rows[7].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_9_winners", self.rows[8].xpath('./td/text()').getall()[2])
        if check_date == self.draw_date:
            yield LottoItem.load_item()
        else:
            pass


class MexicoRevancha(scrapy.Spider):

    name = "MexicoRevancha"

    # Add-on game to Melate

    def start_requests(self):
        self.name = "MexicoRevancha"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://tulotero.mx/resultados/melate"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        jackpot = response.xpath('//div[@class="results"]//div[@class="result"]')
        self.jackpot = jackpot[2].xpath('.//span//text()').getall()[1]
        url = "http://www.pronosticos.gob.mx/Melate/Resultados"
        yield scrapy.Request(url=url, callback=self.parse_next, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse_next(self, response):
        LottoItem = ItemLoader(item=MexicoRevanchaItem(), selector=response)
        latest = response.xpath('//table')[1]
        balls = latest.xpath('.//td[@colspan="8"]//h3/text()').get()
        if u"\xa0" in balls:
            balls = balls.replace(u"\xa0", u" ")
        balls_lst = [i for i in balls.split(' ') if len(i.strip())>0]
        rows = latest.xpath('.//tr')[3:]
        draw_info = latest.xpath('.//td[@colspan="8"]/text()').getall()
        if rows[0].xpath('./td/text()').getall()[2] == '0':
            LottoItem.add_value("cat_1_prize", self.jackpot)
        else:
            LottoItem.add_value("cat_1_prize", rows[0].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        draw_date = clean_datetime(draw_info[1].strip())
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d/%m/%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", draw_info[0].strip())
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_4_prize", rows[3].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_5_prize", rows[4].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_5_winners", rows[4].xpath('./td/text()').getall()[2])
        yield LottoItem.load_item()


class MexicoRevanchita(scrapy.Spider):

    name = "MexicoRevanchita"

    # Add-on game to Melate & Revancha

    def start_requests(self):
        self.name = "MexicoRevanchita"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://tulotero.mx/resultados/melate"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        jackpot = response.xpath('//div[@class="results"]//div[@class="result"]')
        self.jackpot = jackpot[1].xpath('.//span//text()').getall()[1]
        url = "http://www.pronosticos.gob.mx/Melate/Resultados"
        yield scrapy.Request(url=url, callback=self.parse_next, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse_next(self, response):
        LottoItem = ItemLoader(item=MexicoRevanchitaItem(), selector=response)
        latest = response.xpath('//table')[2]
        balls = latest.xpath('.//td[@colspan="8"]/h3/text()').get()
        if u"\xa0" in balls:
            balls = balls.replace(u"\xa0", u" ")
        balls_lst = [i for i in balls.split(' ') if len(i.strip())>0]
        rows = latest.xpath('.//tr')[3:]
        draw_info = latest.xpath('.//td[@colspan="8"]/text()').getall()
        if rows[0].xpath('./td/text()').getall()[2] == '0':
            LottoItem.add_value("cat_1_prize", self.jackpot)
        else:
            LottoItem.add_value("cat_1_prize", rows[0].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        draw_date = clean_datetime(draw_info[1].strip())
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d/%m/%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", draw_info[0].strip())
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td/text()').getall()[2])
        yield LottoItem.load_item()


class MoroccoLoto(scrapy.Spider):

    name = "MoroccoLoto"

    def start_requests(self):
        self.name = "MoroccoLoto"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.eloterie.ma/loto"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        self.next_jackpot = response.xpath('//div[@id="game-gain"]/text()').get().replace(' ','')
        game_id = response.xpath('//span[@id="next-extraction-number"]//text()').get()
        self.latest_game_id = re.sub('[^0-9]','', game_id)
        self.latest_game_id = str(int(self.latest_game_id) - 1)
        self.draw_year = (datetime.now()-timedelta(days=1)).strftime("%Y")
        url = f'https://www.eloterie.ma/detail-du-concours/-/resultats-details/loto/{self.draw_year}/{self.latest_game_id}'
        yield scrapy.Request(url=url, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":10})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=MoroccoLotoItem(), selector=response)
        balls_lst = response.xpath('//div[@class="row searchContainerResults"]/div/span/span/text()').getall()
        rows = response.xpath('//tbody/tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("bonus_ball", balls_lst[6])
        raw_date = response.xpath(
            '//div[@class="result-details-container"]/div/div[@class="col-xs-12 result-details-tirage-label"]/text()').getall()[1]
        draw_date = raw_date.split('-')[0].strip().encode('utf-8').decode('utf-8')
        locale.setlocale(locale.LC_TIME, "fr_FR.ISO8859-1")
        if "avr." in draw_date:
            draw_date = draw_date.replace("avr.", "avril")
        clean_date = datetime.strptime(draw_date, "%a %d %b %Y")
        locale.setlocale(locale.LC_TIME, "en_GB.ISO8859-1")
        LottoItem.add_value("draw_datetime", clean_date.strftime("%Y-%m-%d"))
        LottoItem.add_value("estimated_next_jackpot", self.next_jackpot)
        # prizes will be '0' unless won
        LottoItem.add_value("cat_1_prize", rows[0].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_4_prize", rows[3].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_5_prize", rows[4].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_5_winners", rows[4].xpath('./td/text()').getall()[1])
        yield LottoItem.load_item()


class NetherlandsLotto(scrapy.Spider):

    name = "NetherlandsLotto"

    # NO WINNERS DATA

    def start_requests(self):
        self.name = "NetherlandsLotto"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://lotto.nederlandseloterij.nl/"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        self.next_jackpot = response.xpath('//div[@class="jackpot-banner"]/span/text()').get().strip()
        url = 'https://lotto.nederlandseloterij.nl/trekkingsuitslag'
        yield scrapy.Request(url=url, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":10})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=NetherlandsLottoItem(), selector=response)
        balls_lst = response.xpath('//ul[@class="draw-result"]')[0].xpath('.//span[@class="number"]/text()').getall()

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("bonus_ball", balls_lst[6])
        draw_date = response.xpath('//label/select[@name="date"]/option/@value').get().strip()
        LottoItem.add_value("draw_datetime", draw_date)
        LottoItem.add_value("estimated_next_jackpot", self.next_jackpot)
        yield LottoItem.load_item()

class NetherlandsStateRaffle(scrapy.Spider):
    name = "NetherlandsStateRaffle"

    def start_requests(self):
        self.name = "NetherlandsStateRaffle"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://staatsloterij.nederlandseloterij.nl/trekkingsuitslag"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):

        self.jackpot = response.xpath('//div[@class="jackpot-prize"]//p//text()').get()
        self.jackpot = self.jackpot + ' mil'
        self.jackpot = swap_commas_fullstops(self.jackpot)
        self.raffle_balls = response.xpath('//div[@class="draw-prize-summary-block grid one-third one-quarter-large one-half-small"]//td[@class="ticket-number"]')
        self.raffle_letters = self.raffle_balls.xpath('.//div[@class="ticket-letters"]//text()').getall()
        self.raffle_numbers = self.raffle_balls.xpath('.//div[@class="ticket-numbers"]//text()').getall()
        self.jackpot_winner = response.xpath('//div[@class="jackpot-prize-block-content"]//h3[@class="stl-title-small"]//text()').getall()
        self.date_draw = response.xpath('//header[@class="game-type-theme-reg draw-result-header base-page-block"]//h1[@class="stl-title-medium"]//text()').get()
        self.date_draw = re.sub('.*?10', '10', self.date_draw)
        self.date_draw = self.date_draw.replace('\n', '').replace('\t', '')
        locale.setlocale(locale.LC_TIME, "nl_NL.ISO8859-1")
        self.clean = datetime.strptime(self.date_draw, "%d %B")
        href_date = self.clean - relativedelta(months=1)
        href_date = datetime.strftime(href_date, "%d-%B")
        locale.setlocale(locale.LC_TIME, "en_GB.ISO8859-1")
        today = datetime.today()
        year = today.strftime("%Y")
        self.clean = self.clean.replace(year=int(year))

        if 'niet' in self.jackpot_winner[1]:
            jackpot_balls_left = response.xpath('//p[@class="jackpot-text"]//text()').get()[-2]
            jackpot_balls_left = str(int(jackpot_balls_left) + 1)
            LottoItem = ItemLoader(item=NetherlandsStateRaffleItem(), selector=response)
            LottoItem.add_value("cat_1_winners", str('0'))
            LottoItem.add_value("name", self.name)
            LottoItem.add_value("bonus_ball0", self.raffle_letters[0])
            LottoItem.add_value("bonus_ball1", self.raffle_letters[1])
            LottoItem.add_value("ball0", self.raffle_numbers[0])
            LottoItem.add_value("ball1", self.raffle_numbers[1])
            LottoItem.add_value("ball2", self.raffle_numbers[2])
            LottoItem.add_value("ball3", self.raffle_numbers[3])
            LottoItem.add_value("ball4", self.raffle_numbers[4])
            LottoItem.add_value("cat_1_prize", str(prize_to_num(self.jackpot)))
            LottoItem.add_value("draw_datetime", self.clean.strftime("%Y-%m-%d"))
            LottoItem.add_value("jackpot_balls_left", jackpot_balls_left)

            yield LottoItem.load_item()
        else:
            url = f"https://staatsloterij.nederlandseloterij.nl/trekkingsuitslag/{href_date}-trekking"
            yield scrapy.Request(url=url, callback=self.parse_next, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse_next(self, response):
        LottoItem = ItemLoader(item=NetherlandsStateRaffleItem(), selector=response)
        jackpot_balls_left = response.xpath('//p[@class="jackpot-text"]//text()').get()[-2]
        LottoItem.add_value("cat_1_winners", str('1'))
        LottoItem.add_value("name", self.name)
        LottoItem.add_value("bonus_ball0", self.raffle_letters[0])
        LottoItem.add_value("bonus_ball1", self.raffle_letters[1])
        LottoItem.add_value("ball0", self.raffle_numbers[0])
        LottoItem.add_value("ball1", self.raffle_numbers[1])
        LottoItem.add_value("ball2", self.raffle_numbers[2])
        LottoItem.add_value("ball3", self.raffle_numbers[3])
        LottoItem.add_value("ball4", self.raffle_numbers[4])
        LottoItem.add_value("cat_1_prize", str(prize_to_num(self.jackpot)))
        LottoItem.add_value("draw_datetime", self.clean.strftime("%Y-%m-%d"))
        LottoItem.add_value("jackpot_balls_left", jackpot_balls_left)

        yield LottoItem.load_item()



class NewZealandBullseye(scrapy.Spider):

    name = "NewZealandBullseye"

    def start_requests(self):
        self.name = "NewZealandBullseye"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = 'https://gateway.mylotto.co.nz/api/content/jackpotdata'
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        data = response.json()
        self.jackpot = str(data['bullseye_jackpot'])
        url = 'https://gateway.mylotto.co.nz/api/results/v1/results/bullseye'
        yield scrapy.Request(url=url, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":10})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=NewZealandBullseyeItem(), selector=response)
        latest = response.json()

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("bullseye_number", str(latest['bullseyeWinningNumbers']['numbers']))
        LottoItem.add_value("draw_datetime", str(latest['drawDate']))
        LottoItem.add_value("draw_number", str(latest['drawNumber']))
        # Note: jackpot_won will be '0' unless it is won
        LottoItem.add_value("prize_pool", str(latest['bullseyePrizePool']))
        LottoItem.add_value("estimated_next_jackpot", self.jackpot)
        LottoItem.add_value("cat_1_prize", str(latest['bullseyeWinners'][0]['prizeValue']))
        LottoItem.add_value("cat_2_prize", str(latest['bullseyeWinners'][1]['prizeValue']))
        LottoItem.add_value("cat_3_prize", str(latest['bullseyeWinners'][2]['prizeValue']))
        LottoItem.add_value("cat_4_prize", str(latest['bullseyeWinners'][3]['prizeValue']))
        LottoItem.add_value("cat_5_prize", str(latest['bullseyeWinners'][4]['prizeValue']))
        LottoItem.add_value("cat_6_prize", '2') # prize is free ticket
        LottoItem.add_value("cat_1_winners", str(latest['bullseyeWinners'][0]['numberOfWinners']))
        LottoItem.add_value("cat_2_winners", str(latest['bullseyeWinners'][1]['numberOfWinners']))
        LottoItem.add_value("cat_3_winners", str(latest['bullseyeWinners'][2]['numberOfWinners']))
        LottoItem.add_value("cat_4_winners", str(latest['bullseyeWinners'][3]['numberOfWinners']))
        LottoItem.add_value("cat_5_winners", str(latest['bullseyeWinners'][4]['numberOfWinners']))
        LottoItem.add_value("cat_6_winners", str(latest['bullseyeWinners'][5]['numberOfWinners']))
        if "rolldown" in str(latest['bullseyeWinners'][0]['prizeValue']).lower():
            LottoItem.add_value("rolldown", 'yes')
        else:
            LottoItem.add_value("rolldown", 'no')
        yield LottoItem.load_item()


class NewZealandLotto(scrapy.Spider):

    name = "NewZealandLotto"

    # Fixed prize jackpot but scraped for powerball
    # scraped via lotto.net since NZ API doesn't give cat_1_prize values unless won

    def start_requests(self):
        self.name = "NewZealandLotto"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)
        headers = {
        'authority': 'www.lotto.net',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        # 'cookie': 'ASP.NET_SessionId=doqyx3n0nix2fzqyogeffiiu; _ga=GA1.2.1986781982.1673866307; _gid=GA1.2.761891478.1673866307; _gat=1',
        'referer': 'https://www.lotto.net/new-zealand-powerball/results',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        }
        url = "https://www.lotto.net/new-zealand-lotto/results"
        yield scrapy.Request(url=url, callback=self.parse, headers=headers, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        self.next_jackpot = response.xpath('//div[@class="jackpot"]//span/text()').getall()[1].strip()
        self.draw_date = response.xpath('//div[@class="date"]/span/text()').get().strip()
        next_page = response.xpath("//div[@class='row-3']/a/@href").get()
        url = urljoin(response.url, next_page)
        yield scrapy.Request(url, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":10})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=NewZealandLottoItem(), selector=response)
        balls_lst = response.xpath('//ul[@class="balls"]/li/span/text()').getall()
        rows = response.xpath('//table//tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("bonus_ball", balls_lst[6])
        LottoItem.add_value("draw_datetime", datetime.strptime(self.draw_date, "%d %B %Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("estimated_next_jackpot", self.next_jackpot)
        LottoItem.add_value("cat_1_prize", rows[1].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_2_prize", rows[2].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_3_prize", rows[3].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_4_prize", rows[4].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_5_prize", rows[5].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_6_prize", rows[6].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_7_prize", '2.8') # prize is 4 free QPs
        LottoItem.add_value("cat_1_winners", rows[1].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_2_winners", rows[2].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_3_winners", rows[3].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_4_winners", rows[4].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_5_winners", rows[5].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_6_winners", rows[6].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_7_winners", rows[7].xpath('./td/text()').getall()[-1].strip())
        yield LottoItem.load_item()


class NewZealandPowerball(scrapy.Spider):

    name = "NewZealandPowerball"

    # Add-on game to the NZLotto game; additional powerball_number
    # scraped via lotto.net since NZ API doesn't give cat_1_prize values unless won

    def start_requests(self):
        self.name = "NewZealandPowerball"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)
        headers = {
        'authority': 'www.lotto.net',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        # 'cookie': 'ASP.NET_SessionId=doqyx3n0nix2fzqyogeffiiu; _ga=GA1.2.1986781982.1673866307; _gid=GA1.2.761891478.1673866307; _gat=1',
        'referer': 'https://www.lotto.net/new-zealand-powerball/results',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        }
        url = "https://www.lotto.net/new-zealand-powerball/results"
        yield scrapy.Request(url=url, callback=self.parse,headers=headers, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=NewZealandPowerballItem(), selector=response)
        draw_date = response.xpath('//div[@class="date"]/span/text()').get().strip()
        next_jackpot = response.xpath('//div[@class="jackpot"]//span/text()').getall()[1].strip()
        next_jackpot = prize_to_num(next_jackpot)
        LottoItem.add_value("name", self.name)
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d %B %Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("estimated_next_jackpot", str(next_jackpot))
        yield LottoItem.load_item()


class NewZealandStrike(scrapy.Spider):

    name = "NewZealandStrike"

    # Must match numbers in exact order; i.e. match_4 is matching all 4 numbers in exact order
    # match_3 is matching 3 numbers in exact order, any 3

    def start_requests(self):
        self.name = "NewZealandStrike"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = 'https://gateway.mylotto.co.nz/api/content/jackpotdata'
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        data = response.json()
        self.jackpot = str(data['strike_jackpot'])
        must_be_won = str(data['strike_must_be_won'])
        if 'true' in must_be_won.lower():
            self.rolldown = 'yes'
        else:
            self.rolldown = 'no'
        url = 'https://gateway.mylotto.co.nz/api/results/v1/results/lotto'
        yield scrapy.Request(url=url, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":10})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=NewZealandStrikeItem(), selector=response)
        latest = response.json()['strike']
        lotto = response.json()['lotto']

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", str(latest['strikeWinningNumbers'][0]))
        LottoItem.add_value("ball1", str(latest['strikeWinningNumbers'][1]))
        LottoItem.add_value("ball2", str(latest['strikeWinningNumbers'][2]))
        LottoItem.add_value("ball3", str(latest['strikeWinningNumbers'][3]))
        LottoItem.add_value("draw_datetime", str(lotto['drawDate']))
        LottoItem.add_value("draw_number", str(lotto['drawNumber']))
        LottoItem.add_value("prize_pool", str(latest['strikePrizePool']))
        LottoItem.add_value("estimated_next_jackpot", self.jackpot)
        # Note: jackpot_won will be '0' unless won
        LottoItem.add_value("cat_1_prize", str(latest['strikeWinners'][0]['prizeValue']))
        LottoItem.add_value("cat_2_prize", str(latest['strikeWinners'][1]['prizeValue']))
        LottoItem.add_value("cat_3_prize", str(latest['strikeWinners'][2]['prizeValue']))
        LottoItem.add_value("cat_4_prize", '1') # prize is free ticket
        LottoItem.add_value("cat_1_winners", str(latest['strikeWinners'][0]['numberOfWinners']))
        LottoItem.add_value("cat_2_winners", str(latest['strikeWinners'][1]['numberOfWinners']))
        LottoItem.add_value("cat_3_winners", str(latest['strikeWinners'][2]['numberOfWinners']))
        LottoItem.add_value("cat_4_winners", str(latest['strikeWinners'][3]['numberOfWinners']))
        #if "rolldown" in str(latest['strikeWinners'][0]['prizeValue']).lower():
        LottoItem.add_value("rolldown", self.rolldown)
        yield LottoItem.load_item()


class NorwayLotto(scrapy.Spider):

    name = "NorwayLotto"

    def start_requests(self):
        self.name = "NorwayLotto"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        params = (
            ('fromDate', str(datetime.now().date() - timedelta(days=30))),
            ('toDate', str(datetime.now().date() + timedelta(days=1))),
        )
        url = f'https://api.norsk-tipping.no/LotteryGameInfo/v1/api/results/lotto?{urllib.parse.urlencode(params)}'
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=NorwayLottoItem(), selector=response)
        latest = response.json()['gameResult'][0]
        balls_lst = latest['winnerNumber']

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", str(balls_lst[0]['number']))
        LottoItem.add_value("ball1", str(balls_lst[1]['number']))
        LottoItem.add_value("ball2", str(balls_lst[2]['number']))
        LottoItem.add_value("ball3", str(balls_lst[3]['number']))
        LottoItem.add_value("ball4", str(balls_lst[4]['number']))
        LottoItem.add_value("ball5", str(balls_lst[5]['number']))
        LottoItem.add_value("ball6", str(balls_lst[6]['number']))
        LottoItem.add_value("bonus_ball", str(balls_lst[7]['number']))
        LottoItem.add_value("draw_datetime", str(latest['drawDate']).split('T')[0])
        LottoItem.add_value("draw_number", str(latest['drawId']))
        LottoItem.add_value("sales", str(float(latest['turnover'])))
        LottoItem.add_value("cat_1_prize", str(latest['prize'][0]['value']))
        LottoItem.add_value("cat_2_prize", str(latest['prize'][1]['value']))
        LottoItem.add_value("cat_3_prize", str(latest['prize'][2]['value']))
        LottoItem.add_value("cat_4_prize", str(latest['prize'][3]['value']))
        LottoItem.add_value("cat_5_prize", str(latest['prize'][4]['value']))
        LottoItem.add_value("cat_1_winners", str(latest['prize'][0]['winners']))
        LottoItem.add_value("cat_2_winners", str(latest['prize'][1]['winners']))
        LottoItem.add_value("cat_3_winners", str(latest['prize'][2]['winners']))
        LottoItem.add_value("cat_4_winners", str(latest['prize'][3]['winners']))
        LottoItem.add_value("cat_5_winners", str(latest['prize'][4]['winners']))
        yield LottoItem.load_item()


class PeruTinka(scrapy.Spider):

    name = "PeruTinka"

    # NO NUM OF WINNERS DATA
    # note: official page: https://www.latinka.com.pe/p/
    # But easier to scrape from aggregator site

    def start_requests(self):
        self.name = "PeruTinka"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = 'https://www.thelotter.com/lottery-results/peru-tinka/'
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        LottoItem = ItemLoader(item=PeruTinkaItem(), selector=response)
        balls_lst = response.xpath('//div[@class="results_balls"]//li/span/span/text()').getall()
        raw_datetime = response.xpath('//div[@id="wrapper-ddlDrawNumber"]/select/option[@selected="true"]/text()').get()
        draw_year = raw_datetime.split('/')[0].strip()
        draw_day = " ".join(raw_datetime.split('|')[1].strip().split(' ')[:2])
        draw_date = draw_year + " " + draw_day
        draw_num = raw_datetime.split('|')[0].split('/')[1].strip()

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("bonus_ball", balls_lst[6])
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%Y %d %b").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", draw_num)
        LottoItem.add_value("estimated_next_jackpot", ' '.join(response.xpath(
            '//div[@class="jackpot-text ng-binding"]/span/text()').getall()))
        yield LottoItem.load_item()


class PeruKabala(scrapy.Spider):

    name = "PeruKabala"

    # NO NUM OF WINNERS DATA
    # note: official page: https://www.latinka.com.pe/p/
    # But easier to scrape from aggregator site

    def start_requests(self):
        self.name = "PeruKabala"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = 'https://www.thelotter.com/lottery-results/peru-kabala/'
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        LottoItem = ItemLoader(item=PeruKabalaItem(), selector=response)
        balls_lst = response.xpath('//div[@class="results_balls"]//li/span/span/text()').getall()
        raw_datetime = response.xpath('//div[@id="wrapper-ddlDrawNumber"]/select/option[@selected="true"]/text()').get()
        draw_year = raw_datetime.split('/')[0].strip()
        draw_day = " ".join(raw_datetime.split('|')[1].strip().split(' ')[:2])
        draw_date = draw_year + " " + draw_day
        draw_num = raw_datetime.split('|')[0].split('/')[1].strip()

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%Y %d %b").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", draw_num)
        next_jackpot = ' '.join(response.xpath('//div[@class="jackpot-text ng-binding"]/span/text()').getall())
        if "K" in next_jackpot:
            next_jackpot = next_jackpot.replace("K", "000")
        LottoItem.add_value("estimated_next_jackpot", next_jackpot)
        yield LottoItem.load_item()


class PhilippinesLotto6x58(scrapy.Spider):

    name = "PhilippinesLotto6x58"

    # scrape will fail whilst latest draw data is being loaded

    def start_requests(self):
        self.name = "PhilippinesLotto6x58"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.philippinepcsolotto.com/results/6-58-lotto-results"
        headers = {
            'authority': 'philippinepcsolotto.com',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
            'sec-ch-ua-mobile': '?0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'cookie': '_ga=GA1.2.465908668.1610974140; __cfduid=d2555bb5a9960a834b17cbd7c4d599bbd1618561764; _gid=GA1.2.837889524.1619425231; _gat_gtag_UA_41199028_1=1',
        }
        yield scrapy.Request(url=url, callback=self.parse, headers=headers,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        LottoItem = ItemLoader(item=PhilippinesLotto6x58Item(), selector=response)
        rows = response.xpath('//table[@class="major-results"]//tr')
        balls_lst = rows[2].xpath('./td/text()').getall()[-1].strip().split('-')
        jackpot = prize_to_num(rows[3].xpath('./td/text()').getall()[-1].strip())
        jackpot_winners = prize_to_num(rows[4].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        draw_date = rows[1].xpath('./td/text()').getall()[-1].strip()
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%B %d, %Y").strftime("%Y-%m-%d"))

        if jackpot_winners > 0:
            jackpot = jackpot/jackpot_winners
        LottoItem.add_value("cat_1_prize", str(jackpot))
        LottoItem.add_value("cat_1_winners", str(jackpot_winners))
        if int(jackpot) == 0:
            pass
        else:
            yield LottoItem.load_item()


class PhilippinesLotto6x55(scrapy.Spider):

    name = "PhilippinesLotto6x55"

    # scrape will fail whilst latest draw data is being loaded

    def start_requests(self):
        self.name = "PhilippinesLotto6x55"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.philippinepcsolotto.com/results/6-55-lotto-results"
        headers = {
            'authority': 'philippinepcsolotto.com',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
            'sec-ch-ua-mobile': '?0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'cookie': '_ga=GA1.2.465908668.1610974140; __cfduid=d2555bb5a9960a834b17cbd7c4d599bbd1618561764; _gid=GA1.2.837889524.1619425231; _gat_gtag_UA_41199028_1=1',
        }
        yield scrapy.Request(url=url, callback=self.parse, headers=headers,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        LottoItem = ItemLoader(item=PhilippinesLotto6x55Item(), selector=response)
        rows = response.xpath('//table[@class="major-results"]//tr')
        balls_lst = rows[2].xpath('./td/text()').getall()[-1].strip().split('-')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        draw_date = rows[1].xpath('./td/text()').getall()[-1].strip()
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%B %d, %Y").strftime("%Y-%m-%d"))
        jackpot = prize_to_num(rows[3].xpath('./td/text()').getall()[-1].strip())
        jackpot_winners = prize_to_num(rows[4].xpath('./td/text()').getall()[-1].strip())
        if jackpot_winners > 0:
            jackpot = jackpot/jackpot_winners
        LottoItem.add_value("cat_1_prize", str(jackpot))
        LottoItem.add_value("cat_1_winners", str(jackpot_winners))
        if int(jackpot) == 0:
            pass
        else:
            yield LottoItem.load_item()


class PhilippinesLotto6x49(scrapy.Spider):

    name = "PhilippinesLotto6x49"

    # scrape will fail whilst latest draw data is being loaded

    def start_requests(self):
        self.name = "PhilippinesLotto6x49"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.philippinepcsolotto.com/results/6-49-lotto-results"
        headers = {
            'authority': 'philippinepcsolotto.com',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
            'sec-ch-ua-mobile': '?0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'cookie': '_ga=GA1.2.465908668.1610974140; __cfduid=d2555bb5a9960a834b17cbd7c4d599bbd1618561764; _gid=GA1.2.837889524.1619425231; _gat_gtag_UA_41199028_1=1',
        }
        yield scrapy.Request(url=url, callback=self.parse, headers=headers,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        LottoItem = ItemLoader(item=PhilippinesLotto6x49Item(), selector=response)
        rows = response.xpath('//table[@class="major-results"]//tr')
        balls_lst = rows[2].xpath('./td/text()').getall()[-1].strip().split('-')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        draw_date = rows[1].xpath('./td/text()').getall()[-1].strip()
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%B %d, %Y").strftime("%Y-%m-%d"))
        jackpot = prize_to_num(rows[3].xpath('./td/text()').getall()[-1].strip())
        jackpot_winners = prize_to_num(rows[4].xpath('./td/text()').getall()[-1].strip())
        if jackpot_winners > 0:
            jackpot = jackpot/jackpot_winners
        LottoItem.add_value("cat_1_prize", str(jackpot))
        LottoItem.add_value("cat_1_winners", str(jackpot_winners))
        if int(jackpot) == 0:
            pass
        else:
            yield LottoItem.load_item()


class PhilippinesLotto6x45(scrapy.Spider):

    name = "PhilippinesLotto6x45"

    # scrape will fail whilst latest draw data is being loaded

    def start_requests(self):
        self.name = "PhilippinesLotto6x45"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.philippinepcsolotto.com/results/6-45-lotto-results"
        headers = {
            'authority': 'philippinepcsolotto.com',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
            'sec-ch-ua-mobile': '?0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'cookie': '_ga=GA1.2.465908668.1610974140; __cfduid=d2555bb5a9960a834b17cbd7c4d599bbd1618561764; _gid=GA1.2.837889524.1619425231; _gat_gtag_UA_41199028_1=1',
        }
        yield scrapy.Request(url=url, callback=self.parse, headers=headers,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        LottoItem = ItemLoader(item=PhilippinesLotto6x45Item(), selector=response)
        rows = response.xpath('//table[@class="major-results"]//tr')
        balls_lst = rows[2].xpath('./td/text()').getall()[-1].strip().split('-')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        draw_date = rows[1].xpath('./td/text()').getall()[-1].strip()
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%B %d, %Y").strftime("%Y-%m-%d"))
        jackpot = prize_to_num(rows[3].xpath('./td/text()').getall()[-1].strip())
        jackpot_winners = prize_to_num(rows[4].xpath('./td/text()').getall()[-1].strip())
        if jackpot_winners > 0:
            jackpot = jackpot/jackpot_winners
        LottoItem.add_value("cat_1_prize", str(jackpot))
        LottoItem.add_value("cat_1_winners", str(jackpot_winners))
        if int(jackpot) == 0:
            pass
        else:
            yield LottoItem.load_item()


class PhilippinesLotto6x42(scrapy.Spider):

    name = "PhilippinesLotto6x42"

    # scrape will fail whilst latest draw data is being loaded

    def start_requests(self):
        self.name = "PhilippinesLotto6x42"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.philippinepcsolotto.com/results/6-42-lotto-results"
        headers = {
            'authority': 'philippinepcsolotto.com',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
            'sec-ch-ua-mobile': '?0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'cookie': '_ga=GA1.2.465908668.1610974140; __cfduid=d2555bb5a9960a834b17cbd7c4d599bbd1618561764; _gid=GA1.2.837889524.1619425231; _gat_gtag_UA_41199028_1=1',
        }
        yield scrapy.Request(url=url, callback=self.parse, headers=headers,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        LottoItem = ItemLoader(item=PhilippinesLotto6x42Item(), selector=response)
        rows = response.xpath('//table[@class="major-results"]//tr')
        balls_lst = rows[2].xpath('./td/text()').getall()[-1].strip().split('-')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        draw_date = rows[1].xpath('./td/text()').getall()[-1].strip()
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%B %d, %Y").strftime("%Y-%m-%d"))
        jackpot = prize_to_num(rows[3].xpath('./td/text()').getall()[-1].strip())
        jackpot_winners = prize_to_num(rows[4].xpath('./td/text()').getall()[-1].strip())
        if jackpot_winners > 0:
            jackpot = jackpot/jackpot_winners
        LottoItem.add_value("cat_1_prize", str(jackpot))
        LottoItem.add_value("cat_1_winners", str(jackpot_winners))
        if int(jackpot) == 0:
            pass
        else:
            yield LottoItem.load_item()


class PolandLotto(scrapy.Spider):

    name = "PolandLotto"

    def start_requests(self):
        self.name = "PolandLotto"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        headers = {
            'authority': 'www.lotto.pl',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
            'accept': 'application/json, text/plain, */*',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.lotto.pl/lotto',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'cookie': 'ai_user=c6+5O|2021-01-11T12:14:50.173Z; _ga=GA1.2.1702929379.1610367291; _hjTLDTest=1; _hjid=9f392d91-db9d-43b0-afa9-915d1beb5bb8; _gcl_au=1.1.1336877857.1619089498; _gid=GA1.2.1417254208.1619438635; _hjAbsoluteSessionInProgress=1; ai_session=eCL3Sg7jUhqkmlB6rUc7G6|1619438634138|1619438706863; _gat_UA-8741095-1=1',
        }
        url = "https://www.lotto.pl/api/lotteries/info/play-banner?gameType=Lotto"
        yield scrapy.Request(url=url, headers=headers, callback=self.parse_jackpot, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse_jackpot(self, response):
        self.next_jackpot = response.json()['closestPrizeValue']
        url = "https://www.lotto.pl/lotto/wyniki-i-wygrane"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        latest = response.xpath('//div[@class="recent-results-box"]')[0]
        self.balls_lst = latest.xpath(
            './/div[@class="result-item__balls-box"]/div[@class="scoreline-item circle"]//text()').getall()
        self.draw_number = latest.xpath('.//p[@class="result-item__number"]/text()').get().strip()
        headers = {
            'authority': 'www.lotto.pl',
            'accept': 'application/json, text/plain, */*',
            'request-id': '|2749131d19964ec28b2138786c32dcba.16024ddf2a0b4018',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
            'request-context': 'appId=cid-v1:c0da44c9-9395-4569-bfd2-2d0363a264f0',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.lotto.pl/lotto/wyniki-i-wygrane',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'cookie': '_hjid=07c60336-f51d-4b01-9db3-ad9b41ef98af; __utmc=23770919; __utmz=23770919.1584984978.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ga=GA1.2.174648639.1584984978; __utma=23770919.174648639.1584984978.1591780519.1591811665.24; ai_user=j+QQz|2020-06-26T13:12:31.394Z; _gid=GA1.2.384538263.1598437450; _hjAbsoluteSessionInProgress=0; ai_session=LHoP6|1598437449051.68|1598437531855.345',
        }
        root_url = "https://www.lotto.pl/api/lotteries/draw-prizes?drawType=Lotto&drawSystemId="
        url = root_url + self.draw_number
        yield scrapy.Request(url=url, callback=self.parse_draw, headers=headers)

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=PolandLottoItem(), selector=response)
        balls_lst = self.balls_lst
        data = response.json()[0]

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("draw_datetime", str(data['drawDate']).split('T')[0])
        LottoItem.add_value("draw_number", self.draw_number)
        LottoItem.add_value("estimated_next_jackpot", str(self.next_jackpot))
        LottoItem.add_value("cat_1_prize", str(data['prizes']['1']['prizeValue']))
        LottoItem.add_value("cat_2_prize", str(data['prizes']['2']['prizeValue']))
        LottoItem.add_value("cat_3_prize", str(data['prizes']['3']['prizeValue']))
        LottoItem.add_value("cat_4_prize", str(data['prizes']['4']['prizeValue']))
        LottoItem.add_value("cat_1_winners", str(data['prizes']['1']['prize']))
        LottoItem.add_value("cat_2_winners", str(data['prizes']['2']['prize']))
        LottoItem.add_value("cat_3_winners", str(data['prizes']['3']['prize']))
        LottoItem.add_value("cat_4_winners", str(data['prizes']['4']['prize']))
        yield LottoItem.load_item()



class PortugalLottoToto(scrapy.Spider):

    name = "PortugalLottoToto"

    def start_requests(self):
        self.name = "PortugalLottoToto"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.jogossantacasa.pt/web/SCCartazResult/totolotoNew"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        LottoItem = ItemLoader(item=PortugalLottoTotoItem(), selector=response)
        balls_lst = response.xpath(
            '//div[@class="betMiddle twocol regPad"]/ul[@class="colums"]/li/text()').get().split(' ')
        bonus_ball = response.xpath(
            '//div[@class="betMiddle twocol regPad"]/ul[@class="colums"]/li/text()').get().split('+')[1].strip()
        rows = response.xpath('//div[@class="stripped betMiddle fourcol regPad"]/ul')
        raw_game_info = response.xpath('//div[@class="betMiddle twocol"]/ul[@class="noLine"]/li//text()').getall()
        game_info = [info.lower().strip() for info in raw_game_info if len(info.strip()) > 1]

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("bonus_ball", bonus_ball)
        draw_date = response.xpath('//span[@class="dataInfo"]/text()').getall()[1].split('-')[-1].strip()
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d/%m/%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", response.xpath(
            '//span[@class="dataInfo"]/text()').get().split(':')[1].split('/20')[0].strip())
        LottoItem.add_value("tickets", game_info[3])
        LottoItem.add_value("sales", game_info[5])
        LottoItem.add_value("prize_pool", game_info[7])
        if prize_to_num(rows[0].xpath('./li/text()').getall()[2].strip()) == 0:
            LottoItem.add_value("cat_1_prize", game_info[-1])
        else:
            LottoItem.add_value("cat_1_prize", rows[0].xpath('./li/text()').getall()[3])
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./li/text()').getall()[3])
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./li/text()').getall()[3])
        LottoItem.add_value("cat_4_prize", rows[3].xpath('./li/text()').getall()[3])
        LottoItem.add_value("cat_5_prize", rows[4].xpath('./li/text()').getall()[3])
        LottoItem.add_value("cat_6_prize", '0.9') # prize is refund of ticket price
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./li/text()').getall()[2])
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./li/text()').getall()[2])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./li/text()').getall()[2])
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./li/text()').getall()[2])
        LottoItem.add_value("cat_5_winners", rows[4].xpath('./li/text()').getall()[2])
        LottoItem.add_value("cat_6_winners", rows[5].xpath('./li/text()').getall()[2])
        yield LottoItem.load_item()

class RomaniaLoto6x49(scrapy.Spider):

    name = "RomaniaLoto6x49"

    def start_requests(self):
        self.name = "RomaniaLoto6x49"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.loto.ro/loto-new/newLotoSiteNexioFinalVersion/web/app2.php/jocuri/649_si_noroc/rezultate_extragere.html"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=RomaniaLoto6x49Item(), selector=response)
        latest = response.xpath('//div[@class="rezultate-extrageri-content resultDiv "]')[0]
        balls_lst = [i.split('.png')[0].split('/')[-1] for i in latest.xpath('.//img/@src').getall()]
        rows = latest.xpath('.//tbody/tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        draw_date = latest.xpath('.//p/span//text()').get()
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d.%m.%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("prize_pool", rows[4].xpath('./td/strong/text()').get())

        cat_1_winners = rows[0].xpath('./td//text()').getall()[1]
        if "report" in cat_1_winners.lower():
            LottoItem.add_value("jackpot_increase", rows[0].xpath('./td/text()').getall()[2])
            LottoItem.add_value("cat_1_prize", rows[0].xpath('./td/text()').getall()[-1])
        else:
            LottoItem.add_value("jackpot_increase", '0')
            LottoItem.add_value("cat_1_prize", rows[0].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./td//text()').getall()[2])
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./td//text()').getall()[2])
        LottoItem.add_value("cat_4_prize", rows[3].xpath('./td//text()').getall()[2])
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td//text()').getall()[1])
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./td//text()').getall()[1])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./td//text()').getall()[1])
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./td//text()').getall()[1])
        yield LottoItem.load_item()


class RomaniaLoto5x40(scrapy.Spider):

    name = "RomaniaLoto5x40"

    def start_requests(self):
        self.name = "RomaniaLoto5x40"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.loto.ro/loto-new/newLotoSiteNexioFinalVersion/web/app2.php/jocuri/540_si_super_noroc/rezultate_extrageri.html"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=RomaniaLoto5x40Item(), selector=response)
        latest = response.xpath('//div[@class="rezultate-extrageri-content resultDiv "]')[0]
        balls_lst = [i.split('.png')[0].split('/')[-1] for i in latest.xpath('.//img/@src').getall()]
        rows = latest.xpath('.//tbody/tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        draw_date = latest.xpath('.//p/span//text()').get()
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d.%m.%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("prize_pool", rows[3].xpath('./td/strong/text()').get())

        cat_1_winners = rows[0].xpath('./td//text()').getall()[1]
        if "report" in cat_1_winners.lower():
            LottoItem.add_value("jackpot_increase", rows[0].xpath('./td/text()').getall()[2])
            LottoItem.add_value("cat_1_prize", rows[0].xpath('./td/text()').getall()[-1])
        else:
            LottoItem.add_value("jackpot_increase", '0')
            LottoItem.add_value("cat_1_prize", rows[0].xpath('./td/text()').getall()[2])
        cat_2_winners = rows[1].xpath('./td//text()').getall()[1]
        if "report" in cat_2_winners.lower():
            LottoItem.add_value("cat_2_prize", rows[1].xpath('./td/text()').getall()[-1])
        else:
            LottoItem.add_value("cat_2_prize", rows[1].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./td//text()').getall()[2])
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td//text()').getall()[1])
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./td//text()').getall()[1])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./td//text()').getall()[1])
        yield LottoItem.load_item()


class RomaniaJoker(scrapy.Spider):

    name = "RomaniaJoker"

    # 45C5 + 20C1 game; not "traditional" game

    def start_requests(self):
        self.name = "RomaniaJoker"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.loto.ro/loto-new/newLotoSiteNexioFinalVersion/web/app2.php/jocuri/joker_si_noroc_plus/rezultate_extrageri.html"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=RomaniaJokerItem(), selector=response)
        latest = response.xpath('//div[@class="rezultate-extrageri-content resultDiv "]')[0]
        balls_lst = [i.split('.png')[0].split('/')[-1] for i in latest.xpath('.//img/@src').getall()]
        rows = latest.xpath('.//tbody/tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("bonus_ball", balls_lst[5])
        draw_date = latest.xpath('.//p/span//text()').get()
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d.%m.%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("prize_pool", rows[8].xpath('./td/strong/text()').get())

        cat_1_winners = rows[0].xpath('./td//text()').getall()[1]
        if "report" in cat_1_winners.lower():
            LottoItem.add_value("jackpot_increase", rows[0].xpath('./td/text()').getall()[2])
            LottoItem.add_value("cat_1_prize", rows[0].xpath('./td/text()').getall()[-1])
        else:
            LottoItem.add_value("jackpot_increase", '0')
            LottoItem.add_value("cat_1_prize", rows[0].xpath('./td/text()').getall()[2])
        cat_2_winners = rows[1].xpath('./td//text()').getall()[1]
        if "report" in cat_2_winners.lower():
            LottoItem.add_value("cat_2_prize", rows[1].xpath('./td/text()').getall()[-1])
        else:
            LottoItem.add_value("cat_2_prize", rows[1].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./td//text()').getall()[2])
        LottoItem.add_value("cat_4_prize", rows[3].xpath('./td//text()').getall()[2])
        LottoItem.add_value("cat_5_prize", rows[4].xpath('./td//text()').getall()[2])
        LottoItem.add_value("cat_6_prize", rows[5].xpath('./td//text()').getall()[2])
        LottoItem.add_value("cat_7_prize", rows[6].xpath('./td//text()').getall()[2])
        LottoItem.add_value("cat_8_prize", rows[7].xpath('./td//text()').getall()[2])
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td//text()').getall()[1])
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./td//text()').getall()[1])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./td//text()').getall()[1])
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./td//text()').getall()[1])
        LottoItem.add_value("cat_5_winners", rows[4].xpath('./td//text()').getall()[1])
        LottoItem.add_value("cat_6_winners", rows[5].xpath('./td//text()').getall()[1])
        LottoItem.add_value("cat_7_winners", rows[6].xpath('./td//text()').getall()[1])
        LottoItem.add_value("cat_8_winners", rows[7].xpath('./td//text()').getall()[1])
        yield LottoItem.load_item()


class RussiaLoto7x49(scrapy.Spider):

    name = "RussiaLoto7x49"

    def start_requests(self):
        self.name = "RussiaLoto7x49"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://stoloto.ru/7x49/archive"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        latest = response.xpath('//div[@class="data drawings_data"]//div[@class="elem"]')[0]
        self.balls_lst = [i.strip() for i in latest.xpath('.//div[@class="numbers"]//span/b/text()').getall()]
        self.draw_number = latest.xpath('.//div[@class="draw"]/a/text()').get()
        self.draw_datetime = latest.xpath('.//div[@class="draw_date"]/text()').get()
        self.jackpot = latest.xpath('.//div[@class="prize  "]/text()').get().strip()
        next_page = latest.xpath('.//div[@class="draw"]/a/@href').get()
        url = urljoin(response.url, next_page)
        yield scrapy.Request(url=url, callback=self.parse_draw,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=RussiaLoto7x49Item(), selector=response)
        rows = response.xpath('//div[@class="col prizes"]//tbody/tr')
        details_rows = response.xpath('//div[@class="col drawing_details"]//tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", self.balls_lst[0])
        LottoItem.add_value("ball1", self.balls_lst[1])
        LottoItem.add_value("ball2", self.balls_lst[2])
        LottoItem.add_value("ball3", self.balls_lst[3])
        LottoItem.add_value("ball4", self.balls_lst[4])
        LottoItem.add_value("ball5", self.balls_lst[5])
        LottoItem.add_value("ball6", self.balls_lst[6])
        LottoItem.add_value("draw_datetime", datetime.strptime(self.draw_datetime, "%d.%m.%Y %H:%M").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", self.draw_number)
        LottoItem.add_value("tickets", details_rows[1].xpath('./td[@class="numeric"]/text()').get())
        if prize_to_num(rows[0].xpath('./td//text()').getall()[1].strip()) == 0:
            LottoItem.add_value("cat_1_prize", self.jackpot)
        else:
            LottoItem.add_value("cat_1_prize", rows[0].xpath('./td//text()').getall()[2])
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./td//text()').getall()[2])
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./td//text()').getall()[2])
        LottoItem.add_value("cat_4_prize", rows[3].xpath('./td//text()').getall()[2])
        LottoItem.add_value("cat_5_prize", rows[4].xpath('./td//text()').getall()[2])
        LottoItem.add_value("cat_6_prize", rows[5].xpath('./td//text()').getall()[2])
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td//text()').getall()[1])
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./td//text()').getall()[1])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./td//text()').getall()[1])
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./td//text()').getall()[1])
        LottoItem.add_value("cat_5_winners", rows[4].xpath('./td//text()').getall()[1])
        LottoItem.add_value("cat_6_winners", rows[5].xpath('./td//text()').getall()[1])
        yield LottoItem.load_item()


class RussiaLoto6x45(scrapy.Spider):

    name = "RussiaLoto6x45"

    def start_requests(self):
        self.name = "RussiaLoto6x45"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://stoloto.ru/6x45/archive"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        latest = response.xpath('//div[@class="data drawings_data"]//div[@class="elem"]')[0]
        self.balls_lst = [i.strip() for i in latest.xpath('.//div[@class="numbers"]//span/b/text()').getall()]
        self.draw_number = latest.xpath('.//div[@class="draw"]/a/text()').get()
        self.draw_datetime = latest.xpath('.//div[@class="draw_date"]/text()').get()
        self.jackpot = latest.xpath('.//div[@class="prize  "]/text()').get().strip()
        next_page = latest.xpath('.//div[@class="draw"]/a/@href').get()
        url = urljoin(response.url, next_page)
        yield scrapy.Request(url=url, callback=self.parse_draw,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=RussiaLoto6x45Item(), selector=response)
        rows = response.xpath('//div[@class="col prizes"]//tbody/tr')
        details_rows = response.xpath('//div[@class="col drawing_details"]//tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", self.balls_lst[0])
        LottoItem.add_value("ball1", self.balls_lst[1])
        LottoItem.add_value("ball2", self.balls_lst[2])
        LottoItem.add_value("ball3", self.balls_lst[3])
        LottoItem.add_value("ball4", self.balls_lst[4])
        LottoItem.add_value("ball5", self.balls_lst[5])
        LottoItem.add_value("draw_datetime", datetime.strptime(self.draw_datetime, "%d.%m.%Y %H:%M").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", self.draw_number)
        LottoItem.add_value("tickets", details_rows[1].xpath('./td[@class="numeric"]/text()').get())
        if prize_to_num(rows[0].xpath('./td//text()').getall()[1].strip()) == 0:
            LottoItem.add_value("cat_1_prize", self.jackpot)
        else:
            LottoItem.add_value("cat_1_prize", rows[0].xpath('./td//text()').getall()[2])
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./td//text()').getall()[2])
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./td//text()').getall()[2])
        LottoItem.add_value("cat_4_prize", rows[3].xpath('./td//text()').getall()[2])
        LottoItem.add_value("cat_5_prize", rows[4].xpath('./td//text()').getall()[2])
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td//text()').getall()[1])
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./td//text()').getall()[1])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./td//text()').getall()[1])
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./td//text()').getall()[1])
        LottoItem.add_value("cat_5_winners", rows[4].xpath('./td//text()').getall()[1])
        yield LottoItem.load_item()


class RussiaLoto5x36(scrapy.Spider):

    name = "RussiaLoto5x36"

    # jackpot = match_5_bonus, secondary_jackpot = match_5
    # note: jackpot value can be larger than super_jackpot

    def start_requests(self):
        self.name = "RussiaLoto5x36"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://stoloto.ru/5x36plus/archive"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        latest = response.xpath('//div[@class="data drawings_data"]//div[@class="elem"]')[0]
        self.balls_lst = [i.strip() for i in latest.xpath('.//div[@class="numbers"]//span/b/text()').getall()]
        self.draw_number = latest.xpath('.//div[@class="draw"]/a/text()').get()
        self.draw_datetime = latest.xpath('.//div[@class="draw_date"]/text()').get()
        next_page = latest.xpath('.//div[@class="draw"]/a/@href').get()
        url = urljoin(response.url, next_page)
        yield scrapy.Request(url=url, callback=self.parse_draw,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=RussiaLoto5x36Item(), selector=response)
        rows = response.xpath('//div[@class="col prizes"]//tbody/tr')
        details_rows = response.xpath('//div[@class="col drawing_details"]//tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", self.balls_lst[0])
        LottoItem.add_value("ball1", self.balls_lst[1])
        LottoItem.add_value("ball2", self.balls_lst[2])
        LottoItem.add_value("ball3", self.balls_lst[3])
        LottoItem.add_value("ball4", self.balls_lst[4])
        LottoItem.add_value("bonus_ball", self.balls_lst[5])
        LottoItem.add_value("draw_datetime", datetime.strptime(self.draw_datetime, "%d.%m.%Y %H:%M").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", self.draw_number)
        LottoItem.add_value("tickets", details_rows[1].xpath('./td[@class="numeric"]/text()').get())
        if prize_to_num(rows[0].xpath('./td//text()').getall()[1].strip()) == 0:
            LottoItem.add_value("cat_1_prize", details_rows[3].xpath('./td[@class="numeric"]/text()').get())
        else:
            LottoItem.add_value("cat_1_prize", rows[0].xpath('./td//text()').getall()[2])
        if prize_to_num(rows[1].xpath('./td//text()').getall()[1].strip()) == 0:
            LottoItem.add_value("cat_2_prize", details_rows[4].xpath('./td[@class="numeric"]/text()').get())
        else:
            LottoItem.add_value("cat_2_prize", rows[1].xpath('./td//text()').getall()[2])
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./td//text()').getall()[2])
        LottoItem.add_value("cat_4_prize", rows[3].xpath('./td//text()').getall()[2])
        LottoItem.add_value("cat_5_prize", rows[4].xpath('./td//text()').getall()[2])
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td//text()').getall()[1])
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./td//text()').getall()[1])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./td//text()').getall()[1])
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./td//text()').getall()[1])
        LottoItem.add_value("cat_5_winners", rows[4].xpath('./td//text()').getall()[1])
        yield LottoItem.load_item()


class RussiaLoto4x20(scrapy.Spider):

    name = "RussiaLoto4x20"

    # note: technically two sets of 4 numbers (set1 = ball0-ball3, set2 = ball4-ball7)

    def start_requests(self):
        self.name = "RussiaLoto4x20"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://stoloto.ru/4x20/archive"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        try:
            latest = response.xpath('//div[@class="data drawings_data"]//div[@class="elem"]')[0]
            self.balls_lst = [i.strip() for i in latest.xpath('.//div[@class="numbers"]//span/b/text()').getall()]
            check_draw_test = self.balls_lst[1]
            self.draw_number = latest.xpath('.//div[@class="draw"]/a/text()').get()
            self.draw_datetime = latest.xpath('.//div[@class="draw_date"]/text()').get()
            self.jackpot = latest.xpath('.//div[@class="prize  "]/text()').get().strip()
            next_page = latest.xpath('.//div[@class="draw"]/a/@href').get()
        except IndexError:
            latest = response.xpath('//div[@class="data drawings_data"]//div[@class="elem"]')[1]
            self.balls_lst = [i.strip() for i in latest.xpath('.//div[@class="numbers"]//span/b/text()').getall()]
            self.draw_number = latest.xpath('.//div[@class="draw"]/a/text()').get()
            self.draw_datetime = latest.xpath('.//div[@class="draw_date"]/text()').get()
            self.jackpot = latest.xpath('.//div[@class="prize  "]/text()').get().strip()
            next_page = latest.xpath('.//div[@class="draw"]/a/@href').get()
        url = urljoin(response.url, next_page)
        yield scrapy.Request(url=url, callback=self.parse_draw,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=RussiaLoto4x20Item(), selector=response)
        rows = response.xpath('//div[@class="col prizes"]//tbody/tr')
        details_rows = response.xpath('//div[@class="col drawing_details"]//tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", self.balls_lst[0])
        LottoItem.add_value("ball1", self.balls_lst[1])
        LottoItem.add_value("ball2", self.balls_lst[2])
        LottoItem.add_value("ball3", self.balls_lst[3])
        LottoItem.add_value("ball4", self.balls_lst[4])
        LottoItem.add_value("ball5", self.balls_lst[5])
        LottoItem.add_value("ball6", self.balls_lst[6])
        LottoItem.add_value("ball7", self.balls_lst[7])
        LottoItem.add_value("draw_datetime", datetime.strptime(self.draw_datetime, "%d.%m.%Y %H:%M").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", self.draw_number)
        LottoItem.add_value("tickets", details_rows[1].xpath('./td[@class="numeric"]/text()').get())
        if prize_to_num(rows[0].xpath('./td//text()').getall()[-3].strip()) == 0:
            LottoItem.add_value("cat_1_prize", self.jackpot)
        else:
            LottoItem.add_value("cat_1_prize", rows[0].xpath('./td//text()').getall()[-2])
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./td//text()').getall()[-2])
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./td//text()').getall()[-2])
        LottoItem.add_value("cat_4_prize", rows[3].xpath('./td//text()').getall()[-2])
        LottoItem.add_value("cat_5_prize", rows[4].xpath('./td//text()').getall()[-2])
        LottoItem.add_value("cat_6_prize", rows[5].xpath('./td//text()').getall()[-2])
        LottoItem.add_value("cat_7_prize", rows[6].xpath('./td//text()').getall()[-2])
        LottoItem.add_value("cat_8_prize", rows[7].xpath('./td//text()').getall()[-2])
        LottoItem.add_value("cat_9_prize", rows[8].xpath('./td//text()').getall()[-2])
        LottoItem.add_value("cat_10_prize", rows[9].xpath('./td//text()').getall()[-2])
        LottoItem.add_value("cat_11_prize", rows[10].xpath('./td//text()').getall()[-2])
        LottoItem.add_value("cat_12_prize", rows[11].xpath('./td//text()').getall()[-2])
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td/text()').getall()[-3])
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./td/text()').getall()[-3])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./td/text()').getall()[-3])
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./td/text()').getall()[-3])
        LottoItem.add_value("cat_5_winners", rows[4].xpath('./td/text()').getall()[-3])
        LottoItem.add_value("cat_6_winners", rows[5].xpath('./td/text()').getall()[-3])
        LottoItem.add_value("cat_7_winners", rows[6].xpath('./td/text()').getall()[-3])
        LottoItem.add_value("cat_8_winners", rows[7].xpath('./td/text()').getall()[-3])
        LottoItem.add_value("cat_9_winners", rows[8].xpath('./td/text()').getall()[-3])
        LottoItem.add_value("cat_10_winners", rows[9].xpath('./td/text()').getall()[-3])
        LottoItem.add_value("cat_11_winners", rows[10].xpath('./td/text()').getall()[-3])
        LottoItem.add_value("cat_12_winners", rows[11].xpath('./td/text()').getall()[-3])
        yield LottoItem.load_item()


class SamoaLotto(scrapy.Spider):

    name = "SamoaLotto"
    def start_requests(self):
        self.name = "SamoaLotto"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.gca.gov.ws/sports-lotto/samoa-national-lotto/"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        LottoItem = ItemLoader(item=SamoaLottoItem(), selector=response)
        balls_lst = response.xpath('//span[@class="elemntor-counter-number"]/@data-to-value').getall()
        rows = response.xpath('//tbody/tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("bonus_ball", balls_lst[6])
        draw_date = response.xpath('//div[@id="Lotto-results-last-week"]/h2/span/text()').getall()[1]
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%A %d %B %Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", response.xpath('//div[@id="Lotto-results-last-week"]/h2/span/text()').getall()[0])
        LottoItem.add_value("estimated_next_jackpot", response.xpath('//div[@id="lotto-jackpot"]//h2//strong/span/text()').get())
        LottoItem.add_value("cat_1_prize", rows[0].xpath('./td/strong/text()').getall()[1])
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./td/strong/text()').getall()[1])
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./td/strong/text()').getall()[1])
        LottoItem.add_value("cat_4_prize", rows[3].xpath('./td/strong/text()').getall()[1])
        LottoItem.add_value("cat_5_prize", rows[4].xpath('./td/strong/text()').getall()[1])
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td//text()').getall()[-1])
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./td//text()').getall()[-1])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./td//text()').getall()[-1])
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./td//text()').getall()[-1])
        LottoItem.add_value("cat_5_winners", rows[4].xpath('./td//text()').getall()[-1])
        yield LottoItem.load_item()


class SerbiaLoto(scrapy.Spider):

    name = "SerbiaLoto"

    # note: jackpot in RSD, est_next_jackpot in EUR
    # LotoPlus is additional 20 RSD for chance at 2nd prog. jackpot
    # RUNS BUT REPORTS LOGGING ERROR (UnicodeEncodeError for character '\u010d' = Cyrillic c)

    def start_requests(self):
        self.name = "SerbiaLoto"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.lutrija.rs/Results"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=SerbiaLotoItem(), selector=response)
        balls_lst = response.xpath(
            '//div[@class="DIV_Rez_Loto_Left"]')[1].xpath('.//div[@class="Rez_Brojevi_Txt_Gray"]/text()').getall()
        rows = response.xpath('//table[@id="table-prize-breakdown"]/tbody/tr')
        detail_rows = response.xpath('//table[@id="table-loto-payments"]//tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("ball6", balls_lst[6])
        draw_date = clean_datetime(response.xpath('//div[@class="Rez_Txt_Title"]/label/text()').get().lower().split('-')[1])
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d.%m.%Y.").strftime("%Y-%m-%d"))
        LottoItem.add_value("tickets", detail_rows[4].xpath('./td/label/text()').getall()[-1])
        LottoItem.add_value("estimated_next_jackpot", response.xpath(
            '//div[@class="DIV_Rez_Loto_Right"]')[0].xpath('./div[@class="Rez_Txt_Normal_Red"]/text()').get())
        if prize_to_num(rows[0].xpath('./td/text()').getall()[1]) == 0:
            LottoItem.add_value("cat_1_prize", detail_rows[2].xpath('./td/label/text()').getall()[-1])
        else:
            LottoItem.add_value("cat_1_prize", rows[0].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_4_prize", rows[3].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_5_prize", rows[4].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_5_winners", rows[4].xpath('./td/text()').getall()[1])
        yield LottoItem.load_item()


class SerbiaLotoPlus(scrapy.Spider):

    name = "SerbiaLotoPlus"

    # LotoPlus is additional 20 RSD (must play Loto) for chance at 2nd prog. jackpot
    # note: jackpot in RSD, est_next_jackpot in EUR
    # note: draw_sales / 20 == number of lotoplus players

    def start_requests(self):
        self.name = "SerbiaLotoPlus"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.lutrija.rs/Results"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=SerbiaLotoPlusItem(), selector=response)
        balls_lst = response.xpath(
            '//div[@class="DIV_Rez_Loto_Left"]')[2].xpath('.//div[@class="Rez_Brojevi_Txt_Gray"]/text()').getall()
        lotoplus_rows = response.xpath('//table[@id="table-loto-plus"]//tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("ball6", balls_lst[6])
        draw_date = clean_datetime(response.xpath('//div[@class="Rez_Txt_Title"]/label/text()').get().lower().split('-')[1])
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d.%m.%Y.").strftime("%Y-%m-%d"))
        LottoItem.add_value("sales", lotoplus_rows[0].xpath('./td/label/text()').getall()[-1])
        LottoItem.add_value("estimated_next_jackpot", response.xpath(
            '//div[@class="DIV_Rez_Loto_Right"]')[1].xpath('./div[@class="Rez_Txt_Normal_Red"]/text()').get())
        if prize_to_num(lotoplus_rows[3].xpath('./td/label/text()').getall()[-1]) == 0:
            LottoItem.add_value("cat_1_prize", lotoplus_rows[1].xpath('./td/label/text()').getall()[-1])
        else:
            LottoItem.add_value("cat_1_prize", lotoplus_rows[4].xpath('./td/label/text()').getall()[-1])
        LottoItem.add_value("cat_1_winners", lotoplus_rows[3].xpath('./td/label/text()').getall()[-1])
        yield LottoItem.load_item()


class SingaporeToto(scrapy.Spider):

    name = "SingaporeToto"

    def start_requests(self):
        self.name = "SingaporeToto"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.singaporepools.com.sg/en/product/Pages/toto_results.aspx"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        LottoItem = ItemLoader(item=SingaporeTotoItem(), selector=response)
        latest = response.xpath('//div[@class="slide-wrapper toto"]/ul/li')[0]
        rows = latest.xpath('.//table[@class="table table-striped tableWinningShares"]/tbody/tr')[1:]

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", latest.xpath('.//td[@class="win1"]/text()').get())
        LottoItem.add_value("ball1", latest.xpath('.//td[@class="win2"]/text()').get())
        LottoItem.add_value("ball2", latest.xpath('.//td[@class="win3"]/text()').get())
        LottoItem.add_value("ball3", latest.xpath('.//td[@class="win4"]/text()').get())
        LottoItem.add_value("ball4", latest.xpath('.//td[@class="win5"]/text()').get())
        LottoItem.add_value("ball5", latest.xpath('.//td[@class="win6"]/text()').get())
        LottoItem.add_value("bonus_ball", latest.xpath('.//td[@class="additional"]/text()').get())
        draw_date = latest.xpath('.//th[@class="drawDate"]/text()').get().split(',')[1].strip()
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d %b %Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", latest.xpath('.//th[@class="drawNumber"]/text()').get())
        LottoItem.add_value("estimated_next_jackpot", response.xpath('//div[@class="col-md-9"]//span/text()').getall()[-1])
        if prize_to_num(rows[0].xpath('./td/text()').getall()[-1]) == 0:
            LottoItem.add_value("cat_1_prize", latest.xpath('.//td[@class="jackpotPrize"]/text()').get())
        else:
            LottoItem.add_value("cat_1_prize", rows[0].xpath('./td/text()').getall()[-2])
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./td/text()').getall()[-2])
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./td/text()').getall()[-2])
        LottoItem.add_value("cat_4_prize", rows[3].xpath('./td/text()').getall()[-2])
        LottoItem.add_value("cat_5_prize", rows[4].xpath('./td/text()').getall()[-2])
        LottoItem.add_value("cat_6_prize", rows[5].xpath('./td/text()').getall()[-2])
        LottoItem.add_value("cat_7_prize", rows[6].xpath('./td/text()').getall()[-2])
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_5_winners", rows[4].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_6_winners", rows[5].xpath('./td/text()').getall()[-1])
        LottoItem.add_value("cat_7_winners", rows[6].xpath('./td/text()').getall()[-1])
        yield LottoItem.load_item()


class SlovakiaLoto(scrapy.Spider):

    name = "SlovakiaLoto"

    # Two draws; draw_1 is prog. jackpot, draw_2 is fixed €500,000

    def start_requests(self):
        self.name = "SlovakiaLoto"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.tipos.sk/loterie/loto"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        LottoItem = ItemLoader(item=SlovakiaLotoItem(), selector=response)
        d1_balls_lst = response.xpath('//ul[@id="results-1"]/li/@data-value').getall()
        d2_balls_lst = response.xpath('//ul[@id="results-2"]/li/@data-value').getall()
        rows = response.xpath('//table//tr')[1:]

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("draw1_ball0", d1_balls_lst[0])
        LottoItem.add_value("draw1_ball1", d1_balls_lst[1])
        LottoItem.add_value("draw1_ball2", d1_balls_lst[2])
        LottoItem.add_value("draw1_ball3", d1_balls_lst[3])
        LottoItem.add_value("draw1_ball4", d1_balls_lst[4])
        LottoItem.add_value("draw1_ball5", d1_balls_lst[5])
        LottoItem.add_value("draw1_bonus_ball", d1_balls_lst[6])
        LottoItem.add_value("draw2_ball0", d2_balls_lst[0])
        LottoItem.add_value("draw2_ball1", d2_balls_lst[1])
        LottoItem.add_value("draw2_ball2", d2_balls_lst[2])
        LottoItem.add_value("draw2_ball3", d2_balls_lst[3])
        LottoItem.add_value("draw2_ball4", d2_balls_lst[4])
        LottoItem.add_value("draw2_ball5", d2_balls_lst[5])
        LottoItem.add_value("draw2_bonus_ball", d2_balls_lst[6])
        draw_date = response.xpath('//div[@class="date"]/input[@name="tiposDate"]/@value').get().split(',')[0].strip()
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d. %m. %Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("sales", response.xpath('//li[@id="info-deposit"]/label/text()').get())
        LottoItem.add_value("estimated_next_jackpot", response.xpath('//ul[@class="bottom-winner"]/li/strong//text()').get())
        # note: jackpot values will be '0' if not won
        LottoItem.add_value("draw1_cat_1_prize", rows[0].xpath('./td[@class="win"]//text()').get())
        LottoItem.add_value("draw1_cat_2_prize", rows[1].xpath('./td[@class="win"]//text()').get())
        LottoItem.add_value("draw1_cat_3_prize", rows[2].xpath('./td[@class="win"]//text()').get())
        LottoItem.add_value("draw1_cat_4_prize", rows[3].xpath('./td[@class="win"]//text()').get())
        LottoItem.add_value("draw1_cat_5_prize", rows[4].xpath('./td[@class="win"]//text()').get())
        LottoItem.add_value("draw1_cat_6_prize", rows[5].xpath('./td[@class="win"]//text()').get())
        LottoItem.add_value("draw1_cat_7_prize", rows[6].xpath('./td[@class="win"]//text()').get())
        for i in range(7):
            winner_value = "".join(rows[i].xpath('./td')[3].xpath('.//text()').getall())
            LottoItem.add_value(f"draw1_cat_{i+1}_winners", winner_value)
        LottoItem.add_value("draw2_cat_1_prize", "€500,000")
        LottoItem.add_value("draw2_cat_2_prize", rows[1].xpath('./td[@class="win"]//text()').getall()[1])
        LottoItem.add_value("draw2_cat_3_prize", rows[2].xpath('./td[@class="win"]//text()').getall()[1])
        LottoItem.add_value("draw2_cat_4_prize", rows[3].xpath('./td[@class="win"]//text()').getall()[1])
        LottoItem.add_value("draw2_cat_5_prize", rows[4].xpath('./td[@class="win"]//text()').getall()[1])
        LottoItem.add_value("draw2_cat_6_prize", rows[5].xpath('./td[@class="win"]//text()').getall()[1])
        LottoItem.add_value("draw2_cat_7_prize", rows[6].xpath('./td[@class="win"]//text()').getall()[1])
        for i in range(7):
            winner_value = "".join(rows[i].xpath('./td')[5].xpath('.//text()').getall())
            LottoItem.add_value(f"draw2_cat_{i+1}_winners", winner_value)
        yield LottoItem.load_item()


class SlovakiaLoto5x35(scrapy.Spider):

    name = "SlovakiaLoto5x35"

    def start_requests(self):
        self.name = "SlovakiaLoto5x35"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.tipos.sk/loterie/loto-5-z-35"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        LottoItem = ItemLoader(item=SlovakiaLoto5x35Item(), selector=response)
        balls_lst = response.xpath('//ul[@id="results"]/li/@data-value').getall()
        rows = response.xpath('//table//tr')[1:]

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        draw_date = response.xpath('//div[@class="date"]/input[@name="tiposDate"]/@value').get().split(',')[0].strip()
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d. %m. %Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("sales", response.xpath('//li[@id="info-deposit"]/label/text()').get())
        try:
            cat_1_winners = [i.strip() for i in rows[0].xpath('./td/span//text()').getall() if len(i.strip())>0][0]
        except:
            cat_1_winners = '0'
        if prize_to_num(cat_1_winners) == 0:
            LottoItem.add_value("cat_1_prize", response.xpath('//ul[@class="bottom-winner"]/li/strong//text()').get())
        else:
            LottoItem.add_value("cat_1_prize", rows[0].xpath('./td[@class="win"]//text()').get())
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./td[@class="win"]//text()').get())
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./td[@class="win"]//text()').get())
        for i in range(3):
            try:
                winner_value = [i.strip() for i in rows[i].xpath('./td/span//text()').getall() if len(i.strip())>0][0]
            except:
                winner_value = '0'
            LottoItem.add_value(f"cat_{i+1}_winners", winner_value)
        yield LottoItem.load_item()


class SloveniaLoto(scrapy.Spider):

    name = "SloveniaLoto"

    def start_requests(self):
        self.name = "SloveniaLoto"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.loterija.si/loto/rezultati"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=SloveniaLotoItem(), selector=response)
        latest= response.xpath('//div[@role="table"]')[0]
        rows = latest.xpath('.//div[@class="row no-gutters details-row-data"]')
        balls_lst = response.xpath('//div[@class="number bg-prim"]/text()').getall()
        bonus_ball = response.xpath('//div[@class="number additional bg-second"]/text()').get()

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("ball6", balls_lst[6])
        LottoItem.add_value("bonus_ball", bonus_ball)
        draw_date = clean_datetime(response.xpath('//div[@id="results-draw"]//h2[@class="title mb-2"]/text()').get())
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d.%m.%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("cat_1_prize", rows[0].xpath('./div[@role="cell"]/text()').getall()[2])
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./div[@role="cell"]/text()').getall()[2])
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./div[@role="cell"]/text()').getall()[2])
        LottoItem.add_value("cat_4_prize", rows[3].xpath('./div[@role="cell"]/text()').getall()[2])
        LottoItem.add_value("cat_5_prize", rows[4].xpath('./div[@role="cell"]/text()').getall()[2])
        LottoItem.add_value("cat_6_prize", rows[5].xpath('./div[@role="cell"]/text()').getall()[2])
        LottoItem.add_value("cat_7_prize", rows[6].xpath('./div[@role="cell"]/text()').getall()[2])
        LottoItem.add_value("cat_8_prize", rows[7].xpath('./div[@role="cell"]/text()').getall()[2])
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./div[@role="cell"]/text()').getall()[1])
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./div[@role="cell"]/text()').getall()[1])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./div[@role="cell"]/text()').getall()[1])
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./div[@role="cell"]/text()').getall()[1])
        LottoItem.add_value("cat_5_winners", rows[4].xpath('./div[@role="cell"]/text()').getall()[1])
        LottoItem.add_value("cat_6_winners", rows[5].xpath('./div[@role="cell"]/text()').getall()[1])
        LottoItem.add_value("cat_7_winners", rows[6].xpath('./div[@role="cell"]/text()').getall()[1])
        LottoItem.add_value("cat_8_winners", rows[7].xpath('./div[@role="cell"]/text()').getall()[1])
        yield LottoItem.load_item()


class SloveniaLotoPlus(scrapy.Spider):

    name = "SloveniaLotoPlus"

    # Add-on game to main Loto; participate with same numbers for 2nd prog jackpot; additional 0.4 euros

    def start_requests(self):
        self.name = "SloveniaLotoPlus"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.loterija.si/loto/rezultati"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=SloveniaLotoPlusItem(), selector=response)
        latest= response.xpath('//div[@role="table"]')[1]
        rows = latest.xpath('.//div[@class="row no-gutters details-row-data"]')
        balls_lst = response.xpath('//div[@class="number bg-second"]/text()').getall()
        bonus_ball = response.xpath('//div[@class="number additional bg-prim"]/text()').get()

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("ball6", balls_lst[6])
        LottoItem.add_value("bonus_ball", bonus_ball)
        draw_date = clean_datetime(response.xpath('//div[@id="results-draw"]//h2[@class="title mb-2"]/text()').get())
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d.%m.%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("cat_1_prize", rows[0].xpath('./div[@role="cell"]/text()').getall()[2])
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./div[@role="cell"]/text()').getall()[2])
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./div[@role="cell"]/text()').getall()[2])
        LottoItem.add_value("cat_4_prize", rows[3].xpath('./div[@role="cell"]/text()').getall()[2])
        LottoItem.add_value("cat_5_prize", rows[4].xpath('./div[@role="cell"]/text()').getall()[2])
        LottoItem.add_value("cat_6_prize", rows[5].xpath('./div[@role="cell"]/text()').getall()[2])
        LottoItem.add_value("cat_7_prize", rows[6].xpath('./div[@role="cell"]/text()').getall()[2])
        LottoItem.add_value("cat_8_prize", rows[7].xpath('./div[@role="cell"]/text()').getall()[2])
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./div[@role="cell"]/text()').getall()[1])
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./div[@role="cell"]/text()').getall()[1])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./div[@role="cell"]/text()').getall()[1])
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./div[@role="cell"]/text()').getall()[1])
        LottoItem.add_value("cat_5_winners", rows[4].xpath('./div[@role="cell"]/text()').getall()[1])
        LottoItem.add_value("cat_6_winners", rows[5].xpath('./div[@role="cell"]/text()').getall()[1])
        LottoItem.add_value("cat_7_winners", rows[6].xpath('./div[@role="cell"]/text()').getall()[1])
        LottoItem.add_value("cat_8_winners", rows[7].xpath('./div[@role="cell"]/text()').getall()[1])
        yield LottoItem.load_item()


class SloveniaLotko(scrapy.Spider):

    name = "SloveniaLotko"

    # "Joker"-style draw-game with prog. jackpot
    # Add-on game to main Loto; additional 1.5 euros

    def start_requests(self):
        self.name = "SloveniaLotko"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.loterija.si/loto/rezultati"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=SloveniaLotkoItem(), selector=response)
        latest= response.xpath('//div[@role="table"]')[2]
        rows = latest.xpath('.//div[@class="row no-gutters details-row-data"]')
        balls_lst = response.xpath('//div[@class="number bg-prim"]/text()').getall()

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[7])
        LottoItem.add_value("ball1", balls_lst[8])
        LottoItem.add_value("ball2", balls_lst[9])
        LottoItem.add_value("ball3", balls_lst[10])
        LottoItem.add_value("ball4", balls_lst[11])
        LottoItem.add_value("ball5", balls_lst[12])
        draw_date = clean_datetime(response.xpath('//div[@id="results-draw"]//h2[@class="title mb-2"]/text()').get())
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d.%m.%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("cat_1_prize", rows[0].xpath('./div[@role="cell"]/text()').getall()[2])
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./div[@role="cell"]/text()').getall()[2])
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./div[@role="cell"]/text()').getall()[2])
        LottoItem.add_value("cat_4_prize", rows[3].xpath('./div[@role="cell"]/text()').getall()[2])
        LottoItem.add_value("cat_5_prize", rows[4].xpath('./div[@role="cell"]/text()').getall()[2])
        LottoItem.add_value("cat_6_prize", rows[5].xpath('./div[@role="cell"]/text()').getall()[2])
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./div[@role="cell"]/text()').getall()[1])
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./div[@role="cell"]/text()').getall()[1])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./div[@role="cell"]/text()').getall()[1])
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./div[@role="cell"]/text()').getall()[1])
        LottoItem.add_value("cat_5_winners", rows[4].xpath('./div[@role="cell"]/text()').getall()[1])
        LottoItem.add_value("cat_6_winners", rows[5].xpath('./div[@role="cell"]/text()').getall()[1])
        yield LottoItem.load_item()


class SpainLaPrimitiva(scrapy.Spider):

    name = "SpainLaPrimitiva"

    # number_R = Reintegro i.e. randomly assigned to tickets to receive free refund

    def start_requests(self):
        self.name = "SpainLaPrimitiva"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.loteriasyapuestas.es/en/resultados/primitiva"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        est_next_jackpot = response.xpath('//p[@class="c-cabecera-juego__bote_topaz c-cabecera-juego__bote--primitiva"]//text()').getall()
        self.next_jackpot = " ".join([s for s in est_next_jackpot if len(s.strip())>0])
        headers = {
            'Connection': 'keep-alive',
            'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://www.loteriasyapuestas.es/en/resultados/primitiva',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }
        root_url = 'https://www.loteriasyapuestas.es/servicios/buscadorSorteos?game_id=LAPR&celebrados=true&fechaInicioInclusiva=XXXX&fechaFinInclusiva=YYYY'
        end_date = datetime.strftime(datetime.now(), "%Y%m%d")
        start_date = datetime.strftime(datetime.now()-timedelta(days=92), "%Y%m%d")
        url = root_url.replace("YYYY", end_date)
        url = url.replace("XXXX", start_date)
        yield scrapy.Request(url=url, headers=headers, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":10})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=SpainLaPrimitivaItem(), selector=response)
        latest = response.json()[0]
        balls_lst = [i.strip() for i in latest['combinacion'].split(' ') if i != "-"]

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("ball_C", "".join([i for i in balls_lst[6] if i.isdigit()]))
        LottoItem.add_value("ball_R", "".join([i for i in balls_lst[7] if i.isdigit()]))
        LottoItem.add_value("draw_datetime", latest['fecha_sorteo'].split(' ')[0])
        LottoItem.add_value("tickets", latest['apuestas'])
        LottoItem.add_value("prize_pool", str(int(latest['premios'])/100.0))
        LottoItem.add_value("estimated_next_jackpot", self.next_jackpot)
        if int(latest['escrutinio'][0]['ganadores']) == 0:
            LottoItem.add_value("cat_1_prize", latest['premio_bote'])
        else:
            LottoItem.add_value("cat_1_prize", latest['escrutinio'][0]['premio'])
        LottoItem.add_value("cat_2_prize", latest['escrutinio'][1]['premio'])
        LottoItem.add_value("cat_3_prize", latest['escrutinio'][2]['premio'])
        LottoItem.add_value("cat_4_prize", latest['escrutinio'][3]['premio'])
        LottoItem.add_value("cat_5_prize", latest['escrutinio'][4]['premio'])
        LottoItem.add_value("cat_6_prize", latest['escrutinio'][5]['premio'])
        LottoItem.add_value("cat_7_prize", latest['escrutinio'][6]['premio'])
        LottoItem.add_value("cat_1_winners", latest['escrutinio'][0]['ganadores'])
        LottoItem.add_value("cat_2_winners", latest['escrutinio'][1]['ganadores'])
        LottoItem.add_value("cat_3_winners", latest['escrutinio'][2]['ganadores'])
        LottoItem.add_value("cat_4_winners", latest['escrutinio'][3]['ganadores'])
        LottoItem.add_value("cat_5_winners", latest['escrutinio'][4]['ganadores'])
        LottoItem.add_value("cat_6_winners", latest['escrutinio'][5]['ganadores'])
        LottoItem.add_value("cat_7_winners", latest['escrutinio'][6]['ganadores'])
        yield LottoItem.load_item()


class SpainBonoLoto(scrapy.Spider):

    name = "SpainBonoLoto"

    # number_R = Reintegro i.e. randomly assigned to tickets to receive free refund

    def start_requests(self):
        self.name = "SpainBonoLoto"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.loteriasyapuestas.es/en/resultados/bonoloto"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        est_next_jackpot = response.xpath('//p[@class="c-cabecera-juego__bote_topaz c-cabecera-juego__bote--bonoloto"]//text()').getall()
        self.next_jackpot = " ".join([s for s in est_next_jackpot if len(s.strip())>0])
        headers = {
            'Connection': 'keep-alive',
            'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://www.loteriasyapuestas.es/en/resultados/bonoloto',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }
        root_url = 'https://www.loteriasyapuestas.es/servicios/buscadorSorteos?game_id=BONO&celebrados=true&fechaInicioInclusiva=XXXX&fechaFinInclusiva=YYYY'
        end_date = datetime.strftime(datetime.now(), "%Y%m%d")
        start_date = datetime.strftime(datetime.now()-timedelta(days=92), "%Y%m%d")
        url = root_url.replace("YYYY", end_date)
        url = url.replace("XXXX", start_date)
        yield scrapy.Request(url=url, headers=headers, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":10})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=SpainBonoLotoItem(), selector=response)
        latest = response.json()[0]
        balls_lst = [i.strip() for i in latest['combinacion'].split(' ') if i != "-"]

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("ball_C", "".join([i for i in balls_lst[6] if i.isdigit()]))
        LottoItem.add_value("ball_R", "".join([i for i in balls_lst[7] if i.isdigit()]))
        LottoItem.add_value("draw_datetime", latest['fecha_sorteo'].split(' ')[0])
        LottoItem.add_value("tickets", latest['apuestas'])
        LottoItem.add_value("prize_pool", str(int(latest['premios'])/100.0))
        LottoItem.add_value("estimated_next_jackpot", self.next_jackpot)
        if int(latest['escrutinio'][0]['ganadores']) == 0:
            LottoItem.add_value("cat_1_prize", latest['premio_bote'])
        else:
            LottoItem.add_value("cat_1_prize", latest['escrutinio'][0]['premio'])
        LottoItem.add_value("cat_2_prize", latest['escrutinio'][1]['premio'])
        LottoItem.add_value("cat_3_prize", latest['escrutinio'][2]['premio'])
        LottoItem.add_value("cat_4_prize", latest['escrutinio'][3]['premio'])
        LottoItem.add_value("cat_5_prize", latest['escrutinio'][4]['premio'])
        LottoItem.add_value("cat_6_prize", latest['escrutinio'][5]['premio'])
        LottoItem.add_value("cat_1_winners", latest['escrutinio'][0]['ganadores'])
        LottoItem.add_value("cat_2_winners", latest['escrutinio'][1]['ganadores'])
        LottoItem.add_value("cat_3_winners", latest['escrutinio'][2]['ganadores'])
        LottoItem.add_value("cat_4_winners", latest['escrutinio'][3]['ganadores'])
        LottoItem.add_value("cat_5_winners", latest['escrutinio'][4]['ganadores'])
        LottoItem.add_value("cat_6_winners", latest['escrutinio'][5]['ganadores'])
        yield LottoItem.load_item()


class SpainElGordo(scrapy.Spider):

    name = "SpainElGordo"

    def start_requests(self):
        self.name = "SpainElGordo"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.loteriasyapuestas.es/en/resultados/gordo-primitiva"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        est_next_jackpot = response.xpath('//p[@class="c-cabecera-juego__bote_topaz c-cabecera-juego__bote_topaz--elgordo c-cabecera-juego__bote--gordo"]//text()').getall()
        self.next_jackpot = " ".join([s for s in est_next_jackpot if len(s.strip())>0])
        headers = {
            'Connection': 'keep-alive',
            'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://www.loteriasyapuestas.es/en/resultados/gordo-primitiva',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }
        root_url = 'https://www.loteriasyapuestas.es/servicios/buscadorSorteos?game_id=ELGR&celebrados=true&fechaInicioInclusiva=XXXX&fechaFinInclusiva=YYYY'
        end_date = datetime.strftime(datetime.now(), "%Y%m%d")
        start_date = datetime.strftime(datetime.now()-timedelta(days=92), "%Y%m%d")
        url = root_url.replace("YYYY", end_date)
        url = url.replace("XXXX", start_date)
        yield scrapy.Request(url=url, headers=headers, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":10})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=SpainElGordoItem(), selector=response)
        latest = response.json()[0]
        balls_lst = [i.strip() for i in latest['combinacion'].split(' ') if i != "-"]

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("bonus_ball", "".join([i for i in balls_lst[5] if i.isdigit()]))
        LottoItem.add_value("draw_datetime", latest['fecha_sorteo'].split(' ')[0])
        LottoItem.add_value("tickets", latest['apuestas'])
        LottoItem.add_value("prize_pool", str(int(latest['premios'])/100.0))
        LottoItem.add_value("estimated_next_jackpot", self.next_jackpot)
        if int(latest['escrutinio'][0]['ganadores']) == 0:
            LottoItem.add_value("cat_1_prize", latest['premio_bote'])
        else:
            LottoItem.add_value("cat_1_prize", latest['escrutinio'][0]['premio'])
        LottoItem.add_value("cat_2_prize", latest['escrutinio'][1]['premio'])
        LottoItem.add_value("cat_3_prize", latest['escrutinio'][2]['premio'])
        LottoItem.add_value("cat_4_prize", latest['escrutinio'][3]['premio'])
        LottoItem.add_value("cat_5_prize", latest['escrutinio'][4]['premio'])
        LottoItem.add_value("cat_6_prize", latest['escrutinio'][5]['premio'])
        LottoItem.add_value("cat_7_prize", latest['escrutinio'][6]['premio'])
        LottoItem.add_value("cat_8_prize", latest['escrutinio'][7]['premio'])
        LottoItem.add_value("cat_9_prize", latest['escrutinio'][8]['premio'])
        LottoItem.add_value("cat_1_winners", latest['escrutinio'][0]['ganadores'])
        LottoItem.add_value("cat_2_winners", latest['escrutinio'][1]['ganadores'])
        LottoItem.add_value("cat_3_winners", latest['escrutinio'][2]['ganadores'])
        LottoItem.add_value("cat_4_winners", latest['escrutinio'][3]['ganadores'])
        LottoItem.add_value("cat_5_winners", latest['escrutinio'][4]['ganadores'])
        LottoItem.add_value("cat_6_winners", latest['escrutinio'][5]['ganadores'])
        LottoItem.add_value("cat_7_winners", latest['escrutinio'][6]['ganadores'])
        LottoItem.add_value("cat_8_winners", latest['escrutinio'][7]['ganadores'])
        LottoItem.add_value("cat_9_winners", latest['escrutinio'][8]['ganadores'])
        yield LottoItem.load_item()


class SpainLotoTurf(scrapy.Spider):

    name = "SpainLotoTurf"

    # number_R = Reintegro i.e. randomly assigned to tickets to receive free refund

    def start_requests(self):
        self.name = "SpainLotoTurf"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.loteriasyapuestas.es/en/resultados/lototurf"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        est_next_jackpot = response.xpath('//p[@class="c-cabecera-juego__bote_topaz c-cabecera-juego__bote--lototurf"]//text()').getall()
        self.next_jackpot = " ".join([s for s in est_next_jackpot if len(s.strip())>0])
        headers = {
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
            'sec-ch-ua-mobile': '?0',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://www.loteriasyapuestas.es/en/resultados/lototurf',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'If-None-Match': '"afd67e83-2549-40b0-b48f-09933bf03375"',
        }
        root_url = 'https://www.loteriasyapuestas.es/servicios/buscadorSorteos?game_id=LOTU&celebrados=true&fechaInicioInclusiva=XXXX&fechaFinInclusiva=YYYY'
        end_date = datetime.strftime(datetime.now(), "%Y%m%d")
        start_date = datetime.strftime(datetime.now()-timedelta(days=92), "%Y%m%d")
        url = root_url.replace("YYYY", end_date)
        url = url.replace("XXXX", start_date)
        yield scrapy.Request(url=url, headers=headers, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":10})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=SpainLotoTurfItem(), selector=response)
        latest = response.json()[0]
        balls_lst = [i.strip() for i in latest['combinacion'].split(' ') if i != "-"]

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("ball_C", "".join([i for i in balls_lst[6] if i.isdigit()]))
        LottoItem.add_value("ball_R", "".join([i for i in balls_lst[7] if i.isdigit()]))
        LottoItem.add_value("draw_datetime", latest['fecha_sorteo'].split(' ')[0])
        LottoItem.add_value("tickets", latest['apuestas'])
        LottoItem.add_value("prize_pool", str(int(latest['premios'])/100.0))
        LottoItem.add_value("estimated_next_jackpot", self.next_jackpot)
        if int(latest['escrutinio'][0]['ganadores']) == 0:
            LottoItem.add_value("cat_1_prize", latest['premio_bote'])
        else:
            LottoItem.add_value("cat_1_prize", latest['escrutinio'][0]['premio'])
        LottoItem.add_value("cat_2_prize", latest['escrutinio'][1]['premio'])
        LottoItem.add_value("cat_3_prize", latest['escrutinio'][2]['premio'])
        LottoItem.add_value("cat_4_prize", latest['escrutinio'][3]['premio'])
        LottoItem.add_value("cat_5_prize", latest['escrutinio'][4]['premio'])
        LottoItem.add_value("cat_6_prize", latest['escrutinio'][5]['premio'])
        LottoItem.add_value("cat_7_prize", latest['escrutinio'][6]['premio'])
        LottoItem.add_value("cat_8_prize", latest['escrutinio'][7]['premio'])
        LottoItem.add_value("cat_1_winners", latest['escrutinio'][0]['ganadores'])
        LottoItem.add_value("cat_2_winners", latest['escrutinio'][1]['ganadores'])
        LottoItem.add_value("cat_3_winners", latest['escrutinio'][2]['ganadores'])
        LottoItem.add_value("cat_4_winners", latest['escrutinio'][3]['ganadores'])
        LottoItem.add_value("cat_5_winners", latest['escrutinio'][4]['ganadores'])
        LottoItem.add_value("cat_6_winners", latest['escrutinio'][5]['ganadores'])
        LottoItem.add_value("cat_7_winners", latest['escrutinio'][6]['ganadores'])
        LottoItem.add_value("cat_8_winners", latest['escrutinio'][7]['ganadores'])
        yield LottoItem.load_item()


class SouthAfricaLotto(scrapy.Spider):

    name = "SouthAfricaLotto"

    def start_requests(self):
        self.name = "SouthAfricaLotto"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        # self.headers = {
        #     'authority': 'www.nationallottery.co.za',
        #     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        #     'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        #     'cache-control': 'max-age=0',
        #     'dnt': '1',
        #     'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        #     'sec-ch-ua-mobile': '?0',
        #     'sec-ch-ua-platform': '"Windows"',
        #     'sec-fetch-dest': 'document',
        #     'sec-fetch-mode': 'navigate',
        #     'sec-fetch-site': 'none',
        #     'sec-fetch-user': '?1',
        #     'upgrade-insecure-requests': '1',
        #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        # }
        #url = "https://www.nationallottery.co.za/results/lotto"
        # yield scrapy.Request(url=url, callback=self.parse1, headers=self.headers
        #     meta={'playwright': True, "playwright_context": "new",
        #         "playwright_context_kwargs": {
        #             "java_script_enabled": True,
        #             "ignore_https_errors": True,
        #             "proxy": {
        #                 "server": self.req_proxy,
        #                 "username": "keizzermop",
        #                 "password": "WSPassword123",
        #             },
        #         },
        #     })


    #def parse1(self, response):
        #self.draw_id = [i.lower() for i in response.xpath('//div[@class="title"]/text()').getall() if "draw id" in i.lower()][0]
        #self.total_sales = response.xpath('//div[@class="tableBody"]')[1].xpath('.//div[@class="dataValue"]/text()').getall()[3]
        #self.rollover_amount = response.xpath('//div[@class="tableBody"]')[1].xpath('.//div[@class="dataValue"]/text()').getall()[0]
        #self.rollover_number = response.xpath('//div[@class="tableBody"]')[1].xpath('.//div[@class="dataValue"]/text()').getall()[1]
        url = "https://www.lotto.net/south-africa-lotto/results"
        yield scrapy.Request(url=url, callback=self.parse2, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse2(self, response):
        self.next_jackpot = response.xpath('//div[@class="jackpot"]//span/text()').getall()[1].strip()
        self.draw_date = response.xpath('//div[@class="date"]/span/text()').get().strip()
        next_page = response.xpath("//div[@class='row-3']/a/@href").get()
        url = urljoin(response.url, next_page)
        yield scrapy.Request(url, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":10})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=SouthAfricaLottoItem(), selector=response)
        balls_lst = response.xpath('//ul[@class="balls"]/li/span/text()').getall()
        rows = response.xpath('//table//tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("bonus_ball", balls_lst[6])
        LottoItem.add_value("draw_datetime", datetime.strptime(self.draw_date, "%d %B %Y").strftime("%Y-%m-%d"))
        #LottoItem.add_value("draw_number", self.draw_id)
        #LottoItem.add_value("sales", self.total_sales)
        #LottoItem.add_value("rollover_amount", self.rollover_amount)
        #LottoItem.add_value("rollover_number", self.rollover_number)
        LottoItem.add_value("estimated_next_jackpot", self.next_jackpot)
        LottoItem.add_value("cat_1_prize", rows[1].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_2_prize", rows[2].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_3_prize", rows[3].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_4_prize", rows[4].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_5_prize", rows[5].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_6_prize", rows[6].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_7_prize", rows[7].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_8_prize", rows[8].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_1_winners", rows[1].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_2_winners", rows[2].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_3_winners", rows[3].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_4_winners", rows[4].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_5_winners", rows[5].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_6_winners", rows[6].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_7_winners", rows[7].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_8_winners", rows[8].xpath('./td/text()').getall()[-1].strip())
        yield LottoItem.load_item()


class SouthAfricaLottoPlus1(scrapy.Spider):

    name = "SouthAfricaLottoPlus1"

    def start_requests(self):
        self.name = "SouthAfricaLottoPlus1"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        #url = "https://www.nationallottery.co.za/results/lotto-plus-1-results"
        #yield scrapy.Request(url=url, callback=self.parse1, meta={"proxy": self.req_proxy, "download_timeout":10})

    #def parse1(self, response):
        #raw_draw_id = [i.lower() for i in response.xpath('//div[@class="title"]/text()').getall() if "draw id" in i.lower()][0]
        #self.draw_id = raw_draw_id.split('draw')[1]
        #self.total_sales = response.xpath('//div[@class="tableBody"]')[1].xpath('.//div[@class="dataValue"]/text()').getall()[3]
        #self.rollover_amount = response.xpath('//div[@class="tableBody"]')[1].xpath('.//div[@class="dataValue"]/text()').getall()[0]
        #self.rollover_number = response.xpath('//div[@class="tableBody"]')[1].xpath('.//div[@class="dataValue"]/text()').getall()[1]
        url = "https://www.lotto.net/south-africa-lotto-plus-1/results"
        yield scrapy.Request(url=url, callback=self.parse2, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse2(self, response):
        self.next_jackpot = response.xpath('//div[@class="jackpot"]//span/text()').getall()[1].strip()
        self.draw_date = response.xpath('//div[@class="date"]/span/text()').get().strip()
        next_page = response.xpath("//div[@class='row-3']/a/@href").get()
        url = urljoin(response.url, next_page)
        yield scrapy.Request(url, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":10})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=SouthAfricaLottoPlus1Item(), selector=response)
        balls_lst = response.xpath('//ul[@class="balls"]/li/span/text()').getall()
        rows = response.xpath('//table//tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("bonus_ball", balls_lst[6])
        LottoItem.add_value("draw_datetime", datetime.strptime(self.draw_date, "%d %B %Y").strftime("%Y-%m-%d"))
        #LottoItem.add_value("draw_number", self.draw_id)
        #LottoItem.add_value("sales", self.total_sales)
        #LottoItem.add_value("rollover_amount", self.rollover_amount)
        #LottoItem.add_value("rollover_number", self.rollover_number)
        LottoItem.add_value("estimated_next_jackpot", self.next_jackpot)
        LottoItem.add_value("cat_1_prize", rows[1].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_2_prize", rows[2].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_3_prize", rows[3].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_4_prize", rows[4].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_5_prize", rows[5].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_6_prize", rows[6].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_7_prize", rows[7].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_8_prize", rows[8].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_1_winners", rows[1].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_2_winners", rows[2].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_3_winners", rows[3].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_4_winners", rows[4].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_5_winners", rows[5].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_6_winners", rows[6].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_7_winners", rows[7].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_8_winners", rows[8].xpath('./td/text()').getall()[-1].strip())
        yield LottoItem.load_item()


class SouthAfricaLottoPlus2(scrapy.Spider):

    name = "SouthAfricaLottoPlus2"

    def start_requests(self):
        self.name = "SouthAfricaLottoPlus2"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        #url = "https://www.nationallottery.co.za/results/lotto-plus-2-results"
        #yield scrapy.Request(url=url, callback=self.parse1, meta={"proxy": self.req_proxy, "download_timeout":10})

    #def parse1(self, response):
        #raw_draw_id = [i.lower() for i in response.xpath('//div[@class="title"]/text()').getall() if "draw id" in i.lower()][0]
        #self.draw_id = raw_draw_id.split('draw')[1]
        #self.total_sales = response.xpath('//div[@class="tableBody"]')[1].xpath('.//div[@class="dataValue"]/text()').getall()[3]
        #self.rollover_amount = response.xpath('//div[@class="tableBody"]')[1].xpath('.//div[@class="dataValue"]/text()').getall()[0]
        #self.rollover_number = response.xpath('//div[@class="tableBody"]')[1].xpath('.//div[@class="dataValue"]/text()').getall()[1]
        url = "https://www.lotto.net/south-africa-lotto-plus-2/results"
        yield scrapy.Request(url=url, callback=self.parse2, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse2(self, response):
        self.next_jackpot = response.xpath('//div[@class="jackpot"]//span/text()').getall()[1].strip()
        self.draw_date = response.xpath('//div[@class="date"]/span/text()').get().strip()
        next_page = response.xpath("//div[@class='row-3']/a/@href").get()
        url = urljoin(response.url, next_page)
        yield scrapy.Request(url, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":10})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=SouthAfricaLottoPlus2Item(), selector=response)
        balls_lst = response.xpath('//ul[@class="balls"]/li/span/text()').getall()
        rows = response.xpath('//table//tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("bonus_ball", balls_lst[6])
        LottoItem.add_value("draw_datetime", datetime.strptime(self.draw_date, "%d %B %Y").strftime("%Y-%m-%d"))
        #LottoItem.add_value("draw_number", self.draw_id)
        #LottoItem.add_value("sales", self.total_sales)
        #LottoItem.add_value("rollover_amount", self.rollover_amount)
        #LottoItem.add_value("rollover_number", self.rollover_number)
        LottoItem.add_value("estimated_next_jackpot", self.next_jackpot)
        LottoItem.add_value("cat_1_prize", rows[1].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_2_prize", rows[2].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_3_prize", rows[3].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_4_prize", rows[4].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_5_prize", rows[5].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_6_prize", rows[6].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_7_prize", rows[7].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_8_prize", rows[8].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_1_winners", rows[1].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_2_winners", rows[2].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_3_winners", rows[3].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_4_winners", rows[4].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_5_winners", rows[5].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_6_winners", rows[6].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_7_winners", rows[7].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_8_winners", rows[8].xpath('./td/text()').getall()[-1].strip())
        yield LottoItem.load_item()


class SouthAfricaPowerball(scrapy.Spider):

    name = "SouthAfricaPowerball"

    def start_requests(self):
        self.name = "SouthAfricaPowerball"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        #url = "https://www.nationallottery.co.za/results/powerball"
        #yield scrapy.Request(url=url, callback=self.parse1, meta={"proxy": self.req_proxy, "download_timeout":10})

    #def parse1(self, response):
        #raw_draw_id = [i.lower() for i in response.xpath('//div[@class="title"]/text()').getall() if "draw id" in i.lower()][0]
        #self.draw_id = raw_draw_id.split('draw')[1]
        #self.total_sales = response.xpath('//div[@class="tableBody"]')[1].xpath('.//div[@class="dataValue"]/text()').getall()[3]
        #self.rollover_amount = response.xpath('//div[@class="tableBody"]')[1].xpath('.//div[@class="dataValue"]/text()').getall()[0]
        #self.rollover_number = response.xpath('//div[@class="tableBody"]')[1].xpath('.//div[@class="dataValue"]/text()').getall()[1]
        url = "https://www.lotto.net/south-africa-powerball/results"
        yield scrapy.Request(url=url, callback=self.parse2, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse2(self, response):
        self.next_jackpot = response.xpath('//div[@class="jackpot"]//span/text()').getall()[1].strip()
        self.draw_date = response.xpath('//div[@class="date"]/span/text()').get().strip()
        next_page = response.xpath("//div[@class='row-3']/a/@href").get()
        url = urljoin(response.url, next_page)
        yield scrapy.Request(url, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":10})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=SouthAfricaPowerballItem(), selector=response)
        balls_lst = response.xpath('//ul[@class="balls"]/li/span/text()').getall()
        rows = response.xpath('//table//tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("bonus_ball", balls_lst[5])
        LottoItem.add_value("draw_datetime", datetime.strptime(self.draw_date, "%d %B %Y").strftime("%Y-%m-%d"))
        #LottoItem.add_value("draw_number", self.draw_id)
        #LottoItem.add_value("sales", self.total_sales)
        #LottoItem.add_value("rollover_amount", self.rollover_amount)
        #LottoItem.add_value("rollover_number", self.rollover_number)
        LottoItem.add_value("estimated_next_jackpot", self.next_jackpot)
        LottoItem.add_value("cat_1_prize", rows[1].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_2_prize", rows[2].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_3_prize", rows[3].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_4_prize", rows[4].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_5_prize", rows[5].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_6_prize", rows[6].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_7_prize", rows[7].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_8_prize", rows[8].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_9_prize", rows[9].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_1_winners", rows[1].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_2_winners", rows[2].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_3_winners", rows[3].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_4_winners", rows[4].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_5_winners", rows[5].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_6_winners", rows[6].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_7_winners", rows[7].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_8_winners", rows[8].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_9_winners", rows[9].xpath('./td/text()').getall()[-1].strip())
        yield LottoItem.load_item()


class SouthAfricaPowerballPlus(scrapy.Spider):

    name = "SouthAfricaPowerballPlus"

    def start_requests(self):
        self.name = "SouthAfricaPowerballPlus"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        #url = "https://www.nationallottery.co.za/results/powerball-plus"
        #yield scrapy.Request(url=url, callback=self.parse1, meta={"proxy": self.req_proxy, "download_timeout":10})

    #def parse1(self, response):
        #raw_draw_id = [i.lower() for i in response.xpath('//div[@class="title"]/text()').getall() if "draw id" in i.lower()][0]
        #self.draw_id = raw_draw_id.split('draw')[1]
        #self.total_sales = response.xpath('//div[@class="tableBody"]')[1].xpath('.//div[@class="dataValue"]/text()').getall()[3]
        #self.rollover_amount = response.xpath('//div[@class="tableBody"]')[1].xpath('.//div[@class="dataValue"]/text()').getall()[0]
        #self.rollover_number = response.xpath('//div[@class="tableBody"]')[1].xpath('.//div[@class="dataValue"]/text()').getall()[1]
        url = "https://www.lotto.net/south-africa-powerball-plus/results"
        yield scrapy.Request(url=url, callback=self.parse2, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse2(self, response):
        self.next_jackpot = response.xpath('//div[@class="jackpot"]//span/text()').getall()[1].strip()
        self.draw_date = response.xpath('//div[@class="date"]/span/text()').get().strip()
        next_page = response.xpath("//div[@class='row-3']/a/@href").get()
        url = urljoin(response.url, next_page)
        yield scrapy.Request(url, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":10})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=SouthAfricaPowerballPlusItem(), selector=response)
        balls_lst = response.xpath('//ul[@class="balls"]/li/span/text()').getall()
        rows = response.xpath('//table//tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("bonus_ball", balls_lst[5])
        LottoItem.add_value("draw_datetime", datetime.strptime(self.draw_date, "%d %B %Y").strftime("%Y-%m-%d"))
        #LottoItem.add_value("draw_number", self.draw_id)
        #LottoItem.add_value("sales", self.total_sales)
        #LottoItem.add_value("rollover_amount", self.rollover_amount)
        #LottoItem.add_value("rollover_number", self.rollover_number)
        LottoItem.add_value("estimated_next_jackpot", self.next_jackpot)
        LottoItem.add_value("cat_1_prize", rows[1].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_2_prize", rows[2].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_3_prize", rows[3].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_4_prize", rows[4].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_5_prize", rows[5].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_6_prize", rows[6].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_7_prize", rows[7].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_8_prize", rows[8].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_9_prize", rows[9].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_1_winners", rows[1].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_2_winners", rows[2].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_3_winners", rows[3].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_4_winners", rows[4].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_5_winners", rows[5].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_6_winners", rows[6].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_7_winners", rows[7].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_8_winners", rows[8].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_9_winners", rows[9].xpath('./td/text()').getall()[-1].strip())
        yield LottoItem.load_item()


class SouthKoreaLotto6x45(scrapy.Spider):

    name = "SouthKoreaLotto6x45"

    def start_requests(self):
        self.name = "SouthKoreaLotto6x45"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://dhlottery.co.kr/gameResult.do?method=byWin"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=SouthKoreaLotto6x45Item(), selector=response)
        rows = response.xpath('//tbody/tr')
        balls_lst = response.xpath('//div[@class="nums"]//p/span//text()').getall()

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("bonus_ball", balls_lst[6])
        draw_date = response.xpath('//p[@class="desc"]//text()').get()
        date_str = []
        for i in draw_date[:-1]:
            if i.isdigit() == True:
                date_str.append(i)
            elif i == ' ':
                date_str.append('-')
        LottoItem.add_value("draw_datetime", "".join(date_str)[:-1])
        LottoItem.add_value("draw_number", response.xpath('//h4/strong//text()').get())
        LottoItem.add_value("sales", response.xpath('//ul/li/strong//text()').get())
        LottoItem.add_value("cat_1_prize", rows[0].xpath('./td//text()').getall()[3])
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./td//text()').getall()[3])
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./td//text()').getall()[3])
        LottoItem.add_value("cat_4_prize", rows[3].xpath('./td//text()').getall()[3])
        LottoItem.add_value("cat_5_prize", rows[4].xpath('./td//text()').getall()[3])
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td//text()').getall()[2])
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./td//text()').getall()[2])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./td//text()').getall()[2])
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./td//text()').getall()[2])
        LottoItem.add_value("cat_5_winners", rows[4].xpath('./td//text()').getall()[2])
        yield LottoItem.load_item()


class SwedenLotto1(scrapy.Spider):

    name = "SwedenLotto1"

    # match_dream is match_7 as well as at least 2 joker digits (front or back)
    # jackpot = dream win (match_7 + 2 joker), secondary_jackpot = match_7
    # note: jackpot values will be 0 unless won
    # note: DREAM-WIN NOW SCRAPED IN SWEDENJOKER

    def start_requests(self):
        self.name = "SwedenLotto1"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://lotteryguru.com/sweden-lottery-results"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=SwedenLotto1Item(), selector=response)
        next_jackpot = response.xpath('//div[@class="lg-card lg-link"]')
        draw_datetime = next_jackpot[1].xpath('.//div[@class="lg-card-row"]//span[@class="lg-date"]//text()').get()
        next_jackpot = next_jackpot[1].xpath('.//div[@class="lg-card-row lg-jackpot-info"]//div[@class="lg-sum"]//text()').get()
        LottoItem.add_value("name", self.name)
        LottoItem.add_value("estimated_next_jackpot", next_jackpot)
        LottoItem.add_value("draw_datetime",  datetime.strptime(draw_datetime, "%d %b %Y").strftime("%Y-%m-%d"))
        yield LottoItem.load_item()


class SwedenLotto2(scrapy.Spider):

    name = "SwedenLotto2"

    # match_dream is match_7 as well as at least 2 joker digits (front or back)
    # jackpot = dream win (match_7 + 2 joker), secondary_jackpot = match_7
    # note: jackpot values will be 0 unless won
    # note: DREAM-WIN NOW SCRAPED IN SWEDENJOKER

    def start_requests(self):
        self.name = "SwedenLotto2"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        headers = {
            'authority': 'api.www.svenskaspel.se',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
            'content-type': 'text/plain',
            'origin': 'https://www.svenskaspel.se',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.svenskaspel.se/',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'cookie': 'devid=c971eb83-6924-46b8-90b4-c139c330804e; _ga=GA1.2.1204281379.1610617826; AMCVS_88743E6A5A74B5900A495D61%40AdobeOrg=1; s_cc=true; adobeujs-optin=%7B%22aam%22%3Afalse%2C%22adcloud%22%3Afalse%2C%22aa%22%3Atrue%2C%22campaign%22%3Afalse%2C%22ecid%22%3Atrue%2C%22livefyre%22%3Afalse%2C%22target%22%3Afalse%2C%22mediaaa%22%3Afalse%7D; AMCV_88743E6A5A74B5900A495D61%40AdobeOrg=-637568504%7CMCIDTS%7C18647%7CMCMID%7C01531841484907949164140167357533082406%7CMCAAMLH-1611676140%7C6%7CMCAAMB-1611676140%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1611078540s%7CNONE%7CvVersion%7C5.1.1; _gid=GA1.2.89385455.1619707838; AMCV_88743E6A5A74B5900A495D61%40AdobeOrg=-637568504%7CMCIDTS%7C18747%7CMCMID%7C01531841484907949164140167357533082406%7CMCAAMLH-1620315573%7C6%7CMCAAMB-1620315573%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1619717973s%7CNONE%7CvVersion%7C5.1.1; gpv=lotto%3Aresultat%3A2021-04-21',
        }
        sat_lotto_id, sat_joker_id, sat_date = 2120, 1911, "2021-04-24"
        wed_lotto_id, wed_joker_id, wed_date = 2122, 937, "2021-04-28"

        weekday_decimal = int(datetime.now().strftime("%w"))
        if weekday_decimal in [0, 1, 2, 3]: # Sunday, Monday, Tuesday, Wednesday
            # use saturday url since draw is in evening
            num_days_difference = (datetime.now() - datetime.strptime(sat_date, "%Y-%m-%d")).days
            num_weeks_difference = math.floor(num_days_difference/7)
            new_lotto_id = sat_lotto_id + num_weeks_difference
            new_joker_id = sat_joker_id + num_weeks_difference
            url = f'https://api.www.svenskaspel.se/multifetch?urls=/draw/lottosaturday/draws/{new_lotto_id}/result|draw/jokersaturday/draws/{new_joker_id}/result'
        elif weekday_decimal in [4, 5, 6]: # Thursday, Friday, Saturday
            # wednesday url
            num_days_difference = (datetime.now() - datetime.strptime(wed_date, "%Y-%m-%d")).days
            num_weeks_difference = math.floor(num_days_difference/7)
            new_lotto_id = wed_lotto_id + num_weeks_difference
            new_joker_id = wed_joker_id + num_weeks_difference
            url = f'https://api.www.svenskaspel.se/multifetch?urls=/draw/lottowednesday/draws/{new_lotto_id}/result|draw/jokerwednesday/draws/{new_joker_id}/result'

        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=SwedenLotto2Item(), selector=response)
        latest = response.json()['responses'][0]['result']
        balls_lst = latest['drawResult'][1]['drawNumbers'][0]['numbers']
        bonus_balls_lst = latest['drawResult'][1]['drawNumbers'][1]['numbers']
        rows = latest['distribution'][1]['distribution']

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", str(balls_lst[0]))
        LottoItem.add_value("ball1", str(balls_lst[1]))
        LottoItem.add_value("ball2", str(balls_lst[2]))
        LottoItem.add_value("ball3", str(balls_lst[3]))
        LottoItem.add_value("ball4", str(balls_lst[4]))
        LottoItem.add_value("ball5", str(balls_lst[5]))
        LottoItem.add_value("ball6", str(balls_lst[6]))
        LottoItem.add_value("bonus_ball0", str(bonus_balls_lst[0]))
        LottoItem.add_value("bonus_ball1", str(bonus_balls_lst[1]))
        LottoItem.add_value("bonus_ball2", str(bonus_balls_lst[2]))
        LottoItem.add_value("bonus_ball3", str(bonus_balls_lst[3]))
        LottoItem.add_value("draw_datetime", latest['regCloseTime'].split('T')[0])
        LottoItem.add_value("combined_sales", latest['currentNetSale'])
        if "mvinsten" in rows[5]['name']:
            LottoItem.add_value("cat_1_prize", str(rows[0]['amount']))
            LottoItem.add_value("cat_2_prize", str(rows[1]['amount']))
            LottoItem.add_value("cat_3_prize", str(rows[2]['amount']))
            LottoItem.add_value("cat_4_prize", str(rows[3]['amount']))
            LottoItem.add_value("cat_5_prize", str(rows[4]['amount']))
            LottoItem.add_value("cat_1_winners", str(rows[0]['winners']))
            LottoItem.add_value("cat_2_winners", str(rows[1]['winners']))
            LottoItem.add_value("cat_3_winners", str(rows[2]['winners']))
            LottoItem.add_value("cat_4_winners", str(rows[3]['winners']))
            LottoItem.add_value("cat_5_winners", str(rows[4]['winners']))
        elif "mvinsten" in rows[0]['name']:
            # In the case match_dream has been won and order is rearranged
            LottoItem.add_value("cat_1_prize", str(rows[1]['amount']))
            LottoItem.add_value("cat_2_prize", str(rows[2]['amount']))
            LottoItem.add_value("cat_3_prize", str(rows[3]['amount']))
            LottoItem.add_value("cat_4_prize", str(rows[4]['amount']))
            LottoItem.add_value("cat_5_prize", str(rows[5]['amount']))
            LottoItem.add_value("cat_1_winners", str(rows[1]['winners']))
            LottoItem.add_value("cat_2_winners", str(rows[2]['winners']))
            LottoItem.add_value("cat_3_winners", str(rows[3]['winners']))
            LottoItem.add_value("cat_4_winners", str(rows[4]['winners']))
            LottoItem.add_value("cat_5_winners", str(rows[5]['winners']))
        yield LottoItem.load_item()


class SwedenJoker(scrapy.Spider):

    name = "SwedenJoker"

    # note: DREAMWIN IS cat_1

    def start_requests(self):
        self.name = "SwedenJoker"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.svenskaspel.se/lotto/resultat"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        self.dream_jackpot = [i for i in response.xpath('//span[@class="nav-list-item-link-jackpot"]/text()').getall()
            if "vinsten" in i.lower()][0]
        headers = {
            'authority': 'api.www.svenskaspel.se',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
            'content-type': 'text/plain',
            'origin': 'https://www.svenskaspel.se',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.svenskaspel.se/',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'cookie': 'devid=c971eb83-6924-46b8-90b4-c139c330804e; _ga=GA1.2.1204281379.1610617826; AMCVS_88743E6A5A74B5900A495D61%40AdobeOrg=1; s_cc=true; adobeujs-optin=%7B%22aam%22%3Afalse%2C%22adcloud%22%3Afalse%2C%22aa%22%3Atrue%2C%22campaign%22%3Afalse%2C%22ecid%22%3Atrue%2C%22livefyre%22%3Afalse%2C%22target%22%3Afalse%2C%22mediaaa%22%3Afalse%7D; AMCV_88743E6A5A74B5900A495D61%40AdobeOrg=-637568504%7CMCIDTS%7C18647%7CMCMID%7C01531841484907949164140167357533082406%7CMCAAMLH-1611676140%7C6%7CMCAAMB-1611676140%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1611078540s%7CNONE%7CvVersion%7C5.1.1; _gid=GA1.2.89385455.1619707838; AMCV_88743E6A5A74B5900A495D61%40AdobeOrg=-637568504%7CMCIDTS%7C18747%7CMCMID%7C01531841484907949164140167357533082406%7CMCAAMLH-1620315573%7C6%7CMCAAMB-1620315573%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1619717973s%7CNONE%7CvVersion%7C5.1.1; gpv=lotto%3Aresultat%3A2021-04-21',
        }
        sat_lotto_id, sat_joker_id, sat_date = 2120, 1911, "2021-04-24"
        wed_lotto_id, wed_joker_id, wed_date = 2122, 937, "2021-04-28"

        weekday_decimal = int(datetime.now().strftime("%w"))
        if weekday_decimal in [0, 1, 2, 3]: # Sunday, Monday, Tuesday, Wednesday
            # use saturday url since draw is in evening
            num_days_difference = (datetime.now() - datetime.strptime(sat_date, "%Y-%m-%d")).days
            num_weeks_difference = math.floor(num_days_difference/7)
            new_lotto_id = sat_lotto_id + num_weeks_difference
            new_joker_id = sat_joker_id + num_weeks_difference
            url = f'https://api.www.svenskaspel.se/multifetch?urls=/draw/lottosaturday/draws/{new_lotto_id}/result|draw/jokersaturday/draws/{new_joker_id}/result'
        elif weekday_decimal in [4, 5, 6]: # Thursday, Friday, Saturday
            # wednesday url
            num_days_difference = (datetime.now() - datetime.strptime(wed_date, "%Y-%m-%d")).days
            num_weeks_difference = math.floor(num_days_difference/7)
            new_lotto_id = wed_lotto_id + num_weeks_difference
            new_joker_id = wed_joker_id + num_weeks_difference
            url = f'https://api.www.svenskaspel.se/multifetch?urls=/draw/lottowednesday/draws/{new_lotto_id}/result|draw/jokerwednesday/draws/{new_joker_id}/result'
        yield scrapy.Request(url=url, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":10})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=SwedenJokerItem(), selector=response)
        latest = response.json()['responses'][1]['result']
        balls_lst = latest['drawResult']['numbers']
        rows = latest['distribution']

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", str(balls_lst[0]))
        LottoItem.add_value("ball1", str(balls_lst[1]))
        LottoItem.add_value("ball2", str(balls_lst[2]))
        LottoItem.add_value("ball3", str(balls_lst[3]))
        LottoItem.add_value("ball4", str(balls_lst[4]))
        LottoItem.add_value("ball5", str(balls_lst[5]))
        LottoItem.add_value("ball6", str(balls_lst[6]))
        LottoItem.add_value("draw_datetime", latest['regCloseTime'].split('T')[0])
        LottoItem.add_value("sales", latest['currentNetSale'])
        LottoItem.add_value("estimated_next_jackpot", self.dream_jackpot)
        """
        check lotto prize tables for dreamwinners
        """
        lotto_latest = response.json()['responses'][0]['result']
        lotto_rows = lotto_latest['distribution'][1]['distribution']
        if "mvinsten" in lotto_rows[5]['name']:
            cat_1_prize = lotto_rows[5]['amount']
            cat_1_winners = lotto_rows[5]['winners']
        elif "mvinsten" in lotto_rows[0]['name']:
            cat_1_prize = lotto_rows[0]['amount']
            cat_1_winners = lotto_rows[0]['winners']

        LottoItem.add_value("cat_1_prize", str(cat_1_prize))
        LottoItem.add_value("cat_2_prize", str(rows[0]['amount']))
        LottoItem.add_value("cat_3_prize", str(rows[1]['amount']))
        LottoItem.add_value("cat_4_prize", str(rows[2]['amount']))
        LottoItem.add_value("cat_5_prize", str(rows[3]['amount']))
        LottoItem.add_value("cat_6_prize", str(rows[4]['amount']))
        LottoItem.add_value("cat_7_prize", str(rows[5]['amount']))
        LottoItem.add_value("cat_1_winners", str(cat_1_winners))
        LottoItem.add_value("cat_2_winners", str(rows[0]['winners']))
        LottoItem.add_value("cat_3_winners", str(rows[1]['winners']))
        LottoItem.add_value("cat_4_winners", str(rows[2]['winners']))
        LottoItem.add_value("cat_5_winners", str(rows[3]['winners']))
        LottoItem.add_value("cat_6_winners", str(rows[4]['winners']))
        LottoItem.add_value("cat_7_winners", str(rows[5]['winners']))
        yield LottoItem.load_item()


class SwitzerlandLotto(scrapy.Spider):

    name = "SwitzerlandLotto"

    def start_requests(self):
        self.name = "SwitzerlandLotto"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.swisslos.ch/en/swisslotto/information/winning-numbers/winning-numbers.html"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=SwitzerlandLottoItem(), selector=response)
        balls_lst = response.xpath('//li[@class="actual-numbers__number actual-numbers__number___normal"]/span/text()').getall()
        bonus_ball = response.xpath('//li[@class="actual-numbers__number actual-numbers__number___lucky"]/span/text()').get()
        rows = response.xpath('//table[@class="quotes__game-table"]/tbody/tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("bonus_ball", bonus_ball)
        draw_date = response.xpath('//label/div/input/@value').get()
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d.%m.%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("estimated_next_jackpot", response.xpath('//td[@class="quotes__game-jackpot-value"]/text()').get())
        # jackpot will be '0' unless won
        LottoItem.add_value("cat_1_prize", rows[0].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_4_prize", rows[3].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_5_prize", rows[4].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_6_prize", rows[5].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_7_prize", rows[6].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_8_prize", rows[7].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_5_winners", rows[4].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_6_winners", rows[5].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_7_winners", rows[6].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_8_winners", rows[7].xpath('./td/text()').getall()[1])
        yield LottoItem.load_item()


class SwitzerlandJoker(scrapy.Spider):

    name = "SwitzerlandJoker"

    def start_requests(self):
        self.name = "SwitzerlandJoker"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.swisslos.ch/en/swisslotto/information/winning-numbers/winning-numbers.html"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=SwitzerlandJokerItem(), selector=response)
        balls_lst = response.xpath('//div[@class="actual-numbers__extra-game___number"]/div/text()').get()
        rows = response.xpath('//table[@class="quotes__extra-game-table"]/tbody/tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        draw_date = response.xpath('//label/div/input/@value').get()
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d.%m.%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("estimated_next_jackpot", response.xpath('//td[@class="quotes__game-jackpot-value"]/text()').getall()[1])
        LottoItem.add_value("cat_1_prize", rows[0].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_2_prize", rows[1].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_4_prize", rows[3].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_5_prize", rows[4].xpath('./td/text()').getall()[2])
        LottoItem.add_value("cat_1_winners", rows[0].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_2_winners", rows[1].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_3_winners", rows[2].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_4_winners", rows[3].xpath('./td/text()').getall()[1])
        LottoItem.add_value("cat_5_winners", rows[4].xpath('./td/text()').getall()[1])
        yield LottoItem.load_item()



class TaiwanLotto649(scrapy.Spider):

    name = "TaiwanLotto649"

    def start_requests(self):
        self.name = "TaiwanLotto649"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://en.lottolyzer.com/home/taiwan/lotto-649"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=TaiwanLotto649Item(), selector=response)
        latest = response.xpath('//div[@class="latest"]')[0]
        rows = latest.xpath('.//tbody/tr')
        balls_lst = latest.xpath('.//img[@class="ball"]/@alt').getall()

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("bonus_ball", balls_lst[6])
        draw_date = latest.xpath('.//span[@id="latest_date"]/text()').get().strip()
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d %b %Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("estimated_next_jackpot", latest.xpath(
            './div[@class="upcoming"]//span[@class="prize-data"]/text()').get().strip())
        for i in range(8):
            cat_text = rows[i].xpath('./td/text()').getall()[-1]
            if any(string in cat_text.lower() for string in ['winners of', 'winner of']):
                LottoItem.add_value(f"cat_{i+1}_prize", cat_text.split('of')[1].strip())
                LottoItem.add_value(f"cat_{i+1}_winners", cat_text.split('of')[0].strip())
            else:
                LottoItem.add_value(f"cat_{i+1}_prize", '0')
                LottoItem.add_value(f"cat_{i+1}_winners", '0')

        yield LottoItem.load_item()


class TaiwanSuperLotto638(scrapy.Spider):

    name = "TaiwanSuperLotto638"

    def start_requests(self):
        self.name = "TaiwanSuperLotto638"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://en.lottolyzer.com/home/taiwan/super-lotto-638"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=TaiwanSuperLotto638Item(), selector=response)
        latest = response.xpath('//div[@class="latest"]')[0]
        rows = latest.xpath('.//tbody/tr')
        balls_lst = latest.xpath('.//img[@class="ball"]/@alt').getall()

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("bonus_ball", balls_lst[6])
        draw_date = latest.xpath('.//span[@id="latest_date"]/text()').get().strip()
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d %b %Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("estimated_next_jackpot", latest.xpath(
            './div[@class="upcoming"]//span[@class="prize-data"]/text()').get().strip())
        for i in range(10):
            cat_text = rows[i].xpath('./td/text()').getall()[-1]
            if any(string in cat_text.lower() for string in ['winners of', 'winner of']):
                LottoItem.add_value(f"cat_{i+1}_prize", cat_text.split('of')[1].strip())
                LottoItem.add_value(f"cat_{i+1}_winners", cat_text.split('of')[0].strip())
            else:
                LottoItem.add_value(f"cat_{i+1}_prize", '0')
                LottoItem.add_value(f"cat_{i+1}_winners", '0')

        yield LottoItem.load_item()


class TrinidadLottoPlus(scrapy.Spider):

    name = "TrinidadLottoPlus"

    def start_requests(self):
        self.name = "TrinidadLottoPlus"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "http://www.nlcbplaywhelotto.com/nlcb-lotto-plus-results/"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=TrinidadLottoPlusItem(), selector=response)
        latest = response.xpath('//div[@id="results"]')[0]
        balls_lst = latest.xpath('//div[@class="drawDetails"]/div/text()').getall()[1:]

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("bonus_ball", balls_lst[5])
        draw_date = [i for i in response.xpath('//div[@id="results"]/strong/text()').getall() if "date" in i.lower()][0].split(':')[1].strip()
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d-%b-%y").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", latest.xpath('.//div[@class="drawnum"]/text()').get())
        LottoItem.add_value("estimated_next_jackpot", latest.xpath('./div[@id="jackpot"]/strong/text()').get())
        yield LottoItem.load_item()


class TurkeySansTopu(scrapy.Spider):

    name = "TurkeySansTopu"

    #note: scrape will fail at beginning of the month until a draw occurs

    def start_requests(self):
        self.name = "TurkeySansTopu"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        headers = {
            'authority': 'www.millipiyangoonline.com',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'content-type': 'application/json',
            'dnt': '1',
            'referer': 'https://www.millipiyangoonline.com/sans-topu/sonuclar',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        date_str = (datetime.now()-timedelta(days=1)).strftime("%m.%Y")
        url = f'https://www.millipiyangoonline.com/sisalsans/result.sanstopu.{date_str}.json?cache=false'
        yield scrapy.Request(url=url, headers=headers, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":20})

    def parse(self, response):
        latest = response.json()
        for draw in reversed(latest):
            if len(draw['drawNumbers']) == 0:
                continue
            elif len(draw['drawNumbers']) == 5:
                draw_number = draw['drawnNr']
                draw_year = draw['drawYear']
                break

        headers = {
            'authority': 'www.millipiyangoonline.com',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'content-type': 'application/json',
            'dnt': '1',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        url = f"https://www.millipiyangoonline.com/sisalsans/drawdetails.sanstopu.{draw_number}.{draw_year}.json"
        yield scrapy.Request(url=url, headers=headers, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":20})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=TurkeySansTopuItem(), selector=response)
        latest = response.json()
        balls_lst = [str(i) for i in latest['winningNumber']]

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("bonus_ball", str(latest['numberJolly'][0]))
        drawdate = datetime.strptime(latest['dateDetails'], "%m/%d/%Y").strftime("%Y-%m-%d")
        LottoItem.add_value("draw_datetime", drawdate)
        LottoItem.add_value("draw_number", str(latest['number']))
        if int(latest['tableResult'][0]['totalWinners']) == 0:
            LottoItem.add_value("cat_1_prize", str(int(latest['tableResult'][0]['prizeFound'])/1000.0))
        else:
            LottoItem.add_value("cat_1_prize", str(int(latest['tableResult'][0]['prizeWinner'])/1000.0))
        LottoItem.add_value("cat_2_prize", str(int(latest['tableResult'][1]['prizeWinner'])/1000.0))
        LottoItem.add_value("cat_3_prize", str(int(latest['tableResult'][2]['prizeWinner'])/1000.0))
        LottoItem.add_value("cat_4_prize", str(int(latest['tableResult'][3]['prizeWinner'])/1000.0))
        LottoItem.add_value("cat_5_prize", str(int(latest['tableResult'][4]['prizeWinner'])/1000.0))
        LottoItem.add_value("cat_6_prize", str(int(latest['tableResult'][5]['prizeWinner'])/1000.0))
        LottoItem.add_value("cat_7_prize", str(int(latest['tableResult'][6]['prizeWinner'])/1000.0))
        LottoItem.add_value("cat_8_prize", str(int(latest['tableResult'][7]['prizeWinner'])/1000.0))
        LottoItem.add_value("cat_9_prize", str(int(latest['tableResult'][8]['prizeWinner'])/1000.0))
        LottoItem.add_value("cat_1_winners", latest['tableResult'][0]['totalWinners'])
        LottoItem.add_value("cat_2_winners", latest['tableResult'][1]['totalWinners'])
        LottoItem.add_value("cat_3_winners", latest['tableResult'][2]['totalWinners'])
        LottoItem.add_value("cat_4_winners", latest['tableResult'][3]['totalWinners'])
        LottoItem.add_value("cat_5_winners", latest['tableResult'][4]['totalWinners'])
        LottoItem.add_value("cat_6_winners", latest['tableResult'][5]['totalWinners'])
        LottoItem.add_value("cat_7_winners", latest['tableResult'][6]['totalWinners'])
        LottoItem.add_value("cat_8_winners", latest['tableResult'][7]['totalWinners'])
        LottoItem.add_value("cat_9_winners", latest['tableResult'][8]['totalWinners'])
        yield LottoItem.load_item()


class TurkeySayisalLoto(scrapy.Spider):

    name = "TurkeySayisalLoto"

    #note: scrape will fail at beginning of the month until a draw occurs

    def start_requests(self):
        self.name = "TurkeySayisalLoto"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        headers = {
            'authority': 'www.millipiyangoonline.com',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'content-type': 'application/json',
            'dnt': '1',
            'referer': 'https://www.millipiyangoonline.com/sayisal-loto/sonuclar',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        date_str = (datetime.now()-timedelta(days=1)).strftime("%m.%Y")
        url = f"https://www.millipiyangoonline.com/sisalsans/result.sayisaloto.{date_str}.json?cache=false"
        yield scrapy.Request(url=url, headers=headers, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":20})

    def parse(self, response):
        latest = response.json()
        for draw in reversed(latest):
            if len(draw['drawNumbers']) == 0:
                continue
            elif len(draw['drawNumbers']) == 6:
                draw_number = draw['drawnNr']
                draw_year = draw['drawYear']
                break

        headers = {
            'authority': 'www.millipiyangoonline.com',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'content-type': 'application/json',
            'dnt': '1',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        url = f"https://www.millipiyangoonline.com/sisalsans/drawdetails.sayisaloto.{draw_number}.{draw_year}.json"
        yield scrapy.Request(url=url, headers=headers, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":20})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=TurkeySayisalLotoItem(), selector=response)
        latest = response.json()
        balls_lst = [str(i) for i in latest['winningNumber']]

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("bonus_ball", str(latest['numberJolly'][0]))
        drawdate = datetime.strptime(latest['dateDetails'], "%m/%d/%Y").strftime("%Y-%m-%d")
        LottoItem.add_value("draw_datetime", drawdate)
        LottoItem.add_value("draw_number", str(latest['number']))
        if int(latest['tableResult'][0]['totalWinners']) == 0:
            LottoItem.add_value("cat_1_prize", str(int(latest['tableResult'][0]['prizeFound'])/1000.0))
        else:
            LottoItem.add_value("cat_1_prize", str(int(latest['tableResult'][0]['prizeWinner'])/1000.0))
        LottoItem.add_value("cat_2_prize", str(int(latest['tableResult'][1]['prizeWinner'])/1000.0))
        LottoItem.add_value("cat_3_prize", str(int(latest['tableResult'][2]['prizeWinner'])/1000.0))
        LottoItem.add_value("cat_4_prize", str(int(latest['tableResult'][3]['prizeWinner'])/1000.0))
        LottoItem.add_value("cat_5_prize", str(int(latest['tableResult'][4]['prizeWinner'])/1000.0))
        LottoItem.add_value("cat_6_prize", str(int(latest['tableResult'][5]['prizeWinner'])/1000.0))
        LottoItem.add_value("cat_1_winners", latest['tableResult'][0]['totalWinners'])
        LottoItem.add_value("cat_2_winners", latest['tableResult'][1]['totalWinners'])
        LottoItem.add_value("cat_3_winners", latest['tableResult'][2]['totalWinners'])
        LottoItem.add_value("cat_4_winners", latest['tableResult'][3]['totalWinners'])
        LottoItem.add_value("cat_5_winners", latest['tableResult'][4]['totalWinners'])
        LottoItem.add_value("cat_6_winners", latest['tableResult'][5]['totalWinners'])
        yield LottoItem.load_item()


class TurkeySuperLoto(scrapy.Spider):

    name = "TurkeySuperLoto"

    #note: scrape will fail at beginning of the month until a draw occurs

    def start_requests(self):
        self.name = "TurkeySuperLoto"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        headers = {
            'authority': 'www.millipiyangoonline.com',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'content-type': 'application/json',
            'dnt': '1',
            'referer': 'https://www.millipiyangoonline.com/super-loto/sonuclar',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        date_str = (datetime.now()-timedelta(days=1)).strftime("%m.%Y")
        url = f"https://www.millipiyangoonline.com/sisalsans/result.superloto.{date_str}.json?cache=false"
        yield scrapy.Request(url=url, headers=headers, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":20})

    def parse(self, response):
        latest = response.json()
        for draw in reversed(latest):
            if len(draw['drawNumbers']) == 0:
                continue
            elif len(draw['drawNumbers']) == 6:
                draw_number = draw['drawnNr']
                draw_year = draw['drawYear']
                break

        headers = {
            'authority': 'www.millipiyangoonline.com',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'content-type': 'application/json',
            'dnt': '1',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        url = f"https://www.millipiyangoonline.com/sisalsans/drawdetails.superloto.{draw_number}.{draw_year}.json"
        yield scrapy.Request(url=url, headers=headers, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":20})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=TurkeySuperLotoItem(), selector=response)
        latest = response.json()
        balls_lst = [str(i) for i in latest['winningNumber']]

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        drawdate = datetime.strptime(latest['dateDetails'], "%m/%d/%Y").strftime("%Y-%m-%d")
        LottoItem.add_value("draw_datetime", drawdate)
        LottoItem.add_value("draw_number", str(latest['number']))
        if int(latest['tableResult'][0]['totalWinners']) == 0:
            LottoItem.add_value("cat_1_prize", str(int(latest['tableResult'][0]['prizeFound'])/1000.0))
        else:
            LottoItem.add_value("cat_1_prize", str(int(latest['tableResult'][0]['prizeWinner'])/1000.0))
        LottoItem.add_value("cat_2_prize", str(int(latest['tableResult'][1]['prizeWinner'])/1000.0))
        LottoItem.add_value("cat_3_prize", str(int(latest['tableResult'][2]['prizeWinner'])/1000.0))
        LottoItem.add_value("cat_4_prize", str(int(latest['tableResult'][3]['prizeWinner'])/1000.0))
        LottoItem.add_value("cat_5_prize", str(int(latest['tableResult'][4]['prizeWinner'])/1000.0))
        LottoItem.add_value("cat_1_winners", latest['tableResult'][0]['totalWinners'])
        LottoItem.add_value("cat_2_winners", latest['tableResult'][1]['totalWinners'])
        LottoItem.add_value("cat_3_winners", latest['tableResult'][2]['totalWinners'])
        LottoItem.add_value("cat_4_winners", latest['tableResult'][3]['totalWinners'])
        LottoItem.add_value("cat_5_winners", latest['tableResult'][4]['totalWinners'])
        yield LottoItem.load_item()


class UKLotto(scrapy.Spider):

    name = "UKLotto"

    def start_requests(self):
        self.name = "UKLotto"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www.lotto.net/uk-lotto/results"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        self.next_jackpot = response.xpath('//div[@class="jackpot"]//span/text()').getall()[1].strip()
        self.draw_date = response.xpath('//div[@class="date"]/span/text()').get().strip()
        next_page = response.xpath("//div[@class='results-big']/div[@class='row-3']/a/@href").get()
        url = urljoin(response.url, next_page)
        yield scrapy.Request(url, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":10})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=UKLottoItem(), selector=response)
        balls_lst = response.xpath('//ul[@class="balls"]/li/span/text()').getall()
        rows = response.xpath('//table//tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("ball5", balls_lst[5])
        LottoItem.add_value("bonus_ball", balls_lst[6])
        LottoItem.add_value("draw_datetime", datetime.strptime(self.draw_date, "%d %B %Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("estimated_next_jackpot", self.next_jackpot)
        LottoItem.add_value("cat_1_prize", rows[1].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_2_prize", rows[2].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_3_prize", rows[3].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_4_prize", rows[4].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_5_prize", rows[5].xpath('./td[@align="right"]/text()').get().strip())
        LottoItem.add_value("cat_6_prize", "2")
        LottoItem.add_value("cat_1_winners", rows[1].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_2_winners", rows[2].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_3_winners", rows[3].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_4_winners", rows[4].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_5_winners", rows[5].xpath('./td/text()').getall()[-1].strip())
        LottoItem.add_value("cat_6_winners", rows[6].xpath('./td/text()').getall()[-1].strip())
        try:
            rolldown_check = rows[1].xpath('./td[@align="right"]/span/text()').getall()[-1].lower()
            if "rolldown" in rolldown_check:
                LottoItem.add_value("rolldown", "yes")
            else:
                LottoItem.add_value("rolldown", "no")
        except:
            LottoItem.add_value("rolldown", "no")
        yield LottoItem.load_item()


class UkraineSuperLoto(scrapy.Spider):

    name = "UkraineSuperLoto"

    def start_requests(self):
        self.name = "UkraineSuperLoto"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://unl.ua/api/result/superloto"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=UkraineSuperLotoItem(), selector=response)
        latest = response.json()

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", str(latest['balls'][0]))
        LottoItem.add_value("ball1", str(latest['balls'][1]))
        LottoItem.add_value("ball2", str(latest['balls'][2]))
        LottoItem.add_value("ball3", str(latest['balls'][3]))
        LottoItem.add_value("ball4", str(latest['balls'][4]))
        LottoItem.add_value("ball5", str(latest['balls'][5]))
        LottoItem.add_value("draw_datetime", str(latest['timestamp']))
        LottoItem.add_value("draw_number", str(latest['draw']))
        LottoItem.add_value("cat_1_prize", str(latest['winners'][0]['prize']))
        LottoItem.add_value("cat_2_prize", str(latest['winners'][1]['prize']))
        LottoItem.add_value("cat_3_prize", str(latest['winners'][2]['prize']))
        LottoItem.add_value("cat_4_prize", str(latest['winners'][3]['prize']))
        LottoItem.add_value("cat_5_prize", str(latest['winners'][4]['prize']))
        LottoItem.add_value("cat_1_winners", str(latest['winners'][0]['people_win']))
        LottoItem.add_value("cat_2_winners", str(latest['winners'][1]['people_win']))
        LottoItem.add_value("cat_3_winners", str(latest['winners'][2]['people_win']))
        LottoItem.add_value("cat_4_winners", str(latest['winners'][3]['people_win']))
        LottoItem.add_value("cat_5_winners", str(latest['winners'][4]['people_win']))
        yield LottoItem.load_item()


class UkraineMaxima(scrapy.Spider):

    name = "UkraineMaxima"

    def start_requests(self):
        self.name = "UkraineMaxima"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = 'https://unl.ua/api/result/maxima'
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        LottoItem = ItemLoader(item=UkraineMaximaItem(), selector=response)
        latest = response.json()

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", str(latest['balls'][0]))
        LottoItem.add_value("ball1", str(latest['balls'][1]))
        LottoItem.add_value("ball2", str(latest['balls'][2]))
        LottoItem.add_value("ball3", str(latest['balls'][3]))
        LottoItem.add_value("ball4", str(latest['balls'][4]))
        LottoItem.add_value("draw_datetime", str(latest['timestamp']))
        LottoItem.add_value("draw_number", str(latest['draw']))
        LottoItem.add_value("cat_1_prize", str(latest['winners'][0]['prize']))
        LottoItem.add_value("cat_2_prize", str(latest['winners'][1]['prize']))
        LottoItem.add_value("cat_3_prize", str(latest['winners'][2]['prize']))
        LottoItem.add_value("cat_4_prize", str(latest['winners'][3]['prize']))
        LottoItem.add_value("cat_1_winners", str(latest['winners'][0]['people_win']))
        LottoItem.add_value("cat_2_winners", str(latest['winners'][1]['people_win']))
        LottoItem.add_value("cat_3_winners", str(latest['winners'][2]['people_win']))
        LottoItem.add_value("cat_4_winners", str(latest['winners'][3]['people_win']))
        yield LottoItem.load_item()


class UkraineMegalot(scrapy.Spider):

    name = "UkraineMegalot"

    # jackpot = match_6_bonus; secondary_jackpot = match_6 (also prog. jackpot)
    # NO NUMBER OF WINNERS DATA (CAN ONLY SEE IF JACKPOTS HAVE BEEN WON OR NOT)

    def start_requests(self):
        self.name = "UkraineMegalot"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://msl.ua/megalote/ru/archive"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        latest = response.xpath('//div[@class="archive_results"]/div[@class="archive_results-item"]')[0]
        next_page = latest.xpath('.//a/@href').get()
        self.draw_datetime = latest.xpath('.//p[@class="archive_result-date"]/text()').get().strip()
        self.draw_number = latest.xpath('.//a/@href').get().split('/')[-1]
        self.balls_lst = latest.xpath('.//span[@class="ball-number"]/text()').getall()
        self.megajackpot = latest.xpath('.//p/span/text()').getall()[-1]
        self.megaprize = latest.xpath('.//p/span/text()').getall()[-2]
        url = urljoin(response.url, next_page)
        yield scrapy.Request(url, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":10})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=UkraineMegalotItem(), selector=response)
        rows = response.xpath('//div[@class="results_stats results_stats-cent"]/div[@class="results_stats-line"]')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", self.balls_lst[0])
        LottoItem.add_value("ball1", self.balls_lst[1])
        LottoItem.add_value("ball2", self.balls_lst[2])
        LottoItem.add_value("ball3", self.balls_lst[3])
        LottoItem.add_value("ball4", self.balls_lst[4])
        LottoItem.add_value("ball5", self.balls_lst[5])
        LottoItem.add_value("bonus_ball", self.balls_lst[6])
        month_dict = {'января':1, 'февраля':2, 'марта':3, 'апреля':4, 'мая':5, 'июня':6,
        'июля':7, 'августа':8, 'сентября':9, 'октября':10, 'ноября':11, 'декабря':12}
        day = self.draw_datetime.split(' ')[0]
        month = month_dict[self.draw_datetime.split(' ')[1].encode('utf-8').decode('utf-8')]
        year = self.draw_datetime.split(' ')[2]
        full_date = f"{year}-{month}-{day}"
        LottoItem.add_value("draw_datetime", datetime.strptime(full_date, "%Y-%m-%d").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", self.draw_number)
        LottoItem.add_value("estimated_next_jackpot", response.xpath(
            '//div[@class="ml-prizes"]/p[@class="ml-prizes_sum"]/text()').get())
        LottoItem.add_value("estimated_next_secondary_jackpot", response.xpath(
            '//div[@class="ml-prizes"]/p[@class="ml-prizes_sum"]/text()').getall()[2])
        LottoItem.add_value("cat_1_prize", self.megajackpot)
        LottoItem.add_value("cat_2_prize", self.megaprize)
        LottoItem.add_value("cat_3_prize", rows[2].xpath('./p/text()').getall()[-1])
        LottoItem.add_value("cat_4_prize", rows[3].xpath('./p/text()').getall()[-1])
        LottoItem.add_value("cat_5_prize", rows[4].xpath('./p/text()').getall()[-1])
        LottoItem.add_value("cat_6_prize", rows[5].xpath('./p/text()').getall()[-1])
        LottoItem.add_value("cat_7_prize", rows[6].xpath('./p/text()').getall()[-1])
        LottoItem.add_value("cat_8_prize", rows[7].xpath('./p/text()').getall()[-1])
        yield LottoItem.load_item()


class UruguayGold5(scrapy.Spider):

    name = "UruguayGold5"

    def start_requests(self):
        self.name = "UruguayGold5"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www3.labanca.com.uy/resultados/cincodeoro"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        LottoItem = ItemLoader(item=UruguayGold5Item(), selector=response)
        balls_lst = response.xpath('//ul/li/img/@alt').getall()

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[0])
        LottoItem.add_value("ball1", balls_lst[1])
        LottoItem.add_value("ball2", balls_lst[2])
        LottoItem.add_value("ball3", balls_lst[3])
        LottoItem.add_value("ball4", balls_lst[4])
        LottoItem.add_value("bonus_ball", balls_lst[5])
        draw_date = clean_datetime(response.xpath('//select[@id="fecha_sorteo"]/option[@selected="selected"]/text()').get())
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d/%m/%Y").strftime("%Y-%m-%d"))
        cat_1_prize_temp = swap_commas_fullstops(response.xpath('//span[@class="monto-pozo"]/text()').get())
        cat_2_prize_temp = swap_commas_fullstops(response.xpath('//span[@class="monto-pozo"]/text()').getall()[1])
        cat_1_prize = prize_to_num(cat_1_prize_temp)
        cat_2_prize = prize_to_num(cat_2_prize_temp)
        cat_1_winners = prize_to_num(response.xpath('//span[@class="aciertos"]/text()').get())
        cat_2_winners = prize_to_num(response.xpath('//span[@class="aciertos"]/text()').getall()[1])
        if cat_1_winners > 0:
            LottoItem.add_value("cat_1_prize", str(int(cat_1_prize/cat_1_winners)))
        else:
            LottoItem.add_value("cat_1_prize", str(cat_1_prize))
        if cat_2_winners > 0:
            LottoItem.add_value("cat_2_prize", str(int(cat_2_prize/cat_2_winners)))
        else:
            LottoItem.add_value("cat_2_prize", str(cat_2_prize))
        LottoItem.add_value("cat_1_winners", str(cat_1_winners))
        LottoItem.add_value("cat_2_winners", str(cat_2_winners))
        yield LottoItem.load_item()


class UruguayGold5Revancha(scrapy.Spider):

    name = "UruguayGold5Revancha"

    # Revancha (draw_2) is $50 (cf. standard $35) for chance at 2nd prog. jackpot

    def start_requests(self):
        self.name = "UruguayGold5Revancha"
        self.req_proxy = get_US_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://www3.labanca.com.uy/resultados/cincodeoro"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        LottoItem = ItemLoader(item=UruguayGold5RevanchaItem(), selector=response)
        balls_lst = response.xpath('//ul/li/img/@alt').getall()

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", balls_lst[6])
        LottoItem.add_value("ball1", balls_lst[7])
        LottoItem.add_value("ball2", balls_lst[8])
        LottoItem.add_value("ball3", balls_lst[9])
        LottoItem.add_value("ball4", balls_lst[10])
        draw_date = clean_datetime(response.xpath('//select[@id="fecha_sorteo"]/option[@selected="selected"]/text()').get())
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d/%m/%Y").strftime("%Y-%m-%d"))
        cat_1_prize_temp = swap_commas_fullstops(response.xpath('//span[@class="monto-pozo"]/text()').getall()[2])
        cat_1_prize = prize_to_num(cat_1_prize_temp)
        cat_1_winners = prize_to_num(response.xpath('//span[@class="aciertos"]/text()').getall()[2])
        if cat_1_winners > 0:
            LottoItem.add_value("cat_1_prize", str(int(cat_1_prize/cat_1_winners)))
        else:
            LottoItem.add_value("cat_1_prize", str(cat_1_prize))
        LottoItem.add_value("cat_1_winners", str(cat_1_winners))
        yield LottoItem.load_item()


class VietLottMega645(scrapy.Spider):

    name = "VietLottMega645"

    def start_requests(self):
        self.name = "VietLottMega645"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://vietlott.vn/vi/trung-thuong/ket-qua-trung-thuong/645"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        LottoItem = ItemLoader(item=VietLottMega645Item(), selector=response)
        rows = response.xpath('//div[@class="table-responsive"]/table/tbody/tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", response.xpath("//div[@class='day_so_ket_qua_v2']/span/text()").getall()[0])
        LottoItem.add_value("ball1", response.xpath("//div[@class='day_so_ket_qua_v2']/span/text()").getall()[1])
        LottoItem.add_value("ball2", response.xpath("//div[@class='day_so_ket_qua_v2']/span/text()").getall()[2])
        LottoItem.add_value("ball3", response.xpath("//div[@class='day_so_ket_qua_v2']/span/text()").getall()[3])
        LottoItem.add_value("ball4", response.xpath("//div[@class='day_so_ket_qua_v2']/span/text()").getall()[4])
        LottoItem.add_value("ball5", response.xpath("//div[@class='day_so_ket_qua_v2']/span/text()").getall()[5])
        draw_date = response.xpath('//div[@class="header"]//h5//b//text()').getall()[1]
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d/%m/%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", response.xpath('//div[@class="header"]//h5//b//text()').getall()[0])
        jackpot = prize_to_num(swap_commas_fullstops(rows[0].xpath("./td//text()").getall()[3]))
        cat_1_winners = prize_to_num(rows[0].xpath("./td//text()").getall()[2])
        if cat_1_winners > 1:
            jackpot = jackpot/cat_1_winners
        LottoItem.add_value("cat_1_prize", str(jackpot))
        LottoItem.add_value("cat_2_prize", rows[1].xpath("./td//text()").getall()[3])
        LottoItem.add_value("cat_3_prize", rows[2].xpath("./td//text()").getall()[3])
        LottoItem.add_value("cat_4_prize", rows[3].xpath("./td//text()").getall()[3])
        LottoItem.add_value("cat_1_winners", str(int(cat_1_winners)))
        LottoItem.add_value("cat_2_winners", rows[1].xpath("./td//text()").getall()[2])
        LottoItem.add_value("cat_3_winners", rows[2].xpath("./td//text()").getall()[2])
        LottoItem.add_value("cat_4_winners", rows[3].xpath("./td//text()").getall()[2])
        yield LottoItem.load_item()


class VietLottPower655(scrapy.Spider):

    name = "VietLottPower655"

    def start_requests(self):
        self.name = "VietLottPower655"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = "https://vietlott.vn/vi/trung-thuong/ket-qua-trung-thuong/655"
        yield scrapy.Request(url=url, callback=self.parse,
            meta={'playwright': True, "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": self.req_proxy,
                        "username": "keizzermop",
                        "password": "WSPassword123",
                    },
                },
            })

    def parse(self, response):
        LottoItem = ItemLoader(item=VietLottPower655Item(), selector=response)
        rows = response.xpath('//div[@class="table-responsive"]/table/tbody/tr')

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", response.xpath("//div[@class='day_so_ket_qua_v2']/span/text()").getall()[0])
        LottoItem.add_value("ball1", response.xpath("//div[@class='day_so_ket_qua_v2']/span/text()").getall()[1])
        LottoItem.add_value("ball2", response.xpath("//div[@class='day_so_ket_qua_v2']/span/text()").getall()[2])
        LottoItem.add_value("ball3", response.xpath("//div[@class='day_so_ket_qua_v2']/span/text()").getall()[3])
        LottoItem.add_value("ball4", response.xpath("//div[@class='day_so_ket_qua_v2']/span/text()").getall()[4])
        LottoItem.add_value("ball5", response.xpath("//div[@class='day_so_ket_qua_v2']/span/text()").getall()[5])
        LottoItem.add_value("bonus_ball", response.xpath("//div[@class='day_so_ket_qua_v2']/span/text()").getall()[-1])
        draw_date = response.xpath('//div[@class="header"]//h5//b//text()').getall()[1]
        LottoItem.add_value("draw_datetime", datetime.strptime(draw_date, "%d/%m/%Y").strftime("%Y-%m-%d"))
        LottoItem.add_value("draw_number", response.xpath('//div[@class="header"]//h5//b//text()').getall()[0])
        cat_1_prize = prize_to_num(swap_commas_fullstops(rows[0].xpath("./td//text()").getall()[-1]))
        cat_1_winners = prize_to_num(rows[0].xpath("./td//text()").getall()[-2])
        if cat_1_winners > 1:
            cat_1_prize = cat_1_prize/cat_1_winners
        LottoItem.add_value("cat_1_prize", str(cat_1_prize))
        LottoItem.add_value("cat_2_prize", rows[1].xpath("./td//text()").getall()[-1])
        LottoItem.add_value("cat_3_prize", rows[2].xpath("./td//text()").getall()[-1])
        LottoItem.add_value("cat_4_prize", rows[3].xpath("./td//text()").getall()[-1])
        LottoItem.add_value("cat_5_prize", rows[4].xpath("./td//text()").getall()[-1])
        LottoItem.add_value("cat_1_winners", str(int(cat_1_winners)))
        LottoItem.add_value("cat_2_winners", rows[1].xpath("./td//text()").getall()[-2])
        LottoItem.add_value("cat_3_winners", rows[2].xpath("./td//text()").getall()[-2])
        LottoItem.add_value("cat_4_winners", rows[3].xpath("./td//text()").getall()[-2])
        LottoItem.add_value("cat_5_winners", rows[4].xpath("./td//text()").getall()[-2])
        yield LottoItem.load_item()


class VikingLotto(scrapy.Spider):

    name = "VikingLotto"

    # Scraping Denmark winners data since most playable country
    # Multinational Lotto played in Finland, Norway, Denmark, Sweden, Iceland, Estonia, Latvia, Lithuania and Slovenia

    def start_requests(self):
        self.name = "VikingLotto"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = 'https://viking-lotto.net/en/results'
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        self.draw_num = response.xpath('//div[@class="content"]//tbody//td')[1].xpath('./text()').get()
        self.balls_lst = response.xpath('//div[@class="content"]//tbody//td/ul')[0].xpath('./li/text()').getall()
        url = "https://viking-lotto.net" + response.xpath('//div[@class="content"]//tbody//td/a/@href').get()
        yield scrapy.Request(url=url, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":10})

    async def parse_draw(self, response):
        rows = response.xpath('//div[@id="DK"]//tbody/tr')
        LottoItem = ItemLoader(item=VikingLottoItem(), selector=response)

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", str(self.balls_lst[0]))
        LottoItem.add_value("ball1", str(self.balls_lst[1]))
        LottoItem.add_value("ball2", str(self.balls_lst[2]))
        LottoItem.add_value("ball3", str(self.balls_lst[3]))
        LottoItem.add_value("ball4", str(self.balls_lst[4]))
        LottoItem.add_value("ball5", str(self.balls_lst[5]))
        LottoItem.add_value("bonus_ball", str(self.balls_lst[6]))
        LottoItem.add_value("draw_datetime", response.url.split('/')[-1].strip())
        LottoItem.add_value("draw_number", str(self.draw_num))
        LottoItem.add_value("cat_1_prize", str(rows[0].xpath('./td/text()').getall()[-3]))
        LottoItem.add_value("cat_2_prize", str(rows[1].xpath('./td/text()').getall()[-3]))
        LottoItem.add_value("cat_3_prize", str(rows[2].xpath('./td/text()').getall()[-3]))
        LottoItem.add_value("cat_4_prize", str(rows[3].xpath('./td/text()').getall()[-3]))
        LottoItem.add_value("cat_5_prize", str(rows[4].xpath('./td/text()').getall()[-3]))
        LottoItem.add_value("cat_6_prize", str(rows[5].xpath('./td/text()').getall()[-3]))
        LottoItem.add_value("cat_7_prize", str(rows[6].xpath('./td/text()').getall()[-3]))
        LottoItem.add_value("cat_1_winners", str(rows[0].xpath('./td/text()').getall()[-2]))
        LottoItem.add_value("cat_2_winners", str(rows[1].xpath('./td/text()').getall()[-2]))
        LottoItem.add_value("cat_3_winners", str(rows[2].xpath('./td/text()').getall()[-2]))
        LottoItem.add_value("cat_4_winners", str(rows[3].xpath('./td/text()').getall()[-2]))
        LottoItem.add_value("cat_5_winners", str(rows[4].xpath('./td/text()').getall()[-2]))
        LottoItem.add_value("cat_6_winners", str(rows[5].xpath('./td/text()').getall()[-2]))
        LottoItem.add_value("cat_7_winners", str(rows[6].xpath('./td/text()').getall()[-2]))
        yield LottoItem.load_item()


# class VikingLotto(scrapy.Spider):

#     name = "VikingLotto"

#     # Scraped via Finland API
#     # Multinational Lotto played in Finland, Norway, Denmark, Sweden, Iceland, Estonia, Latvia, Lithuania and Slovenia

#     def start_requests(self):
#         self.name = "VikingLotto"
#         self.req_proxy = get_UK_proxy()['http']
#         print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)
# 
#         self.year = datetime.strftime(datetime.now(), "%Y")
#         self.week_num = datetime.strftime(datetime.now(), "%V")
#         self.last_week_num = datetime.strftime(datetime.now()-timedelta(days=7), "%V")
#         self.last_year_num = datetime.strftime(datetime.now()-timedelta(days=7), "%Y")
#         url = f'https://www.veikkaus.fi/api/draw-results/v1/games/VIKING/draws/by-week/{self.year}-W{self.week_num}'
#         yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

#     def parse(self, response):
#         try:
#             latest = response.json()[0]
#             LottoItem = ItemLoader(item=VikingLottoItem(), selector=response)

#             LottoItem.add_value("name", self.name)
#             LottoItem.add_value("ball0", str(latest['results'][0]['primary'][0]))
#             LottoItem.add_value("ball1", str(latest['results'][0]['primary'][1]))
#             LottoItem.add_value("ball2", str(latest['results'][0]['primary'][2]))
#             LottoItem.add_value("ball3", str(latest['results'][0]['primary'][3]))
#             LottoItem.add_value("ball4", str(latest['results'][0]['primary'][4]))
#             LottoItem.add_value("ball5", str(latest['results'][0]['primary'][5]))
#             LottoItem.add_value("bonus_ball", str(latest['results'][0]['secondary'][0]))
#             LottoItem.add_value("draw_datetime", str(latest['drawTime']))
#             LottoItem.add_value("draw_number", str(latest['id']))
#             if int(latest['prizeTiers'][0]['shareCount']) == 0:
#                 LottoItem.add_value("cat_1_prize", str(latest['jackpots'][0]['amount']/100.0))
#             else:
#                 LottoItem.add_value("cat_1_prize", str(latest['prizeTiers'][0]['shareAmount']/100.0))
#             LottoItem.add_value("cat_2_prize", str(latest['prizeTiers'][1]['shareAmount']/100.0))
#             LottoItem.add_value("cat_3_prize", str(latest['prizeTiers'][2]['shareAmount']/100.0))
#             LottoItem.add_value("cat_4_prize", str(latest['prizeTiers'][3]['shareAmount']/100.0))
#             LottoItem.add_value("cat_5_prize", str(latest['prizeTiers'][4]['shareAmount']/100.0))
#             LottoItem.add_value("cat_6_prize", str(latest['prizeTiers'][5]['shareAmount']/100.0))
#             LottoItem.add_value("cat_7_prize", str(latest['prizeTiers'][6]['shareAmount']/100.0))
#             LottoItem.add_value("cat_8_prize", str(latest['prizeTiers'][7]['shareAmount']/100.0))
#             LottoItem.add_value("cat_1_winners", str(latest['prizeTiers'][0]['shareCount']))
#             LottoItem.add_value("cat_2_winners", str(latest['prizeTiers'][1]['shareCount']))
#             LottoItem.add_value("cat_3_winners", str(latest['prizeTiers'][2]['shareCount']))
#             LottoItem.add_value("cat_4_winners", str(latest['prizeTiers'][3]['shareCount']))
#             LottoItem.add_value("cat_5_winners", str(latest['prizeTiers'][4]['shareCount']))
#             LottoItem.add_value("cat_6_winners", str(latest['prizeTiers'][5]['shareCount']))
#             LottoItem.add_value("cat_7_winners", str(latest['prizeTiers'][6]['shareCount']))
#             LottoItem.add_value("cat_8_winners", str(latest['prizeTiers'][7]['shareCount']))
#             yield LottoItem.load_item()
#         except:
#             url = f'https://www.veikkaus.fi/api/draw-results/v1/games/VIKING/draws/by-week/{self.last_year_num}-W{self.last_week_num}'
#             yield scrapy.Request(url=url, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":10})

#     def parse_draw(self, response):
#         latest = response.json()[0]
#         LottoItem = ItemLoader(item=VikingLottoItem(), selector=response)

#         LottoItem.add_value("name", self.name)
#         LottoItem.add_value("ball0", str(latest['results'][0]['primary'][0]))
#         LottoItem.add_value("ball1", str(latest['results'][0]['primary'][1]))
#         LottoItem.add_value("ball2", str(latest['results'][0]['primary'][2]))
#         LottoItem.add_value("ball3", str(latest['results'][0]['primary'][3]))
#         LottoItem.add_value("ball4", str(latest['results'][0]['primary'][4]))
#         LottoItem.add_value("ball5", str(latest['results'][0]['primary'][5]))
#         LottoItem.add_value("bonus_ball", str(latest['results'][0]['secondary'][0]))
#         LottoItem.add_value("draw_datetime", str(latest['drawTime']))
#         LottoItem.add_value("draw_number", str(latest['id']))
#         if int(latest['prizeTiers'][0]['shareCount']) == 0:
#             LottoItem.add_value("cat_1_prize", str(latest['jackpots'][0]['amount']/100.0))
#         else:
#             LottoItem.add_value("cat_1_prize", str(latest['prizeTiers'][0]['shareAmount']/100.0))
#         LottoItem.add_value("cat_2_prize", str(latest['prizeTiers'][1]['shareAmount']/100.0))
#         LottoItem.add_value("cat_3_prize", str(latest['prizeTiers'][2]['shareAmount']/100.0))
#         LottoItem.add_value("cat_4_prize", str(latest['prizeTiers'][3]['shareAmount']/100.0))
#         LottoItem.add_value("cat_5_prize", str(latest['prizeTiers'][4]['shareAmount']/100.0))
#         LottoItem.add_value("cat_6_prize", str(latest['prizeTiers'][5]['shareAmount']/100.0))
#         LottoItem.add_value("cat_7_prize", str(latest['prizeTiers'][6]['shareAmount']/100.0))
#         LottoItem.add_value("cat_8_prize", str(latest['prizeTiers'][7]['shareAmount']/100.0))
#         LottoItem.add_value("cat_1_winners", str(latest['prizeTiers'][0]['shareCount']))
#         LottoItem.add_value("cat_2_winners", str(latest['prizeTiers'][1]['shareCount']))
#         LottoItem.add_value("cat_3_winners", str(latest['prizeTiers'][2]['shareCount']))
#         LottoItem.add_value("cat_4_winners", str(latest['prizeTiers'][3]['shareCount']))
#         LottoItem.add_value("cat_5_winners", str(latest['prizeTiers'][4]['shareCount']))
#         LottoItem.add_value("cat_6_winners", str(latest['prizeTiers'][5]['shareCount']))
#         LottoItem.add_value("cat_7_winners", str(latest['prizeTiers'][6]['shareCount']))
#         LottoItem.add_value("cat_8_winners", str(latest['prizeTiers'][7]['shareCount']))
#         yield LottoItem.load_item()


class ZambiaGGWorldX(scrapy.Spider):

    name = "ZambiaGGWorldX"

    def start_requests(self):
        self.name = "ZambiaGGWorldX"
        self.req_proxy = get_UK_proxy()['http']
        print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)

        url = 'https://lottozambia.com/site/api/current-jackpot'
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

    def parse(self, response):
        self.next_jackpot = response.json()['jackpot']
        url = 'https://lottozambia.com/site/api/latest-results'
        yield scrapy.Request(url=url, callback=self.parse_draw, meta={"proxy": self.req_proxy, "download_timeout":10})

    async def parse_draw(self, response):
        LottoItem = ItemLoader(item=ZambiaGGWorldXItem(), selector=response)
        latest = response.json()

        LottoItem.add_value("name", self.name)
        LottoItem.add_value("ball0", str(latest['numbers'][0][0]))
        LottoItem.add_value("ball1", str(latest['numbers'][0][1]))
        LottoItem.add_value("ball2", str(latest['numbers'][0][2]))
        LottoItem.add_value("ball3", str(latest['numbers'][0][3]))
        LottoItem.add_value("ball4", str(latest['numbers'][0][4]))
        LottoItem.add_value("bonus_ball0", str(latest['numbers'][1][0]))
        LottoItem.add_value("bonus_ball1", str(latest['numbers'][1][1]))
        LottoItem.add_value("draw_datetime", str(latest['date']).split('T')[0])
        LottoItem.add_value("estimated_next_jackpot", self.next_jackpot)
        yield LottoItem.load_item()


# class ZambiaMegaJackpot(scrapy.Spider):
#       Doesn't work from March 2022


#     name = "ZambiaMegaJackpot"

#     # jackpot = match_6; secondary_jackpot = match_5_bonus
#

#     def start_requests(self):
#         self.name = "ZambiaMegaJackpot"
#         self.req_proxy = get_UK_proxy()['http']
#         print(f"RUNNING: {self.name}, {self.req_proxy}", flush=True)
# 
#         url = "http://www.zambianlotto.co.zm/"
#         yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": self.req_proxy, "download_timeout":10})

#     def parse(self, response):
#         frmdata = {'id': 'xxxx'}
#         self.draw_id = response.xpath('//span[@id="jackpotdraw"]/text()').get().strip()
#         frmdata['id'] = self.draw_id
#         url = "http://www.zambianlotto.co.zm/jackpotsearchdata"
#         yield scrapy.Request(url=url, method='POST', body=json.dumps(frmdata), callback=self.parse_draw,
#             meta={"proxy": self.req_proxy, "download_timeout":10})

#     async def parse_draw(self, response):
#         LottoItem = ItemLoader(item=ZambiaMegaJackpotItem(), selector=response)
#         latest = response.json()[0]

#         LottoItem.add_value("name", self.name)
#         LottoItem.add_value("ball0", str(latest['Ball1']))
#         LottoItem.add_value("ball1", str(latest['Ball2']))
#         LottoItem.add_value("ball2", str(latest['Ball3']))
#         LottoItem.add_value("ball3", str(latest['Ball4']))
#         LottoItem.add_value("ball4", str(latest['Ball5']))
#         LottoItem.add_value("ball5", str(latest['Ball6']))
#         LottoItem.add_value("bonus_ball", str(latest['BallBonus']))
#         LottoItem.add_value("draw_datetime", str(latest['DrawDate']).split('T')[0])
#         LottoItem.add_value("draw_number", str(latest['DrawId']))
#         if int(latest['Winner6']) == 0:
#             LottoItem.add_value("cat_1_prize", str(latest['JackpotPrize']))
#         else:
#             LottoItem.add_value("cat_1_prize", str(latest['Prizes6unit']))
#         if int(latest['Winner5plus']) == 0:
#             LottoItem.add_value("cat_2_prize", str(latest['FiveplusPrize']))
#         else:
#             LottoItem.add_value("cat_2_prize", str(latest['Prizes5plusunit']))
#         LottoItem.add_value("cat_3_prize", str(latest['Prizes5unit']))
#         LottoItem.add_value("cat_4_prize", str(latest['Prizes4unit']))
#         LottoItem.add_value("cat_5_prize", str(latest['Prizes3unit']))
#         LottoItem.add_value("cat_1_winners", str(latest['Winner6']))
#         LottoItem.add_value("cat_2_winners", str(latest['Winner5plus']))
#         LottoItem.add_value("cat_3_winners", str(latest['Winner5']))
#         LottoItem.add_value("cat_4_winners", str(latest['Winner4']))
#         LottoItem.add_value("cat_5_winners", str(latest['Winner3']))
#         yield LottoItem.load_item()
