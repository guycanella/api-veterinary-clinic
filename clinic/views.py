from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, filters
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
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'cpf', 'email']
    search_fields = ['name', 'cpf', 'email']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    queryset = Owner.objects.all().order_by('-created_at')
    serializer_class = OwnerSerializer
    permission_classes = [AllowAny]

class PetViewSet(mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['owner', 'species', 'gender']
    search_fields = ['name', 'breed']
    ordering_fields = ['name', 'birth_date', 'created_at']
    ordering = ['name']
    queryset = Pet.objects.all().order_by('name')
    serializer_class = PetSerializer
    permission_classes = [AllowAny]

class AppointmentViewSet(mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['pet', 'appointment_date']
    search_fields = ['pet__name']
    ordering_fields = ['appointment_date', 'created_at']
    ordering = ['appointment_date']
    queryset = Appointment.objects.all().order_by('-appointment_date')
    serializer_class = AppointmentSerializer
    permission_classes = [AllowAny]

class OrderViewSet(mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['owner', 'date']
    search_fields = ['owner__name']
    ordering_fields = ['date', 'created_at']
    ordering = ['date']
    queryset = Order.objects.all().order_by('-date')
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]