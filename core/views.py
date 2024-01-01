from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from account.models import Account, Doctor, Hospital, Patient
from core.models import (
    MedicalHistory,
    LabResult,
    Treatment,
    Examination,
    AuditTrail,
    Appointment,
)
from dateutil.parser import parse


@login_required
def dashboard(request):
    user = request.user
    account = Account.objects.get(user=user)
    if account.role == "patient":
        patient = Patient.objects.get(account=account)
        medical_history = MedicalHistory.objects.filter(patient=patient)
        lab_results = LabResult.objects.filter(patient=patient)
        treatments = Treatment.objects.filter(patient=patient)
        examinations = Examination.objects.filter(patient=patient)
        appointments = Appointment.objects.filter(patient=patient)
        
        template = "core/dashboard.html"
        
        context = {
            "account": account,
            "examinations": examinations,
            "treatments": treatments,
            "medical_history": medical_history,
            "lab_results": lab_results,
            "appointments": appointments,
        }
    elif account.role == "healthcare_professional":
        template = "core/doctor_dashboard.html"
        
        doctor = Doctor.objects.get(account=account)
        patients = Patient.objects.filter(hospital=doctor.hospital)
        treatments = Treatment.objects.filter(doctor=doctor)
        examinations = Examination.objects.filter(examiner=doctor)
        appointments = Appointment.objects.filter(doctor=doctor)

        context = {
            "account": account,
            "doctor": doctor,
            "patients": patients,
            "examinations": examinations,
            "treatments": treatments,
            "appointments": appointments,
        }
    else:
        hospitals = Hospital.objects.all()
        doctors = Doctor.objects.all()
        patients = Patient.objects.all()

        template = "core/admin_dashboard.html"

        context = {
            "account": account,
            "doctors": doctors,
            "patients": patients,
            "hospitals": hospitals,
        }
    return render(request, template, context)


@login_required
def create_hospital(request):
    account = Account.objects.get(user=request.user)

    if request.method == "POST":
        name = request.POST["name"]
        address = request.POST["address"]
        city = request.POST["city"]
        state = request.POST["state"]
        zip_code = request.POST["zip_code"]

        hospital = Hospital.objects.create(
            name=name,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            admin=account,
        )

        return redirect("core:hospital", uid=hospital.uid)

    else:
        template = "core/create_hospital.html"
        context = {
            "account": account,
        }
        return render(request, template)


@login_required
def view_hospital(request, uid):
    account = Account.objects.get(user=request.user)
    hospital = Hospital.objects.get(uid=uid)
    template = "core/hospital.html"
    context = {
        "hospital": hospital,
        "account": account,
    }
    return render(request, template, context)


@login_required
def add_treatment(request):
    account = Account.objects.get(user=request.user)

    if request.method == "POST":
        name = request.POST["name"]
        description = request.POST["description"]
        date_started = request.POST["date_started"]
        date_ended = request.POST["date_ended"]

        date_started = parse(date_started)
        date_ended = parse(date_ended)

        treatment = Treatment.objects.create(
            name=name,
            description=description,
            date_started=date_started,
            date_ended=date_ended,
        )

        if "is_started" in request.POST:
            treatment.is_started = True
        if "is_completed" in request.POST:
            treatment.is_completed = True

        if account.role == "patient":
            patient = Patient.objects.get(account=account)
            treatment.patient = patient
            doctor_id = request.POST["doctor_id"]
            p_account = Account.objects.get(email=doctor_id)
            doctor = Doctor.objects.get(account=p_account)
            treatment.doctor = doctor

        else:
            account.role == "healthcare_professional"
            doctor = Doctor.objects.get(account=account)
            treatment.doctor = doctor
            patient_id = request.POST["patient_id"]
            p_account = Account.objects.get(email=patient_id)
            patient = Patient.objects.get(account=p_account)
            treatment.patient = patient

        if "patient_number" in request.POST:
            patient_number = request.POST["patient_number"]
            patient = Patient.objects.get(patient_number=patient_number)
            treatment.patient

        treatment.save()
        return redirect("core:treatment", uid=treatment.uid)

    else:
        template = "core/add_treatment.html"
        patients = Patient.objects.all()
        doctors = Doctor.objects.all()

        patients = [{'title': x.account.email} for x in patients]
        doctors = [{'title': x.account.email} for x in doctors]

        context = {
            "account": account,
            "doctors": doctors,
            "patients": patients,
        }
        return render(request, template, context)


