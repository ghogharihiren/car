
from django.db import models

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
        self.name + '@' + self.email
    
