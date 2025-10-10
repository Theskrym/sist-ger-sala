from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()

class Building(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.TextField(null=True, blank=True)  # Making it optional
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class FloorPlan(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='floor_plans')
    floor_name = models.CharField(max_length=50)  # ex: "ANDAR 1", "ANDAR -1"
    plan_image = models.URLField()
    
    class Meta:
        unique_together = ['building', 'floor_name']

    def __str__(self):
        return f"{self.building.name} - {self.floor_name}"

class SpaceType(models.Model):
    type = models.CharField(
        max_length=90,
        default='Sala Padrão'  # Adding a default value
    )
    description = models.CharField(
        max_length=500,
        default='Descrição padrão'  # Adding a default value for description as well
    )

    class Meta:
        ordering = ['type']

    def __str__(self):
        return self.type

class Space(models.Model):
    building = models.ForeignKey(
        Building, 
        on_delete=models.CASCADE,
        null=True,  # Temporariamente permitir null
        blank=True
    )
    space_type = models.ForeignKey(
        SpaceType, 
        on_delete=models.CASCADE,
        null=True,  # Temporariamente permitir null
        blank=True
    )
    name = models.CharField(max_length=90)
    capacity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    floor = models.ForeignKey(
        FloorPlan, 
        on_delete=models.CASCADE,
        null=True,  # Temporariamente permitir null
        blank=True
    )
    location_x = models.FloatField(null=True, blank=True)  # Coordenada X do ponto na planta
    location_y = models.FloatField(null=True, blank=True)  # Coordenada Y do ponto na planta

    class Meta:
        ordering = ['building__name', 'name']
        unique_together = ['building', 'name']

    def __str__(self):
        return f"{self.building.name} - {self.name} ({self.space_type.type})"  # Changed from space_type.name to space_type.type

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('approved', 'Aprovado'),
        ('rejected', 'Rejeitado'),
        ('canceled', 'Cancelado'),
        ('completed', 'Concluído'),
        ('in_progress', 'Em Andamento'),
    ]

    building = models.ForeignKey(
        Building, 
        on_delete=models.CASCADE,
        null=True,  # Temporariamente permitir null
        blank=True
    )
    space = models.ForeignKey(
        Space, 
        on_delete=models.CASCADE,
        null=True,  # Temporariamente permitir null
        blank=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Add this line
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1400)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_recurring = models.BooleanField(default=False)
    recurrence_end_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['start_datetime']
        indexes = [
            models.Index(fields=['space', 'start_datetime', 'end_datetime']),
            models.Index(fields=['user', 'start_datetime']),
        ]

    def clean(self):
        # Validar que o horário final é depois do inicial
        if self.end_datetime <= self.start_datetime:
            raise ValidationError('O horário final deve ser depois do horário inicial.')

        # Validar que a reserva não sobrepõe outras reservas aprovadas
        if self.pk is None:  # Nova reserva
            overlapping_reservations = Reservation.objects.filter(
                space=self.space,
                status='approved',
                start_datetime__lt=self.end_datetime,
                end_datetime__gt=self.start_datetime
            )
        else:  # Reserva existente sendo editada
            overlapping_reservations = Reservation.objects.filter(
                space=self.space,
                status='approved',
                start_datetime__lt=self.end_datetime,
                end_datetime__gt=self.start_datetime
            ).exclude(pk=self.pk)

        if overlapping_reservations.exists():
            raise ValidationError('Já existe uma reserva aprovada para este horário.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.space} ({self.start_datetime} to {self.end_datetime})"

    @property
    def duration(self):
        return self.end_datetime - self.start_datetime

class Notification(models.Model):
    STATUS_CHOICES = [
        ('not_seen', 'Não Visto'),
        ('open', 'Em Aberto'),
        ('closed', 'Fechado'),
    ]

    reservation = models.ForeignKey(
        Reservation, 
        on_delete=models.CASCADE,
        null=True,  # Temporariamente permitir null
        blank=True
    )
    user = models.ForeignKey(
        'accounts.CustomUser', 
        on_delete=models.CASCADE,
        null=True,  # Temporariamente permitir null
        blank=True
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_seen')
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_by = models.ForeignKey(
        'accounts.CustomUser', 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='modified_notifications'
    )