@login_required
def treatments(request):
    account = Account.objects.get(user=request.user)
    patient = Patient.objects.get(account=account)
    treatments = Treatment.objects.filter(patient=patient)
    template = "core/treatments.html"
    context = {
        "treatments": treatments,
        "account": account,
        "patient": patient,
    }
    return render(request, template, context)


@login_required
def view_treatment(request, uid):
    account = Account.objects.get(user=request.user)
    treatment = Treatment.objects.get(uid=uid)
    template = "core/treatment.html"
    context = {
        "treatment": treatment,
        "account": account,
    }
    return render(request, template, context)



@login_required
def add_lab_result(request):
    account = Account.objects.get(user=request.user)

    if request.method == "POST":
        patient_id = request.POST["patient_id"]

        date = request.POST["date"]
        test_name = request.POST["test_name"]
        result = request.POST["result"]
        #reference_range = request.POST["reference_range"]

        p_account = Account.objects.get(email=patient_id)
        patient = Patient.objects.get(account=p_account)

        date = parse(date)

        lab_result = LabResult.objects.create(
            patient=patient,
            date=date,
            test_name=test_name,
            result=result,
            reference_range="Not available"
        )
        lab_result.save()
        return redirect("core:lab_result", uid=lab_result.uid)
    else:
        patients = Patient.objects.all()
        patients = [{'title': x.account.email} for x in patients]
        context = {
            "account": account,
            "patients": patients
        }
        template = "core/add_lab_result.html"
        return render(request, template, context)


@login_required
def view_lab_results(request):
    account = Account.objects.get(user=request.user)
    patient = Patient.objects.get(account=account)
    lab_results = LabResult.objects.filter(patient=patient)

    template = "core/lab_results.html"
    context = {
        "account": account,
        "lab_results": lab_results,
        "patient": patient,
    }
    return render(request, template, context)


@login_required
def view_lab_result(request, uid):
    account = Account.objects.get(user=request.user)
    lab_result = LabResult.objects.get(uid=uid)

    template = "core/lab_result.html"
    context = {
        "account": account,
        "lab_result": lab_result,
    }
    return render(request, template, context)


@login_required
def add_medical_history(request):
    account = Account.objects.get(user=request.user)
    if request.method == "POST":
        medical_condition = request.POST["medical_condition"]
        medications = request.POST["medications"]
        disease = request.POST["disease"]
        date = request.POST["date"]
        date = parse(date)
        patient = Patient.objects.get(account=account)

        medical_history = MedicalHistory.objects.create(
            medical_condition=medical_condition,
            medications=medications,
            disease=disease,
            date=date,
            patient=patient,
        )
        medical_history.save()

        return redirect("core:view_medical_history", uid=medical_history.id)

    else:
        context = {
            "diseases": MedicalHistory.DISEASE_CHOICES,
            "account": account,
        }
        template = "core/add_medical_history.html"
        return render(request, template, context)


@login_required
def view_medical_history(request, uid):
    template = "core/medical_history.html"
    account = Account.objects.get(user=request.user)
    patient = Patient.objects.get(account=account)
    medical_history = MedicalHistory.objects.get(id=uid)

    context = {
        "account": account,
        "patient": patient,
        "medical_history": medical_history,
    }
    return render(request, template, context)


