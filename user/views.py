from random import randrange,choices
from django.shortcuts import render,redirect
from .models import *
from django.conf import settings
from django.core.mail import send_mail
from owner import models as o
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from datetime import date
from random import randrange

def user_index(request): 
    uid = passenger.objects.get(email=request.session['uemail'])
    Car=o.car.objects.all().order_by('?')
    Startpoint=o.startpoint.objects.all()
    Destination=o.destination.objects.all()
    return render(request,'user-index.html',{'uid':uid,'Car':Car,'Startpoint':Startpoint,'Destination':Destination})
    
 
    
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

def search(request):
    Startpoint=startpoint.objects.all()
    Destination=destination.objects.all()
    
    if request.method == 'POST':
        query=request.POST['start']
        Car = list(car.objects.filter(startpoint=query))
        a = query.split()
            
        temp = list(Car)[0::]
        # for i in products:
        pro = list(car.objects.filter(startpoint =car.startpoint)) + Car
        return render(request,'search.html', {'pro':pro,'Startpoint':Startpoint,'Destination': Destination})
    return render(request,'search.html',{'Startpoint':Startpoint,'Destination': Destination})

def userview_car(request,pk):
    Car = o.car.objects.get(id=pk)
    reco = o.car.objects.filter(startpoint=Car.startpoint)[:4]
    return render(request,'userview-car.html',{'Car':Car,'reco':reco})


def  add_watchlist(request,pk):
    try:
        uid = passenger.objects.get(email=request.session['uemail'])
        Car = car.objects.get(id=pk)
        try:
            Cart=cart.objects.get(uid=uid)
            Cart.car.add(Car)
            Cart.save()
        except:
            cart.objects.create(uid=uid)
            Cart = cart.objects.get(uid=uid)
            Cart.car.add(Car)
            Cart.save()

        return render(request,'userview-car.html',{'msg':'Car added','Car':Car})
    except:
        return render(request,'user-login.html')
   


def my_watchlist(request):
    uid = passenger.objects.get(email=request.session['uemail'])
    Cart = cart.objects.get(uid=uid)
    return render(request,'my-watchlist.html',{'uid':uid,'Cart':Cart})

def remove_to_watchlist(request,pk):
    Car=car.objects.get(id=pk)
    uid= passenger.objects.get(email=request.session['uemail'])
    Cart=cart.objects.get(uid=uid)
    Cart.car.remove(Car)
    Cart.save()
    return redirect('my-watchlist')
    


razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
 
 
def book_now(request,pk):
    uid=passenger.objects.get(email=request.session['uemail'])
    Car=car.objects.get(id=pk)
    pr= Car.availableseat*Car.price
    currency = 'INR'
    amount = Car.availableseat*Car.price*100  # Rs. 200
 
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = f'paymenthandler/{Car.id}'
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    context['Car'] = Car
    context['pr']=pr
    context['uid']=uid
    
    
   
    return render(request,'book-now.html', context=context)
 
 
# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request,pk):
 
    # only accept POST request.
    Car=car.objects.get(id=pk)
    uid=passenger.objects.get(email=request.session['uemail'])
    if request.method == "POST":
        
        try:
           
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            
            amount =Car.availableseat*Car.price*100  # Rs. 200
            try:
                Ts=Car.availableseat
                today = date.today()
                razorpay_client.payment.capture(payment_id, amount)
                Car.availableseat -= Car.availableseat
                Car.save()
                book.objects.create(
                    Car=Car,
                    Passenger=uid,
                    pay_id=payment_id,
                    booking_date=today,
                    bookingseat=Ts,
                    amount=amount/100
                )
               
                return render(request, 'user-index.html',{'msg':'payment secces'})
            except:

                # if there is an error while capturing payment.
                return render(request, 'userview-car.html',{'msg':'payment fail'})
            # else:
 
            #     # if signature verification fails.
            #     return render(request, 'paymentfail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest() 
    
def my_booking(request):
    uid = passenger.objects.get(email=request.session['uemail'])
    Book=book.objects.filter(Passenger=uid)      
    emails = list(passenger.objects.values_list('email',flat=True))
    return render(request,'my-booking.html',{'uid':uid,'Book':Book})                     
   
def cancel_booking(request,pk):
    Book=book.objects.get(id=pk)
    Book.journy_status=False
    Book.save()
    Car = car.objects.get(id=Book.Car.id)
    Car.availableseat += Book.bookingseat
    Car.save()
    Book.delete()
    return redirect('my-booking')

    