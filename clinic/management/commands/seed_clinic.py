from decimal import Decimal, ROUND_HALF_UP
import random
import re

from django.core.management.base import BaseCommand
from django.utils import timezone

from faker import Faker

from clinic.models import Owner, Pet, Appointment, Order, Species

fake = Faker('pt_BR')
Faker.seed(123)
random.seed(123)

DOG_BREEDS = [
    "Labrador", "Golden Retriever", "Bulldog", "Poodle", "Beagle",
    "Shih Tzu", "Rottweiler", "Yorkshire", "German Shepherd", "Not defined"
]

CAT_BREEDS = [
    "Siamese", "Persian", "Maine Coon", "Ragdoll", "Bengal",
    "Sphynx", "British Shorthair", "Scottish Fold", "Not defined"
]

def only_digits(s: str) -> str:
    """Remove everything that is not digit (returns empty string if None)."""
    return re.sub(r'\D', '', s or '')

def random_species_and_breed():
    if random.random() < 0.6:
        return Species.DOG, random.choice(DOG_BREEDS)
    else:
        return Species.CAT, random.choice(CAT_BREEDS)

def money(v):
    return Decimal(v).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete existing data from clinic app models before seeding.",
        )

    def handle(self, *args, **options):
        if options['flush']:
            self.stdout.write("Deleting existing data...")
            Owner.objects.all().delete()
            Pet.objects.all().delete()
            Appointment.objects.all().delete()
            Order.objects.all().delete()
            self.stdout.write("Deletied existing data.")

        pet_counts = [1, 1, 1, 2, 2]
        random.shuffle(pet_counts)

        owners = []
        for i in range(5):
            cpf = only_digits(fake.cpf())
            while Owner.objects.filter(cpf=cpf).exists():
                cpf = only_digits(fake.cpf())

            phone = only_digits(fake.numerify("##9########"))
            if len(phone) < 11:
                phone = only_digits(fake.numerify("###########"))
            phone = phone[:11].rjust(11, "0")

            email = fake.unique.ascii_free_email() if hasattr(fake, "ascii_free_email") else fake.unique.email()
            while Owner.objects.filter(email=email).exists():
                email = fake.unique.email()

            owner = Owner.objects.create(
                name=fake.name(),
                cpf=cpf,
                phone=phone,
                email=email,
                address=fake.address(),
            )
            owners.append((owner, pet_counts[i]))

        pets_created = []
        appointments_created = []
        orders_created = []

        order_counts = [0, 0, 1, 1, 2]
        random.shuffle(order_counts)

        for idx, (owner, pet_count) in enumerate(owners):
            for pidx in range(pet_count):
                pet_name = fake.first_name()
                species, breed = random_species_and_breed()

                gender = random.choice(['M', 'F'])

                pet = Pet.objects.create(
                    name=pet_name,
                    gender=gender,
                    species=species,
                    breed=breed,
                    birth_date=fake.date_of_birth(minimum_age=0, maximum_age=15),
                    owner=owner,
                )
                pets_created.append(pet)

                appt_count = random.choice([1, 2])
                for _ in range(appt_count):
                    appt_dt = fake.date_time_between(start_date='-1y', end_date='now', tzinfo=timezone.get_current_timezone())
                    reason = fake.sentence(nb_words=6)
                    notes = fake.paragraph(nb_sentences=2)
                    doctor = fake.name()
                    price = money(random.uniform(50, 500))

                    appt = Appointment.objects.create(
                        pet=pet,
                        appointment_date=appt_dt,
                        reason=reason,
                        notes=notes,
                        doctor=doctor,
                        price=price,
                    )
                    appointments_created.append(appt)

            orders_for_owner = order_counts[idx]
            for _ in range(orders_for_owner):
                items = []
                n_items = random.randint(1, 4)
                total = Decimal('0.00')

                for i_item in range(n_items):
                    item_name = random.choice([
                        "Ração", "Vacina", "Consulta", 
                        "Antipulgas", "Medicamento", "Brinquedo", 
                        "Coleira"
                    ])

                    qty = random.randint(1, 3)
                    unit_price = money(random.uniform(10, 200))
                    item_total = unit_price * qty
                    total += item_total

                    items.append({
                        "name": item_name,
                        "quantity": qty,
                        "unit_price": float(unit_price),
                        "line_total": float(item_total)
                    })

                total = total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                order = Order.objects.create(
                    owner=owner,
                    items=items,
                    total=total,
                    notes=fake.sentence(nb_words=8),
                )
                orders_created.append(order)

        self.stdout.write(self.style.SUCCESS("Seeding completed. Summary:"))
        self.stdout.write(f"Owners created: {len(owners)}")
        self.stdout.write(f"Pets created: {len(pets_created)}")
        self.stdout.write(f"Appointments created: {len(appointments_created)}")
        self.stdout.write(f"Orders created: {len(orders_created)}")
        self.stdout.write(" ")
        self.stdout.write("Owners and their pets/orders:")

        for idx, (owner, pet_count) in enumerate(owners):
            oc = Order.objects.filter(owner=owner).count()
            pc = Pet.objects.filter(owner=owner).count()
            self.stdout.write(f"- {owner.name} (cpf={owner.cpf}) -> pets={pc}, orders={oc}")

        self.stdout.write(self.style.SUCCESS("Done."))
