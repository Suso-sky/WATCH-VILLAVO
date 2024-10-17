from django.urls import path
from .views import RoboListCreateView, RoboDetailView, UsuarioListView, mapa_robos, descargar_mapa, obtener_opciones_filtros

urlpatterns = [
    path('robos/', RoboListCreateView.as_view(), name='robo-list-create'),
    path('robos/<int:pk>/', RoboDetailView.as_view(), name='robo-detail'),
    path('usuarios/', UsuarioListView.as_view(), name='usuario-list'),
    path('mapa_calor/', mapa_robos, name='mapa_calor'),
    path('descargar-mapa/', descargar_mapa, name='descargar_mapa'),
    path('obtener_opciones_filtros/', obtener_opciones_filtros, name='obtener_opciones_filtros'),
]
