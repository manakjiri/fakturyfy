from rest_framework import serializers
from .models import Entity

class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = '__all__' 
