from django.shortcuts import render,redirect, get_object_or_404
from .forms import *
from datetime import datetime, timedelta
from django.http import HttpResponse, JsonResponse,Http404 ,HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db.models import Q, Prefetch
import matplotlib
matplotlib.use('Agg')
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import json
import random
import requests
from django.conf import settings

from django.utils.timezone import localtime, now, make_aware, is_aware, localdate
from pytz import timezone
import smtplib
from email.mime.text import MIMEText
from django.contrib.auth import logout

PH_TZ = timezone("Asia/Manila")

from functools import wraps

def login_required(view_func):
    @wraps(view_func)  # ✅ Keeps function metadata
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            messages.error(request, "You need to log in first.")  # Show message
            return redirect('login')  # ✅ Redirect to login page
        return view_func(request, *args, **kwargs)
    return wrapper


# Temporary storage for OTPs (consider using a session for better security)
RESET_OTP_STORAGE = {}
ADMIN_EMAIL = "carataojoegie@gmail.com"  # The only email receiving OTPs

# Generate a random OTP
def generate_otp():
    return str(random.randint(100000, 999999))

# Function to send OTP only to ADMIN_EMAIL
def send_otp_email(otp):
    sender_email = "carataojoegie@gmail.com"  # Use your Gmail
    sender_password = "svdd pqan vcbh tagf"  # Use Gmail App Password
    subject = "Your Secure OTP"
    body = f"Your OTP is: {otp}. Share it only with authorized employees."

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = ADMIN_EMAIL

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, ADMIN_EMAIL, msg.as_string())
        server.quit()
        print(f"OTP email sent to {ADMIN_EMAIL} successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

def forgot_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')

        try:
            user = Account.objects.get(account_username=username)  # Find user by username
            otp = generate_otp()
            RESET_OTP_STORAGE[username] = otp  # Store OTP linked to the username
            send_otp_email(otp)  # Send OTP to ADMIN_EMAIL
            request.session['reset_username'] = username  # Store username in session
            messages.success(request, "OTP has been sent to the admin. Contact them for the code.")
            return redirect('verify_reset_otp')

        except Account.DoesNotExist:
            messages.error(request, "Username not found. Please enter a valid account username.")

    return render(request, 'clinic/Login/forgot_password.html')


def verify_reset_otp(request):
    if request.method == 'POST':
        username = request.session.get('reset_username')  # Retrieve stored username
        entered_otp = request.POST.get('otp')

        if username in RESET_OTP_STORAGE and RESET_OTP_STORAGE[username] == entered_otp:
            return redirect('reset_password')  # Redirect to reset password form
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, 'clinic/Login/verify_reset_otp.html')

