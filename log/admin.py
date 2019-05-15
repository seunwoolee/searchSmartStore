from django.contrib import admin
from .models import Log


# Register your models here

@admin.register(Log)
class TrackAdmin(admin.ModelAdmin):
    pass
