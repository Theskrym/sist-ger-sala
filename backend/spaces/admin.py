from django.contrib import admin
from .models import Building, SpaceType, Space, Reservation

@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(SpaceType)
class SpaceTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Space)
class SpaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'building', 'space_type', 'capacity', 'is_active']
    list_filter = ['building', 'space_type', 'is_active']
    search_fields = ['name', 'building__name']

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['title', 'space', 'user', 'start_time', 'end_time', 'status']
    list_filter = ['status', 'space__building', 'space__space_type']
    search_fields = ['title', 'user__email', 'space__name']
    readonly_fields = ['created_at', 'updated_at']