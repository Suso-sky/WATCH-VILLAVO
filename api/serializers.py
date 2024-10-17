from rest_framework import serializers
from .models import RoboMedellin

class RoboMedellinSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoboMedellin
        fields = '__all__'
