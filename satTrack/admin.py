from django.contrib import admin
from .models import Satellite, Sensor, TLE
# Register your models here.

# Register your models here.
class SatelliteAdmin(admin.ModelAdmin):
  list_display = ("name", "norad_id", "launch_date","launch_site","status","orbit","swath",)



admin.site.register(Satellite, SatelliteAdmin)
admin.site.register(Sensor)
admin.site.register(TLE)