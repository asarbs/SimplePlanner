# Generated by Django 3.0.5 on 2020-05-01 11:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PlannerApp', '0019_auto_20200501_1138'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='planned_end_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='item',
            name='planned_start_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
