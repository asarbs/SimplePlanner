# Generated by Django 3.0.5 on 2020-05-01 09:27

import PlannerApp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PlannerApp', '0015_item_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='status',
            field=models.CharField(choices=[(1, 'NEW'), (2, 'GROOMED'), (3, 'IN_PROGRESS'), (4, 'IN_TESTING'), (5, 'DONE'), (6, 'REJECTED')], default=PlannerApp.models.Status['NEW'], max_length=5),
        ),
    ]
