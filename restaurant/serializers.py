from rest_framework import serializers
from .models import Menu , Booking 
from decimal import Decimal
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields=['id','first_name','reservation_date','no_of_guests','reservation_slot']

class MenuItemSerializer(serializers.ModelSerializer):
  
    
    class Meta:
        model = Menu
        fields =['id','name','price','inventory','menu_item_description']
        extra_kwargs = {
            'price': {'min_value':2},
            
            'name':{
                'validators':[
                    UniqueValidator(
                        queryset=Menu.objects.all()
                    )
                ]
            }
        }

    def calculate_tax(self, product:Menu):
        return product.price * Decimal(1.1)
    

