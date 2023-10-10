# Generated by Django 4.2.4 on 2023-10-10 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_aiengineversion_max_iteration_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='aiengineversion',
            name='cpu_limit',
            field=models.CharField(default='4000m', max_length=50),
        ),
        migrations.AddField(
            model_name='aiengineversion',
            name='cpu_request',
            field=models.CharField(default='250m', max_length=50),
        ),
        migrations.AddField(
            model_name='aiengineversion',
            name='memory_limit',
            field=models.CharField(default='3584Mi', max_length=50),
        ),
        migrations.AddField(
            model_name='aiengineversion',
            name='memory_request',
            field=models.CharField(default='3584Mi', max_length=50),
        ),
    ]
