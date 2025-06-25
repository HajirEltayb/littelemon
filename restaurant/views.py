# from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .forms import BookingForm
from .models import Menu
from django.core.paginator import Paginator,EmptyPage
from .models import Booking
from datetime import datetime
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.decorators import api_view
from .serializers import MenuItemSerializer,BookingSerializer
from rest_framework import status
from rest_framework.response import Response

# Create your views here.
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def reservations(request):
    date = request.GET.get('date',datetime.today().date())
    bookings = Booking.objects.all()
    booking_json = BookingSerializer(bookings)
    return render(request, 'bookings.html',{"bookings":booking_json})

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
        perpage=request.query_params.get('perpage',default=2)
        page=request.query_params.get('page',default=1)
        
        if to_price:
            items=items.filter(price__lte=to_price)
        if search:
            items=items.filter(title__contains=search)
        if ordering:
            ordering_fields= ordering.spilt(",")
            items=items.order_by(*ordering_fields)

        paginator=Paginator(items,per_page=perpage)
        try:
            items=paginator.page(number=page)
        except EmptyPage:
            items=[]
        serialized_item = MenuItemSerializer(items, many=True)
        return Response(serialized_item.data)
    elif request.method in ['POST','PUT','DELETE','PATCH']:
        if request.user.groups.filter(name='Manager').exists():
           serialized_item =MenuItemSerializer(data=request.data)
           serialized_item.is_valid(raise_exception=True)
           serialized_item.save()
           return Response(serialized_item.validated_data,status.HTTP_201_CREATED)
        else :
           return Response({"message":"youare not authorized "},403)
        

@api_view(['GET','PUT','DELETE','PATCH'])
def single_item(request, pk):
    if request.method=='GET':
       item = get_object_or_404(Menu,id=pk)
       serialized_item = MenuItemSerializer(item)
       return Response(serialized_item.data)
    
    elif request.method == 'PUT':
        if request.user.groups.filter(name='Manager').exists():
           item=get_object_or_404( Menu ,id=pk)
           serialized_item =MenuItemSerializer(item,data=request.data)
           serialized_item.is_valid(raise_exception=True)
           serialized_item.save()
           return Response(serialized_item.validated_data,status.HTTP_201_CREATED)
        else:
            return Response({"message":"youare not authorized "},403)
        
    elif request.method == 'PATCH':
        if request.user.groups.filter(name='Manager').exists():
           item=get_object_or_404( Menu ,id=pk)
           serialized_item =MenuItemSerializer(item,data=request.data,partial=True)
           serialized_item.is_valid(raise_exception=True)
           serialized_item.save()
           return Response(serialized_item.validated_data,status.HTTP_201_CREATED)
        else:
            return Response({"message":"youare not authorized "},403)
        
    elif request.method =='DELETE':
      if request.user.groups.filter(name='Manager').exists():
        item=get_object_or_404( Menu ,id=pk)
        item.delete()
        return Response({"message":"ok "},status=status.HTTP_204_NO_CONTENT)
      else:
            return Response({"message":"youare not authorized "},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
@api_view(['GET','POST','PUT','DELETE','PATCH'])
@csrf_exempt
def bookings(request) :
    if request.method == 'POST':
        data = json.load(request)
        exist=Booking.objects.filter(reservation_date=data['reservation_date'],
            reservation_slot=data['reservation_slot']).exists()
        if not exist:
         booking=Booking(
            first_name=data['first_name'],
            reservation_date=data['reservation_date'],
            reservation_slot=data['reservation_slot'],
         )
         booking.save()
        else: return HttpResponse("{'error':1}",content_type='application/json')

    date = request.GET.get('date',datetime.today().date())
    bookings= Booking.objects.filter(reservation_date=date)
    booking_json=BookingSerializer(bookings)
    return HttpResponse(booking_json,content_type='application/json')
