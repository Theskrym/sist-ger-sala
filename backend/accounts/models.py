from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

def validate_cesmac_email(value):
    if not value.endswith('@cesmac.edu.br'):
        raise ValidationError('Apenas emails @cesmac.edu.br são permitidos.')

class CustomUser(AbstractUser):
    email = models.EmailField(
        unique=True,
        validators=[validate_cesmac_email]
    )
    
    # Tornar email como campo de login único
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        # Garantir que o email seja salvo em lowercase
        self.email = self.email.lower()
        super().save(*args, **kwargs)