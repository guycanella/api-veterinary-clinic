from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import OwnerViewSet, PetViewSet, AppointmentViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'owners', OwnerViewSet, basename='owner')
router.register(r'pets', PetViewSet, basename='pet')
router.register(r'appointments', AppointmentViewSet, basename='appointment')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]