def reset_password(request):
    if request.method == 'POST':
        username = request.session.get('reset_username')  # Get stored username
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('reset_password')

        try:
            user = Account.objects.get(account_username=username)  # Get user by username
            user.account_password = new_password  # Hash in production
            user.save()
            del request.session['reset_username']  # Remove session data after reset
            messages.success(request, "Password reset successful! You can now log in.")
            return redirect('login')

        except Account.DoesNotExist:
            messages.error(request, "Error resetting password. Please try again.")

    return render(request, 'clinic/Login/reset_password.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if Account.objects.filter(account_username=username).exists():
            messages.error(request, 'Username already exists. Please choose another.')
        else:
            otp = generate_otp()
            print(f"Generated OTP: {otp}")  # Debugging
            RESET_OTP_STORAGE['signup_otp'] = otp  # Store OTP temporarily
            send_otp_email(otp)  # Send OTP to ADMIN_EMAIL
            request.session['pending_user'] = {'username': username, 'password': password}
            return redirect('verify_otp')  # Redirect to OTP verification page

    return render(request, 'clinic/Signup/signup.html')

def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')

        if 'signup_otp' in RESET_OTP_STORAGE and RESET_OTP_STORAGE['signup_otp'] == entered_otp:
            user_data = request.session.get('pending_user')
            if user_data:
                Account.objects.create(
                    account_username=user_data['username'],
                    account_password=user_data['password']  # Hash this in production
                )
                del RESET_OTP_STORAGE['signup_otp']  # Remove OTP after successful registration
                del request.session['pending_user']  # Clear session
                messages.success(request, 'Registration successful! You can now log in.')
                return redirect('login')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')

    return render(request, 'clinic/Signup/verify_otp.html')




#______________________________________LOGIN___________________________________________________________
@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = Account.objects.get(account_username=username, account_password=password)
            
            # ✅ Store user ID in session
            request.session['user_id'] = user.account_id  # Store primary key
            request.session['username'] = user.account_username  # Store username (optional)

            messages.success(request, "Login successful!")
            return redirect('dashboard')  # ✅ Now it will redirect properly
        except Account.DoesNotExist:
            messages.error(request, 'Invalid username or password. Please try again.')

    return render(request, "clinic/Login/login.html")

#_____________________________________DASHBOARD__________________________________________________________
# @login_required
def dashboard(request):
    auto_cancel_appointments(request)
    # Get the selected date from the request or default to today
    selected_date_str = request.GET.get('selected_date')
    
    if selected_date_str:
        try:
            # ✅ Correctly parse the date string
            selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
        except ValueError:
            selected_date = localdate()  # ✅ Ensure timezone-aware date
    else:
        selected_date = localdate()  # ✅ Ensure timezone-aware date

    # Filter appointments for the selected date (adjust timezone if needed)
    appointments = Appointment.objects.filter(app_date=selected_date).order_by('app_time')

    # Query for items with low stock
    low_stock_items = Item.objects.filter(item_quantity__lt=3)

    return render(request, 'clinic/Dashboard/dashboard.html', {
        'appointments': appointments,
        'selected_date': selected_date,  # Ensure it's timezone-aware
        'low_stock_items': low_stock_items,  # Pass low stock items
    })


# @login_required
@csrf_exempt
def cancel_appointment(request):
    if request.method == 'POST':
        try:
            # Parse JSON data
            data = json.loads(request.body)
            appointment_id = data.get('appointment_id')

            if not appointment_id:
                return JsonResponse({'success': False, 'error': 'Appointment ID is missing'})

            # Retrieve the appointment and update its status to "Cancelled"
            appointment = get_object_or_404(Appointment, pk=appointment_id)
            appointment.app_status = 'Cancelled'
            appointment.save()

            # Return success message
            return JsonResponse({'success': True, 'message': 'Appointment cancelled successfully'})
        except Appointment.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Appointment not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

# @login_required
@csrf_exempt
def update_appointment_status(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            appointment_id = data.get('appointment_id')  # ID passed from frontend
            next_status = data.get('next_status')  # Next status to update

            # Retrieve the appointment using the correct field name
            appointment = Appointment.objects.get(app_id=appointment_id)
            appointment.app_status = next_status
            appointment.save()

            return JsonResponse({'success': True, 'new_status': next_status})
        except Appointment.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Appointment not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})

# @login_required
def generate_wordcloud(request):
    try:
        # Fetch purchased item data and aggregate frequencies
        purchases = Purchased_Item.objects.select_related('item_code__item_category_id').all()
        item_counts = {}

        for purchase in purchases:
            if purchase.item_code:  # Ensure item_code is not None
                # Use item category and brand to generate key
                item_category = (
                    purchase.item_code.item_category_id.item_category_name
                    if purchase.item_code.item_category_id else "Unknown Category"
                )
                item_name = f"{item_category} {purchase.item_code.item_brand}"
                item_counts[item_name] = item_counts.get(item_name, 0) + 1  # Increment count for each purchase
            else:
                # Handle cases where item_code is NULL
                item_counts["Unknown Item"] = item_counts.get("Unknown Item", 0) + 1

        if not item_counts:
            item_counts = {"No Data Available": 1}  # Prevent word cloud errors if no data exists

        # Generate the word cloud
        wordcloud = WordCloud(width=800, height=200, background_color="white").generate_from_frequencies(item_counts)

        # Render the word cloud to an image
        buffer = io.BytesIO()
        plt.figure(figsize=(10, 5), dpi=100)
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.savefig(buffer, format="png")
        plt.close()
        buffer.seek(0)

        return HttpResponse(buffer, content_type="image/png")
    except Exception as e:
        print(f"Error generating word cloud: {e}")
        return HttpResponse("Error generating word cloud", content_type="text/plain")
    
