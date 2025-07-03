from django.forms import ModelForm
from .models import Booking
from django import forms
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


# Code added for loading form data on the Booking page
class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields=['id','first_name','reservation_date','reservation_slot']
