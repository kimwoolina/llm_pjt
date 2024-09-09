from rest_framework import serializers

class LocationDataSerializer(serializers.Serializer):
    name = serializers.CharField()
    x = serializers.IntegerField()
    y = serializers.IntegerField()
