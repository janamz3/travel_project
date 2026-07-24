from django.contrib import admin
from .models import Trip, Destination

admin.site.register(Destination)
admin.site.register(Trip)