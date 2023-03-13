from django.shortcuts import render,redirect
from django.contrib import messages
from .models import SeedFarm,FarmStatus
from Expert.models import FarmerProducts
from Home.models import UserData
from Expert.models import FramemerCheckout
from django.contrib.auth.models import User

import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from datetime import datetime

razorpay_client = razorpay.Client(
  auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))



def StartFarm(request):
    farm = SeedFarm.objects.filter(user = request.user)
    farmstatus = []
    for i in farm:
        fm = FarmStatus.objects.filter(Farm = i)
    
    context = {
        "farm":farm,
        # "farmstatus":fm
        
    }
    return render(request,"farmer/startfarm.html",context)

def AddNewSeedFarm(request):
    if request.method == "POST":
        name = request.POST["seed"]
        field = request.POST["farmfields"]
        area = request.POST["area"]
        status = request.POST["status"]
        img = request.FILES["img"]
        
        farm = SeedFarm.objects.create(seedname=name,farmfield=field,framarea=area,framstatus=status,image=img,user=request.user)
        farm.save()
        messages.info(request,"New Seed Farm Created")
        return redirect('StartFarm')
    return redirect('StartFarm')

def FramStatusUpdate(request,pk):
    Farm = SeedFarm.objects.filter(id = pk)
    farm = SeedFarm.objects.get(id = pk)
    if request.method == "POST":
        status = request.POST["status"]
        questions = request.POST['questions']
        FarmStatus.objects.create(Farm=farm,Status=status,questions=questions).save()
        farm.framstatus = status
        farm.save()
        messages.info(request,"Status Updated")   
    
    farmstatus = FarmStatus.objects.filter(Farm = farm) 
    
    context = {
        "Farm":Farm,
        "farmstatus":farmstatus
    }
    return render(request,'farmer/farmstatusupdate.html',context)

def DeleteOpinion(request,pk,hk):
    FarmStatus.objects.get(id =pk).delete()
    messages.info(request,"item deleted")
    return redirect('FramStatusUpdate',pk = hk)

def UpdateAnswer(request,pk):
    farmstatus = FarmStatus.objects.get(id = pk)
    if request.method == "POST":
        ans = request.POST['ans']
        farmstatus.answers = ans
        farmstatus.save()
        return redirect("ExpertHome")
        
    return redirect("ExpertHome")

def FarmProducts(request):
    products = FarmerProducts.objects.all()
    context = {
        "products":products
    }
    return render(request,'farmer/productforfarm.html',context)

def FarmerMybooking(request):
    product = FramemerCheckout.objects.filter(user = request.user)
    return render(request,"farmer/mybooking.html",{'product':product})

def ProductSignleView(request,pk):
    product = FarmerProducts.objects.filter(id = pk)
    # form = UserDetailsForm()
    userdata1 = UserData.objects.filter(user = request.user)
    
    product1 = FarmerProducts.objects.get(id = pk)
    
    
    if request.method == "POST":
        name = request.POST["name"]
        phone = request.POST["phone"]
        city = request.POST["city"]
        state = request.POST["state"]
        house = request.POST["house"]
        
        if UserData.objects.filter(user = request.user).exists():
            userdata = UserData.objects.get(user = request.user)
            userdata1 = UserData.objects.filter(user = request.user)
            
            userdata.name = name
            userdata.phone = phone
            userdata.city = city
            userdata.state = state
            userdata.house = house
            userdata.save()
        else:
            userdata = UserData.objects.create(name = name, house = house,phone = phone,city = city,state = state,user = request.user)
            userdata.save()
        
        checkout = FramemerCheckout.objects.create(product = product1 ,user = request.user,status = "Customer Ordered")
        checkout.save()
        
        return redirect("MakePayment" ,pk =pk)
        
    context = {
        "product":product,
        "userdata1":userdata1,
        "datalen":len(userdata1)
        # "form":form
        
    }
    
    
    
    return render(request,"farmer/farmerproductview.html",context)

def CancelOrderFarmer(request,pk):
    FRCKOT = FramemerCheckout.objects.get(id = pk)
    FRCKOT.status = "Cancelled By User"
    FRCKOT.save()
    messages.info(request,"Item Cancelled")
    return redirect("FarmerMybooking")

def DeleteOrderFarmer(request,pk):
    FramemerCheckout.objects.get(id = pk).delete()
    messages.info(request,"Item Deleted")
    return redirect("FarmerMybooking")
    
    
def MyProducts(request):
    return render(request,"farmer/myproducts.html")


def CustomerView(request,pk):
    user  = User.objects.get(id = pk)
    userdata = UserData.objects.filter(user = user)
    return render(request,'farmer/viewcustomer.html',{"udata":userdata})


def MakePayment(request,pk):
    
    product1 = FarmerProducts.objects.get(id = pk)
    
    currency = 'INR'
    amount = product1.Product_price * 100 # Rs. 200
    

  # Create a Razorpay Order Pyament Integration.....
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                          currency=currency,
                          payment_capture='0'))

  # order id of newly created order.
    razorpay_order_id = razorpay_order["id"]
    callback_url = 'paymenthandler'

  # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url 
    context['slotid'] = "1"
    
    return render(request,"farmer/makepayment.html",context)

@csrf_exempt
def paymenthandler(request):
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
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result is not None:
                amount = 800 * 100 # Rs. 200
                try:
                    print("working 1")
                    razorpay_client.payment.capture(payment_id, amount)
                    return redirect('Success')
          # render success page on successful caputre of payment
                except:
                    print("working 2")
                    return redirect('Success')
                    
                    
          # if there is an error while capturing payment.
            else:
                return render(request, 'paymentfail.html')
        # if signature verification fails.    
        except:
            return HttpResponseBadRequest()
        
      # if we don't find the required parameters in POST data
    else:
  # if other than POST request is made.
        return HttpResponseBadRequest()
    
def Success(request):
    return render(request,'farmer/Paymentconfirm.html')
        



