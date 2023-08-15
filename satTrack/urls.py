from django.urls import path 
from .views import data, data_buffer, list_view, search_page, search_word, sensor_list, detail_view, compare_tle

urlpatterns = [
    path('', search_page, name="search_page"),
    path('searchword', search_word, name='search_word'),
    path('sat', list_view.as_view(), name='list_view'),
    path('sat/<int:norad_id>', sensor_list, name="detail_view"),
    path('sat/<int:norad_id>', sensor_list, name="detail_view"),
    path('sat/<int:norad_id>/compare', compare_tle, name='compare',),
    path('databuffer/<int:norad_id>', data_buffer, name='databuffer'),
    path('sat/<int:norad_id>/<str:sensor_name>', detail_view, name='detail_view'),

]

