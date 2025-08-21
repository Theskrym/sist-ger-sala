from django import forms
from .models import Reservation, Space, Building, SpaceType
from django.utils import timezone

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['space', 'title', 'description', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['space'].queryset = Space.objects.filter(is_active=True)
        
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time:
            # Validar que a reserva é no futuro
            if start_time < timezone.now():
                raise forms.ValidationError('Não é possível fazer reservas no passado.')

            # Validar duração mínima (30 minutos)
            if (end_time - start_time).total_seconds() < 1800:
                raise forms.ValidationError('A reserva deve ter pelo menos 30 minutos de duração.')

            # Validar duração máxima (8 horas)
            if (end_time - start_time).total_seconds() > 28800:
                raise forms.ValidationError('A reserva não pode exceder 8 horas de duração.')

        return cleaned_data