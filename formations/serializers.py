from rest_framework import serializers
from .models import Formation

class FormationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formation
        fields = ['id', 'titre', 'duree', 'prix']