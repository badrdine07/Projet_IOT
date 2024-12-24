from django.contrib import admin
from .models import Dht11

@admin.register(Dht11)
class Dht11Admin(admin.ModelAdmin):
    list_display = ('temperature', 'humidity', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('temperature', 'humidity')
