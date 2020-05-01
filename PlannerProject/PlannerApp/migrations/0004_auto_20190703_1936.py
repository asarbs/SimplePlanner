# Generated by Django 2.2.3 on 2019-07-03 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PlannerApp', '0003_team_teammembers'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sprint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='Sprint number')),
            ],
        ),
        migrations.AddField(
            model_name='board',
            name='sprints',
            field=models.ManyToManyField(to='PlannerApp.Sprint'),
        ),
        migrations.AddField(
            model_name='item',
            name='sprint',
            field=models.ManyToManyField(to='PlannerApp.Sprint'),
        ),
    ]