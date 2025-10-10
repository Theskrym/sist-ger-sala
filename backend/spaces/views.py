from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import Building, SpaceType, Space, Reservation, FloorPlan
from .serializers import (
    BuildingSerializer, SpaceTypeSerializer, 
    SpaceSerializer, ReservationSerializer
)

class BuildingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    permission_classes = [IsAuthenticated]

class SpaceTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SpaceType.objects.all()
    serializer_class = SpaceTypeSerializer
    permission_classes = [IsAuthenticated]

class SpaceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Space.objects.filter(is_active=True)
    serializer_class = SpaceSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        space = self.get_object()
        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')
        
        if not start_time or not end_time:
            return Response({'error': 'start_time and end_time parameters are required'}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        try:
            start_time = timezone.datetime.fromisoformat(start_time)
            end_time = timezone.datetime.fromisoformat(end_time)
        except (ValueError, TypeError):
            return Response({'error': 'Invalid datetime format'}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        # Verificar reservas conflitantes
        conflicting_reservations = Reservation.objects.filter(
            space=space,
            status='approved',
            start_time__lt=end_time,
            end_time__gt=start_time
        )
        
        is_available = not conflicting_reservations.exists()
        
        return Response({
            'space': space.name,
            'start_time': start_time,
            'end_time': end_time,
            'is_available': is_available,
            'conflicting_reservations': conflicting_reservations.count()
        })

class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Reservation.objects.all()
        return Reservation.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        if not request.user.is_staff:
            return Response({'error': 'Apenas administradores podem aprovar reservas'}, 
                           status=status.HTTP_403_FORBIDDEN)
        
        reservation = self.get_object()
        reservation.status = 'approved'
        reservation.save()
        
        return Response({'status': 'Reserva aprovada'})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        if not request.user.is_staff:
            return Response({'error': 'Apenas administradores podem rejeitar reservas'}, 
                           status=status.HTTP_403_FORBIDDEN)
        
        reservation = self.get_object()
        reservation.status = 'rejected'
        reservation.save()
        
        return Response({'status': 'Reserva rejeitada'})

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        reservation = self.get_object()
        
        if reservation.user != request.user and not request.user.is_staff:
            return Response({'error': 'Você só pode cancelar suas próprias reservas'}, 
                           status=status.HTTP_403_FORBIDDEN)
        
        reservation.status = 'cancelled'
        reservation.save()
        
        return Response({'status': 'Reserva cancelada'})

@api_view(['GET'])
def get_floor_plan(request, plan_id):
    floor_plan = get_object_or_404(FloorPlan, id=plan_id)
    return Response({
        'plan_image': floor_plan.plan_image.url if hasattr(floor_plan.plan_image, 'url') else floor_plan.plan_image,
        'floor_name': floor_plan.floor_name,
        'building_name': floor_plan.building.name
    })