from django.db import models

# Create your models here.
from datetime import datetime
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
    return (r['tle'], last_tle_update)

STATUS_CHOICES = (( 'active','ACTIVE'),
                  ('not_tracked','NOT TRACKED'))

class Sensor(models.Model):
    name = models.CharField('Sensor Name', max_length=20)

TILT_CHOICES = (('ROLL', 'ROLL'),
                ('YAW','YAW'),
                ('PITCH', 'PITCH'))

class Satellite(models.Model):
    norad_id = models.IntegerField('NORAD ID', primary_key=True)
    


    
