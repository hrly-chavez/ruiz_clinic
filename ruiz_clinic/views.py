from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, 'clinic/Dashboard/dashboard.html')

def appointment(request):
    return render(request, 'clinic/Appointment/appointment.html')

def inventory(request):
    return render(request, 'clinic/Inventory/inventory.html')

def patient(request):
    return render(request, 'clinic/Patient/patient.html')

def sales(request):
    return render(request, 'clinic/Sales/sales.html')