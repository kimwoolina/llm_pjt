from rest_framework import serializers

class WeatherInfoSerializer(serializers.Serializer):
    rain = serializers.CharField()
    temperature = serializers.CharField()
    humidity = serializers.CharField()
    wind_direction = serializers.CharField()
    wind_speed = serializers.CharField()
