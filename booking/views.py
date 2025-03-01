from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import MessageSending
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import AmbulanceBooking, Payment
import random
import string


def home(request):
    return render(request, 'index.html')

def booking_success(request):
    return render(request, 'booking_success.html')

def adminView(request):
    return render(request, 'adminDashboard.html')

def user_logout(request):
    logout(request)
    return redirect('home') 

def booking_success(request):
    return render(request, 'booking_success.html')

def adminView(request):
    return render(request, 'adminDashboard.html')


def user_register(request):
    if request.method == 'POST':
        try:
            # Get form data
            username = request.POST.get('name')
            # phone = request.POST.get('phone')
            email = request.POST.get('email')
            # dob = request.POST.get('dob')
            password = request.POST.get('pwd')

            # Validate if username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists!")
                return render(request, 'registration/registration.html')

            # Validate if email already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered!")
                return render(request, 'registration/registration.html')

            # Create new user
            user = User.objects.create(
                username=username,
                email=email,
                password=make_password(password)
            )

            # If you want to store additional fields like phone and dob,
            # you'll need to create a UserProfile model:
            """
            from django.db import models
            from django.contrib.auth.models import User

            class UserProfile(models.Model):
                user = models.OneToOneField(User, on_delete=models.CASCADE)
                phone = models.CharField(max_length=15)
                dob = models.DateField()

                def __str__(self):
                    return self.user.username
            """
            
            # Then create the profile:
            # UserProfile.objects.create(
            #     user=user,
            #     phone=phone,
            #     dob=dob
            # )

            messages.success(request, "Registration successful! Please login.")
            return redirect('login')

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return render(request, 'registration/registration.html')

    return render(request, 'registration/registration.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('pwd')
        
        # Check for admin credentials
        if username == 'admin' and password == '123456':
            print("Admin login attempted")  # Debug print
            return render(request, 'adminDashboard.html', {
                'bookings': AmbulanceBooking.objects.all(),
                'messages': MessageSending.objects.all()
            })
        
        # Regular user authentication
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Incorrect username or password.")
            return render(request, 'registration/login.html')
            
    return render(request, 'registration/login.html')

# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('name')
#         password = request.POST.get('pwd')
        
#         # First, check if user is already authenticated
#         if request.user.is_authenticated:
#             return redirect('home')
            
#         # Check for admin credentials
#         if username == 'admin' and password == '123456':
#             return redirect('adminDashboard.html')
            
#         # Regular user authentication
#         user = authenticate(request, username=username, password=password)
        
#         if user is not None:
#             login(request, user)
#             return redirect('home')
#         else:
#             messages.error(request, "Incorrect username or password.")
#             return render(request, 'registration/login.html')
            
#     return render(request, 'registration/login.html')



@login_required
def user_profile(request):
    try:
        # Get current logged in user
        current_user = request.user
        
        # Get user's bookings
        bookings = AmbulanceBooking.objects.filter(name=current_user.username)
        
        # Get user's messages
        user_messages = MessageSending.objects.filter(name=current_user.username)
        
        context = {
            'user': current_user,
            'bookings': bookings,
            'messages': user_messages,
            'total_bookings': bookings.count(),
            'total_messages': user_messages.count()
        }
        
        return render(request, 'profile.html', context)
        
    except User.DoesNotExist:
        messages.error(request, "User profile not found.")
        return redirect('login')
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('login')



def sendMessage(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if not name or not phone or not email:
            error_message = "Please fill out all required fields."
            return render(request, 'index.html', {'error_message': error_message})

        msg = MessageSending(name=name, email=email, phone=phone, subject=subject, message=message)
        
        try:
            msg.save()
            return render(request, 'index.html', {'success_message': 'Message sent successfully!'})
        except Exception as e:
            error_message = f"Message sending failed: {str(e)}"
            return render(request, 'index.html', {'error_message': error_message})

    return redirect('home')  # Changed from direct render to redirect

def home(request):
    # Add debugging prints
    print(f"Request method: {request.method}")
    
    if request.method == 'POST':
        # Print all POST data
        print(f"POST data: {request.POST}")
        
        # Get form data
        name = request.POST.get('name')
        number = request.POST.get('number')
        location = request.POST.get('location')
        textarea_message = request.POST.get('textarea_message')
        
        # Print individual fields
        print(f"Name: {name}")
        print(f"Number: {number}")
        print(f"Location: {location}")
        print(f"Message: {textarea_message}")

        if not name or not number or not location:
            messages.error(request, "Please fill out all required fields.")
            return render(request, 'index.html')

        try:
            # Create and save the booking
            booking = AmbulanceBooking.objects.create(
                name=name,
                number=number,
                location=location,
                textarea_message=textarea_message,
                status='Pending'
            )
            
            # Print booking object
            print(f"Booking created: {booking}")
            
            messages.success(request, "Booking successful! Please proceed to payment.")
            return redirect('payment', booking_id=booking.id)

        except Exception as e:
            # Print the full error
            import traceback
            print(f"Error saving booking: {str(e)}")
            print(traceback.format_exc())
            
            messages.error(request, f"Booking failed: {str(e)}")
            return render(request, 'index.html')

    # For GET requests
    context = {
        'error_message': messages.get_messages(request)
    }
    return render(request, 'index.html', context)

import random
import string

def payment(request, booking_id):
    try:
        booking = get_object_or_404(AmbulanceBooking, id=booking_id)
        context = {
            'booking': booking,
        }
        return render(request, 'payment.html', context)
    except Exception as e:
        messages.error(request, "Error loading payment page.")
        return redirect('home')

def process_payment(request, booking_id):
    if request.method == 'POST':
        try:
            booking = get_object_or_404(AmbulanceBooking, id=booking_id)
            
            # Generate a random transaction ID
            transaction_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            
            # Create payment record
            payment = Payment.objects.create(
                booking=booking,
                amount=1000,
                payment_status='Completed',
                transaction_id=transaction_id
            )
            
            # Update booking status
            booking.status = 'Paid'
            booking.save()
            
            messages.success(request, "Payment successful! Your booking has been confirmed.")
            return redirect('booking_success')
            
        except Exception as e:
            messages.error(request, "Payment failed. Please try again.")
            return redirect('payment', booking_id=booking_id)
    
    return redirect('payment', booking_id=booking_id)

def booking_success(request):
    messages.success(request, "Thank you for your booking! Your ambulance is on the way.")
    return render(request, 'booking_success.html')


def custom_admin(request):
    bookings = AmbulanceBooking.objects.all()
    messages = MessageSending.objects.all()

    if request.method == 'POST':
        if 'delete_booking' in request.POST:
            booking_id = request.POST.get('delete_booking')
            AmbulanceBooking.objects.filter(id=booking_id).delete()
            return redirect('custom_admin')

        if 'delete_message' in request.POST:
            message_id = request.POST.get('delete_message')
            MessageSending.objects.filter(id=message_id).delete()
            return redirect('custom_admin')

    context = {
        'bookings': bookings,
        'messages': messages,
    }
    return render(request, 'adminDashboard.html', context)