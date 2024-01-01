from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

from django_countries.fields import CountryField
import uuid
from datetime import date

import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File


class Account(models.Model):
    ROLE_CHOICES = (
        ("healthcare_professional", "Healthcare Professional"),
        ("administrator", "Administrator"),
        ("patient", "Patient"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


class Hospital(models.Model):
    uid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    name = models.CharField(max_length=255)
    admin = models.ForeignKey(Account, related_name="hospital_admin", on_delete=models.CASCADE, null=True, blank=True)
    staff = models.ManyToManyField(Account, related_name="hospital_staff", blank=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)

    def patients(self):
        return Patient.objects.filter(hospital=self)

    def doctors(self):
        return Doctor.objects.filter(hospital=self)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    QUALIFICATION_CHOICES = [
        ("MD", "Doctor of Medicine"),
        ("DO", "Doctor of Osteopathic Medicine"),
        ("MBBS", "Bachelor of Medicine, Bachelor of Surgery"),
        ("MS", "Master of Surgery"),
        ("DNP", "Doctor of Nursing Practice"),
        ("PhD", "Doctor of Philosophy in Medical Science"),
        ("DPM", "Doctor of Podiatric Medicine"),
    ]
    uid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    qualification = models.CharField(max_length=50, choices=QUALIFICATION_CHOICES)
    specialization = models.CharField(max_length=255)

    hospital = models.ForeignKey(
        Hospital, on_delete=models.CASCADE, blank=True, null=True
    )

    def fullname(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name}"
    


class Patient(models.Model):
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]

    uid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )

    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, null=True, blank=True
    )

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.TextField()
    nationality = CountryField(null=True)

    patient_number = models.CharField(max_length=20, unique=True, blank=True)
    nhis_number = models.CharField(max_length=20, unique=True, blank=True)
    file_number = models.CharField(max_length=20, unique=True, blank=True)

    mobile_number = models.CharField(max_length=15)
    house_number = models.CharField(max_length=10, blank=True, null=True)

    emergency_contact_email = models.EmailField(unique=True)
    emergency_contact_mobile = models.CharField(max_length=15)

    height = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0)])
    weight = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0)])
    blood_group = models.CharField(max_length=5, blank=True)
    genotype = models.CharField(max_length=5, blank=True)

    hospital = models.ForeignKey(
        Hospital, on_delete=models.CASCADE, blank=True, null=True
    )

    date_of_open_file = models.DateField(auto_now_add=True)
    barcode = models.ImageField(upload_to='barcodes/', blank=True)

    @property
    def age(self):
        today = date.today()
        birth_date = self.date_of_birth
        age = (
            today.year
            - birth_date.year
            - ((today.month, today.day) < (birth_date.month, birth_date.day))
        )
        return age
    
    def save(self, *args, **kwargs):
        if not self.barcode:
            EAN = barcode.get_barcode_class('ean13')
            ean = EAN(f'{self.nhis_number}{self.patient_number}', writer=ImageWriter())
            buffer = BytesIO()
            ean.write(buffer)
            self.barcode.save(f'{self.last_name}.png', File(buffer), save=False)
        return super().save(*args, **kwargs)

    def fullname(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
