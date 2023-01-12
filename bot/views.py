from django.shortcuts import render, redirect
from .models import Scraper
from .forms import LottoForm, ScheduledaysForm, DaysIntervalForm
from django.http import HttpResponseRedirect, HttpResponse
import asyncio
from django.core import management
from subprocess import Popen, PIPE, STDOUT
import os
from lotto_bot import settings
import subprocess
import sys
import slack
from datetime import datetime
from .scheduler import scheduler

# Create your views here.

def get_scraper(form, get_time, interval):
    script_path = os.path.join(settings.BASE_DIR, 'manage.py')
    subprocess.call([sys.executable, script_path, 'crawl', form])
    model = Scraper.objects.get(name=form)
    model.scheduler = get_time
    model.run_every = interval
    model.save()
    scheduler.start()
    if model.ticked_option == 'True':
        slackbot(model, True)
        model.ticked_option = 'False'
        model.save()
    else:
        slackbot(model, False)

def home(request):
    name = Scraper.objects.all()
    form = LottoForm()
    temp_list = []
    scheduler_form = ScheduledaysForm()
    days_interval = DaysIntervalForm()
    if request.method == 'POST':
        form = LottoForm(request.POST)
        schedule = ScheduledaysForm(request.POST)
        days_interval = DaysIntervalForm(request.POST)
        if form.is_valid() and schedule.is_valid():
            form = form['lottery'].value()
            for x in schedule.cleaned_data:
                temp_list.append(schedule[x].value())
            temp_list = ":".join(temp_list)
            get_time = datetime.strptime(temp_list, "%Y-%m-%d:%H:%M:%S")
            get_scraper(form, get_time, days_interval['pick_interval'].value())
            return redirect('home')
        else:
            form = LottoForm()
    context = {'name' : name, 'form' : form, 'days':scheduler_form, 'interval':days_interval}
    return render(request, 'base.html', context=context)


def slackbot(lottery, checking):
    client = slack.WebClient(token=settings.SLACK_TOKEN)
    if checking == True:
        client.chat_postMessage(channel ='#testing_channel', text=f"Hey this lottery has been won: {lottery}")
    else:
        client.chat_postMessage(channel ='#testing_channel', text=f"We are still rolling for: {lottery}")