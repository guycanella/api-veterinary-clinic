from django.contrib import admin
from .models import Owner, Pet, Appointment, Order

# Register your models here.
@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'cpf', 'phone', 'email', 'address')
    search_fields = ('name', 'cpf', 'email')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'breed', 'birth_date', 'owner')
    search_fields = ('name', 'breed', 'owner__name')
    list_filter = ('gender','created_at',)
    list_select_related = ('owner',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('pet', 'appointment_date', 'reason', 'notes', 'doctor', 'price')
    search_fields = ('pet__name', 'appointment_date', 'doctor')
    list_filter = ('created_at',)
    list_select_related = ('pet', 'pet__owner')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('owner', 'date', 'items', 'total', 'notes')
    search_fields = ('owner__name', 'date')
    list_filter = ('created_at','date')
    readonly_fields = ('created_at', 'updated_at')
    list_select_related = ('owner',)