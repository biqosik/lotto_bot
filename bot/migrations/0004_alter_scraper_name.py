# Generated by Django 4.1.5 on 2023-01-09 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0003_scraper_cat_1_prize'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scraper',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
