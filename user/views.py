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
    
    return render(request,'user-index.html',{'uid':uid}) 
    
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
    Car=o.car.objects.all().order_by('?')
    Startpoint=o.startpoint.objects.all()
    Destination=o.destination.objects.all()
    return render(request,'show-car.html',{'Car':Car,'Startpoint':Startpoint,'Destination':Destination})

def userview_car(request,pk):
    Car = o.car.objects.get(id=pk)
    reco = o.car.objects.filter(startpoint=Car.startpoint)
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
   
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
def book_now(request,pk):
    Car = car.objects.get(id=pk)
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
    context['product'] = Car
    return render(request, 'payment-book.html', context=context)
@csrf_exempt
def paymenthandler(request,pk):
 
    # only accept POST request.
    if request.method == "POST":
        try:
            Car =car.objects.get(id=pk)
            Passenger = passenger.objects.get(email=request.session['uemail'])
            # get the required parameters from post request.
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
            # if result is None:
            amount = Car.availableseat*Car.price*100 # Rs. 200
            try:
                today = date.today()

                # capture the payemt
                razorpay_client.payment.capture(payment_id, amount)
                Car.avalibaleseat -= 1
                Car.save()
                book.objects.create(
                    Car = car,
                    Passenger =  passenger,
                    pay_id = payment_id,
                    
                )
                # render success page on successful caputre of payment
                return render(request, 'paymentsuccess.html')
            except:

                # if there is an error while capturing payment.
                return render(request, 'paymentfail.html')
            # else:
 
            #     # if signature verification fails.
            #     return render(request, 'paymentfail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()


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
    
