from rest_framework import serializers
from .models import Owner, Pet, Appointment, Order, Species, Gender

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ('id', 'name', 'cpf', 'phone', 'email', 'address', 'created_at', 'updated_at')

class PetSerializer(serializers.ModelSerializer):
    gender = serializers.ChoiceField(choices=Pet._meta.get_field('gender').choices)
    species = serializers.ChoiceField(choices=Pet._meta.get_field('species').choices)
    owner = serializers.PrimaryKeyRelatedField(queryset=Owner.objects.all())

    class Meta:
        model = Pet
        fields = ('id', 'name', 'gender', 'species', 'breed', 'birth_date', 'owner', 'created_at', 'updated_at')

class AppointmentSerializer(serializers.ModelSerializer):
    pet = serializers.PrimaryKeyRelatedField(queryset=Pet.objects.all())

    class Meta:
        model = Appointment
        fields = ('id', 'pet', 'appointment_date', 'reason', 'notes', 'doctor', 'price', 'created_at', 'updated_at')

class OrderSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=Owner.objects.all())

    class Meta:
        model = Order
        fields = ('id', 'owner', 'date', 'items', 'total', 'notes', 'created_at', 'updated_at')
        read_only_fields = ('date',)