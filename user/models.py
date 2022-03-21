
from django.db import models
from owner.models import *

# Create your models here.

        
class passenger(models.Model):
    
    name=models.CharField(max_length=20)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=20)
    cpassword=models.CharField(max_length=20)
    mobile=models.CharField(max_length=10)
    address=models.TextField(max_length=100)
    pic=models.FileField(upload_to='profile',default='1.png')
    
    
    def __self__(self):
       return self.name + '@' + self.email
        
class cart(models.Model):
    uid=models.ForeignKey(passenger,on_delete=models.CASCADE)      
    car=models.ManyToManyField(car,related_name='cart')
    
    
class book(models.Model):
    car=models.ForeignKey(car,on_delete=models.CASCADE)
    passenger=models.ForeignKey(passenger,on_delete=models.CASCADE)
    pay_id = models.CharField(max_length=50,null=True,blank=True)
    pay_method = models.BooleanField(default=True) # True - online # false - COD
    booking_date = models.DateTimeField(auto_now_add=True)
    feedback = models.TextField(null=True,blank=True)

    def __self__(self):
        return self.car.name + self.passenger.name
    
