from django.contrib import admin
from core.models import (
    MedicalHistory,
    LabResult,
    Treatment,
    Examination,
    AuditTrail,
    Appointment,
)

admin.site.register(MedicalHistory)
admin.site.register(LabResult)
admin.site.register(Treatment)
admin.site.register(Examination)
admin.site.register(AuditTrail)
admin.site.register(Appointment)
