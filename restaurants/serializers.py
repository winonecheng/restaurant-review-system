from rest_framework import serializers
from .models import Restaurant

class RestaurantSerializer(serializers.ModelSerializer):
    average_score = serializers.FloatField(read_only=True)
    
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'cuisine_type', 'average_score', 'created_at']
