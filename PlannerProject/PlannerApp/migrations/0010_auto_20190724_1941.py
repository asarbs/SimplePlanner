# Generated by Django 2.2.3 on 2019-07-24 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PlannerApp', '0009_auto_20190722_1841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='items',
            field=models.ManyToManyField(blank=True, null=True, to='PlannerApp.Item'),
        ),
    ]
