from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

def welcome(request):
    return HttpResponse("Hello world!")

urlpatterns = [
    path("", welcome, name="welcome"),
    path("admin/", admin.site.urls),
    path('api/', include('api.urls')),
    path('accounts', include('knox.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
