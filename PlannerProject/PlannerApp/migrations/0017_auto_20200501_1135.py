# Generated by Django 3.0.5 on 2020-05-01 09:35

import PlannerApp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PlannerApp', '0016_auto_20200501_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='status',
            field=models.CharField(choices=[(PlannerApp.models.Status['NEW'], 'NEW'), (PlannerApp.models.Status['GROOMED'], 'GROOMED'), (PlannerApp.models.Status['IN_PROGRESS'], 'IN_PROGRESS'), (PlannerApp.models.Status['IN_TESTING'], 'IN_TESTING'), (PlannerApp.models.Status['DONE'], 'DONE'), (PlannerApp.models.Status['REJECTED'], 'REJECTED')], default=PlannerApp.models.Status['NEW'], max_length=5),
        ),
    ]
