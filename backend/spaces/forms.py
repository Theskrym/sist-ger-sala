from django import forms
from .models import Reservation, Space, Building, FloorPlan
from django.contrib.admin.widgets import AdminTimeWidget, AdminSplitDateTime

class ReservationAdminForm(forms.ModelForm):
    is_recurring = forms.BooleanField(required=False)
    day_of_week = forms.ChoiceField(
        choices=[
            (0, 'Segunda-feira'),
            (1, 'Terça-feira'),
            (2, 'Quarta-feira'),
            (3, 'Quinta-feira'),
            (4, 'Sexta-feira'),
            (5, 'Sábado'),
            (6, 'Domingo')
        ],
        required=False
    )
    start_time = forms.TimeField(
        required=False,
        widget=AdminTimeWidget(),
        label='Horário inicial'
    )
    end_time = forms.TimeField(
        required=False,
        widget=AdminTimeWidget(),
        label='Horário final'
    )

    class Meta:
        model = Reservation
        exclude = ['user', 'status']  # Remove user and status fields
        widgets = {
            'start_datetime': AdminSplitDateTime(),
            'end_datetime': AdminSplitDateTime(),
            'building': forms.Select(attrs={'class': 'building-selector'}),
            'floor': forms.Select(attrs={'class': 'floor-selector'}),
            'space': forms.Select(attrs={'class': 'space-selector'}),
            'recurrence_end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['floor'].queryset = FloorPlan.objects.none()
        self.fields['space'].queryset = Space.objects.none()
        
        # Hide recurrence fields initially
        self.fields['day_of_week'].widget.attrs['style'] = 'display:none;'
        self.fields['recurrence_end_date'].widget.attrs['style'] = 'display:none;'
        
        # Setup date formats
        self.fields['start_datetime'].widget.widgets[0].attrs['placeholder'] = 'dd/mm/yyyy'
        self.fields['end_datetime'].widget.widgets[0].attrs['placeholder'] = 'dd/mm/yyyy'
        
        if 'building' in self.data:
            try:
                building_id = int(self.data['building'])
                self.fields['floor'].queryset = FloorPlan.objects.filter(building_id=building_id)
            except (ValueError, TypeError):
                pass

        if 'floor' in self.data:
            try:
                floor_id = int(self.data['floor'])
                self.fields['space'].queryset = Space.objects.filter(floor_id=floor_id)
            except (ValueError, TypeError):
                pass

        elif self.instance.pk:
            if self.instance.building:
                self.fields['floor'].queryset = FloorPlan.objects.filter(
                    building=self.instance.building
                )
            if self.instance.floor:
                self.fields['space'].queryset = Space.objects.filter(
                    floor=self.instance.floor
                )