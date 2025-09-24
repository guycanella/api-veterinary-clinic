from django.shortcuts import render
from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

from .models import Owner, Pet, Appointment, Order
from .serializers import OwnerSerializer, PetSerializer, AppointmentSerializer, OrderSerializer

# Create your views here.
class OwnerViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Owner.objects.all().order_by('-created_at')
    serializer_class = OwnerSerializer
    permission_classes = [AllowAny]

class PetViewSet(mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Pet.objects.all().order_by('name')
    serializer_class = PetSerializer
    permission_classes = [AllowAny]

class AppointmentViewSet(mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Appointment.objects.all().order_by('-appointment_date')
    serializer_class = AppointmentSerializer
    permission_classes = [AllowAny]

class OrderViewSet(mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Order.objects.all().order_by('-date')
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]