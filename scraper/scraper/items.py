# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from scrapy_djangoitem import DjangoItem
from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose, TakeFirst
from bot.models import Scraper
import scrapy
import re
from w3lib.html import remove_tags
from itemloaders.processors import Join, MapCompose, TakeFirst, Identity
from datetime import datetime

# method to convert a string with commas and decimal point into a float
def string_with_commas_to_float(element):

    element = str(element)
    element = element.replace(",", "")
    element = float("0" + element)  # makes sure type conversion works

    return element


# method to remove white space and line breaks
def strip_new_lines(x):

    if isinstance(x, str):
        out = re.sub(r"\n","",x).strip()
        out = re.sub(r'\s{2,}', ' ', out)
        if out == '':
            return '0'
        else:
            return out
    else:
        return x


# method to remove symbols/non-integers from a string
def strip_symbols(element):

    digits = [s for s in element if s.isdigit()]
    value = ''.join(digits)
    return value


# method to swap commas and fullstops
def swap_commas_fullstops(element):

    if "," and "." in element:
        return element.replace('.', '@').replace(',', '.').replace('@', ',')
    elif "," in element:
        return element.replace(',', '.')
    elif "." in element:
        return element.replace('.', ',')
    else:
        return element


# method to clean a jackpot string to a float (string)
def prize_to_num(element):

    digits = [s for s in element if s.isdigit() or s == '.']
    value = ''.join(digits)
    if len(value) > 0:
        if "thousand" in element.lower():
            value = float(value) * 1_000
        if any(string in element.lower() for string in ['million', 'mil']):
            value = float(value) * 1_000_000
        if "billion" in element.lower():
            value = float(value) * 1_000_000_000
        return str(value)
    else:
        return '0'


# method to clean a more specific prize value
def prize_to_num_specific(element):

    if "kr." in element.lower():
        element = element.split('kr.')[1]
    digits = [s for s in element if s.isdigit() or s == '.']
    value = ''.join(digits)
    if len(value) > 0:
        if any(string in element for string in ['M', 'millió', 'miljoner', 'milj']):
            value = float(value) * 1_000_000
        elif any(string in element for string in ['milliárd']):
            value = float(value) * 1_000_000_000
        return str(value)
    else:
        return '0'


# method to remove unicode characters
def remove_unicode(element):

    if type(element) == str:
        if u"\xa0" in element:
            element = element.replace(u"\xa0", u" ")
        if r"\u" in element:
            element = (element.encode('ascii', 'ignore')).decode("utf-8")

    return element


# method to convert timestamp (ms) to datetime string
def convert_timestamp(timestamp):

    if len(timestamp) == 13:
        d_timestamp = datetime.fromtimestamp(int(timestamp)/1000)
        datetime_string = d_timestamp.strftime("%Y-%m-%d")
    elif len(timestamp) == 10:
        d_timestamp = datetime.fromtimestamp(int(timestamp))
        datetime_string = d_timestamp.strftime("%Y-%m-%d")
    else:
        datetime_string = 'INVALID TIMESTAMP'
    return datetime_string


# method to remove letters and unnecessary symbols from datetime
def clean_datetime(element):

    if "/" in element:
        digits = [s for s in element if s.isdigit() or s =='/']
        value = ''.join(digits)
    elif "." in element:
        digits = [s for s in element if s.isdigit() or s =='.']
        value = ''.join(digits)
    return value



class USMegaMillionsItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    megaplier = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    jackpot_cash = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_8_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_9_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_8_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_9_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())


class USPowerballItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_8_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_9_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_8_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_9_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())


class USLottoAmericaItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_8_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_9_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_8_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_9_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class USArizonaThePickItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())


class USArizonaFantasy5Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())


class USArizonaTripleTwistItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class USArkansasLottoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_8_prize = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_8_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class USArkansasNaturalStateItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class USCaliforniaDailyDerbyItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class USCaliforniaFantasy5Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class USCaliforniaSuperLottoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_8_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_9_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_8_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_9_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class USColoradoLottoPlusItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    jackpot_cash = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class USConnecticutLottoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    estimated_next_jackpot_cash = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class USDelawareMultiWinItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(), output_processor=Join())
    cat_8_prize = Field(input_processor=MapCompose(), output_processor=Join())
    cat_9_prize = Field(input_processor=MapCompose(), output_processor=Join())
    cat_10_prize = Field(input_processor=MapCompose(), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_8_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_9_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_10_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class USFloridaLottoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class USFloridaTriplePlayItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    rolldown = Field(input_processor=MapCompose(), output_processor=Join())


class USGeorgiaFantasy5Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(strip_new_lines, convert_timestamp), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class USGeorgiaJumboBucksItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(strip_new_lines, convert_timestamp), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class USIdaho5StarItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())


class USIdahoCashItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())


class USIllinoisLuckyDayItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=TakeFirst())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=TakeFirst())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class USIllinoisLottoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class USIndianaHoosierLottoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class USIndianaCash5Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class USKansasSuperCashItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_8_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_8_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class USLouisianaLottoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=TakeFirst())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=TakeFirst())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class USLouisianaEasy5Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=TakeFirst())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=TakeFirst())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class USMarylandMultiMatchItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    estimated_next_jackpot_cash = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_prize_cash = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_8_prize = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_9_prize = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_10_prize = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_8_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_9_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_10_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class USMassachusettsMegaBucksItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines, remove_tags), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot_cash = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    jackpot = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())


class USMichiganLotto47Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=TakeFirst())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=TakeFirst())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class USMichiganFantasy5Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=TakeFirst())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=TakeFirst())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class USMinnesotaGopher5Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())


class USMinnesotaNorthstarCashItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())

class USMississippiMatch5Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class USMissouriLottoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class USMissouriShowMeCashItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class USMontanaBigSkyBonusItem(DjangoItem):
    name = Field(input_processor=MapCompose(), output_processor=TakeFirst())
    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines, remove_tags), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class USMontanaCashItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines, remove_tags), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class USMontanaMaxCashItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines, remove_tags), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class USNebraskaPick5Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=TakeFirst())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class USNewJerseyPick6Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())


class USNewJerseyCash5Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(strip_new_lines, convert_timestamp), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines, remove_tags), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    jackpot_cash = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=TakeFirst())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=TakeFirst())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class USNewMexicoRoadRunnerCashItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())


class USNewYorkLottoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=TakeFirst())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=TakeFirst())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class USNorthCarolinaCash5Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class USOhioLottoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    total_winnings = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())


class USOhioRollingCash5Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())


class USOregonMegaBucksItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines, remove_tags), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class USOregonLuckyLinesItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines, remove_tags), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball6 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball7 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class USPennsylvaniaCash5Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(strip_new_lines, strip_symbols, convert_timestamp), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines, remove_tags, strip_symbols), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class USPennsylvaniaMatch6Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(strip_new_lines, strip_symbols, convert_timestamp), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_8_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_9_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_10_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_11_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_8_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_9_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_10_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_11_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class USPennsylvaniaTreasureHuntItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(strip_new_lines, strip_symbols, convert_timestamp), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class USPuertoRicoLotoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    multiplier = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    jackpot = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())


class USPuertoRicoRevanchaItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    multiplier = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    jackpot = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())


class USRhodeIslandWildMoneyItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(strip_new_lines, convert_timestamp), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class USSouthDakotaCashItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class USTennesseeCashItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_8_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_8_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())

class USTennesseeDailyCashItem(DjangoItem):
    
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())

class USTexasLottoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    estimated_next_jackpot_cash = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class USTexasTwoStepItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class USTristateMegaBucksItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_8_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_9_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=TakeFirst())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=TakeFirst())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=TakeFirst())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=TakeFirst())
    cat_7_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_8_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_9_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=TakeFirst())


class USVirginiaCash5Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=TakeFirst())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=TakeFirst())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=TakeFirst())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=TakeFirst())


class USWashingtonLottoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=TakeFirst())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=TakeFirst())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=TakeFirst())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=TakeFirst())


class USWashingtonHit5Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=TakeFirst())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=TakeFirst())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=TakeFirst())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=TakeFirst())


class USWisconsinMegaBucksItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    estimated_next_jackpot_cash = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class USWisconsinBadger5Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class USWyomingCowboyDrawItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


### REST OF THE WORLD


class AntiguaSuperLottoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    jackpot = Field(input_processor=MapCompose(), output_processor=Join())


class ArgentinaLotoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines, remove_tags), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines, remove_unicode), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines, remove_unicode), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines, remove_unicode), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines, remove_unicode), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines, remove_unicode), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines, remove_unicode), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines, remove_unicode), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_symbols, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())


class ArgentinaLotoPlusItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines, remove_tags), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines, remove_unicode), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines, remove_unicode), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines, remove_unicode), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines, remove_unicode), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines, remove_unicode), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines, remove_unicode), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines, remove_unicode), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_symbols, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())


class ArgentinaLoto5Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines, remove_tags), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_symbols, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())

class ArgentinaLotoTradicionalItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines, remove_tags), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())

class ArgentinaLotoMatchItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines, remove_tags), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())

class ArgentinaLotoDesquiteItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines, remove_tags), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())

class ArgentinaLotoSaleItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines, remove_tags), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())

