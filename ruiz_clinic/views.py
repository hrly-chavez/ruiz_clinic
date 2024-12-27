
from django.contrib import messages
from django.shortcuts import render,redirect, get_object_or_404
from .forms import *
from django.http import HttpResponse, JsonResponse,Http404


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


def delete_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)  # Fetch the item by id
    if request.method == 'POST': 
        item.delete()  
        return redirect('inventory')  
    return redirect('inventory') 

def view_item(request, item_id):
   
    item = get_object_or_404(Item, item_code=item_id)  # Using item_code as the primary key
    return render(request, 'clinic/Inventory/view_item.html', {'item': item})

#_________________________________________PATIENT________________________________________________________

def patient(request):
    patients = Patient.objects.all()
    return render(request, 'clinic/Patient/patient.html', {'patients': patients})

def patient_detail(request, patient_id):
    # Use patient_id instead of id in the query
    patient = get_object_or_404(Patient, patient_id=patient_id)  # Use patient_id here
    
    # Create the form, passing the patient to pre-fill the patient_id field
    form = PurchasedItemForm(request.POST or None, patient=patient)
    
    if form.is_valid():
        form.save()
        # Redirect to a success page or handle the success case
        return redirect('success_url')  # Replace with actual success URL
    
    return render(request, 'clinic/Patient/patient_detail.html', {'patient': patient, 'form': form})

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

def delete_patient(request, patient_id):
    if request.method == 'POST':
        patient = get_object_or_404(Patient, pk=patient_id)
        patient.delete()
        return redirect('patient')  # Redirect to the patient list after deletion
    return HttpResponse(status=400)

def add_purchased_item(request, patient_id):
    patient = get_object_or_404(Patient, patient_id=patient_id)
    purchased_item_form = PurchasedItemForm(request.POST or None, patient=patient)
    payment_form = ItemPaymentForm(request.POST or None)

    if request.method == 'POST':
        if purchased_item_form.is_valid() and payment_form.is_valid():
            # Save payment first
            payment = payment_form.save()

            # Save purchased item with the created payment and patient
            purchased_item = purchased_item_form.save(commit=False)
            purchased_item.payment_id = payment
            purchased_item.patient_id = patient
            purchased_item.save()

            messages.success(request, "Item and payment added successfully!")
            return redirect('patient_detail', patient_id=patient_id)
        else:
            messages.error(request, "There was an error adding the item or payment.")

    return render(request, 'clinic/Patient/patient_bought.html', {
        'purchased_item_form': purchased_item_form,
        'payment_form': payment_form,
        'patient': patient,
    })

def item_search(request):
    query = request.GET.get('q', '')
    items = Item.objects.filter(item_brand__icontains=query)[:10]  # Limit the number of items returned
    results = [{'id': item.item_code, 'text': f'{item.item_brand} - {item.item_model}'} for item in items]
    return JsonResponse({'items': results})

def item_price(request):
    item_id = request.GET.get('item_id')
    try:
        item = Item.objects.get(pk=item_id)
        return JsonResponse({'price': item.item_price})
    except Item.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)
#_____________________________________SALES__________________________________________________________
def sales(request):
    return render(request, 'clinic/Sales/sales.html')