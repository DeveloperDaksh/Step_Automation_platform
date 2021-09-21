from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('stepautomationapp.urls')),
    path('forms/',include('userforms.urls')),
]
