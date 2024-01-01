from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from account.models import Account, Doctor, Hospital, Patient
from django.utils import timezone
from datetime import datetime


def signin(request):
    template = "account/signin.html"
    return render(request, template)


def signup(request):
    template = "account/signup.html"
    return render(request, template)


@login_required
def patient(request):
    template = "account/patient.html"
    account = Account.objects.get(user=request.user)
    patient = Patient.objects.get(account=account)
    context = {
        "account": account,
        "patient": patient,
    }
    return render(request, template, context)


def patient_signup(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]

        address = request.POST["address"]
        nationality = request.POST["nationality"]
        gender = request.POST["gender"]

        nhis_number = request.POST["nhis_number"]
        file_number = request.POST["file_number"]

        mobile_number = request.POST["mobile_number"]
        house_number = request.POST["house_number"]

        emergency_contact_email = request.POST["emergency_contact_email"]
        emergency_contact_mobile = request.POST["emergency_contact_mobile"]

        height = request.POST["height"]
        weight = request.POST["weight"]
        blood_group = request.POST["blood_group"]
        genotype = request.POST["genotype"]

        password = request.POST["password"]

        day = int(request.POST.get('day'))
        month = int(request.POST.get('month'))
        year = int(request.POST.get('year'))

        try:
            date_of_birth = datetime(year, month, day).date()
        except ValueError:
            date_of_birth = None

        user = User.objects.create(
            username=email, email=email, first_name=first_name, last_name=last_name
        )

        user.set_password(password)
        user.save()

        account = Account.objects.create(user=user, email=email, role="patient")

        patient = Patient.objects.create(
            account=account,
            first_name=first_name,
            last_name=last_name,
            address=address,
            nationality=nationality,
            gender=gender,
            nhis_number=nhis_number,
            file_number=file_number,
            mobile_number=mobile_number,
            house_number=house_number,
            emergency_contact_email=emergency_contact_email,
            emergency_contact_mobile=emergency_contact_mobile,
            height=height,
            weight=weight,
            blood_group=blood_group,
            genotype=genotype,
            date_of_birth=date_of_birth
        )

        auth.login(request, user)
        messages.success(request, "Patient Registration Successful!")

        return redirect("core:dashboard")
    else:
        template = "account/patient_signup.html"

        gender_list = Patient.GENDER_CHOICES

        context = {
            "gender_list": gender_list,
        }

        return render(request, template, context)


def doctor_signup(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        password = request.POST["password"]

        qualification = request.POST["qualification"]
        specialization = request.POST["specialization"]

        user = User.objects.create(
            username=email, email=email, first_name=first_name, last_name=last_name
        )

        user.set_password(password)
        user.save()

        account = Account.objects.create(
            user=user, email=email, role="healthcare_professional"
        )

        doctor = Doctor.objects.create(
            account=account,
            first_name=first_name,
            last_name=last_name,
            qualification=qualification,
            specialization=specialization,
        )
        auth.login(request, user)
        messages.success(request, "Doctor Registration Successful!")

        return redirect("core:dashboard")
    else:
        template = "account/doctor_signup.html"
        qualifications = Doctor.QUALIFICATION_CHOICES

        context = {
            "qualifications": qualifications,
        }

        return render(request, template, context)


def admin_signup(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        password = request.POST["password"]

        user = User.objects.create(
            username=email, email=email, first_name=first_name, last_name=last_name
        )

        user.set_password(password)
        user.save()

        account = Account.objects.create(user=user, email=email, role="administrator")

        auth.login(request, user)
        messages.success(request, "Admin Registration Successful!")

        return redirect("core:dashboard")
    else:
        template = "account/admin_signup.html"
        return render(request, template)


def patient_signin(request):
    if request.method == "POST":
        username = request.POST["email"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "Welcome back " + user.first_name)
            return redirect("core:dashboard")
        else:
            messages.error(request, "Invalid credentials. Please try again.")
            return redirect("account:patient_signin")
    else:
        template = "account/patient_signin.html"
        return render(request, template)


def doctor_signin(request):
    if request.method == "POST":
        username = request.POST["email"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "Welcome back " + user.first_name)
            return redirect("core:dashboard")
        else:
            messages.error(request, "Invalid credentials. Please try again.")
            return redirect("account:doctor_signin")
    else:
        template = "account/doctor_signin.html"
        return render(request, template)


def admin_signin(request):
    if request.method == "POST":
        username = request.POST["email"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "Welcome back " + user.first_name)
            return redirect("core:dashboard")
        else:
            messages.error(request, "Invalid credentials. Please try again.")
            return redirect("account:admin_signin")
    else:
        template = "account/admin_signin.html"
        return render(request, template)
