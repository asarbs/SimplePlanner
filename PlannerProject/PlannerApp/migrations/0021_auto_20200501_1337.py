# Generated by Django 3.0.5 on 2020-05-01 11:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PlannerApp', '0020_auto_20200501_1323'),
    ]

    operations = [
        migrations.AddField(
            model_name='sprint',
            name='end_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='sprint',
            name='start_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