#_____________________________________APPOINTMENT__________________________________________________________
# @login_required
def appointment(request):
    # Fetch all appointment dates from the database
    appointments = Appointment.objects.all().values('app_date')

    # Ensure all appointment dates are in PHT
    appointment_dates = [
        appointment['app_date'].isoformat()  # Convert to string in YYYY-MM-DD format
        for appointment in appointments
    ]

    context = {
        'appointment_dates': appointment_dates,  # Pass corrected dates to the template
    }
    return render(request, 'clinic/Appointment/appointment.html', context)

# @login_required
def view_appointment(request):
    # ✅ Ensure `auto_cancel_appointments` is correctly called
    auto_cancel_appointments(request)

    date_str = request.GET.get('date')
    search_query = request.GET.get('search', '')

    selected_date = None
    formatted_date = "Unknown Date"
    appointments = []
    is_past_date = False
    is_past_time = False
    is_sunday = False

    if date_str:
        try:
            # ✅ Convert date string to a date object (no timezone issues)
            selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            formatted_date = selected_date.strftime("%B %d, %Y")

            # ✅ Use `localtime(now())` instead of `now.localtime()`
            now_pht = localtime(now())  # Use Philippine time
            current_time = now_pht.time()

            if selected_date < now_pht.date():
                is_past_date = True
            elif selected_date == now_pht.date():
                start_time = datetime.strptime("08:00", "%H:%M").time()
                end_time = datetime.strptime("17:00", "%H:%M").time()

                if current_time < start_time or current_time > end_time:
                    is_past_time = True

            if selected_date.weekday() == 6:
                is_sunday = True

            # ✅ Fetch appointments, ensuring correct timezone handling
            appointments = Appointment.objects.filter(app_date=selected_date)

            if search_query:
                appointments = appointments.filter(app_fname__icontains=search_query)

            # ✅ Convert each appointment's time to Philippine timezone
            for appointment in appointments:
                appointment.app_time = localtime(
                    make_aware(datetime.combine(selected_date, appointment.app_time))
                ).time()

        except ValueError:
            pass  

    form = AppointmentForm(initial={'app_date': selected_date})

    context = {
        'formatted_date': formatted_date,
        'selected_date': selected_date,
        'appointments': appointments,
        'form': form,
        'is_past_date': is_past_date,
        'is_past_time': is_past_time,
        'is_sunday': is_sunday,
        'search_query': search_query,
    }

    return render(request, 'clinic/Appointment/view_appointment.html', context)

# @login_required
def create_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.app_date = request.POST.get('app_date')  # Get date from hidden input
            appointment.app_status = 'Waiting'  # Default status

            # Convert date and time to datetime object
            appointment_date = datetime.strptime(appointment.app_date, '%Y-%m-%d').date()
            appointment_time = form.cleaned_data['app_time']
            appointment_start = datetime.combine(appointment_date, appointment_time)
            appointment_end = appointment_start + timedelta(minutes=15)  # Block 15 minutes after
            appointment_start_buffer = appointment_start - timedelta(minutes=14)  # Prevent booking too close

            now = datetime.now()
            if appointment_start < now:
                messages.error(request, "Cannot create an appointment for a past time.")
                return redirect(f"{reverse('view_appointment')}?date={appointment.app_date}")

            # Restrict appointment time between 6:00 AM and 5:45 PM
            earliest_time = datetime.combine(appointment_date, datetime.strptime('06:00', '%H:%M').time())
            latest_time = datetime.combine(appointment_date, datetime.strptime('17:45', '%H:%M').time())

            if not (earliest_time <= appointment_start <= latest_time):
                messages.error(request, "Appointments can only be scheduled between 6:00 AM and 5:45 PM.")
                return redirect(f"{reverse('view_appointment')}?date={appointment.app_date}")

            # Strictly enforce 15-minute slot restriction, excluding "Cancelled" appointments
            overlapping_appointments = Appointment.objects.filter(
                app_date=appointment_date,
                app_status__in=['Waiting', 'Ongoing', 'Done']  # Exclude "Cancelled" appointments
            ).filter(
                app_time__gte=appointment_start_buffer.time(),
                app_time__lt=appointment_end.time()
            )

            if overlapping_appointments.exists():
                messages.error(request, "This appointment time is already taken. Please choose another time.")
                return redirect(f"{reverse('view_appointment')}?date={appointment.app_date}")

            # Save the appointment
            appointment.save()
            messages.success(request, "Appointment created successfully.")
            return redirect(f"{reverse('view_appointment')}?date={appointment.app_date}")
    else:
        form = AppointmentForm()

    return render(request, 'clinic/Appointment/create_appointment.html', {'form': form})

