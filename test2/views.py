import email
from urllib import request
from django.shortcuts import render,redirect
from test2.models import Area,Customer,Vet,Vendor,DeliveryBoy,Appointment,ProductCategory,Product,Order,OrderDetail,AppointmentPayment,OrderPayment,Feedback,Gallery,Wishlist,Cart,VetSchedule

# Create your views here.
from django.contrib.auth.hashers import make_password, check_password

def save_secure_user(model_class, data_dict):
    clean_data = dict(data_dict) 
    if 'password' in clean_data:
        clean_data['password'] = make_password(clean_data['password']) # Built-in use ho raha hai
    return model_class.objects.create(**clean_data)

def show(request):
    return render(request,'export-table.html')


def area_table(request):
    items = Area.objects.all()
    return render(request, 'area_table.html', {'items': items})

def customer_table(request):
    items = Customer.objects.all() 
    return render(request, 'customer_table.html', {'items': items})

def vet_table(request):
    items = Vet.objects.all() 
    return render(request, 'vet_table.html', {'items': items})

def vendor_table(request):
    items = Vendor.objects.all() 
    return render(request, 'vendor_table.html', {'items': items})

def update_vendor_status(request, v_id, action):
    # Bina purane logic ko disturb kiye, specific vendor fetch karein
    # 'v_id' vendor ki primary key hai aur 'action' approve/reject/restrict hai
    vendor = get_object_or_404(Vendor, vendor_id=v_id) 
    
    if action == 'approve':
        vendor.status = 1  # 1 ka matlab Approved (Login Allow hoga)
    elif action == 'reject':
        vendor.status = 2  # 2 ka matlab Rejected
    elif action == 'restrict':
        vendor.status = 3  # 3 ka matlab Restricted/Blocked
    elif action == 'removal_request':
        vendor.status = 4  # Admin ko dikhega — Removal Requested

    vendor.save() 
    # Status update hone ke baad wapas vendor_table refresh ho jayegi
    return redirect('vendor_table')

def delete_vendor(request, v_id):
    vendor = get_object_or_404(Vendor, vendor_id=v_id)
    # Physical deletion sirf tab allowed hai jab status 4 ho
    if vendor.status == 4:
        vendor.delete()
    return redirect('vendor_table')

def deliveryboy_table(request):
    items = DeliveryBoy.objects.all() 
    return render(request, 'deliveryboy_table.html', {'items': items})


def appointment_table(request):
    items = Appointment.objects.all() 
    return render(request, 'appointment_table.html', {'items': items})

def productcategory_table(request):
    items = ProductCategory.objects.all() 
    return render(request, 'productcategory_table.html', {'items': items})


def product_table(request):
    items = Product.objects.all() 
    return render(request, 'product_table.html', {'items': items})

def order_table(request):
    items = Order.objects.all() 
    return render(request, 'order_table.html', {'items': items})

def orderdetail_table(request):
    items = OrderDetail.objects.all() 
    return render(request, 'orderdetail_table.html', {'items': items})

def appointmentpayment_table(request):
    items = AppointmentPayment.objects.all() 
    return render(request, 'appointmentpayment_table.html', {'items': items})

def orderpayment_table(request):
    items = OrderPayment.objects.all() 
    return render(request, 'orderpayment_table.html', {'items': items})

def feedback_table(request):
    items = Feedback.objects.all() 
    return render(request, 'feedback_table.html', {'items': items})

def gallery_table(request):
    items = Gallery.objects.all() 
    return render(request, 'gallery_table.html', {'items': items})

def wishlist_table(request):
    items = Wishlist.objects.all() 
    return render(request, 'wishlist_table.html', {'items': items})


def cart_table(request):
    items = Cart.objects.all() 
    return render(request, 'cart_table.html', {'items': items})

