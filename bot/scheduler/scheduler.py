from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.utils import timezone
from django_apscheduler.models import DjangoJobExecution
import sys
from bot.views import get_scraper
from bot.models import Scraper
from datetime import datetime, timedelta

# This is the function you want to schedule - add as many as you want and then register them in the start() function below

def definitly_scrape(*text):
    text = "".join(text)
    obj = Scraper.objects.get(name=text)
    date_append = obj.scheduler
    date_append +=timedelta(days=1)
    get_scraper(text, date_append, obj.run_every)

def start():
    try:
        scheduler = BackgroundScheduler(timezone="Europe/London")
        scheduler.add_jobstore(DjangoJobStore(), "default")
        scraperobj = Scraper.objects.all()
        for name in scraperobj:
            try:
                temp_name = DjangoJobStore().lookup_job(name.name)
                time_of_scrape = name.scheduler
                get_only_name = str(temp_name).split()
                if None == temp_name and time_of_scrape != None:
                    try:
                        days = name.run_every
                        scheduler.add_job(definitly_scrape,  'interval', args=(name.name),next_run_time=time_of_scrape, days=int(days), id=name.name,name=name.name, jobstore='default')
                    except NameError:
                        print(NameError)
                elif 'paused' in str(temp_name) and time_of_scrape != None:
                    days = name.run_every
                    scheduler.add_job(definitly_scrape,  'interval', args=(name.name),next_run_time=time_of_scrape, days=int(days), id=name.name,name=name.name, jobstore='default')
                elif 'paused' not in str(temp_name) and time_of_scrape == None and temp_name != None:
                    days = name.run_every
                    DjangoJobStore().remove_job(get_only_name[0])
            except Exception as e:
                print(e)
        scheduler.start()
        print("Scheduler started...", file=sys.stdout)
    except Exception as e:
        print(e)




