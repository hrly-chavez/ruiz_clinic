

from django.shortcuts import render,redirect
from .forms import *
# Create your views here.
#_____________________________________DASHBOARD__________________________________________________________

def dashboard(request):
    return render(request, 'clinic/Dashboard/dashboard.html')

#_____________________________________APPOINTMENT__________________________________________________________

def appointment(request):
    return render(request, 'clinic/Appointment/appointment.html')

def add_appointment(request):
    return render(request, 'clinic/Appointment/add_appointment.html')
#_____________________________________INVENTORY__________________________________________________________

def inventory(request):
    items = Item.objects.all()  # Fetch all items from the database
    return render(request, 'clinic/Inventory/inventory.html', {'items': items})

def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory')  
    else:
        form = ItemForm()
    return render(request, 'clinic/Inventory/add_item.html', {'form': form})

#_________________________________________PATIENT________________________________________________________

def patient(request):
    return render(request, 'clinic/Patient/patient.html')

#_____________________________________SALES__________________________________________________________
def sales(request):
    return render(request, 'clinic/Sales/sales.html')