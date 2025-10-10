from django.contrib import admin
from .models import Building, SpaceType, Space, Reservation, FloorPlan, Notification
from .widgets import ImageMapWidget
from django import forms
from .admin_site import admin_site

# Now register your models
class BuildingAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'created_at', 'updated_at']
    search_fields = ['name', 'address']

class FloorPlanAdmin(admin.ModelAdmin):
    list_display = ['building', 'floor_name', 'plan_image']
    list_filter = ['building']
    search_fields = ['floor_name']

class SpaceTypeAdmin(admin.ModelAdmin):
    list_display = ['type', 'description']
    search_fields = ['type']

class SpaceAdminForm(forms.ModelForm):
    preview_url = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Space
        fields = '__all__'
        widgets = {
            'location_x': forms.HiddenInput(attrs={'class': 'coord-x'}),
            'location_y': forms.HiddenInput(attrs={'class': 'coord-y'}),
            'floor': forms.Select(attrs={'class': 'floor-plan-selector', 'onchange': 'loadFloorPlan(this.value)'}),
        }

    class Media:
        css = {
            'all': ('admin/css/floor-plan.css',)
        }
        js = ('admin/js/floor-plan.js',)

class SpaceAdmin(admin.ModelAdmin):
    form = SpaceAdminForm
    list_display = ['name', 'building', 'space_type', 'capacity']
    list_filter = ['building', 'space_type']
    search_fields = ['name', 'building__name']
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "floor":
            kwargs["queryset"] = FloorPlan.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.building:
            form.base_fields['floor'].queryset = FloorPlan.objects.filter(building=obj.building)
        return form

    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get('floor_plan'):
            obj.location_x = form.cleaned_data.get('location_x')
            obj.location_y = form.cleaned_data.get('location_y')
        super().save_model(request, obj, form, change)

class ReservationAdmin(admin.ModelAdmin):
    list_display = ['title', 'space', 'user', 'start_datetime', 'end_datetime', 'status']
    list_filter = ['status', 'building', 'space']
    search_fields = ['title', 'description', 'user__email']
    date_hierarchy = 'start_datetime'

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['reservation', 'user', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['reservation__title', 'user__email']

# Registrar no final do arquivo
admin_site.register(Building, BuildingAdmin)
admin_site.register(FloorPlan, FloorPlanAdmin)
admin_site.register(SpaceType, SpaceTypeAdmin)
admin_site.register(Space, SpaceAdmin)
admin_site.register(Reservation, ReservationAdmin)
admin_site.register(Notification, NotificationAdmin)