from django.core.management.base import BaseCommand
from spaces.models import Building, SpaceType

class Command(BaseCommand):
    help = 'Carrega dados iniciais para o sistema de espaços'

    def handle(self, *args, **options):
        # Tipos de espaço
        space_types = [
            ('Sala', 'Sala de aula comum'),
            ('Laboratório', 'Laboratório de informática ou ciências'),
            ('Auditório', 'Auditório para eventos'),
            ('Quadra', 'Quadra poliesportiva'),
        ]
        
        for name, description in space_types:
            SpaceType.objects.get_or_create(
                name=name,
                defaults={'description': description}
            )
        
        # Prédios
        buildings = [
            'CAMPUS I',
            'CAMPUS II',
            'CAMPUS III',
            'CAMPUS IV',
        ]
        
        for building_name in buildings:
            Building.objects.get_or_create(name=building_name)
        
        self.stdout.write(
            self.style.SUCCESS('Dados iniciais carregados com sucesso!')
        )