# Generated by Django 2.2.3 on 2019-07-22 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PlannerApp', '0008_auto_20190722_1841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='sprint',
            field=models.ManyToManyField(blank=True, to='PlannerApp.Sprint'),
        ),
    ]