class ArgentinaQuini6Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())


class AustraliaTattsLottoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines, remove_tags), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 =  Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=TakeFirst())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=TakeFirst())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=TakeFirst())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=TakeFirst())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class AustraliaOzLottoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines, remove_tags), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball6 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())


class AustraliaPowerballItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines, remove_tags), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball6 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_8_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_9_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_8_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_9_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())


class AustraliaSuper66Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines, remove_tags), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=TakeFirst())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class AustraliaSuperJackpotItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())


class AustraliaMegaJackpotItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines, remove_tags), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())


class AustriaLottoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_8_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_8_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class AustriaJokerItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class AzerbaijanLotto5x36Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())


class AzerbaijanLotto6x40Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())


class BarbadosMega6Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class BelgiumLottoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(convert_timestamp), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_8_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_9_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_8_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_9_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())


class BosniaSuperLotoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_colour = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    sales = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    draw_bonus_colour_sales = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_2_bonus_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_3_bonus_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_4_bonus_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_2_bonus_winners = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_3_bonus_winners = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_4_bonus_winners = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())


class BrazilTimeManiaItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    sales = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball6 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class BrazilMegaSenaItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    sales = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class BrazilLotoManiaItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    sales = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball6 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball7 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball8 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball9 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball10 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball11 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball12 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball13 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball14 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball15 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball16 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball17 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball18 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball19 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class BrazilLotoFacilItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    sales = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball6 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball7 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball8 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball9 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball10 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball11 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball12 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball13 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball14 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class BrazilQuinaItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    sales = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class BrazilDuplaSenaItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    sales = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw1_ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw1_ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw1_ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw1_ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw1_ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw1_ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw2_ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw2_ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw2_ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw2_ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw2_ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw2_ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw1_cat_1_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw1_cat_2_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw1_cat_3_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw1_cat_4_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw2_cat_1_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw2_cat_2_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw2_cat_3_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw2_cat_4_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw1_cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw1_cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw1_cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw1_cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw2_cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw2_cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw2_cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw2_cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class BulgariaLotto6x49Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class BulgariaLotto6x42Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class BulgariaLotto5x35Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw1_ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw1_ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw1_ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw1_ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw1_ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw2_ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw2_ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw2_ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw2_ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw2_ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw1_cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    draw1_cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    draw1_cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    draw2_cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    draw2_cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    draw2_cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    draw1_cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    draw1_cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    draw1_cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    draw2_cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    draw2_cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    draw2_cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class CanadaMaxLottoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    sales = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball6 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    n_MaxMillions = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_8_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_9_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_8_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_9_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class CanadaLotto649Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot_balls_left = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_8_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_8_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class CanadaLottarioItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    eb_ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    eb_ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    eb_ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    eb_ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_8_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_9_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_8_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_9_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class ChileLotoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(strip_new_lines, convert_timestamp), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_8_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_8_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class ChinaTwoColorItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    sales = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    prize_pool = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(), output_processor=Join())


class ChinaHappy8LottoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball6 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball7 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball8 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball9 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball10 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball11 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball12 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball13 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball14 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball15 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball16 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball17 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball18 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball19 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    sales = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    prize_pool = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(), output_processor=Join())


class ChinaSevenLottoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball6 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    sales = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    prize_pool = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(), output_processor=Join())


class ColombiaBalotoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(prize_to_num, swap_commas_fullstops), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(prize_to_num, swap_commas_fullstops), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(prize_to_num, swap_commas_fullstops), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(prize_to_num, swap_commas_fullstops), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(prize_to_num, swap_commas_fullstops), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(prize_to_num, swap_commas_fullstops), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(prize_to_num, swap_commas_fullstops), output_processor=Join())
    cat_8_prize = Field(input_processor=MapCompose(prize_to_num, swap_commas_fullstops), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_8_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class ColombiaRevanchaItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(prize_to_num, swap_commas_fullstops), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(prize_to_num, swap_commas_fullstops), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(prize_to_num, swap_commas_fullstops), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(prize_to_num, swap_commas_fullstops), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(prize_to_num, swap_commas_fullstops), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(prize_to_num, swap_commas_fullstops), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(prize_to_num, swap_commas_fullstops), output_processor=Join())
    cat_8_prize = Field(input_processor=MapCompose(prize_to_num, swap_commas_fullstops), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_8_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class CostaRicaLottoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class CostaRicaRevanchaItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class CroatiaLoto7Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    sales = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball6 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    estimated_next_secondary_jackpot = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    guaranteed_jackpot = Field(input_processor=MapCompose(), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_8_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_9_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_8_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_9_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())


class CroatiaLoto6Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    sales = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    estimated_next_secondary_jackpot = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    guaranteed_jackpot = Field(input_processor=MapCompose(), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())


class CroatiaJokerItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    sales = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())


class CzechiaSportkaItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw1_ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw1_ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw1_ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw1_ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw1_ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw1_ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw1_bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw2_ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw2_ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw2_ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw2_ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw2_ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw2_ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw2_bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_superjackpot = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, prize_to_num), output_processor=Join())
    estimated_next_draw1_jackpot = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, prize_to_num), output_processor=Join())
    estimated_next_draw2_jackpot = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, prize_to_num), output_processor=Join())
    draw1_cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, prize_to_num), output_processor=Join())
    draw1_cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, prize_to_num), output_processor=Join())
    draw1_cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, prize_to_num), output_processor=Join())
    draw1_cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, prize_to_num), output_processor=Join())
    draw1_cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, prize_to_num), output_processor=Join())
    draw1_cat_6_prize = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, prize_to_num), output_processor=Join())
    draw2_cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, prize_to_num), output_processor=Join())
    draw2_cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, prize_to_num), output_processor=Join())
    draw2_cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, prize_to_num), output_processor=Join())
    draw2_cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, prize_to_num), output_processor=Join())
    draw2_cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, prize_to_num), output_processor=Join())
    draw2_cat_6_prize = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, prize_to_num), output_processor=Join())
    draw1_cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, prize_to_num), output_processor=Join())
    draw1_cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, prize_to_num), output_processor=Join())
    draw1_cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, prize_to_num), output_processor=Join())
    draw1_cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, prize_to_num), output_processor=Join())
    draw1_cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, prize_to_num), output_processor=Join())
    draw1_cat_6_winners = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, prize_to_num), output_processor=Join())
    draw2_cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, prize_to_num), output_processor=Join())
    draw2_cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, prize_to_num), output_processor=Join())
    draw2_cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, prize_to_num), output_processor=Join())
    draw2_cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, prize_to_num), output_processor=Join())
    draw2_cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, prize_to_num), output_processor=Join())
    draw2_cat_6_winners = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, prize_to_num), output_processor=Join())


class DenmarkLottoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    ball6 = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class DominicaSuper6Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())


class DominicaPowerballItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())


class DominicanLotoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())


class DominicanLotomasItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())


class DominicanSuperomasItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())


class EuroJackpotItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    sales = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    hessen_sales = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num_specific), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(remove_unicode, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(remove_unicode, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(remove_unicode, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(remove_unicode, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(remove_unicode, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(remove_unicode, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(remove_unicode, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_8_prize = Field(input_processor=MapCompose(remove_unicode, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_9_prize = Field(input_processor=MapCompose(remove_unicode, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_10_prize = Field(input_processor=MapCompose(remove_unicode, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_11_prize = Field(input_processor=MapCompose(remove_unicode, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_12_prize = Field(input_processor=MapCompose(remove_unicode, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_8_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_9_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_10_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_11_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_12_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_1_hessen_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_hessen_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_hessen_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_hessen_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_5_hessen_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_6_hessen_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_7_hessen_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_8_hessen_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_9_hessen_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_10_hessen_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_11_hessen_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_12_hessen_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class EuroMillionsItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    tickets = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    cat_8_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    cat_9_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    cat_10_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    cat_11_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    cat_12_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    cat_13_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    cat_8_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    cat_9_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    cat_10_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    cat_11_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    cat_12_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    cat_13_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    rolldown = Field(input_processor=MapCompose(), output_processor=Join())
    special_draw = Field(input_processor=MapCompose(), output_processor=Join())


class EuroMillionsAllItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    tickets = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    rolldown = Field(input_processor=MapCompose(), output_processor=Join())

    # IRELAND
    IE_cat_1_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    IE_cat_2_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    IE_cat_3_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    IE_cat_4_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    IE_cat_5_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    IE_cat_6_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    IE_cat_7_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    IE_cat_8_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    IE_cat_9_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    IE_cat_10_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    IE_cat_11_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    IE_cat_12_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    IE_cat_13_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    IE_cat_1_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    IE_cat_2_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    IE_cat_3_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    IE_cat_4_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    IE_cat_5_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    IE_cat_6_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    IE_cat_7_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    IE_cat_8_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    IE_cat_9_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    IE_cat_10_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    IE_cat_11_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    IE_cat_12_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    IE_cat_13_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())

    # GB
    GB_cat_1_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    GB_cat_2_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    GB_cat_3_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    GB_cat_4_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    GB_cat_5_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    GB_cat_6_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    GB_cat_7_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    GB_cat_8_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    GB_cat_9_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    GB_cat_10_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    GB_cat_11_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    GB_cat_12_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    GB_cat_13_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    GB_cat_1_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    GB_cat_2_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    GB_cat_3_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    GB_cat_4_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    GB_cat_5_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    GB_cat_6_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    GB_cat_7_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    GB_cat_8_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    GB_cat_9_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    GB_cat_10_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    GB_cat_11_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    GB_cat_12_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    GB_cat_13_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())

    # France
    FR_cat_1_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    FR_cat_2_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    FR_cat_3_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    FR_cat_4_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    FR_cat_5_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    FR_cat_6_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    FR_cat_7_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    FR_cat_8_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    FR_cat_9_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    FR_cat_10_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    FR_cat_11_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    FR_cat_12_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    FR_cat_13_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    FR_cat_14_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    FR_cat_15_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    FR_cat_16_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    FR_cat_17_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    FR_cat_18_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    FR_cat_19_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    FR_cat_20_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    FR_cat_21_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    FR_cat_22_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    FR_cat_23_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    FR_cat_1_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    FR_cat_2_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    FR_cat_3_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    FR_cat_4_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    FR_cat_5_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    FR_cat_6_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    FR_cat_7_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    FR_cat_8_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    FR_cat_9_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    FR_cat_10_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    FR_cat_11_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    FR_cat_12_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    FR_cat_13_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    FR_cat_14_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    FR_cat_15_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    FR_cat_16_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    FR_cat_17_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    FR_cat_18_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    FR_cat_19_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    FR_cat_20_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    FR_cat_21_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    FR_cat_22_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    FR_cat_23_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())

    # Spain
    ES_cat_1_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    ES_cat_2_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    ES_cat_3_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    ES_cat_4_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    ES_cat_5_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    ES_cat_6_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    ES_cat_7_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    ES_cat_8_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    ES_cat_9_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    ES_cat_10_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    ES_cat_11_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    ES_cat_12_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    ES_cat_13_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    ES_cat_1_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    ES_cat_2_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    ES_cat_3_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    ES_cat_4_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    ES_cat_5_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    ES_cat_6_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    ES_cat_7_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    ES_cat_8_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    ES_cat_9_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    ES_cat_10_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    ES_cat_11_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    ES_cat_12_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    ES_cat_13_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())

    # Portugal
    PT_cat_1_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    PT_cat_2_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    PT_cat_3_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    PT_cat_4_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    PT_cat_5_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    PT_cat_6_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    PT_cat_7_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    PT_cat_8_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    PT_cat_9_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    PT_cat_10_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    PT_cat_11_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    PT_cat_12_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    PT_cat_13_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    PT_cat_1_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    PT_cat_2_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    PT_cat_3_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    PT_cat_4_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    PT_cat_5_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    PT_cat_6_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    PT_cat_7_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    PT_cat_8_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    PT_cat_9_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    PT_cat_10_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    PT_cat_11_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    PT_cat_12_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    PT_cat_13_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())

    # Belgium
    BE_cat_1_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    BE_cat_2_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    BE_cat_3_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    BE_cat_4_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    BE_cat_5_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    BE_cat_6_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    BE_cat_7_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    BE_cat_8_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    BE_cat_9_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    BE_cat_10_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    BE_cat_11_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    BE_cat_12_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    BE_cat_13_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    BE_cat_1_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    BE_cat_2_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    BE_cat_3_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    BE_cat_4_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    BE_cat_5_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    BE_cat_6_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    BE_cat_7_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    BE_cat_8_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    BE_cat_9_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    BE_cat_10_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    BE_cat_11_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    BE_cat_12_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    BE_cat_13_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())

    # Austria
    AT_cat_1_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    AT_cat_2_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    AT_cat_3_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    AT_cat_4_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    AT_cat_5_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    AT_cat_6_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    AT_cat_7_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    AT_cat_8_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    AT_cat_9_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    AT_cat_10_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    AT_cat_11_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    AT_cat_12_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    AT_cat_13_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    AT_cat_1_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    AT_cat_2_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    AT_cat_3_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    AT_cat_4_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    AT_cat_5_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    AT_cat_6_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    AT_cat_7_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    AT_cat_8_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    AT_cat_9_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    AT_cat_10_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    AT_cat_11_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    AT_cat_12_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    AT_cat_13_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())

    # Swizerland
    CH_cat_1_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    CH_cat_2_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    CH_cat_3_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    CH_cat_4_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    CH_cat_5_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    CH_cat_6_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    CH_cat_7_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    CH_cat_8_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    CH_cat_9_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    CH_cat_10_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    CH_cat_11_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    CH_cat_12_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    CH_cat_13_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    CH_cat_1_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    CH_cat_2_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    CH_cat_3_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    CH_cat_4_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    CH_cat_5_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    CH_cat_6_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    CH_cat_7_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    CH_cat_8_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    CH_cat_9_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    CH_cat_10_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    CH_cat_11_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    CH_cat_12_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    CH_cat_13_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())

    # Luxembourg
    LU_cat_1_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    LU_cat_2_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    LU_cat_3_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    LU_cat_4_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    LU_cat_5_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    LU_cat_6_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    LU_cat_7_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    LU_cat_8_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    LU_cat_9_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    LU_cat_10_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    LU_cat_11_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    LU_cat_12_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    LU_cat_13_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    LU_cat_1_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    LU_cat_2_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    LU_cat_3_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    LU_cat_4_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    LU_cat_5_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    LU_cat_6_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    LU_cat_7_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    LU_cat_8_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    LU_cat_9_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    LU_cat_10_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    LU_cat_11_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    LU_cat_12_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())
    LU_cat_13_winners = Field(input_processor=MapCompose(remove_unicode, strip_symbols), output_processor=Join())


class FinlandLottoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(strip_new_lines, convert_timestamp), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball6 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class FranceLottoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_8_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_9_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_8_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_9_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    rolldown = Field(input_processor=MapCompose(), output_processor=Join())


class GeorgiaLotto6x42Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(remove_unicode, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(remove_unicode, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(remove_unicode, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(remove_unicode, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(remove_unicode, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(remove_unicode, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class GeorgiaLotto5x35Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    golden_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(remove_unicode, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(remove_unicode, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(remove_unicode, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(remove_unicode, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(remove_unicode, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class Germany6aus49Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    sales = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    hessen_sales = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_8_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_9_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_8_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_9_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    hessen_cat_1_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    hessen_cat_2_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    hessen_cat_3_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    hessen_cat_4_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    hessen_cat_5_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    hessen_cat_6_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    hessen_cat_7_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    hessen_cat_8_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    hessen_cat_9_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    rolldown = Field(input_processor=MapCompose(), output_processor=Join())


class GermanySpiel77Item(DjangoItem):
    name = Field(input_processor=MapCompose(), output_processor=Join())
    draw_datetime = Field(input_processor=MapCompose(convert_timestamp), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(), output_processor=Join())
    ball6 = Field(input_processor=MapCompose(), output_processor=Join())
    sales = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    rolldown = Field(input_processor=MapCompose(), output_processor=Join())


class GreeceLottoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(convert_timestamp), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    tickets = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    perms = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())


class GreeceJokerItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(convert_timestamp), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    tickets = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    perms = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_8_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_8_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())


class GreeceProtoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(convert_timestamp), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball6 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    tickets = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    perms = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())


class GrenadaLottoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())


class GuyanaSupa6Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num_specific), output_processor=Join())


class HongKongMarkSixItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())


class HungaryOtosLottoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops,
        prize_to_num_specific), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class HungaryHatosLottoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops,
        prize_to_num_specific), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class HungarySkandinavLottoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw1_ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw1_ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw1_ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw1_ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw1_ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw1_ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw1_ball6 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw2_ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw2_ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw2_ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw2_ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw2_ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw2_ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw2_ball6 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops,
        prize_to_num_specific), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class HungaryJokerItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops,
        prize_to_num_specific), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class IcelandLottoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())


class IrelandLottoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_8_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_8_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    rolldown = Field(input_processor=MapCompose(), output_processor=Join())


class IsraelDoubleLottoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(strip_new_lines, clean_datetime), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    match_6_bonus = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    match_6 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    match_5_bonus = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    match_5 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    match_4_bonus = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    match_4 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    match_3_bonus = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    match_3 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    double_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    double_match_6_bonus = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    double_match_6 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    double_match_5_bonus = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    double_match_5 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    double_match_4_bonus = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    double_match_4 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    double_match_3_bonus = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    double_match_3 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class ItalySuperEnaLottoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(remove_unicode, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(remove_unicode, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(remove_unicode, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(remove_unicode, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(remove_unicode, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(remove_unicode, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class JamaicaLottoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class JapanLoto7Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball6 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball0 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    bonus_ball1 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    sales = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    carryover = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())


class JapanLoto6Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    sales = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    carryover = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())


class KazakhstanLoto6x49Item(DjangoItem):
    name = Field(input_processor=MapCompose(), output_processor=Join())
    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())


class KazakhstanLoto5x36Item(DjangoItem):
    name = Field(input_processor=MapCompose(), output_processor=Join())
    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())


class LatviaLotto5x35Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())


class LebanonLotoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class MacedoniaLoto7Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball6 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class MalaysiaJackpotItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())


class MalaysiaJackpotGoldItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())


class MaltaSuper5Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_number = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())


class MaltaSuperstarItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_number = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())


class MaltaLottoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_number = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball6 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball7 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())


class MauritiusLotoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    sales = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class MexicoMelateItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_8_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_9_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_8_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_9_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class MexicoRevanchaItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class MexicoRevanchitaItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=TakeFirst())


class MoroccoLotoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines,
        swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines,
        swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines,
        swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines,
        swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines,
        swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines,
        swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class NetherlandsLottoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())

class NetherlandsStateRaffleItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    bonus_ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    jackpot_balls_left = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())



class NewZealandBullseyeItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines, remove_tags), output_processor=Join())
    bullseye_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    prize_pool = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    rolldown = Field(input_processor=MapCompose(), output_processor=Join())


class NewZealandLottoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines, remove_tags), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())


class NewZealandPowerballItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())


class NewZealandStrikeItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines, remove_tags), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    prize_pool = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=TakeFirst())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=TakeFirst())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=TakeFirst())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    rolldown = Field(input_processor=MapCompose(), output_processor=Join())


class NorwayLottoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    sales = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball6 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class PeruTinkaItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())


class PeruKabalaItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())


class PhilippinesLotto6x58Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())


class PhilippinesLotto6x55Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())


class PhilippinesLotto6x49Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())


class PhilippinesLotto6x45Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())


class PhilippinesLotto6x42Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())


class PolandLottoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class PortugalLottoTotoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    tickets = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    sales = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    prize_pool = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class RomaniaLoto6x49Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    prize_pool = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    jackpot_increase = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())


class RomaniaLoto5x40Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    prize_pool = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    jackpot_increase = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())


class RomaniaJokerItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    prize_pool = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    jackpot_increase = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_8_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_8_winners = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())


class RussiaLoto7x49Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball6 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    tickets = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, strip_symbols), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class RussiaLoto6x45Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    tickets = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, strip_symbols), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class RussiaLoto5x36Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    tickets = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, strip_symbols), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class RussiaLoto4x20Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball6 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball7 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    tickets = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, strip_symbols), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    cat_8_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    cat_9_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    cat_10_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    cat_11_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    cat_12_prize = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_8_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_9_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_10_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_11_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_12_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class SamoaLottoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class SerbiaLotoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball6 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    tickets = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class SerbiaLotoPlusItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball6 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    sales = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class SingaporeTotoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())


class SlovakiaLotoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw1_ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw1_ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw1_ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw1_ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw1_ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw1_ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw1_bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw2_ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw2_ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw2_ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw2_ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw2_ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw2_ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    draw2_bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    sales = Field(input_processor=MapCompose(remove_unicode, swap_commas_fullstops, prize_to_num), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, remove_unicode,
        swap_commas_fullstops, prize_to_num), output_processor=Join())
    draw1_cat_1_prize = Field(input_processor=MapCompose(remove_unicode,
        swap_commas_fullstops, prize_to_num), output_processor=Join())
    draw1_cat_2_prize = Field(input_processor=MapCompose(remove_unicode,
        swap_commas_fullstops, prize_to_num), output_processor=Join())
    draw1_cat_3_prize = Field(input_processor=MapCompose(remove_unicode,
        swap_commas_fullstops, prize_to_num), output_processor=Join())
    draw1_cat_4_prize = Field(input_processor=MapCompose(remove_unicode,
        swap_commas_fullstops, prize_to_num), output_processor=Join())
    draw1_cat_5_prize = Field(input_processor=MapCompose(remove_unicode,
        swap_commas_fullstops, prize_to_num), output_processor=Join())
    draw1_cat_6_prize = Field(input_processor=MapCompose(remove_unicode,
        swap_commas_fullstops, prize_to_num), output_processor=Join())
    draw1_cat_7_prize = Field(input_processor=MapCompose(remove_unicode,
        swap_commas_fullstops, prize_to_num), output_processor=Join())
    draw2_cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    draw2_cat_2_prize = Field(input_processor=MapCompose(remove_unicode,
        swap_commas_fullstops, prize_to_num), output_processor=Join())
    draw2_cat_3_prize = Field(input_processor=MapCompose(remove_unicode,
        swap_commas_fullstops, prize_to_num), output_processor=Join())
    draw2_cat_4_prize = Field(input_processor=MapCompose(remove_unicode,
        swap_commas_fullstops, prize_to_num), output_processor=Join())
    draw2_cat_5_prize = Field(input_processor=MapCompose(remove_unicode,
        swap_commas_fullstops, prize_to_num), output_processor=Join())
    draw2_cat_6_prize = Field(input_processor=MapCompose(remove_unicode,
        swap_commas_fullstops, prize_to_num), output_processor=Join())
    draw2_cat_7_prize = Field(input_processor=MapCompose(remove_unicode,
        swap_commas_fullstops, prize_to_num), output_processor=Join())
    draw1_cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    draw1_cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    draw1_cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    draw1_cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    draw1_cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    draw1_cat_6_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    draw1_cat_7_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    draw2_cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    draw2_cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    draw2_cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    draw2_cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    draw2_cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    draw2_cat_6_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    draw2_cat_7_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class SlovakiaLoto5x35Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    sales = Field(input_processor=MapCompose(remove_unicode, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(remove_unicode,swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(remove_unicode,swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(remove_unicode,swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class SloveniaLotoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball6 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_8_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_8_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())


class SloveniaLotoPlusItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball6 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_8_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_8_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())


class SloveniaLotkoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())


class SpainLaPrimitivaItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball_C = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball_R = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    tickets = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    prize_pool = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class SpainBonoLotoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball_C = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball_R = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    tickets = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    prize_pool = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class SpainElGordoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    tickets = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    prize_pool = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_8_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_9_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_8_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_9_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class SpainLotoTurfItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball_C = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball_R = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    tickets = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    prize_pool = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(remove_unicode, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_8_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_8_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class SouthAfricaLottoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    sales = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    rollover_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    rollover_amount = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_8_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_8_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())


class SouthAfricaLottoPlus1Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    sales = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    rollover_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    rollover_amount = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_8_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_8_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())


class SouthAfricaLottoPlus2Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    sales = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    rollover_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    rollover_amount = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_8_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_8_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())


class SouthAfricaPowerballItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    sales = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    rollover_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    rollover_amount = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_8_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_9_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_8_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_9_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())


class SouthAfricaPowerballPlusItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    sales = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    rollover_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    rollover_amount = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_8_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_9_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_8_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_9_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())


class SouthKoreaLotto6x45Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    sales = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class SwedenLotto1Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball6 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    combined_sales = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())


class SwedenLotto2Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball6 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    combined_sales = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())


class SwedenJokerItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball6 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(remove_unicode, prize_to_num_specific), output_processor=Join())
    sales = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())


class SwitzerlandLottoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_8_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_8_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class SwitzerlandJokerItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class TaiwanLotto649Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_8_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_8_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())


class TaiwanSuperLotto638Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_8_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_9_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_10_prize = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_8_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_9_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())
    cat_10_winners = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())


class TrinidadLottoPlusItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, prize_to_num), output_processor=Join())


class TurkeySansTopuItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_8_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_9_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_8_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_9_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())


class TurkeySayisalLotoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())


class TurkeySuperLotoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())


class UKLottoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    rolldown = Field(input_processor=MapCompose(), output_processor=Join())


class UkraineSuperLotoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(strip_new_lines, convert_timestamp), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, strip_symbols), output_processor=Join())


class UkraineMaximaItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(strip_new_lines, convert_timestamp), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, strip_symbols), output_processor=Join())


class UkraineMegalotItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, strip_symbols), output_processor=Join())
    estimated_next_secondary_jackpot = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, strip_symbols), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, strip_symbols), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, strip_symbols), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, strip_symbols), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, strip_symbols), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, strip_symbols), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, strip_symbols), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, strip_symbols), output_processor=Join())
    cat_8_prize = Field(input_processor=MapCompose(strip_new_lines, remove_unicode, strip_symbols), output_processor=Join())


class UruguayGold5Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(), output_processor=Join())


class UruguayGold5RevanchaItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(), output_processor=Join())


class VietLottMega645Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class VietLottPower655Item(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines, swap_commas_fullstops, prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines, strip_symbols), output_processor=Join())


class VikingLottoItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(prize_to_num_specific), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(prize_to_num_specific), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(prize_to_num_specific), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(prize_to_num_specific), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(prize_to_num_specific), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(prize_to_num_specific), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(prize_to_num_specific), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())


class ZambiaGGWorldXItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())


class ZambiaMegaJackpotItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    draw_number = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())


class NationalLotteryUKItem(DjangoItem):
    django_model = Scraper
    name = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())

    draw_datetime = Field(input_processor=MapCompose(), output_processor=Join())
    ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball2 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball3 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball4 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    ball5 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball0 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    bonus_ball1 = Field(input_processor=MapCompose(strip_new_lines), output_processor=Join())
    estimated_next_jackpot = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_2_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_3_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_4_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_5_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_6_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_7_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_8_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_9_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_10_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_11_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_12_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_13_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_14_prize = Field(input_processor=MapCompose(prize_to_num), output_processor=Join())
    cat_1_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_2_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_3_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_4_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_5_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_6_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_7_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_8_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_9_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_10_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_11_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_12_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_13_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())
    cat_14_winners = Field(input_processor=MapCompose(strip_symbols), output_processor=Join())

    rolldown = Field(input_processor=MapCompose(), output_processor=Join())
