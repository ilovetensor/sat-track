# Generated by Django 4.1.4 on 2023-08-02 10:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('satTrack', '0011_alter_satellite_last_tle_update_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='satellite',
            name='last_tle_update',
            field=models.DateField(default=datetime.datetime(2023, 8, 2, 2, 2, 2, 2), editable=False, verbose_name='Launch Date'),
        ),
        migrations.AlterField(
            model_name='satellite',
            name='launch_date',
            field=models.DateField(default=datetime.datetime(2023, 8, 2, 2, 2, 2, 2), verbose_name='Launch Date'),
        ),
        migrations.AlterField(
            model_name='tle',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 2, 2, 2, 2, 2), editable=False, verbose_name='Fech datetime'),
        ),
    ]
