
from django.contrib import admin
from .models import AmbulanceBooking, MessageSending, Registration

admin.site.register(AmbulanceBooking)
admin.site.register(MessageSending)
admin.site.register(Registration)