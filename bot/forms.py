from django import forms
from .models import Scraper
class LottoForm(forms.Form):
    try:
        names = Scraper.objects.all()
        fields = [tuple([x.name,x.name]) for x in names]
        lottery = forms.CharField(label="Choose Lottery", widget=forms.Select(choices=fields))
    except:
        pass

class AddLotto(forms.Form):
    try:
        lottery = forms.CharField(label="Add lottery", initial="add lottery")
    except:
        pass

class ScheduledaysForm(forms.Form):
    try:
        pick_time = forms.DateField(widget=forms.SelectDateWidget())
        hours = [tuple([x,x]) for x  in range(0,24)]
        minutes = [tuple([x,x]) for x in range(0,60)]
        pick_starting_time_hours = forms.CharField(label = "Hour ", widget=forms.Select(choices=hours))
        pick_starting_time_minutes = forms.CharField(label = "Minute ", widget=forms.Select(choices=minutes))
        pick_starting_time_seconds = forms.CharField(label = "Second ", widget=forms.Select(choices=minutes))
    except:
        pass

class DaysIntervalForm(forms.Form):
    try:
        time_fields = [tuple([x,x]) for x in range(1,8)]
        pick_interval = forms.CharField(label="Pick days interval to run: ", widget=forms.Select(choices=time_fields))
    except:
        pass