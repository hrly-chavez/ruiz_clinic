from django import forms
from .models import *
from django.core.exceptions import ValidationError
from datetime import time


#_________________________________IVENTORY___________________________________________________
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_brand','item_model','item_price','item_date_in','item_quantity','item_color','item_measurement','item_category_id','item_frame_type_id',
        ]
        widgets = {
            'item_brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter item brand'}),
            'item_model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter item model'}),
            'item_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price'}),
            'item_date_in': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'item_quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter quantity'}),
            'item_color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter color'}),
            'item_measurement': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter measurements'}),
            'item_category_id': forms.Select(attrs={'class': 'form-control'}),
            'item_frame_type_id': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'item_brand': 'Brand',
            'item_model': 'Model',
            'item_price': 'Price',
            'item_date_in': 'Date In',
            'item_quantity': 'Quantity',
            'item_color': 'Color',
            'item_measurement': 'Measurement',
            'item_category_id': 'Category',
            'item_frame_type_id': 'Frame Type',
        }

#_____________________________________PATIENT__________________________________________________
class PatientForm(forms.ModelForm):
    pass

#_________________________________APPOINTMENT___________________________________________________

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['app_fname', 'app_lname', 'app_contact', 'app_date', 'app_time', 'app_status',]
        widgets = {
            'app_date': forms.DateInput(attrs={'type': 'date'}),
            'app_time': forms.TimeInput(attrs={'type': 'time'}),
            'app_status': forms.Select(choices=Appointment.app_status_choices),
        }
        labels = {
            'app_fname': 'First Name',
            'app_lname': 'Last Name',
            'app_contact': 'Contact Number',
            'app_date': 'Date',
            'app_time': 'Time',
            'app_status': 'Status',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If an initial date is passed, populate the `app_date` field
        if 'initial' in kwargs and 'app_date' in kwargs['initial']:
            self.fields['app_date'].initial = kwargs['initial']['app_date']



# class AppointmentForm(forms.ModelForm):
#     class Meta:
#         model = Appointment
#         fields = ['app_fname', 'app_lname', 'app_contact', 'app_date', 'app_time', 'app_status']
#         widgets = {
#             'app_date': forms.DateInput(attrs={'type': 'date'}),
#             'app_time': forms.TimeInput(attrs={'type': 'time'}),
#             'app_status': forms.Select(choices=Appointment.app_status_choices),
#         }
#         labels = {
#             'app_fname': 'First Name',
#             'app_lname': 'Last Name',
#             'app_contact': 'Contact Number',
#             'app_date': 'Date',
#             'app_time': 'Time',
#             'app_status': 'Status',
#         }

#     def clean(self):
#         cleaned_data = super().clean()
#         app_time = cleaned_data.get('app_time')

#         # Define restricted time range
#         start_restricted_time = time(17, 30)  # 5:30 PM
#         end_restricted_time = time(6, 0)      # 6:00 AM

#         # Check if the time is within the restricted range
#         if app_time:
#             if app_time >= start_restricted_time or app_time < end_restricted_time:
#                 raise ValidationError(
#                     "Appointments cannot be scheduled between 5:30 PM and 6:00 AM."
#                 )

#         return cleaned_data


