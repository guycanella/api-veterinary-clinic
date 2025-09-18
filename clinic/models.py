import uuid

from django.db import models
from django.core.validators import RegexValidator

cpf_validator = RegexValidator(r'^\d{11}$', 'CPF should contain exactly 11 digits.')
phone_validator = RegexValidator(r'^\d{11}$', 'Phone number should contain exactly 11 digits (ex: DDD + número).')

class Gender(models.TextChoices):
    MALE = 'M', 'Male'
    FEMALE = 'F', 'Female'

class Species(models.TextChoices):
    DOG = 'd', 'Dog'
    CAT = 'c', 'Cat'

# Create your models here.
class Owner(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    cpf = models.CharField(max_length=11, unique=True, validators=[cpf_validator])
    phone = models.CharField(max_length=11, validators=[phone_validator])
    email = models.EmailField(unique=True)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Owner'
        verbose_name_plural = 'Owners'

    @property
    def formatted_cpf(self):
        cpf = self.cpf
        return f"{self.cpf[:3]}.{self.cpf[3:6]}.{self.cpf[6:9]}-{self.cpf[9:]}" if cpf and len(cpf) == 11 else self.cpf

    @property
    def formatted_phone(self):
        phone = self.phone
        return f"({self.phone[:2]}) {self.phone[2:7]}-{self.phone[7:]}" if phone and len(phone) == 11 else self.phone

    def __str__(self):
        return f"{self.name} ({self.cpf})"

class Pet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=Gender.choices)
    species = models.CharField(max_length=1, choices=Species.choices)
    breed = models.CharField(max_length=100)
    birth_date = models.DateField(blank=True, null=True)
    owner = models.ForeignKey(Owner, related_name='pets', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.breed})"

class Appointment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pet = models.ForeignKey(Pet, related_name='appointments', on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    reason = models.TextField()
    notes = models.TextField(blank=True, null=True)
    doctor = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-appointment_date']

    def __str__(self):
        return f"Appointment {self.id} - {self.pet.name} @ {self.appointment_date}"

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(Owner, related_name='orders', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    items = models.JSONField(default=list, blank=True)  # List of items in the order
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Order {self.id} - {self.owner.name} - R$ {self.total}"