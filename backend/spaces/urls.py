from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'buildings', views.BuildingViewSet)
router.register(r'space-types', views.SpaceTypeViewSet)
router.register(r'spaces', views.SpaceViewSet)
router.register(r'reservations', views.ReservationViewSet, basename='reservation')

urlpatterns = [
    path('', include(router.urls)),
]
