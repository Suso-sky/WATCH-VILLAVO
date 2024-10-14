from rest_framework import serializers
from .models import Robo, Usuario

class RoboSerializer(serializers.ModelSerializer):
    class Meta:
        model = Robo
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'email', 'rol', 'suscripcion']