import sys
from test2.forms import updatearea
def update_area_table(request,id):
    e = Area.objects.get(area_id=id)
    if request.method == "POST":
        try:
            form = updatearea(request.POST, instance=e)
            print("------------------", form.errors)
            if form.is_valid():
                form.save()
                return redirect("/area_table/")
            else:
                # Form invalid — wapas edit page pe bhejo with errors
                return render(request, 'update_area_table.html', {'e': e, 'form': form})
        except:
            print("---------------------", sys.exc_info())
            return render(request, 'update_area_table.html', {'e': e})
    else:
        form = updatearea(instance=e)
        return render(request, 'update_area_table.html', {'e': e})


def area_delete(request,id):
    e = Area.objects.get(area_id=id)
    e.delete()
    return redirect('/area_table/')

from test2.forms import updateproductcategory
def update_productcategory_table(request,id):
    e = ProductCategory.objects.get(category_id=id)
    if request.method == "POST":
        try:
             form = updateproductcategory(request.POST,instance=e)
             print("------------------",form.errors)

             if form.is_valid():
                 form.save()
                 return redirect("/productcategory_table/")          
        except:
            print("---------------------",sys.exc_info())
    else:
        form = updateproductcategory(instance=e)
        return render(request,'update_productcategory_table.html',{'e':e})


def productcategory_delete(request,id):
    e = ProductCategory.objects.get(category_id=id)
    e.delete()
    return redirect('/productcategory_table/')

import sys
from test2.forms import updateproduct
def update_product_table(request, id):
    # Using .get() as you requested
    e = Product.objects.get(prod_id=id)
    
    if request.method == "POST":
        try:
            
            form = updateproduct(request.POST, instance=e)
            
            if form.is_valid():
                form.save()
                return redirect("/product_table/")
            else:
                
                print("------------------", form.errors)
        except:
            print("---------------------", sys.exc_info())
    else:
        form = updateproduct(instance=e)
    return render(request, 'update_product_table.html', {'e': e})

def product_delete(request,id):
    e = Product.objects.get(prod_id=id)
    e.delete()
    return redirect('/product_table/')

import sys
from test2.forms import updategallery
def update_gallery_table(request, id):
    e = Gallery.objects.get(gallery_id=id)
    
    if request.method == "POST":
        try:
            form = updategallery(request.POST, instance=e)
            
            print("------------------", form.errors)

            if form.is_valid():
                form.save()
                return redirect("/gallery_table/")
        except:
            print("---------------------", sys.exc_info())
    else:
        form = updategallery(instance=e)
    return render(request, 'update_gallery_table.html', {'e': e, 'form': form})

def gallery_delete(request,id):
    e = Gallery.objects.get(gallery_id=id)
    e.delete()
    return redirect('/gallery_table/')

import sys
from test2.forms import updatearea
def insert_area_table(request):
    e = Area.objects.all()
    if request.method == "POST":
        try:
             form = updatearea(request.POST)
             print("------------------",form.errors)

             if form.is_valid():
                 form.save()
                 return redirect("/area_table/")          
        except:
            print("---------------------",sys.exc_info())
    else:
        form = updatearea()
        return render(request,'insert_area_table.html')
    
from test2.forms import updateproductcategory
def insert_productcategory_table(request):
    e = ProductCategory.objects.all()
    if request.method == "POST":
        try:
             form = updateproductcategory(request.POST)
             print("------------------",form.errors)

             if form.is_valid():
                 form.save()
                 return redirect("/productcategory_table/")          
        except:
            print("---------------------",sys.exc_info())
    else:
        form = updateproductcategory()
        return render(request,'insert_productcategory_table.html')
    
import sys
from test2.forms import updateproduct
def insert_product_table(request):
    categories = ProductCategory.objects.all()
    vendors = Vendor.objects.all()
    if request.method == "POST":
        try:
            form = updateproduct(request.POST) 
            if form.is_valid():
                form.save()
                return redirect("/product_table/")
            else:
                print("--- PRODUCT ERRORS ---", form.errors)
        except:
            print("--- SYSTEM ERROR ---", sys.exc_info())
    else:
        form = updateproduct()
    return render(request, 'insert_product_table.html', {'categories': categories,'vendors': vendors})

