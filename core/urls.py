from django.urls import path, include
from . import views

app_name = "core"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("create-hospital/", views.create_hospital, name="create_hospital"),
    path("hospital/<uid>/", views.view_hospital, name="view_hospital"),
    path("add-treatment/", views.add_treatment, name="add_treatment"),
    path("treatments/", views.treatments, name="treatments"),
    path("treatment/<uid>/", views.view_treatment, name="treatment"),
    path("add-lab-result/", views.add_lab_result, name="add_lab_result"),
    path("lab-results/", views.view_lab_results, name="lab_results"),
    path("lab-result/<uid>/", views.view_lab_result, name="lab_result"),
    path("add-medical-history/", views.add_medical_history, name="add_medical_history"),
    path("medical-history/<uid>/", views.view_medical_history, name="view_medical_history"),
    path("medical-history-all/", views.view_all_medical_history, name="view_all_medical_history"),
    path("add-examination/", views.add_examination, name="add_examination"),
    path("examination/<uid>", views.view_examination, name="view_examination"),
    path("examinations/", views.my_examinations, name="examinations"),
    path("create-appointment/", views.create_appointment, name="create_appointment"),
    path("appointments/", views.appointments, name="appointments"),
    path("appointment/<uid>/", views.appointment, name="appointment"),
]