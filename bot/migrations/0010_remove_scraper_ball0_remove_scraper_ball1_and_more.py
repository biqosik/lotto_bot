# Generated by Django 4.1.5 on 2023-01-12 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0009_scraper_ticked_option'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scraper',
            name='ball0',
        ),
        migrations.RemoveField(
            model_name='scraper',
            name='ball1',
        ),
        migrations.RemoveField(
            model_name='scraper',
            name='ball2',
        ),
        migrations.RemoveField(
            model_name='scraper',
            name='ball3',
        ),
        migrations.RemoveField(
            model_name='scraper',
            name='ball4',
        ),
        migrations.RemoveField(
            model_name='scraper',
            name='ball5',
        ),
        migrations.RemoveField(
            model_name='scraper',
            name='bonus_ball',
        ),
        migrations.RemoveField(
            model_name='scraper',
            name='cat_1_winners',
        ),
        migrations.RemoveField(
            model_name='scraper',
            name='cat_2_prize',
        ),
        migrations.RemoveField(
            model_name='scraper',
            name='cat_2_winners',
        ),
        migrations.RemoveField(
            model_name='scraper',
            name='cat_3_prize',
        ),
        migrations.RemoveField(
            model_name='scraper',
            name='cat_3_winners',
        ),
        migrations.RemoveField(
            model_name='scraper',
            name='cat_4_prize',
        ),
        migrations.RemoveField(
            model_name='scraper',
            name='cat_4_winners',
        ),
        migrations.RemoveField(
            model_name='scraper',
            name='cat_5_prize',
        ),
        migrations.RemoveField(
            model_name='scraper',
            name='cat_5_winners',
        ),
        migrations.RemoveField(
            model_name='scraper',
            name='cat_6_prize',
        ),
        migrations.RemoveField(
            model_name='scraper',
            name='cat_6_winners',
        ),
        migrations.RemoveField(
            model_name='scraper',
            name='cat_7_prize',
        ),
        migrations.RemoveField(
            model_name='scraper',
            name='cat_7_winners',
        ),
        migrations.RemoveField(
            model_name='scraper',
            name='cat_8_prize',
        ),
        migrations.RemoveField(
            model_name='scraper',
            name='cat_8_winners',
        ),
        migrations.RemoveField(
            model_name='scraper',
            name='cat_9_winners',
        ),
        migrations.RemoveField(
            model_name='scraper',
            name='draw_datetime',
        ),
        migrations.RemoveField(
            model_name='scraper',
            name='n_MaxMillions',
        ),
        migrations.RemoveField(
            model_name='scraper',
            name='sales',
        ),
        migrations.AlterField(
            model_name='scraper',
            name='cat_1_prize',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='scraper',
            name='estimated_next_jackpot',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='scraper',
            name='ticked_option',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
