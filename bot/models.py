from django.db import models
from django.utils import timezone

# Create your models here.

class Scraper(models.Model):
    name = models.CharField(primary_key=True, max_length=255, editable=True)
    ticked_option = models.CharField(max_length = 10, null=True, blank=True)
    cat_1_prize = models.CharField(max_length=255, null=True, blank=True)
    estimated_next_jackpot = models.CharField(max_length=255, null=True, blank=True)
    scheduler = models.DateTimeField(null=True, blank=True)
    run_every = models.CharField(max_length = 10, null=True, blank=True)
    draw_datetime = models.CharField(null=True,blank=True, max_length=20)
    draw_time = models.CharField(max_length=50, null=True, blank=True)
        
    def __str__(self) -> str:
        return self.name
