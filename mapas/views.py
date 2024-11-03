# views.py
from django.http import JsonResponse
from django.shortcuts import render
import json

def mapa_view(request):
    return render(request, 'mapa.html')

def send_coordinates(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        # Aqui você pode processar os dados ou enviar para outra API
        print(f"Coordenadas recebidas: {latitude}, {longitude}")

        return JsonResponse({'status': 'sucesso', 'latitude': latitude, 'longitude': longitude})
    return JsonResponse({'status': 'falha'}, status=400)

def gps_tracker(request):
    return render(request, 'gps_tracker.html')
