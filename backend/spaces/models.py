from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()

class Building(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class SpaceType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Space(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='spaces')
    space_type = models.ForeignKey(SpaceType, on_delete=models.CASCADE, related_name='spaces')
    name = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField(default=1)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['building__name', 'name']
        unique_together = ['building', 'name']

    def __str__(self):
        return f"{self.building.name} - {self.name} ({self.space_type.name})"

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('approved', 'Aprovado'),
        ('rejected', 'Rejeitado'),
        ('cancelled', 'Cancelado'),
        ('completed', 'Concluído'),
    ]

    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name='reservations')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_time']
        indexes = [
            models.Index(fields=['space', 'start_time', 'end_time']),
            models.Index(fields=['user', 'start_time']),
        ]

    def clean(self):
        # Validar que o horário final é depois do inicial
        if self.end_time <= self.start_time:
            raise ValidationError('O horário final deve ser depois do horário inicial.')

        # Validar que a reserva não sobrepõe outras reservas aprovadas
        if self.pk is None:  # Nova reserva
            overlapping_reservations = Reservation.objects.filter(
                space=self.space,
                status='approved',
                start_time__lt=self.end_time,
                end_time__gt=self.start_time
            )
        else:  # Reserva existente sendo editada
            overlapping_reservations = Reservation.objects.filter(
                space=self.space,
                status='approved',
                start_time__lt=self.end_time,
                end_time__gt=self.start_time
            ).exclude(pk=self.pk)

        if overlapping_reservations.exists():
            raise ValidationError('Já existe uma reserva aprovada para este horário.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.space} ({self.start_time} to {self.end_time})"

    @property
    def duration(self):
        return self.end_time - self.start_time