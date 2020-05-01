# Generated by Django 2.2.3 on 2019-07-24 17:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PlannerApp', '0010_auto_20190724_1941'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='items',
        ),
        migrations.AddField(
            model_name='project',
            name='items',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='PlannerApp.Item'),
        ),
    ]
