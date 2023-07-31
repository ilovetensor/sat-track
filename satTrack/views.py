from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from sgp4.api import Satrec 
from sgp4.api import jday 
import pandas as pd 
from .extract_data import convert, get_live_data, data_over_time
from django.utils import timezone
from django.views.generic.list import ListView

from .models import Satellite, Sensor

def search_page(request):
    model = Satellite
    return render(request, 'search.html')


def search_word(request):
    
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        word = request.GET.get('word', None)
        sat_list = []
        id_dict = {}
        if word:
            sat_objs = Satellite.objects.filter(name__icontains=word)
            for sat in sat_objs:
                id_dict[sat.name] = sat.norad_id
                # print(id_dict)
                sat_list.append(sat.name)
        return JsonResponse({'sat_list': sat_list, 'id_dict': id_dict}, status=200)
    else: 
        return 

    


def data(request, norad_id):
    satellite = Satellite.objects.get(pk=norad_id)
    TLE = satellite.tle
    save_dict = convert(TLE)

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        lat = request.GET.get("cur_loc_lat", None)
        lon = request.GET.get("cur_loc_lon", None)
       
        position = get_live_data(TLE, {'lat':lat, 'lon':lon})
    
        
        if request.method == 'GET':
            return JsonResponse({'context': position})
        return JsonResponse({'status': 'Invalid request'}, status=400)
        
    else:
        context = {'data': save_dict}
        return render(request, 'data.html', context)


def data_buffer(request, norad_id):
    satellite = Satellite.objects.get(pk=norad_id)
    TLE = satellite.tle
    period = convert(TLE)['period']

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        
        time_scale_pos = data_over_time(TLE, period)
    
        if request.method == 'GET':
            return JsonResponse({'context': time_scale_pos})

        return JsonResponse({'status': 'Invalid request'}, status=400)
    else: 
        return 


class list_view(ListView):
    model = Satellite
    paginate_by = 100  # if pagination is desired

    context_object_name = 'satellite_list'
    template_name = 'satellite_list.html'

def detail_view(request, norad_id, sensor_name):
    sensor = Sensor.objects.get(name=sensor_name)
    satellite = Satellite.objects.get(pk=norad_id)
    TLE = satellite.tle
    sat_data = convert(TLE)
    context =  {'satellite': satellite, 'data': sat_data, 'sensor': sensor}
    return render(request, 'home.html', context)

def sensor_list(request, norad_id):
    satellite = Satellite.objects.get(pk=norad_id)
    sensors = satellite.sensors.all()

    context = { 'satellite': satellite ,'sensors': sensors}
    return render(request, 'sensors.html', context)


