# Generated by Django 2.2.3 on 2019-07-24 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PlannerApp', '0011_auto_20190724_1946'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='items',
        ),
        migrations.AddField(
            model_name='project',
            name='items',
            field=models.ManyToManyField(blank=True, null=True, to='PlannerApp.Item'),
        ),
    ]