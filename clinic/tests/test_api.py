from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from decimal import Decimal
from clinic.models import Owner, Pet, Appointment, Order, Species

class ClinicAPITestCase(APITestCase):
    def setUp(self):
        # Owner
        self.owner = Owner.objects.create(
            name="Test Owner",
            cpf="00011122233",
            phone="11999990000",
            email="testowner@example.com",
            address="Rua Teste 1"
        )

        # Pet
        self.pet = Pet.objects.create(
            name="Buddy",
            gender="M",
            species=Species.DOG,
            breed="Labrador",
            owner=self.owner
        )

        # Appointment
        self.appointment = Appointment.objects.create(
            pet=self.pet,
            appointment_date="2025-01-01T10:00:00Z",
            reason="Checkup",
            price=Decimal("120.00")
        )

        # Order
        self.order = Order.objects.create(
            owner=self.owner,
            items=[{"name": "Ração", "quantity": 1, "unit_price": 50.0, "line_total": 50.0}],
            total=Decimal("50.00")
        )

    # Owners
    def test_list_owners(self):
        url = reverse('owner-list')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(any(obj['id'] for obj in resp.json()))

    def test_retrieve_owner(self):
        url = reverse('owner-detail', args=[self.owner.id])
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.json()['cpf'], self.owner.cpf)

    def test_create_owner(self):
        url = reverse('owner-list')
        payload = {
            "name": "New Owner",
            "cpf": "99988877766",
            "phone": "11988887777",
            "email": "new@example.com",
            "address": "Rua Nova 10"
        }

        resp = self.client.post(url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Owner.objects.filter(cpf=payload['cpf']).count(), 1)

    # Pets
    def test_list_pets(self):
        url = reverse('pet-list')

        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_retrieve_pet(self):
        url = reverse('pet-detail', args=[self.pet.id])

        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.json()['name'], self.pet.name)

    def test_create_pet(self):
        url = reverse('pet-list')
        payload = {
            "name": "Mittens",
            "gender": "F",
            "species": "c",
            "breed": "Siamese",
            "birth_date": "2022-03-01",
            "owner": str(self.owner.id)
        }

        resp = self.client.post(url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Pet.objects.filter(name="Mittens").exists())

    # Appointments
    def test_list_appointments(self):
        url = reverse('appointment-list')

        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_retrieve_appointment(self):
        url = reverse('appointment-detail', args=[self.appointment.id])

        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.json()['reason'], self.appointment.reason)

    def test_create_appointment(self):
        url = reverse('appointment-list')
        payload = {
            "pet": str(self.pet.id),
            "appointment_date": "2025-02-01T09:00:00Z",
            "reason": "Vacina",
            "price": "80.00"
        }

        resp = self.client.post(url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Appointment.objects.filter(reason="Vacina").exists())

    # Orders
    def test_list_orders(self):
        url = reverse('order-list')

        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_retrieve_order(self):
        url = reverse('order-detail', args=[self.order.id])

        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(str(resp.json()['total']), str(self.order.total))

    def test_create_order(self):
        url = reverse('order-list')
        payload = {
            "owner": str(self.owner.id),
            "items": [{"name": "Vacina", "quantity": 1, "unit_price": 100.0, "line_total": 100.0}],
            "total": "100.00",
            "notes": "Compra de vacina"
        }

        resp = self.client.post(url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Order.objects.filter(notes="Compra de vacina").exists())

    