# @login_required
def edit_appointment(request):
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        if not appointment_id:
            messages.error(request, "Invalid appointment ID.")
            return redirect('view_appointment')

        appointment = get_object_or_404(Appointment, app_id=appointment_id)
        form = AppointmentForm(request.POST, instance=appointment)
        
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.app_date = request.POST.get('app_date')

            # Convert date and time to datetime object
            appointment_date = datetime.strptime(appointment.app_date, '%Y-%m-%d').date()
            appointment_time = form.cleaned_data['app_time']
            appointment_start = datetime.combine(appointment_date, appointment_time)
            appointment_end = appointment_start + timedelta(minutes=15)
            appointment_start_buffer = appointment_start - timedelta(minutes=14)

            now = datetime.now()
            if appointment_start < now:
                messages.error(request, "Cannot edit an appointment for a past time.")
                return redirect(f"{reverse('view_appointment')}?date={appointment.app_date}")

            # Restrict appointment time between 6:00 AM and 5:45 PM
            earliest_time = datetime.combine(appointment_date, datetime.strptime('06:00', '%H:%M').time())
            latest_time = datetime.combine(appointment_date, datetime.strptime('17:45', '%H:%M').time())

            if not (earliest_time <= appointment_start <= latest_time):
                messages.error(request, "Appointments can only be scheduled between 6:00 AM and 5:45 PM.")
                return redirect(f"{reverse('view_appointment')}?date={appointment.app_date}")

            # Strict 15-minute overlap check, excluding "Cancelled" appointments
            overlapping_appointments = Appointment.objects.filter(
                app_date=appointment_date,
                app_status__in=['Waiting', 'Ongoing', 'Done']  # Exclude "Cancelled" appointments
            ).filter(
                app_time__gte=appointment_start_buffer.time(),
                app_time__lt=appointment_end.time()
            ).exclude(app_id=appointment_id)

            if overlapping_appointments.exists():
                messages.error(request, "This appointment time is already taken. Please choose another time.")
                return redirect(f"{reverse('view_appointment')}?date={appointment.app_date}")

            # Save changes
            appointment.save()
            messages.success(request, "Appointment updated successfully.")
            return redirect(f"{reverse('view_appointment')}?date={appointment.app_date}")
        else:
            messages.error(request, "Invalid form data. Please check your inputs.")
            return redirect(f"{reverse('view_appointment')}?date={appointment.app_date}")

    messages.error(request, "Invalid request method.")
    return redirect('view_appointment')

# @login_required
@csrf_exempt
def delete_appointment(request):
    if request.method == 'POST':
        try:
            # Parse JSON data
            data = json.loads(request.body)
            appointment_id = data.get('appointment_id')

            if not appointment_id:
                return JsonResponse({'success': False, 'error': 'Appointment ID is missing'})

            # Retrieve and delete the appointment
            appointment = get_object_or_404(Appointment, pk=appointment_id)
            appointment.delete()

            # Include a success message for the front-end
            return JsonResponse({'success': True, 'message': 'Appointment deleted successfully'})
        except Appointment.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Appointment not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

# @login_required
def auto_cancel_appointments(request):
    """Automatically cancel appointments that are past their scheduled time by 5 minutes."""
    # Get the current time in the Philippine timezone
    current_time_pht = localtime(now())

    # Filter appointments with status 'Waiting' that are overdue by 5 minutes
    overdue_appointments = Appointment.objects.filter(
        app_status='Waiting',
        app_date__lte=current_time_pht.date(),  # Ensure the date is today or earlier
    ).exclude(
        app_date=current_time_pht.date(),
        app_time__gte=(current_time_pht - timedelta(minutes=5)).time(),  # Exclude appointments within the last 5 minutes
    )

    # Update their status to 'Cancelled'
    count = overdue_appointments.update(app_status='Cancelled')
    return count  # Optionally return the number of updated appointments

# Add this function in any relevant view so it runs when the page is accessed
# @login_required
def check_and_update_appointments(request):
    """
    This view will check and update overdue appointments every time the page is loaded.
    """
    auto_cancel_appointments(request)
    return JsonResponse({'success': True, 'message': 'Overdue appointments have been updated.'})


