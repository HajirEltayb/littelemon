
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate,logout
from django.urls import reverse

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            authenticated_user = authenticate(username=user.username,
                password=request.POST['password1'])
            login(request, authenticated_user)  # Automatically log in the user
            return redirect('home')  # Redirect to a home page after registration
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
def loginn(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:  # Check if both fields are provided
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to your home page
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please fill in both fields.')

    return render(request, 'login.html')
    
def logout_view(request):
      logout(request)
      return HttpResponseRedirect(reverse('home'))
