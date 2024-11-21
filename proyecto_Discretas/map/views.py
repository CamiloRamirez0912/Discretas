import folium
from django.shortcuts import render
import os
from django.conf import settings

def mostrar_mapa(request):
    centro_mapa = [5.5353, -73.3678]
    mapa = folium.Map(location=centro_mapa, zoom_start=13)

    hospital1 = [5.5400, -73.3640]
    hospital2 = [5.5300, -73.3700]
    accidente = [5.5370, -73.3660]

    folium.Marker(hospital1, popup="Hospital 1", icon=folium.Icon(color="green")).add_to(mapa)
    folium.Marker(hospital2, popup="Hospital 2", icon=folium.Icon(color="blue")).add_to(mapa)
    folium.Marker(accidente, popup="Accidente", icon=folium.Icon(color="red")).add_to(mapa)

    templates_dir = os.path.join(settings.BASE_DIR, 'templates')
    mapa_path = os.path.join(templates_dir, 'map.html')

    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)

    print(f"Mapa guardado en: {mapa_path}")  
    mapa.save(mapa_path)

    return render(request, 'map.html')