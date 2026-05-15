from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'artist', 'event_date', 'created_by', 'created_at')
    list_filter = ('event_type', 'event_date')
    search_fields = ('title', 'artist')
    ordering = ('event_date',)