def insert_gallery_table(request):
    p = Product.objects.all()
    e = Gallery.objects.all()
    if request.method == "POST":
        try:
            form = updategallery(request.POST, request.FILES)
            print("------------------", form.errors)
            if form.is_valid():
                form.save()
                return redirect("/gallery_table/")          
        except:
            print("---------------------", sys.exc_info())
    else:
        form = updategallery()
    return render(request, 'insert_gallery_table.html', {'products':p})

from django.db.models import Sum
from test2.models import Product,Appointment,AppointmentPayment,OrderPayment,Order,Appointment

def dashboard(request):
    product_count = Product.objects.count()
    appointment_count = Appointment.objects.count()
    items = Order.objects.all() 
    e = Appointment.objects.all()
    appointment_total = AppointmentPayment.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    order_total = OrderPayment.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    return render(request, 'dashboard.html',{'product_count':product_count,'appointment_count':appointment_count,'appointment_payment':appointment_total,'order_payment':order_total,'items':items,'e':e})


from django.contrib import messages
from django.core.mail import send_mail
import random
from django.conf import settings
from django.contrib.auth.hashers import check_password

def login(request):
    if request.method == "POST":
        e = request.POST.get('email')
        p = request.POST.get('password')
        
        
        user = Customer.objects.filter(email=e, is_admin=1).first()
        
        if user:
            if user.password == p or check_password(p, user.password):
                request.session['admin_id'] = user.cust_id
                request.session['admin_email'] = user.email
                messages.success(request, "Welcome back, Admin! You have successfully logged into the dashboard.")
                
                return redirect('dashboard')
            else:
                messages.error(request,"Invalid Password")
                return redirect('login')
        else:
            messages.error(request, "Invalid Admin Credentials or Access Denied")
            return redirect('login')

    return render(request, 'auth-login.html')


def forgotpass(request):
    if request.method == 'POST':
        e = request.POST.get('email')
        admin_user = Customer.objects.filter(email=e, is_admin=1).first()

        if admin_user:
            otp1 = random.randint(100000, 999999)
            request.session['temail'] = e 
            
            
            Customer.objects.filter(email=e).update(otp=otp1, otp_used=0)

            
            subject = 'Admin Password Reset OTP'
            message = f'Your Admin OTP is: {otp1}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [e]
            send_mail(subject, message, email_from, recipient_list)

            return render(request, 'auth-reset-password.html')
        else:
            messages.error(request, "Admin email not found.")
            
    return render(request, 'auth-forgot-password.html')

from django.contrib.auth.hashers import make_password

def resetpassword(request):
    if request.method == "POST":
        e = request.session.get('temail')
        otp_entered = request.POST.get('otp')
        new_pass = request.POST.get('password')
        confirm_pass = request.POST.get('confirm-password')

        if new_pass != confirm_pass:
            messages.error(request, "Passwords do not match!")
            return render(request, 'auth-reset-password.html')

        
        user = Customer.objects.filter(email=e, otp=otp_entered, otp_used=0).first()
        
        if user:
            hashed_p = make_password(new_pass)
            Customer.objects.filter(email=e).update(password=hashed_p, otp_used=1)
            messages.success(request, "Admin password updated! Please login.")
            return redirect('login')
        else:
            messages.error(request, "Invalid OTP.")

    return render(request, 'auth-reset-password.html')


import re
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Customer

