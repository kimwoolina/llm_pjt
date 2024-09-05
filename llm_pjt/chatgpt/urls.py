from django.urls import path
from .views import WeatherChatAPIView

urlpatterns = [
    path('weather-chat/', WeatherChatAPIView.as_view(), name='weather_chat'),
]
