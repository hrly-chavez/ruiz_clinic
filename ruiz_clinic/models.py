from django.db import models
from django.utils.timezone import now,localtime
from datetime import date
# Create your models here.


def get_today_date():
    return localtime(now()).date()

class Item_Category(models.Model):
    item_category_id = models.AutoField(primary_key=True)
    item_category_name = models.CharField(max_length=50, null=True,blank=True)

    def __str__(self):
        return f"{self.item_category_name}"
    
class Item_Frame_Type(models.Model):
    frame_choices = [
        ('Plastic', 'Plastic'),
        ('Acetate','Acetate'),
        ('Metal','Metal'),
        ('Wood','Wood'),
        ('Titanium','Titanium'),

    ]
    item_frame_type_id = models.AutoField(primary_key=True)
    item_frame_type_name = models.CharField(max_length=20, choices=frame_choices)

    def __str__(self):
        return f"{self.item_frame_type_name}"

class Item(models.Model):
    item_code = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=200,null=True,blank=True)
    item_brand = models.CharField(max_length=200)
    item_model = models.CharField(max_length=20,null=True,blank=True)
    item_price = models.FloatField()
    item_date_in = models.DateField(default=now)
    item_quantity = models.IntegerField()
    item_color = models.CharField(max_length=100,null=True,blank=True)
    item_measurement = models.CharField(max_length=200,null=True,blank=True)
    item_category_id = models.ForeignKey(Item_Category, null=True, blank=True, on_delete=models.SET_NULL)
    item_frame_type_id = models.ForeignKey(Item_Frame_Type,on_delete=models.CASCADE, db_constraint=True, null=True , blank=True)

    def __str__(self):
        return f'{self.item_category_id} | {self.item_brand} | {self.item_model} | {self.item_frame_type_id}'

class Purchased_Item(models.Model):   
    pur_stat_choices = [
        ('For Release', 'For Release'), #deposited or waiting for item to be delivered
        ('For follow up', 'For follow up'), # installment
        ('Done', 'Done'), #paid transaction done
    ]
    pur_id = models.AutoField(primary_key=True)
    pur_date_purchased = models.DateField(default=get_today_date)
    pur_stat = models.CharField(max_length=20, choices= pur_stat_choices,db_default='For Release')
    item_code =  models.ForeignKey(Item,null=True, blank=True, on_delete=models.SET_NULL)
    patient_id = models.ForeignKey('Patient', null=True, blank=True, on_delete=models.CASCADE)
    payment_id = models.ForeignKey('Payment', null=True, blank=True, on_delete=models.CASCADE)
    item_date_out = models.DateField(null=True, blank=True)
    def __str__(self):
        return f"{self.item_code},  {self.pur_date_purchased}"

class Payment(models.Model): 
    payment_method_choices = [
        ('Cash','Cash'),
        ('Debit Card', 'Debit Card'),   
        ('Credit Card','Credit Card'),
        ('E Wallet','E Wallet'),
        ('Other','Other'),
    ]

    pay_terms_choices = [
        ('Installment', 'Installment'),
        ('Deposit', 'Deposit'),
        ('Fully Paid', 'Fully Paid'),
    ]
    
    payment_id = models.AutoField(primary_key=True)
    payment_payed = models.FloatField(null=True,blank=True) #Tracks the total amount the customer has paid so far.
    current_payment = models.FloatField(null=True,blank=True) # Tracks the current payment made by the customer
    current_payment_date = models.DateField(default=now) #when was the current payment made
    payment_to_be_payed = models.FloatField(null=True,blank=True) #Tracks the customer's current balance (how much they still owe).
    payment_method = models.CharField(max_length=50,choices=payment_method_choices,default='Cash')
    payment_terms = models.CharField(max_length=20, choices=pay_terms_choices,default='Fully Paid')
    payment_duration = models.ForeignKey('Payment_Duration', on_delete=models.SET_NULL, null=True, blank=True,
            help_text="Applicable only if payment terms are 'Installment'.")

    def __str__(self):
        return f" {self.payment_payed}, {self.payment_to_be_payed}"
        
    def update_payment(self, amount):
        if amount > self.payment_to_be_payed:
            raise ValueError("Payment exceeds the remaining balance.")
        self.current_payment = amount
        self.current_payment_date = localtime(now()).date()
        self.payment_payed += amount
        self.payment_to_be_payed = max(self.payment_to_be_payed - amount, 0)
        self.save()

        # Update the Sales record
        sales_entry, created = Sales.objects.get_or_create(sales_date=self.current_payment_date)
        sales_entry.sales_total += amount
        sales_entry.save()

class Payment_Duration(models.Model):
    duration_choices = [
        ('3 Months', '3 Months'),
        ('6 Months','6 Months'),
        ('9 Months', '9 Months'),
        ('12 Months','12 Months'),
    ]

    payment_duration_id = models.AutoField(primary_key=True)
    payment_duration_span = models.CharField(max_length=50,choices=duration_choices,null=True,blank=True)
    payment_duration_start = models.DateField(default=now,null=True,blank=True)
    payment_duration_end = models.DateField(null=True,blank=True)


class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    patient_fname = models.CharField(max_length=50)
    patient_lname = models.CharField(max_length=100)
    patient_initial = models.CharField(max_length=1, null=True, blank=True)
    patient_date_checked_up = models.DateField(default=now)
    patient_address = models.CharField(max_length=400)
    patient_occupation = models.CharField(max_length=500, null=True, blank=True)
    patient_birthdate = models.DateField()
    patient_contact = models.CharField(max_length=13)
    patient_diag = models.TextField(null=True, blank=True)
    pur_id = models.ForeignKey(Purchased_Item, null=True, blank=True, on_delete=models.SET_NULL)
    payment_id = models.ForeignKey(Payment, null=True, blank=True, on_delete=models.SET_NULL)

    def age(self):
        today = date.today()
        return today.year - self.patient_birthdate.year - ((today.month, today.day) < (self.patient_birthdate.month, self.patient_birthdate.day))

    def __str__(self):
        return f"{self.patient_fname}, {self.patient_fname}, - Diagnosed with {self.patient_diag[:30]} ,{self.pur_id}, {self.payment_id}"

class Appointment(models.Model):
    app_status_choices = [
        ('Ongoing', 'Ongoing'),
        ('Waiting', 'Waiting'),
        ('Done', 'Done'),
        ('Cancelled', 'Cancelled'),
    ]
    app_id = models.AutoField(primary_key=True)
    app_fname = models.CharField(max_length=50, null=True, blank=True)  # Temporarily allow nulls
    app_lname = models.CharField(max_length=50, null=True, blank=True)  # Temporarily allow nulls
    app_contact = models.CharField(max_length=11, null=True, blank=True)  # Temporarily allow nulls
    app_date = models.DateField(default=now)
    app_time = models.TimeField()
    app_status = models.CharField(max_length=50, choices=app_status_choices)
    patient_id = models.ForeignKey(Patient, null=True, blank=True, on_delete=models.CASCADE)
    
class Account(models.Model):
    account_id = models.AutoField(primary_key=True)
    account_username = models.CharField(max_length=100, unique=True)
    account_password = models.CharField(max_length=100)  # Store as hashed in production

    def __str__(self):
        return self.account_username
    
class Sales(models.Model):
    sales_id = models.AutoField(primary_key=True)
    sales_date = models.DateField(default=get_today_date, unique=True)
    sales_total = models.FloatField(default=0.0)  # Total earnings of the day
    number_products_sold = models.IntegerField(default=0)  # Total product count

    def __str__(self):
        return f"Sales {self.sales_date}: {self.sales_total}, {self.number_products_sold}"