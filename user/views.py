from random import randrange,choices
from django.shortcuts import render,redirect
from .models import *
from django.conf import settings
from django.core.mail import send_mail
from owner import models as o


def user_index(request):
    return render(request,'user-index.html') 
    
def user_register(request):
    if request.method=='POST':
        try:
            passenger.objects.get(email=request.POST['email'])
            msg='email is already registered'
            return render(request,'user-login.html',{'msg':msg})
        except: 
            #if len(request.POST['password']) > 7:
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
                        "address" : request.POST['address'],
                        "password" : request.POST['password'],
                    }
                    return render(request,'user-otp.html',{'otp':otp})
                
                return render(request,'user-register.html',{'msg':'both should be same'})
               
    return render(request,'user-register.html')

def user_otp(request):
    if request.method == 'POST':
        if request.POST['otp'] == request.POST['uotp']:
            global data
            passenger.objects.create(
                name = data['name'],
                email = data['email'],
                mobile = data['mobile'],
                password = data['password'],
                address = data['address'],
            )
            del data
            return render(request,'user-login.html',{'msg':'Account is created'})
        return render(request,'user-otp.html',{'msg':'Invalid OTP','otp':request.POST['otp'],'data':request.POST['data']})

    return render(request,'user-login.html')

def user_login(request):
    try:
        uid=passenger.objects.get(email=request.session['uemail'])
        return redirect('user-index')
    except :
        if request.method == 'POST':
            try:
                uid=passenger.objects.get(email=request.POST['email'])
                if request.POST['password'] == uid.password:
                    request.session['uemail'] = request.POST['email']
                    return redirect('user-index')
                return render(request,'user-login.html',{'msg':'incorrect password'})
            except:
                msg = 'Email is not register'
                return render(request,'user-login.html',{'msg':msg})
        return render(request,'user-login.html')
    
  
def user_logout(request):
    del request.session['uemail']
    return render(request,'user-login.html')
    
def user_forgotpassword(request):
    if request.method == 'POST':
        try:
            uid= passenger.objects.get(email=request.POST['email'],)
            password = ''.join(choices('qwyertovghlk34579385',k=8))
            subject = 'Reset Password'
            message = f"""Hello {uid.name},
            Your Password  is {password}"""
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.POST['email'], ]
            send_mail( subject, message, email_from, recipient_list )
            uid.password = password
            uid.save()
            return render(request,'user-login.html',{'msg':'new password send in your email'})
        except :
            return render(request,'user-forgotpassword.html',{'msg':'your email id not registered'})
    return render(request,'user-forgotpassword.html')    

def my_profile(request):
    uid=passenger.objects.get(email=request.session['uemail'])
    
    if request.method == 'POST':
        uid.name=request.POST['name']
        uid.email=request.POST['email']
        uid.mobile=request.POST['mobile']
        uid.address=request.POST['address']
        if 'pic' in request.FILES:
            uid.pic=request.FILES['pic']
        uid.save()    
    return render(request,'my-profile.html',{'uid':uid})

def show_car(request):
    car=o.car.objects.all().order_by('?')
    Startpoint=o.startpoint.objects.all()
    Destination=o.destination.objects.all()
    return render(request,'show-car1.html',{'car':car,'Startpoint':Startpoint,'Destination':Destination})

def book_car(request,pk):
    return render(request,'user-index.html')

def search(request):
    if request.method == 'POST':
        query = request.POST['search']
        car = list(car.objects.filter(name=query))
        a = query.split()
        temp = list(car)[0]
        # for i in products:
        pro = list(car.objects.filter(category =temp.category)) + car
        print(list(pro))
        return render(request,'search.html', {'pro':pro})
    return render(request,'search.html')