#_____________________________________INVENTORY__________________________________________________________
# @login_required
def inventory(request):
    items = Item.objects.all()  # Fetch all items from the database
    return render(request, 'clinic/Inventory/inventory.html', {'items': items})

# @login_required
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory')  
    else:
        form = ItemForm()
    return render(request, 'clinic/Inventory/add_item.html', {'form': form})

# @login_required
def edit_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)  # Fetch the item by id
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('inventory')  
    else:
        form = ItemForm(instance=item)
    return render(request, 'clinic/Inventory/edit_item.html', {'form': form})

# @login_required
def delete_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)  # Fetch the item by id
    if request.method == 'POST': 
        item.delete()  
        return redirect('inventory')  
    return redirect('inventory') 

def view_item(request, item_id):
    # Fetch the item by its ID
    item = get_object_or_404(Item, pk=item_id)

    # Get all purchases of this item (if any)
    purchased_items = Purchased_Item.objects.filter(item_code=item)

    # Prepare patient details
    patient_details = []
    for purchased_item in purchased_items:
        patient_name = f"{purchased_item.patient_id.patient_fname} {purchased_item.patient_id.patient_lname}"
        item_date_out = purchased_item.item_date_out  # Correctly fetch `item_date_out`
        patient_details.append({
            'patient_name': patient_name,
            'item_date_out': item_date_out,  # Use the correct key
            'pur_date_purchased': purchased_item.pur_date_purchased,
        })

    # Pass these details to the template
    context = {
        'item': item,
        'patient_details': patient_details,  # List of patient details
    }

    return render(request, 'clinic/Inventory/view_item.html', context)


#_________________________________________PATIENT________________________________________________________
# @login_required
def patient(request):
    patients = Patient.objects.all().order_by('patient_lname', 'patient_fname')
    return render(request, 'clinic/Patient/patient.html', {'patients': patients})

# @login_required
def patient_detail(request, patient_id):
    # Fetch the patient object with related purchased items and their associated details
    patient = get_object_or_404(
        Patient.objects.prefetch_related(
            Prefetch(
                'purchased_item_set',  # Related name for Purchased_Item
                queryset=Purchased_Item.objects.select_related(
                    'item_code',  # Fetch related Item for brand and model
                    'payment_id'  # Fetch related Payment for payment details
                )
            )
        ),
        patient_id=patient_id
    )
    
    # Create the form, passing the patient to pre-fill the patient_id field
    form = PurchasedItemForm(request.POST or None, patient=patient)

    if form.is_valid():
        form.save()
        # Redirect to a success page or handle the success case
        return redirect('success_url')  # Replace with actual success URL
    
    return render(request, 'clinic/Patient/patient_detail.html', {
        'patient': patient,
        'form': form
    })

# @login_required
def add_patient(request):
    if request.method == 'POST':
        patient_form = PatientForm(request.POST)

        if patient_form.is_valid():
            patient = patient_form.save(commit=False)
            if not patient.patient_date_checked_up:
                patient.patient_date_checked_up = now()
            patient.save()

            messages.success(request, "Patient added successfully!")
            return redirect('patient')
        else:
            messages.error(request, "There was an error adding the patient.")

    else:
        patient_form = PatientForm(initial={'patient_date_checked_up': now()})

    return render(request, 'clinic/Patient/add_patient.html', {
        'patient_form': patient_form,
    })

# @login_required
def delete_patient(request, patient_id):
    if request.method == 'POST':
        patient = get_object_or_404(Patient, pk=patient_id)
        patient.delete()
        return redirect('patient')  # Redirect to the patient list after deletion
    return HttpResponse(status=400)

