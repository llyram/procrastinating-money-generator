# serializers.py
from rest_framework import serializers
from .models import Reel

class ReelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reel
        fields = '__all__'
