from django import forms
from .models import Scraper
from django.contrib.admin.widgets import AdminDateWidget
class LottoForm(forms.Form):
    try:
        names = Scraper.objects.all()
        fields = [tuple([x.name,x.name]) for x in names]
        lottery = forms.CharField(label="Choose Lottery", widget=forms.Select(choices=fields))
    except:
        pass

class AddLotto(forms.Form):
    try:
        with open('./scraper/scraper/spiders/scrapy.py', 'r', errors='ignore', encoding='utf-8') as f:
            datafile = f.readlines()
        scraper_lst = []
        checks_if_working = []
        for line in datafile:
            if ("self.name =" in line.strip()) & ("#" not in line.strip()):
                name = line.split('=')[1].strip().replace("'", "").replace('"', '')
                scraper_lst.append(str(name))
        all_choices = [tuple([x,x]) for x in scraper_lst]
        lottery = forms.ChoiceField(choices = all_choices)

    except:
        pass
    
class DateInput(forms.DateInput):
    input_type='date'

class TimeInput(forms.TimeInput):
    input_type='time'

class ScheduledaysForm(forms.Form):
    try:
        pick_time = forms.DateField(widget=DateInput)
        pick_starting_time_hours = forms.TimeField(widget=TimeInput)
    except:
        pass

class DaysIntervalForm(forms.Form):
    try:
        time_fields = [tuple([x,x]) for x in range(1,8)]
        pick_interval = forms.CharField(label="Pick days interval to run: ", widget=forms.Select(choices=time_fields))
    except:
        pass