def profile(request):
    # Session se ID fetch karein
    aid = request.session.get('admin_id') 
    user = Customer.objects.get(cust_id=aid)

    if request.method == 'POST':
        # --- Photo Update Logic (Bina baaki logic ko chede) ---
        if 'user_profile' in request.FILES:
            user.user_profile = request.FILES['user_profile']
            user.save()
            messages.success(request, "Profile picture updated successfully!")
            return redirect('profile')

        # --- Aapka Existing Logic ---
        name = request.POST.get('txtname', '').strip() 
        email = request.POST.get('txtemail', '').strip()
        phone = request.POST.get('txtphone', '').strip()
        address = request.POST.get('txtaddress', '').strip()
        
        # 1. Name Validation
        if not re.match(r'^[a-zA-Z\s]+$', name):
            messages.error(request, "Update failed: Name should only contain letters.")
            return redirect('profile')

        # 2. Email Format Validation
        if not re.match(r'^[A-Za-z0-9][A-Za-z0-9._%+-]*@[a-z0-9.-]+\.[a-z]{2,3}$', email):
            messages.error(request, "Update failed: Invalid email format.")
            return redirect('profile')

        # 3. Duplicate Email Check
        if Customer.objects.filter(email=email).exclude(cust_id=aid).exists():
            messages.error(request, "Update failed: This email is already used by another user.")
            return redirect('profile')

        # 4. Phone/Contact Validation
        if not re.match(r'^\d{10}$', phone):
            messages.error(request, "Update failed: Contact must be exactly 10 digits.")
            return redirect('profile')

        # 5. Address Check
        if not address:
            messages.error(request, "Update failed: Address cannot be empty.")
            return redirect('profile')

        # Update Database
        Customer.objects.filter(cust_id=aid).update(
            cust_name=name,
            email=email,
            contact=phone,
            address=address
        )
        messages.success(request, "Your profile has been updated successfully!")
        return redirect('profile')

    return render(request, 'profile.html', {'user': user})

import sys
from django.shortcuts import redirect
from django.contrib import messages

def logout(request):
    try:

        if 'admin_id' in request.session:
            del request.session['admin_id']
        if 'admin_email' in request.session:
            del request.session['admin_email']
            
        request.session.flush() 
        
        messages.success(request, "You have been logged out successfully. See you soon!")
        
        return redirect('login') 
    except:
        print("---------- logout error:", sys.exc_info())
        return redirect('login')
    

from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages

def change_password(request):
    aid = request.session.get('admin_id')
    if not aid:
        return redirect('login')
    
    user = Customer.objects.get(cust_id=aid)

    if request.method == 'POST':
        old_pass = request.POST.get('old_password')
        new_pass = request.POST.get('new_password')
        confirm_pass = request.POST.get('confirm_password')

        # 1. Verify Current Password
        if not (user.password == old_pass or check_password(old_pass, user.password)):
            messages.error(request, "The current password you entered is incorrect.")
        
        # 2. Check if New Passwords Match
        elif new_pass != confirm_pass:
            messages.error(request, "New password and confirmation do not match.")
        
        # 3. Strength Check (Example: Minimum 6 characters)
        elif len(new_pass) < 6:
            messages.error(request, "New password must be at least 6 characters long.")
            
        else:
            # 4. Hash and Update
            hashed_p = make_password(new_pass)
            Customer.objects.filter(cust_id=aid).update(password=hashed_p)
            messages.success(request, "Your password has been changed successfully!")
            return redirect('profile')

    return redirect('profile')
from django.shortcuts import redirect, get_object_or_404
from .models import Vet

def update_vet_status(request, v_id, action):
    # Use get_object_or_404 for safety
    vet = get_object_or_404(Vet, vet_id=v_id)
    
    if action == 'approve':
        vet.status = 1
    elif action == 'reject':
        vet.status = 2
    elif action == 'restrict':
        # Status 3 (Banned) forces Availability to Offline (0)
        vet.status = 3
        vet.availability_status = 0
    elif action == 'remove':
        # Status 4 (Removal Request) forces Availability to Offline (0)
        vet.status = 4
        vet.availability_status = 0 
    
    vet.save()
    return redirect('vet_table')

def delete_vet(request, v_id):
    vet = get_object_or_404(Vet, vet_id=v_id)
    # Physical database deletion only allowed if status is 4
    if vet.status == 4:
        vet.delete()
    return redirect('vet_table')

def vet_schedule_table(request):
    items = VetSchedule.objects.all()
    return render(request, 'vet_schedule.html', {'items': items})

def update_customer_status(request, c_id, action):
    customer = get_object_or_404(Customer, cust_id=c_id)
    
    if customer.is_admin == 1:
        return redirect('customer_table')

    if action == 'restrict':
        customer.is_admin = 2   # Restricted customer
    elif action == 'reactivate':
        customer.is_admin = 0   # Wapas normal customer

    customer.save()
    return redirect('customer_table')