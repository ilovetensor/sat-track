# Generated by Django 4.1.4 on 2023-08-03 09:44

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('satTrack', '0002_rename_tle_satellite_tle_now_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TLE',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tle', models.TextField(default='', editable=False, max_length=100, verbose_name='Satellite Tle ')),
                ('date_added', models.DateTimeField(default=datetime.datetime(2000, 2, 2, 2, 2, 2, 2), editable=False, verbose_name='Fech datetime')),
                ('satellite', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='satTrack.satellite')),
            ],
        ),
    ]