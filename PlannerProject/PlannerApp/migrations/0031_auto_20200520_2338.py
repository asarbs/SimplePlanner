# Generated by Django 3.0.6 on 2020-05-20 21:38

import PlannerApp.models
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('PlannerApp', '0030_historicalteam'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalItem',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('priority', models.FloatField(max_length=25)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('planned_start_date', models.DateField(blank=True, default=datetime.date.today, null=True)),
                ('planned_end_date', models.DateField(blank=True, default=datetime.date.today, null=True)),
                ('status', models.IntegerField(choices=[(1, 'NEW'), (2, 'GROOMED'), (3, 'IN_PROGRESS'), (4, 'IN_TESTING'), (5, 'DONE'), (6, 'REJECTED'), (7, 'DEPLOYED')], default=PlannerApp.models.Status['NEW'])),
                ('description', models.TextField(blank=True, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('assignment', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='PlannerApp.Item')),
                ('team', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='PlannerApp.Team')),
            ],
            options={
                'verbose_name': 'historical item',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.DeleteModel(
            name='Board',
        ),
    ]
