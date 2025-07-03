from django.urls import path
from . import views
#from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LoginView
#from django.conf.urls import url
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.loginn, name='loginn'),
    path('logout/',views.logout_view,name='logoutt')
]