@login_required
def view_all_medical_history(request):
    template = "core/all_medical_history.html"
    account = Account.objects.get(user=request.user)
    patient = Patient.objects.get(account=account)
    all_medical_history = MedicalHistory.objects.filter(patient=patient)

    context = {
        "account": account,
        "patient": patient,
        "all_medical_history": all_medical_history,
    }
    return render(request, template, context)


@login_required
def add_examination(request):
    account = Account.objects.get(user=request.user)
    if request.method == "POST":
        patient_id = request.POST["patient_id"]
        history_of_present_illness = request.POST["history_of_present_illness"]
        physical_examination = request.POST["physical_examination"]
        assessment_and_plan = request.POST["assessment_and_plan"]
        orders_and_prescriptions = request.POST["orders_and_prescriptions"]
        progress_note = request.POST["progress_note"]
        findings = request.POST["findings"]
        disease = request.POST["disease"]

        p_account = Account.objects.get(email=patient_id)
        patient = Patient.objects.get(account=p_account)

        doctor = Doctor.objects.get(account=account)
        
        examination = Examination.objects.create(
            examiner=doctor,
            patient=patient,
            history_of_present_illness=history_of_present_illness,
            physical_examination=physical_examination,
            assessment_and_plan=assessment_and_plan,
            orders_and_prescriptions=orders_and_prescriptions,
            progress_note=progress_note,
            findings=findings,
            disease=disease,
        )
        examination.save()

        return redirect("core:view_examination", uid=examination.uid)
    else:
        diseases = Examination.DISEASE_CHOICES
        patients = Patient.objects.all()
        context = {
            "account": account,
            "diseases": diseases,
            "patients": [{ "title": p.account.email} for p in patients],
        }
        template = "core/add_examination.html"
        return render(request, template, context)


@login_required
def view_examination(request, uid):
    account = Account.objects.get(user=request.user)
    examination = Examination.objects.get(uid=uid)

    context = {
        "account": account,
        "examination": examination,
    }
    template = "core/examination.html"
    return render(request, template, context)


@login_required
def my_examinations(request):
    account = Account.objects.get(user=request.user)
    if account.role == "patient":
        patient = Patient.objects.get(account=account)
        examinations = Examination.objects.filter(patient=patient)
        context = {
            "account": account,
            "examinations": examinations,
            "patient": patient,
        }
    else:
        doctor = Doctor.objects.get(account=account)
        examinations = Examination.objects.filter(examiner=doctor)
        context = {
            "account": account,
            "examinations": examinations,
            "doctor": doctor,
        }
    template = "core/examinations.html"
    return render(request, template, context)


@login_required
def create_appointment(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        doctor = request.POST["doctor"]
        doctor = Account.objects.get(email=doctor)
        doctor = Doctor.objects.get(account=doctor)
        patient = Account.objects.get(user=request.user)
        patient = Patient.objects.get(account=patient)
        scheduled_time = request.POST["date"]
        scheduled_time = parse(scheduled_time)

        appointment = Appointment.objects.create(
            title=title,
            description=description,
            doctor=doctor,
            patient=patient,
            scheduled_time=scheduled_time
        )

        return redirect("core:appointment", appointment.uid)

    else:
        template = "core/create_appointment.html"
        account = Account.objects.get(user=request.user)
        doctors = Doctor.objects.all()
        context = {
            "account": account,
            "doctors": [{"title": doctor.account.email} for doctor in doctors],
        }
        return render(request, template, context)


@login_required
def appointment(request, uid):
    appointment = Appointment.objects.get(uid=uid)
    account = Account.objects.get(user=request.user)
    context = {
        "appointment": appointment,
        "account": account,
    }
    template = "core/appointment.html"
    return render(request, template, context)


@login_required
def appointments(request):
    account = Account.objects.get(user=request.user)
    patient = Patient.objects.get(account=account)
    appointments = Appointment.objects.filter(patient=patient)
    
    context = {
        "appointments": appointments,
        "account": account,
        "patient": patient,
    }
    template = "core/appointments.html"
    return render(request, template, context)