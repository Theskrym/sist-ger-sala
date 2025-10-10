from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import get_floor_plan

router = DefaultRouter()
router.register(r'buildings', views.BuildingViewSet)
router.register(r'space-types', views.SpaceTypeViewSet)
router.register(r'spaces', views.SpaceViewSet)
router.register(r'reservations', views.ReservationViewSet, basename='reservation')

urlpatterns = [
    path('', include(router.urls)),
    path('api/floor-plans/<int:plan_id>/', get_floor_plan, name='get_floor_plan'),
]
