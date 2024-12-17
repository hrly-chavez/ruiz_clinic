from django.shortcuts import render
from .models import *

# Create your views here.
def dashboard(request):
    return render(request, 'clinic/Dashboard/dashboard.html')

def appointment(request):
    appointments = Appointment.objects.select_related('patient_id').all()  # Select related patient data for better efficiency
    return render(request, 'clinic/Appointment/appointment.html', {'appointments': appointments})

def inventory(request):
    return render(request, 'clinic/Inventory/inventory.html')

def patient(request):
    return render(request, 'clinic/Patient/patient.html')

def sales(request):
    return render(request, 'clinic/Sales/sales.html')

def add_appointment(request):
    return render(request, 'clinic/Appointment/add_appointment.html')