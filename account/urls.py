from django.urls import path, include
from . import views

app_name = "account"

urlpatterns = [
    path("signin/", views.signin, name="signin"),
    path("signup/", views.signup, name="signup"),
    path("patient/", views.patient, name="patient"),
    path("signup/patient/", views.patient_signup, name="patient_signup"),
    path("signup/doctor/", views.doctor_signup, name="doctor_signup"),
    path("signup/admin/", views.admin_signup, name="admin_signup"),
    path("signin/patient/", views.patient_signin, name="patient_signin"),
    path("signin/doctor/", views.doctor_signin, name="doctor_signin"),
    path("signin/admin/", views.admin_signin, name="admin_signin"),
]
