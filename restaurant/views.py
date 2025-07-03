# from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from .forms import BookingForm
from .models import Menu
from django.core.paginator import Paginator,EmptyPage
from .models import Booking
from datetime import datetime
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from .serializers import MenuItemSerializer,BookingSerializer, UserSerializer
from rest_framework import status,viewsets
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from rest_framework.permissions import IsAuthenticated

# Create your views here.
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def reservations(request):
    date = request.GET.get('date',datetime.today().date())
    bookings = Booking.objects.all()
    booking_json = BookingSerializer(bookings,many=True)
    return render(request, 'bookings.html',{"bookings":booking_json.data})

def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'book.html', context)


@api_view(['GET','POST','PUT','DELETE','PATCH'])
def menu(request):
    if request.method == 'GET':
        items = Menu.objects.all()

        to_price = request.query_params.get('to_price')
        search= request.query_params.get('search')
        ordering =request.query_params.get('ordering')
        
        if to_price:
            items=items.filter(price__lte=to_price)
        if search:
            items=items.filter(title__contains=search)
        if ordering:
            ordering_fields= ordering.spilt(",")
            items=items.order_by(*ordering_fields)

        
        serialized_item = MenuItemSerializer(items, many=True)
        return Response(serialized_item.data)
        #return render(request,'menu.html',{"menu":serialized_item.data})
    elif request.method in ['POST','PUT','DELETE','PATCH']:
        
           serialized_item =MenuItemSerializer(data=request.data)
           serialized_item.is_valid(raise_exception=True)
           serialized_item.save()
           return Response(serialized_item.validated_data,status.HTTP_201_CREATED)
        
@api_view(['GET','PUT','DELETE','PATCH'])
def single_item(request, pk):
    if request.method=='GET':
       item = get_object_or_404(Menu,id=pk)
       serialized_item = MenuItemSerializer(item)
       return Response(serialized_item.data)
    
    elif request.method == 'PUT':
        
           item=get_object_or_404( Menu ,id=pk)
           serialized_item =MenuItemSerializer(item,data=request.data)
           serialized_item.is_valid(raise_exception=True)
           serialized_item.save()
           return Response(serialized_item.validated_data,status.HTTP_201_CREATED)
       
    elif request.method == 'PATCH':
        
           item=get_object_or_404( Menu ,id=pk)
           serialized_item =MenuItemSerializer(item,data=request.data,partial=True)
           serialized_item.is_valid(raise_exception=True)
           serialized_item.save()
           return Response(serialized_item.validated_data,status.HTTP_201_CREATED)
        
    elif request.method =='DELETE':
      
        item=get_object_or_404( Menu ,id=pk)
        item.delete()
        return Response({"message":"ok "},status=status.HTTP_204_NO_CONTENT)
      
#@api_view(['GET','POST','PUT','DELETE','PATCH'])
#@csrf_exempt
@login_required
def bookings(request) :
    
    if request.method == 'POST':
      try:
        data = json.load(request)
        exist=Booking.objects.filter(reservation_date=data['reservation_date'],
            reservation_slot=data['reservation_slot']).exists()
        if not exist:
         booking=Booking(
            user=request.user,
            first_name=data['first_name'],
            reservation_date=data['reservation_date'],
            reservation_slot=data['reservation_slot'],
         )
         booking.save()
         return JsonResponse({'success': 'Booking created'}, status=201)
        else:    return JsonResponse({'error': 'Booking already exists'}, status=400)
      except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    #date = request.GET.get('date',datetime.today().date())
    date_str = request.GET.get('date')  # Get the date parameter
    if not date_str:  # If it's empty, default to today's date
        date = timezone.now().date()
    else:
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()  # Parse the date
        except ValueError:
            return JsonResponse({'error': 'Invalid date format'}, status=400)

    bookings= Booking.objects.filter(reservation_date=date)
    booking_json=BookingSerializer(bookings,many=True)
    return JsonResponse(booking_json.data, safe=False)
    #return HttpResponse(booking_json.data,content_type='application/json')
class UserViewSet(viewsets.ModelViewSet):
   queryset = User.objects.all()
   serializer_class = UserSerializer
   permission_classes = [IsAuthenticated]