# @login_required
def add_purchased_item(request, patient_id):
    patient = get_object_or_404(Patient, patient_id=patient_id)
    purchased_item_form = PurchasedItemForm(request.POST or None, patient=patient)
    payment_form = ItemPaymentForm(request.POST or None)

    if request.method == 'POST':
        if purchased_item_form.is_valid() and payment_form.is_valid():
            purchased_item = purchased_item_form.save(commit=False)
            item = purchased_item.item_code  # Get the item selected for purchase
            
            # Retrieve the item price and set the payment amount
            item_price = item.item_price
            payment = payment_form.save(commit=False)
            payment.payment_to_be_payed = item_price  # Assign the item price as total amount to pay

            # Save payment and purchased item
            payment.save()
            purchased_item.payment_id = payment
            purchased_item.patient_id = patient
            purchased_item.save()

            # Check payment terms and update purchase status (pur_stat)
            if payment.payment_terms in ['Deposit', 'Fully Paid']:
                purchased_item.pur_stat = 'For Release'
            elif payment.payment_terms == 'Installment':
                purchased_item.pur_stat = 'For follow up'

            messages.success(request, "Item and payment added successfully!")
            return redirect('patient_detail', patient_id=patient_id)
        else:
            messages.error(request, "There was an error adding the item or payment.")

    return render(request, 'clinic/Patient/patient_bought.html', {
        'purchased_item_form': purchased_item_form,
        'payment_form': payment_form,
        'patient': patient,
    })

# @login_required
def item_search(request):
    query = request.GET.get('q', '').strip()  # Retrieve and strip the search query
    items = Item.objects.filter(
        Q(item_category_id__item_category_name__icontains=query) |  # Search in the Item Category name
        Q(item_brand__icontains=query) |  # Search in the Item brand
        Q(item_model__icontains=query) |  # Search in the Item model
        Q(item_frame_type_id__item_frame_type_name__icontains=query)  # Search in the Item Frame Type name
    )[:10]  # Limit the number of items returned

    results = [
        {
            'id': item.item_code,
            'text': f'{item.item_category_id} | {item.item_brand} | {item.item_model} | {item.item_frame_type_id}'
        }
        for item in items
    ]
    return JsonResponse({'items': results})

def item_price(request):
    item_id = request.GET.get('item_id')
    try:
        item = Item.objects.get(pk=item_id)
        return JsonResponse({'price': item.item_price})
    except Item.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)

def edit_purchased_item(request, purchase_id):
    # Fetch the purchased item
    purchased_item = get_object_or_404(Purchased_Item, pk=purchase_id)
    
    if request.method == 'POST':
        # Update fields based on POST data
        item_id = request.POST.get('item_code')
        pur_stat = request.POST.get('pur_stat')
        payment_payed = request.POST.get('payment_payed')
        payment_to_be_payed = request.POST.get('payment_to_be_payed')
        item_date_out = request.POST.get('item_date_out') 
        
        # Update Purchased_Item fields
        purchased_item.item_code = Item.objects.get(pk=item_id) if item_id else None
        purchased_item.pur_stat = pur_stat
        
        # Handle the 'item_date_out' field if provided
        if item_date_out:
            purchased_item.item_date_out = item_date_out

        # Update Payment fields
        payment = purchased_item.payment_id
        if payment:
            payment.payment_payed = payment_payed
            payment.payment_to_be_payed = payment_to_be_payed
            payment.save()
        
        # Save Purchased_Item changes
        purchased_item.save()
        
        return redirect('patient_detail', patient_id=purchased_item.patient_id.patient_id)
    
    # Fetch all items for the dropdown
    items = Item.objects.all()
    return render(request, 'clinic/Patient/edit_purchased_item.html', {
        'purchased_item': purchased_item,
        'items': items,
        'payment': purchased_item.payment_id,
    })


def delete_purchased_item(request, pur_id):
    # Retrieve the purchased item by pur_id
    purchased_item = get_object_or_404(Purchased_Item, pur_id=pur_id)

    # Delete the purchased item
    purchased_item.delete()

    # Display a success message
    messages.success(request, "Purchased item deleted successfully.")

    # Redirect to the patient details page or purchased items list
    return redirect('patient_detail', patient_id=purchased_item.patient_id.patient_id)


#_____________________________________SALES__________________________________________________________
# @login_required
def sales(request):
    return render(request, 'clinic/Sales/sales.html')


#_________________________________________LOGOUT_______________________________________________________
# @login_required
def user_logout(request):
    # ✅ Remove user session manually
    if 'user_id' in request.session:
        del request.session['user_id']  # Remove user ID from session
    if 'username' in request.session:
        del request.session['username']  # Remove username from session
    
    request.session.flush()  # Clear entire session
    messages.success(request, "You have been logged out successfully.")
    
    return redirect('login')
