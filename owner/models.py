from django.db import models



class owner(models.Model):   
    
    doc_choice = (('pan','PAN Card '), ('aadhar','AAdhar Card'))
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    mobile =  models.CharField(max_length=14)
    password = models.CharField(max_length=20)
    doc = models.CharField(max_length=20,choices=doc_choice)
    doc_number = models.CharField(max_length=20)
    address = models.TextField()
    verify = models.BooleanField(default=False) 
    pic= models.FileField(upload_to='profile',default='1.png')
    
   


    def __str__(self):
        return self.name + ' @  ' + self.email
    
class car(models.Model):
   
    uid=models.ForeignKey(owner,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    model=models.CharField(max_length=50)
    number=models.CharField(max_length=50)
    totalseat=models.IntegerField(default=0)
    availableseat=models.IntegerField(default=0)
    startpoint=models.CharField(max_length=50)
    destination=models.CharField(max_length=50)
    price=models.IntegerField(default=0)
    date=models.DateField()
    pic=models.FileField(upload_to='pic',null=True,blank=True)
    
    
    def __str__(self):
        return self.name   
    
class startpoint(models.Model):
     name=models.CharField(max_length=50)
     value=models.CharField(max_length=50)
     
     
     def __str__(self):
         return self.name

class destination(models.Model):
     name=models.CharField(max_length=50)
     value=models.CharField(max_length=50)
     
     
     def __str__(self):
         return self.name     