

from django.shortcuts import render,redirect
from .forms import *
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.utils.timezone import localtime
from django.utils import timezone
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
# Create your views here.
#_____________________________________DASHBOARD__________________________________________________________

def dashboard(request):
    # Get today's date and current time
    today = timezone.localdate()  # Get the current local date
    current_time = timezone.localtime(timezone.now()).time()  # Get the current local time

    # Filter appointments for today with times greater than or equal to the current time
    appointments = Appointment.objects.filter(app_date=today, app_time__gte=current_time).order_by('app_time')

    return render(request, 'clinic/Dashboard/dashboard.html', {'appointments': appointments})

#_____________________________________APPOINTMENT__________________________________________________________

# def appointment(request):
#     return render(request, 'clinic/Appointment/appointment.html')

def appointment(request):
    # Fetch all appointment dates from the database
    appointments = Appointment.objects.all().values('app_date')

    # Convert to datetime and adjust for time zone
    appointment_dates = [
        (datetime.combine(appointment['app_date'], datetime.min.time())  # Combine date with a dummy time
         .astimezone(timezone.get_current_timezone()).date().isoformat())  # Convert to local time zone and then to string
        for appointment in appointments
    ]

    context = {
        'appointment_dates': appointment_dates,  # Pass the dates to the template
    }
    return render(request, 'clinic/Appointment/appointment.html', context)

def view_appointment(request):
    date_str = request.GET.get('date')  # Get the selected date from the query parameters
    selected_date = None
    formatted_date = "Unknown Date"
    appointments = []
    is_past_date = False
    is_past_time = False
    is_sunday = False

    if date_str:
        try:
            selected_date = datetime.strptime(date_str, "%Y-%m-%d")  # Convert to a datetime object
            formatted_date = selected_date.strftime("%B %d, %Y")  # Format the date as 'Month Day, Year'

            # Get today's date and time
            now = datetime.now()
            current_time = now.time()

            # Check if the selected date is in the past
            if selected_date.date() < now.date():  # Compare only the date part
                is_past_date = True
            elif selected_date.date() == now.date():
                # Check if the current time is outside business hours (8:00 AM - 5:00 PM)
                start_time = datetime.strptime("08:00", "%H:%M").time()
                end_time = datetime.strptime("17:00", "%H:%M").time()

                if current_time < start_time or current_time > end_time:
                    is_past_time = True

            # Check if the selected date is a Sunday
            if selected_date.weekday() == 6:  # 6 represents Sunday
                is_sunday = True

            # Get all appointments for the selected date and sort by appointment time
            appointments = Appointment.objects.filter(app_date=selected_date).order_by('app_time')

            # Add a flag to each appointment to indicate if it occurs in the past
            for appointment in appointments:
                appointment_time = datetime.combine(selected_date, appointment.app_time)
                appointment.is_past = appointment_time < now  # Compare with the current datetime

        except ValueError:
            pass  # Handle invalid date strings gracefully

    # Create the form instance and pass the selected date to the form's `app_date` field
    form = AppointmentForm(initial={'app_date': selected_date})

    context = {
        'formatted_date': formatted_date,  # Pass the formatted date
        'selected_date': selected_date,   # Optionally, pass the raw datetime object
        'appointments': appointments,      # Pass the sorted appointments to the template
        'form': form,                      # Pass the form to the template
        'is_past_date': is_past_date,      # Flag to check if it's a past date
        'is_past_time': is_past_time,      # Flag to check if it's a past time for today
        'is_sunday': is_sunday,            # Pass the is_sunday flag to the template
    }

    return render(request, 'clinic/Appointment/view_appointment.html', context)


def create_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to the same date's view after creation
            return redirect(f"{reverse('view_appointment')}?date={form.cleaned_data['app_date']}")
    else:
        form = AppointmentForm()

    return render(request, 'clinic/Appointment/create_appointment.html', {'form': form})

def edit_appointment(request):
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        appointment = Appointment.objects.get(pk=appointment_id)
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()

            # After saving the appointment, we need to ensure that the appointments are still sorted by time
            # Redirect to the same date's view after update
            return redirect(f"{reverse('view_appointment')}?date={appointment.app_date}")
    else:
        return redirect('view_appointment')  # Fallback in case of GET request
    
@csrf_exempt
def delete_appointment(request):
    if request.method == 'POST':
        try:
            # Get the appointment_id from the POST data
            appointment_id = request.POST.get('appointment_id')

            if not appointment_id:
                return JsonResponse({'success': False, 'error': 'Appointment ID is missing'})

            # Retrieve the appointment, using get_object_or_404 for better error handling
            appointment = get_object_or_404(Appointment, pk=appointment_id)

            # Delete the appointment
            appointment.delete()

            return JsonResponse({'success': True})
        
        except Appointment.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Appointment not found'})
        
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

# def appointment(request):
#     if request.method == 'POST':
#         # Handle form submission from the modal
#         form = AppointmentForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('appointment')  # Redirect to the same page after saving
#     else:
#         # Display the page with appointments
#         form = AppointmentForm()

#     # Fetch all appointments sorted by date and time
#     appointments = Appointment.objects.all().order_by('app_date', 'app_time')
#     return render(request, 'clinic/Appointment/appointment.html', {'form': form, 'appointments': appointments})

# def get_appointments(request):
#     # Fetch appointments sorted by date and time
#     appointments = Appointment.objects.all().order_by('app_date', 'app_time')
#     events = []
#     for appointment in appointments:
#         events.append({
#             'title': f"{appointment.app_fname} {appointment.app_lname}",
#             'start': f"{appointment.app_date}T{appointment.app_time}",
#             'status': appointment.app_status,  # Custom field to handle color logic
#         })
#     return JsonResponse(events, safe=False)
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