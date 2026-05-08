from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

from home.models import Department, Doctors
from .forms import BookingForm


from django.contrib.auth import authenticate, login, logout
from .forms import PatientRegisterForm, DoctorRegisterForm
from .models import Profile


from django.contrib.auth.decorators import login_required

from .models import Report


def index(request):
    if request.user.is_authenticated:
        if request.user.profile.role == 'doctor':
            return redirect('doctor_dashboard')
        else:
            return redirect('home')

    return redirect('login')

# Home page
@login_required
def home(request):
    return render(request, 'home.html')


# About page
@login_required
def about(request):
    return render(request, 'about.html')


# Contact page
@login_required
def contact(request):
    return render(request, 'contact.html')


# Departments page
@login_required
def departments(request):
    dept = Department.objects.all()
    return render(request, 'departments.html', {'dept': dept})


# Doctors page
@login_required
def doctors(request):
    docs = Doctors.objects.all()
    return render(request, 'doctors.html', {'docs': docs})


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


# Booking page (FINAL)
@login_required
def booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()

            # 📧 Email to Admin
            subject = f'New Appointment - {booking.patient_name}'
            message = f"""
New booking details:

Name: {booking.patient_name}
Email: {booking.patient_email}
Phone: {booking.patient_phone}
Doctor: {booking.doctor}
Date: {booking.appointment_date}
Time: {booking.appointment_time}
"""

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                ['kamalrajmanu@gmail.com'],  # 🔁 replace with your email
                fail_silently=False,
            )

            # 📧 Confirmation to Patient
            send_mail(
                "Appointment Confirmation",
                f"Hello {booking.patient_name}, your appointment with {booking.doctor} on {booking.appointment_date} is confirmed.",
                settings.EMAIL_HOST_USER,
                [booking.patient_email],
                fail_silently=False,
            )

            # ✅ Success message
            messages.success(request, "Appointment booked successfully!")

            return redirect('booking')

    else:
        form = BookingForm()

    return render(request, 'booking.html', {'form': form})



def patient_signup(request):
    form = PatientRegisterForm()

    if request.method == 'POST':
        form = PatientRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)   
            user.set_password(form.cleaned_data['password'])
            user.save()

            Profile.objects.create(user=user, role='patient')

            messages.success(request, "Patient account created successfully!")
            return redirect('login')

    return render(request, 'patient_signup.html', {'form': form})


def doctor_signup(request):
    form = DoctorRegisterForm()

    if request.method == 'POST':
        form = DoctorRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)   # ✅ FIX
            user.set_password(form.cleaned_data['password'])
            user.save()

            Profile.objects.create(user=user, role='doctor')

            messages.success(request, "Doctor account created successfully!")
            return redirect('login')

    return render(request, 'doctor_signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Safe profile access
            if hasattr(user, 'profile'):
                if user.profile.role == 'doctor':
                    return redirect('doctor_dashboard')
                else:
                    return redirect('patient_dashboard')
            else:
                messages.error(request, "Profile not found!")
                return redirect('login')

        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')




@login_required
def doctor_dashboard(request):
    return render(request, 'doctor_dashboard.html')

@login_required
def patient_dashboard(request):
    return render(request, 'patient_dashboard.html')




@login_required
def upload_report(request):
    if request.method == 'POST':
        file = request.FILES.get('report')   

        if file:
            Report.objects.create(
                patient=request.user,
                report=file
            )
            messages.success(request, "Report uploaded successfully!")
            return redirect('patient_dashboard')
        else:
            messages.error(request, "Please select a file")

    return render(request, 'upload_report.html')



@login_required
def view_reports(request):
    reports = Report.objects.all()
    return render(request, 'view_reports.html', {'reports': reports})

