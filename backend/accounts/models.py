from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

def validate_cesmac_email(value):
    if not value.endswith('@cesmac.edu.br'):
        raise ValidationError('Apenas emails @cesmac.edu.br são permitidos.')

class CustomUser(AbstractUser):
    ACCESS_LEVELS = [
        (0, 'Usuário Comum'),
        (1, 'Funcionário'),
        (2, 'Administrador'),
    ]
    
    email = models.EmailField(
        unique=True,
        validators=[validate_cesmac_email]
    )
    profile_photo = models.URLField(
        blank=True, 
        help_text="URL para foto do perfil"
    )
    access_level = models.IntegerField(
        choices=ACCESS_LEVELS,
        default=0
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