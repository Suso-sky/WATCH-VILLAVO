from django.urls import path
from .views import mapa_robos, descargar_mapa, obtener_opciones_filtros

urlpatterns = [
    path('mapa_calor/', mapa_robos, name='mapa_calor'),
    path('descargar-mapa/', descargar_mapa, name='descargar_mapa'),
    path('obtener_opciones_filtros/', obtener_opciones_filtros, name='obtener_opciones_filtros'),
]
