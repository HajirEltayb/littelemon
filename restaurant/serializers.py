from rest_framework import serializers
from .models import Menu , Booking 
from decimal import Decimal
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','password','email']
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields="__all__"

class MenuItemSerializer(serializers.ModelSerializer):
  
    price_after_tax =serializers.SerializerMethodField(method_name='calculate_tax')
    
    class Meta:
        model = Menu
        fields =['id','name','price','menu_item_description']
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
    

