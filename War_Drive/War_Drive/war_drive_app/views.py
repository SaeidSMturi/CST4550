from django.shortcuts import render
import folium 
from war_drive_app.models import EVChargingLocation

# Create your views here.
def index(request):
    stations = EVChargingLocation.objects.all()

    # Create a map centered around the average location of the stations
    # m = folium.Map(location=[41.5025, -72.699997], zoom_start=9)
    m = folium.Map(location=[25.2048, 55.2708], zoom_start=12)
    # m = folium.Map(location=[37.7749, -122.4194], zoom_start=12)

    #Add Marker for each station
    # for station in stations:
    #     folium.Marker(
    #         location=[station.latitude, station.longitude],
    #         popup=station.name,
    #         icon=folium.Icon(color='blue')
    #     ).add_to(m)


    for station in stations:
        coordinates = (station.latitude, station.longitude)
        folium.Marker(coordinates).add_to(m)

    context = {'map': m._repr_html_()}
    return render(request, 'index.html', context)