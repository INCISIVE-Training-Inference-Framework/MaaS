# Generated by Django 4.1.7 on 2023-09-20 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='aiengineversion',
            name='max_iteration_time',
            field=models.IntegerField(default=1200),
        ),
        migrations.AddField(
            model_name='aimodel',
            name='download_resume_retries',
            field=models.IntegerField(default=4),
        ),
    ]