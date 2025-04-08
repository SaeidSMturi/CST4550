from django.shortcuts import render
import folium 
from war_drive_app.models import  WiFi

# # Create your views here.
# def index(request):
#     stations =  WifiSpot.objects.all()

#     # Create a map centered around the average location of the stations
#     # m = folium.Map(location=[41.5025, -72.699997], zoom_start=9)
#     m = folium.Map(location=[25.2048, 55.2708], zoom_start=12)
#     # m = folium.Map(location=[37.7749, -122.4194], zoom_start=12)

#     #Add Marker for each station
#     # for station in stations:
#     #     folium.Marker(
#     #         location=[station.latitude, station.longitude],
#     #         popup=station.name,
#     #         icon=folium.Icon(color='blue')
#     #     ).add_to(m)


#     for station in stations:
#         coordinates = (station.latitude, station.longitude)
#         folium.Marker(coordinates).add_to(m)

#     context = {'map': m._repr_html_()}
#     return render(request, 'index.html', context)


# app/views.py


def index(request):
    WiFiSpots = WiFi.objects.all()

    # Create a Folium map centered at a default location
    # For example, using coordinates from your sample (adjust as necessary)
    m = folium.Map(location=[25.2048, 55.2708], zoom_start=12)

    # Loop through each station and add a marker with a popup showing the station name
    for WiFiSpot in WiFiSpots:
        coordinates = (WiFiSpot.latitude, WiFiSpot.longitude)
        folium.Marker(
            location=coordinates,
            popup=f'<b>{WiFiSpot.SSID}</b>',
            icon=folium.Icon(color='blue')
        ).add_to(m)

    # Pass the generated HTML representation of the map to the template.
    context = {'map': m._repr_html_()}
    return render(request, 'index.html', context)
