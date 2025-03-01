from django.db import models

# Create your models here.

class AmbulanceBooking(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    number = models.CharField(max_length=20)
    location = models.CharField(max_length=255)
    textarea_message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"Booking for {self.name} - {self.status}"
    
class MessageSending(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)  # User's name
    email = models.EmailField(max_length=255, blank=True, null=True)  # User's email
    phone = models.CharField(max_length=20)  # User's phone number
    subject = models.CharField(max_length=255, blank=True, null=True)  # Message subject
    message = models.TextField(blank=True, null=True)  # Message content
    def __str__(self):
        return f"Message from {self.name}"

class Registration(models.Model):
   c_name=models.CharField(max_length=15)
   c_phone= models.CharField(max_length=10)
   c_email= models.CharField(max_length=120)
   c_password= models.CharField(max_length=120)

class Payment(models.Model):
    booking = models.OneToOneField('AmbulanceBooking', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, default='Pending')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Payment for booking {self.booking.id} - {self.payment_status}"