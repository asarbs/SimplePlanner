# Generated by Django 3.0.5 on 2020-05-01 14:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PlannerApp', '0025_auto_20200501_1413'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='PlannerApp.Team'),
        ),
    ]
