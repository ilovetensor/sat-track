from django.db import models

# Create your models here.
from datetime import datetime, timedelta
import requests

api_key = 'M8PZCZ-5ELM7M-DE5LRK-531A'
API_URL = 'https://api.n2yo.com/rest/v1/satellite/'
params = {'apiKey': api_key}

def get_tle_from_n2yo(id):
    r = requests.get(
        f'{API_URL}tle/{id}',
        params=params
    ).json()
    last_tle_update = datetime.now().date()
    print(r)
    return (r['tle'])

def datetime_from_epoch(day_of_year):
    year = int(day_of_year[:2])
    day_of_year = float(day_of_year[2:])
    date = datetime(year, 1, 1) + timedelta(days=day_of_year - 1)
    time = timedelta(seconds=(day_of_year % 1) * 24 * 60 * 60)
    return date + time

STATUS_CHOICES = (( 'active','ACTIVE'),
                  ('not_tracked','NOT TRACKED'))

class Sensor(models.Model):
    name = models.CharField('Sensor Name', max_length=20)
    resolution_type = models.CharField('Resolution Type', max_length=30, default='resolution')
    resolution_value = models.FloatField('Resolution [m]', default=0)
    swath = models.FloatField('Swath [km]', default=0)
    
    positive_tilting = models.FloatField('Positive Tilting', default=0)
    negative_tilting = models.FloatField('Negative Tilting', default=0)


    
    def __str__(self):
        return f"{self.resolution_type} sensor,\n res.:{self.resolution_value}m, swath: {self.swath}km"

TILT_CHOICES = (('ROLL', 'ROLL'),
                ('YAW','YAW'),
                ('PITCH', 'PITCH'))

class Satellite(models.Model):
    norad_id = models.IntegerField('NORAD ID', primary_key=True)
    name = models.CharField('Satellite Name', max_length=20)
    satellite_type = models.CharField('Satellite type', max_length=30, default='-')
    
    description = models.TextField('About Satellite', default='-')
    tle_now = models.TextField("Satellite Tle" ,default='', editable=False)
    launch_date = models.DateField('Launch Date', default=datetime(2000,2,2,2,2,2,2))
    launch_site = models.CharField('Launch Site', max_length=50, default='not provided')
    last_tle_update = models.DateField('Launch Date', default=datetime(2000,2,2,2,2,2,2),editable=False)
    swath = models.FloatField('Swath [km]', default=0)
    status = models.CharField('Status',max_length=20, choices = STATUS_CHOICES, default='IN ORBIT')
    # resolution_type = models.CharField('Resolution Type',max_length=30, default="")
    # resolution_value = models.FloatField('Resolution Value [m]', default=0)
    orbit = models.CharField('Orbit Type', max_length=20, default='-')
    orbital_period = models.FloatField('Orbital Period [m]', default=0)
    orbit_revisit = models.IntegerField('Revisit Period [days]', default=0)
    orbit_distance = models.FloatField('Successive orbits distance [km]', default=0)
    orbits_per_day = models.IntegerField('Orbits per day', default=0)

    inclination = models.FloatField('Inclination [°]', default=0)
    perigee = models.FloatField('Perigee', default=0)
    apogee = models.FloatField('Apogee', default=0)
    sensors = models.ManyToManyField(Sensor)
    max_saved_tle = 10


    def remove_from_set(self, query_set, items):
        for obj in query_set[:items]:
            obj.delete()

    def save_new_tle(self):
        # query_set = self.tle_set.all()
        # total_tles = len(query_set)
        # if total_tles >= self.max_saved_tle:
        #     items = total_tles - self.max_saved_tle+1
        #     self.remove_from_set(query_set, items)

        tle_fetched = get_tle_from_n2yo(self.norad_id)
        if tle_fetched == self.tle_now:
            print("TLE NOT UPDATED NOW !")
            return
        else: 
            # object = TLE(satellite=self, tle = tle_fetched, epoch_date = datetime.now())
            self.tle_now = tle_fetched
            self.last_tle_update = datetime.now()
            epoch_date = datetime_from_epoch(tle_fetched[18:32])
            object = TLE(satellite=self, tle = tle_fetched, epoch_date = epoch_date)
            object.save()


        

    def __str__(self):
        return self.name
    
    
    def save(self, *args, **kwargs):
        self.save_new_tle()
        super().save(*args, **kwargs)
    

class TLE(models.Model):
    satellite = models.ForeignKey(to=Satellite, on_delete=models.CASCADE , editable=True)
    tle = models.TextField("Satellite Tle" ,max_length=300, default='s', null=True, editable=True)
    epoch_date = models.DateTimeField('Epoch Date', default=datetime(2000,2,2,2,2,2,2))

    def __str__(self):
        return f"{self.satellite.name} on {self.epoch_date.date()} at {self.epoch_date.strftime('%H:%M:%S')}"


"""
for i in df.index:
    ...:     tlef = df.loc[i, ['TLE_LINE1']] + "\n" + df.loc[i, ['TLE_LINE2']]
    ...:     epoch = df.loc[i, 'EPOCH']
    ...:
    ...:     ep = datetime.fromisoformat(epoch.__str__())
    ...:     tleobj = TLE(satellite=sat, tle=tlef, epoch_date=ep)
    ...:     tleobj.save()
    ...:     print(i)
    
"""