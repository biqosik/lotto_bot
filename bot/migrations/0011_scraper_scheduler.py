# Generated by Django 4.1.5 on 2023-01-12 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0010_remove_scraper_ball0_remove_scraper_ball1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='scraper',
            name='scheduler',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
