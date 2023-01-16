from django.shortcuts import render, redirect
from .models import Scraper
from .forms import LottoForm, ScheduledaysForm, DaysIntervalForm, AddLotto
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
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, ("There was an error loggin in, Try Again!!"))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

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
        model.scheduler = None
        model.save()
    else:
        slackbot(model, False)


@login_required(login_url='login')
def home(request):
    name = Scraper.objects.all()
    form = LottoForm()
    add_lotto = AddLotto()
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
    context = {'name' : name, 'form' : form, 'days':scheduler_form, 'interval':days_interval, 'add_lotto':add_lotto}
    return render(request, 'base.html', context=context)

def logout_user(request):
    logout(request)
    return redirect('login')

def slackbot(lottery, checking):
    client = slack.WebClient(token=settings.SLACK_TOKEN)
    if checking == True:
        client.chat_postMessage(channel ='#testing_channel', text=f"Hey this lottery has been won: {lottery}")
        client.chat_postMessage(channel ='#lotto-internal', text=f"Hey this lottery has been won: {lottery}")
    else:
        client.chat_postMessage(channel ='#testing_channel', text=f"We are still rolling for: {lottery}")