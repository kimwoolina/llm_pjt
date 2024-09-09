from django.urls import path
from .views import LocationDataView

app_name = "myapp"

urlpatterns = [
    path('location-data/', LocationDataView.as_view(), name='location-data'),
]
