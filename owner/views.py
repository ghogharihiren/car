import re
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from .models import *
from random import randrange,choices
from django.conf import settings
from django.core.mail import send_mail
from json import loads
from user.models import book



# Create your views here.
def index(request):
    uid = owner.objects.get(email=request.session['email'])
    return render(request,'index.html',{'uid':uid})

def login(request):
        try:
            uid = owner.objects.get(email=request.session['email'])
            return redirect('index')
        except:
            if request.method=='POST':
                try:
                    uid = owner.objects.get(email=request.POST['email'])
                    if request.POST['password'] == uid.password:
                       request.session['email'] = request.POST['email']
                       return redirect('index')
                    return render(request,'login.html',{'msg':'incorrect password'})
                except:
                    msg = 'Email is not register'
                    return render(request,'login.html',{'msg':msg})
        return render(request,'login.html')

  
def register(request): 
    if request.method=='POST':
        try:
            owner.objects.get(email=request.POST['email'])
            msg='email is already registered'
            return render(request,'login.html',{'msg':msg})
        except: 
            if len(request.POST['password']) > 7:
                if request.POST['password'] == request.POST['cpassword']:
                    otp=randrange(1000,9999)
                    message = f"""Hello {request.POST['name']},
                    Your OTP is {otp}"""
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [request.POST['email'],]
                    send_mail( "your registration request otp", message, email_from, recipient_list ) 
                    global data
                    data = {
                        "name" : request.POST['name'],
                        "email" : request.POST['email'],
                        "mobile" : request.POST['mobile'],
                        "doc" : request.POST['doc'],
                        "doc_number" : request.POST['doc_number'],
                        "address" : request.POST['address'],
                        "password" : request.POST['password'],
                    }
                    return render(request,'otp.html',{'otp':otp})
                
                return render(request,'register.html',{'msg':'both should be not same'})
            return render(request,'register.html')   
    return render(request,'register.html')

def profile(request):
    
    uid=owner.objects.get(email=request.session['email'])
    
    if request.method == 'POST':
        uid.name=request.POST['name']
        uid.email=request.POST['email']
        uid.mobile=request.POST['mobile']
        uid.address=request.POST['address']
        if 'pic' in request.FILES:
            uid.pic=request.FILES['pic']
        uid.save()    
    return render(request,'profile.html',{'uid':uid})

def tables(request):
    return render(request,'tables.html')

def otp(request):
    if request.method == 'POST':
        if request.POST['otp'] == request.POST['uotp']:
            # data = loads(request.POST['data'])
            # print(type(request.POST['data']))
            # print(type(data))
            global data
            owner.objects.create(
                name = data['name'],
                email = data['email'],
                mobile = data['mobile'],
                password = data['password'],
                doc = data['doc'],
                doc_number = data['doc_number'],
                address = data['address'],
            )
            del data
            return render(request,'login.html',{'msg':'Account is created'})
        return render(request,'otp.html',{'msg':'Invalid OTP','otp':request.POST['otp'],'data':request.POST['data']})

    return render(request,'login.html')

def forgot_password(request):
    
    if request.method == 'POST':
        try:
            uid= owner.objects.get(email=request.POST['email'],)
            password = ''.join(choices('qwyertovghlk34579385',k=8))
            subject = 'Reset Password'
            message = f"""Hello {uid.name},
            Your Password  is {password}"""
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.POST['email'], ]
            send_mail( subject, message, email_from, recipient_list )
            uid.password = password
            uid.save()
            return render(request,'login.html',{'msg':'new password send in your email'})
        except :
            return render(request,'forgot-password.html',{'msg':'your email id not registered'})
    return render(request,'login.html')       
        
        
def logout(request):
    del request.session['email']
    return redirect('login') 

def add_car(request):
    Startpoint=startpoint.objects.all()
    Destination=destination.objects.all()
    
    uid=owner.objects.get(email=request.session['email'])
    
    if request.method == 'POST':
        
        car.objects.create(
            
            uid=uid,
            name=request.POST['name'],
            model=request.POST['model'],
            number=request.POST['number'],
            totalseat=int(request.POST['totalseat']),
            availableseat=int(request.POST['availableseat']),
            price=int(request.POST['price']),
            startpoint=request.POST['startpoint'],
            destination=request.POST['destination'],
            date=request.POST['date'],
            pic=request.FILES['pic'] if 'pic' in request.FILES else None
        
            
        )

        msg='car added successfully'
        return render(request,'add-car.html',{'uid':uid,'msg':msg,'Startpoint':Startpoint,'Destination':Destination})   
    
    return render(request,'add-car.html',{'uid':uid,'Startpoint':Startpoint,'Destination':Destination})

def view_car(request):
   
   uid=owner.objects.get(email=request.session['email'])
   Car=car.objects.filter(uid=uid)
   return render(request,'view-car.html',{'uid':uid,'Car':Car})

def delete(request,pk):
    Car=car.objects.get(id=pk)
    Car.delete()
    return redirect('view-car')

def edit_car(request,pk):
    uid=owner.objects.get(email=request.session['email'])
    Car=car.objects.get(id=pk)
    if request.method == 'POST':
        Car.name=request.POST['name']
        Car.model=request.POST['model']
        Car.number=request.POST['number']
        Car.totalseat=request.POST['totalseat']
        Car.startpoint=request.POST['startpoint']
        Car.destination=request.POST['destination']
        Car.availableseat=request.POST['availableseat']
        Car.price=request.POST['price']
        Car.date=request.POST['date']
        if 'pic' in request.FILES:
            Car.pic=request.FILES['pic']
        Car.save()
        return render(request,'edit-car.html',{'uid':uid,'Car':Car,'msg':'update car details'})
    return render(request,'edit-car.html',{'uid':uid,'Car':Car})

def book_car(request):
    uid=owner.objects.get(email=request.session['email'])
    if request.method == 'POST':
        Book = book.objects.all()              
            
        return render('book-car.html',{'uid':uid,'Book':Book})
    Book=book.objects.filter(journy_status=False)
    return render(request,'book-car.html',{'uid':uid,'Book':Book})

def complate_journy(request,pk):
    uid=owner.objects.get(email=request.session['email'])
    Book=book.objects.get(id=pk)
    Book.journy_status=True
    Book.save()
    return redirect('book-car')

def my_bookcar(request,pk):
    uid=owner.objects.get(email=request.session['email'])
    Book=book.objects.get(id=pk)
    return render(request,'my-bookcar.html',{'Book':Book,'uid':uid})