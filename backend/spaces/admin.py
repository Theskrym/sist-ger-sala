from django.contrib import admin
from django.utils.html import format_html
from .models import Building, SpaceType, Space, Reservation, FloorPlan, Notification
from .widgets import ImageMapWidget
from django import forms
from .admin_site import admin_site
from .forms import ReservationAdminForm

# Now register your models
class BuildingAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'created_at', 'updated_at']
    search_fields = ['name', 'address']

class FloorPlanAdmin(admin.ModelAdmin):
    list_display = ['building', 'floor_name', 'image_preview']
    list_filter = ['building']
    search_fields = ['building__name', 'floor_name']

    def image_preview(self, obj):
        if obj.plan_image:
            return format_html('<img src="{}" width="100" />', obj.plan_image.url)
        elif obj.plan_image_url:
            return format_html('<img src="{}" width="100" />', obj.plan_image_url)
        return "No Image"
    image_preview.short_description = 'Preview'

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
    form = ReservationAdminForm
    list_display = ['space', 'start_datetime', 'end_datetime', 'status']
    list_filter = ['space__building', 'status']
    search_fields = ['space__name']
    exclude = ['user', 'status']  # Hide these fields from the form
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not obj:  # If adding new reservation
            # Instead of setting on form.instance, we'll use initial data
            form.initial = {
                'user': request.user.id,
                'status': 'pending'
            }
        return form

    def save_model(self, request, obj, form, change):
        if not change:  # If creating new reservation
            obj.user = request.user
            obj.status = 'pending'
        super().save_model(request, obj, form, change)

    class Media:
        css = {
            'all': ('admin/css/floor-plan.css',)
        }
        js = (
            'admin/js/floor-plan.js',
            'admin/js/reservation.js',
        )

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