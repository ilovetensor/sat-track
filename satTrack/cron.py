from .models import Satellite

def my_cron_job():
    objects = Satellite.objects.all()
    for object in objects:
        object.save()

