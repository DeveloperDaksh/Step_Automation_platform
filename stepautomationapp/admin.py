from django.contrib import admin
from .models import UserData
from .models import Country
from .models import City

admin.site.register(UserData)
admin.site.register(Country)
admin.site.register(City)

# Register your models here.
