from django.contrib import admin
from account.models import Account, Doctor, Hospital, Patient

admin.site.register(Account)
admin.site.register(Patient)
admin.site.register(Hospital)
admin.site.register(Doctor)
