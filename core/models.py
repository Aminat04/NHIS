from django.db import models
from django.contrib.auth.models import User
from account.models import Account, Doctor, Patient, Hospital
import uuid


class MedicalHistory(models.Model):
    DISEASE_CHOICES = [
        ("CVD", "Cardiovascular Disease"),
        ("DIAB", "Diabetes"),
        ("CANC", "Cancer"),
        ("INF", "Infectious Disease"),
        ("NEURO", "Neurological Disorder"),
        ("RESPIR", "Respiratory Disorder"),
        ("GI", "Gastrointestinal Disease"),
        ("ORTH", "Orthopedic Condition"),
        ("MENTAL", "Mental Health Disorder"),
        ("ENDO", "Endocrine Disorder"),
        ("RENAL", "Renal Disease"),
        ("HEMATO", "Hematological Disorder"),
        ("AUTOIMMUNE", "Autoimmune Disorder"),
        ("DERMA", "Dermatological Condition"),
        ("ALLERGIC", "Allergic Reaction"),
        ("GENETIC", "Genetic Disorder"),
        ("EYE", "Eye Disease"),
        ("EAR", "Ear, Nose, and Throat Disorder"),
        ("OBGYN", "Obstetric and Gynecological Condition"),
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    medical_condition = models.TextField()
    medications = models.TextField()
    disease = models.CharField(max_length=50, choices=DISEASE_CHOICES)

    def __str__(self):
        return self.patient


class LabResult(models.Model):
    uid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    test_name = models.CharField(max_length=255)
    result = models.TextField()
    reference_range = models.CharField(max_length=255)

    def __str__(self):
        return f"Lab Result for {self.patient}"


class Treatment(models.Model):
    uid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, blank=True, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    date_started = models.DateField()
    date_ended = models.DateField()
    is_started = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    added = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Treatement for {self.patient}"


class Examination(models.Model):
    DISEASE_CHOICES = [
        ("CVD", "Cardiovascular Disease"),
        ("DIAB", "Diabetes"),
        ("CANC", "Cancer"),
        ("INF", "Infectious Disease"),
        ("NEURO", "Neurological Disorder"),
        ("RESPIR", "Respiratory Disorder"),
        ("GI", "Gastrointestinal Disease"),
        ("ORTH", "Orthopedic Condition"),
        ("MENTAL", "Mental Health Disorder"),
        ("ENDO", "Endocrine Disorder"),
        ("RENAL", "Renal Disease"),
        ("HEMATO", "Hematological Disorder"),
        ("AUTOIMMUNE", "Autoimmune Disorder"),
        ("DERMA", "Dermatological Condition"),
        ("ALLERGIC", "Allergic Reaction"),
        ("GENETIC", "Genetic Disorder"),
        ("EYE", "Eye Disease"),
        ("EAR", "Ear, Nose, and Throat Disorder"),
        ("OBGYN", "Obstetric and Gynecological Condition"),
    ]
    uid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    examiner = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="examinations"
    )
    history_of_present_illness = models.TextField()
    physical_examination = models.TextField()
    assessment_and_plan = models.TextField()
    orders_and_prescriptions = models.TextField()
    progress_note = models.TextField()
    findings = models.TextField()
    disease = models.CharField(max_length=50, choices=DISEASE_CHOICES)

    def __str__(self):
        return f"Examination by {self.examiner}"


class Appointment(models.Model):
    uid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    title = models.CharField(max_length=50)
    description = models.TextField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    scheduled_time = models.DateTimeField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class AuditTrail(models.Model):
    ACTION_CHOICES = (
        ("login", "Login"),
        ("data_access", "Data Access"),
        ("modification", "Modification"),
    )
    uid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    action = models.CharField(max_length=30, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
