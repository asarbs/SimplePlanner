# Generated by Django 3.0.6 on 2020-05-24 18:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PlannerApp', '0031_auto_20200520_2338'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicalitem',
            old_name='planned_end_date',
            new_name='_planned_end_date',
        ),
        migrations.RenameField(
            model_name='historicalitem',
            old_name='planned_start_date',
            new_name='_planned_start_date',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='planned_end_date',
            new_name='_planned_end_date',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='planned_start_date',
            new_name='_planned_start_date',
        ),
    ]