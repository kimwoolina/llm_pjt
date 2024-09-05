from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path, re_path
from django.views.generic.base import RedirectView

from myapp import views


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', RedirectView.as_view(url='/index/', permanent=True)),
    path("index/", views.index, name="index"),
    path("accounts/", include("accounts.urls")),
    path("myapp/", include("myapp.urls")),
    path("chatgpt/", include("chatgpt.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
