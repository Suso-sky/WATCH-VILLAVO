import folium
from folium.plugins import HeatMapWithTime
from django.utils import timezone
from datetime import timedelta
from rest_framework import generics
from .models import Robo, Usuario, RoboMedellin
from .serializers import RoboSerializer, UsuarioSerializer
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
import io

class RoboListCreateView(generics.ListCreateAPIView):
    queryset = Robo.objects.all()
    serializer_class = RoboSerializer

class RoboDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Robo.objects.all()
    serializer_class = RoboSerializer

class UsuarioListView(generics.ListAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

def generar_mapa_html(request):
    # Filtros obtenidos del request
    filtro_tiempo = request.GET.get('filtro', '5')
    filtro_sexo = request.GET.get('sexo', None)
    filtro_medio_transporte = request.GET.get('medio_transporte', None)
    filtro_modalidad = request.GET.get('modalidad', None)

    # Definir el rango de tiempo basado en el filtro de tiempo
    if filtro_tiempo == '1':
        fecha_inicio = timezone.now() - timedelta(days=365)
    elif filtro_tiempo == '2':
        fecha_inicio = timezone.now() - timedelta(days=2*365)
    else:
        fecha_inicio = timezone.now() - timedelta(days=5*365)

    robos = RoboMedellin.objects.filter(fecha_hecho__gte=fecha_inicio)

    if filtro_sexo:
        robos = robos.filter(sexo=filtro_sexo)

    if filtro_medio_transporte:
        robos = robos.filter(medio_transporte=filtro_medio_transporte)

    if filtro_modalidad:
        robos = robos.filter(modalidad=filtro_modalidad)

    if robos.count() == 0:
        return "<p>No hay datos disponibles para los filtros seleccionados.</p>"

    map_center = [6.2442, -75.5812]  # Centro de Medellín
    mapa = folium.Map(location=map_center, zoom_start=12)

    data = {
        'latitud': [robo.latitud for robo in robos],
        'longitud': [robo.longitud for robo in robos],
        'fecha_hecho': [robo.fecha_hecho for robo in robos]
    }

    df = pd.DataFrame(data)

    df['mes'] = df['fecha_hecho'].dt.to_period('M')
    grouped_data = df.groupby('mes')

    heat_data_by_month = []
    time_index = []

    for month, group in grouped_data:
        monthly_data = group[['latitud', 'longitud']].values.tolist()
        heat_data_by_month.append(monthly_data)
        time_index.append(month.strftime('%B %Y'))

    if heat_data_by_month:
        HeatMapWithTime(
            heat_data_by_month,
            index=time_index,
            radius=12,
            gradient={0.5: 'yellow', 0.8: 'orange', 1: 'red'}
        ).add_to(mapa)
        
    return mapa._repr_html_()


def mapa_robos(request):
    
    mapa_html = generar_mapa_html(request)

    filtro_tiempo = request.GET.get('filtro', '5')
    filtro_sexo = request.GET.get('sexo', '')
    filtro_medio_transporte = request.GET.get('medio_transporte', '')
    filtro_modalidad = request.GET.get('modalidad', '')

    return render(request, 'mapa_calor.html', {
        'mapa_html': mapa_html,
        'filtro_tiempo': filtro_tiempo,
        'filtro_sexo': filtro_sexo,
        'filtro_medio_transporte': filtro_medio_transporte,
        'filtro_modalidad': filtro_modalidad
    })

def obtener_opciones_filtros(request):
    opciones_sexo = RoboMedellin.objects.values_list('sexo', flat=True).distinct()
    opciones_medio_transporte = RoboMedellin.objects.values_list('medio_transporte', flat=True).distinct()
    opciones_modalidad = RoboMedellin.objects.values_list('modalidad', flat=True).distinct()

    return JsonResponse({
        'sexo': list(opciones_sexo),
        'medio_transporte': list(opciones_medio_transporte),
        'modalidad': list(opciones_modalidad)
    })

def descargar_mapa(request):
    mapa_html = generar_mapa_html(request)

    buffer = io.StringIO()
    buffer.write(mapa_html)
    buffer.seek(0)

    response = HttpResponse(buffer.getvalue(), content_type='text/html')
    response['Content-Disposition'] = 'attachment; filename="mapa_robos.html"'

    return response
