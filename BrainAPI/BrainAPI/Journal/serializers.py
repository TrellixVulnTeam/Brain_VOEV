from rest_framework import serializers
from .models import Journal

class JournalsSerializer(serializers.ModelSerializer):


    class Meta:
        model = Journal
        fields = ('anxiety', 'depression', 'energy', 'mood')
