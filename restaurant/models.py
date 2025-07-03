from django.db import models



from django.contrib.auth.models import User


# Create your models here.
class Booking(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    first_name = models.CharField(max_length=200)
    no_of_guests=models.IntegerField(null=True)
    reservation_date = models.DateField()
    reservation_slot = models.SmallIntegerField(default=10)


    def __str__(self): 
        return self.first_name


# Add code to create Menu model
class Menu(models.Model):
   name = models.CharField(max_length=200) 
   price = models.IntegerField(null=False)
   inventory=models.IntegerField(null=True) 
   menu_item_description = models.TextField(max_length=1000, default='') 

   def __str__(self):
      return f'{self.title} : {str(self.price)}'
   def get_item(self):
      return f'{self.title} : {str(self.price)}'