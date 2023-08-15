from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from sgp4.api import Satrec 
from sgp4.api import jday 
import pandas as pd 
from .extract_data import convert, get_live_data, data_over_time, get_position
from django.utils import timezone
from django.views.generic.list import ListView

from .models import Satellite, Sensor, TLE

def search_page(request):
    model = Satellite
    # all_objects = Satellite.objects.all()
    # for object in all_objects:
    #     object.save()
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
    TLE_DATA = satellite.tle_now
    save_dict = convert(TLE_DATA)


  

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        lat = request.GET.get("cur_loc_lat", None)
        lon = request.GET.get("cur_loc_lon", None)
        compare_tle = request.GET.get("compare_tle", None)
        position = get_live_data(TLE_DATA, {'lat':lat, 'lon':lon})
        if compare_tle:
            TLE_COMPARE = TLE.objects.get(id=compare_tle).tle
            position1 = get_live_data(TLE_COMPARE, {'lat':lat, 'lon':lon})
        else:
            position1 = position
            
        diff = {'lat': position['lat'] - position1['lat'], 
                'lon': position['lon'] - position1['lon'], 
                'height': position['height'] - position1['height'], 
                }
        
        if request.method == 'GET':
            return JsonResponse({'context': position1,'difference':diff})
        return JsonResponse({'status': 'Invalid request'}, status=400)
        
    else:
        context = {'data': save_dict}
        return render(request, 'data.html', context)


def data_buffer(request, norad_id):
    satellite = Satellite.objects.get(pk=norad_id)
    TLE_DATA = satellite.tle_now
    period = convert(TLE_DATA)['period']

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        
        time_scale_pos = data_over_time(TLE_DATA, period)
    
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
    tle_list = satellite.tle_set.all()
    TLE_DATA = satellite.tle_now
    sat_data = convert(TLE_DATA)
    context =  {'satellite': satellite, 'data': sat_data, 'sensor': sensor, 'tle_list': tle_list}
    return render(request, 'home.html', context)

def sensor_list(request, norad_id):
    satellite = Satellite.objects.get(pk=norad_id)
    sensors = satellite.sensors.all()
    TLE_DATA = satellite.tle_now
    save_dict = convert(TLE_DATA)

    context = { 'satellite': satellite ,'sensors': sensors, 'data': save_dict}
    return render(request, 'sensors.html', context)


def compare_tle(request, norad_id):
    print("running")
    satellite = Satellite.objects.get(pk=norad_id)
    tle_list = satellite.tle_set.all()
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        id_1 = request.GET.get("tle1", None)
        id_2 = request.GET.get("tle2", None)
        time = request.GET.get("time", None)
        print(time)
        TLE1 = TLE.objects.get(id=id_1).tle
        TLE2 = TLE.objects.get(id=id_2).tle
        position = get_position(TLE1, time)
        position1 = get_position(TLE2, time)
        diff = {'lat': position['lat'] - position1['lat'], 
                'lon': position['lon'] - position1['lon'], 
                'height': position['height'] - position1['height'], 
                }
        if request.method == 'GET':
            return JsonResponse({'context': diff})
    else:
        context = {'satellite': satellite, 'tle_list': tle_list }
        return render(request, 'compare.html', context)
