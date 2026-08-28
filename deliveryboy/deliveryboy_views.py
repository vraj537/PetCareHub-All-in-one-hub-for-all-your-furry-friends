from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from test2.models import DeliveryBoy, Vendor, Order,Area #
from django.contrib import messages
import os
import re

# --- 1. REGISTRATION (Redirects to Login) ---
def delivery_register(request):
    vendors = Vendor.objects.all()
    areas = Area.objects.all()

    if request.method == "POST":
        v_id      = request.POST.get('vendor_id')
        a_id      = request.POST.get('area_id')
        name      = request.POST.get('deliveryboy_name', '').strip()
        email     = request.POST.get('email', '').strip()
        contact   = request.POST.get('contact', '').strip()
        password  = request.POST.get('password', '')
        profile_img = request.FILES.get('deliveryboy_profile')

        # --- SERVER-SIDE VALIDATION START ---

        # 1. Name Validation
        if not (re.match(r'^[A-Za-z\s]+$', name) and len(name) > 1):
            messages.error(request, "Invalid Name: Please use alphabets and spaces only.", extra_tags='del_reg')
            return render(request, 'registration.html', {'vendors': vendors, 'areas': areas})

        # 2. Email Format Validation
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9._%+-]*@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            messages.error(request, "Invalid Email: Must start with a letter (e.g., petcarehub@gmail.com).", extra_tags='del_reg')
            return render(request, 'registration.html', {'vendors': vendors, 'areas': areas})

        # 3. Duplicate Email Check
        if DeliveryBoy.objects.filter(email=email).exists():
            messages.error(request, "This email is already registered!", extra_tags='del_reg')
            return render(request, 'registration.html', {'vendors': vendors, 'areas': areas})

        # 4. Contact Validation
        if not re.match(r'^[6-9]\d{9}$', contact):
            messages.error(request, "Invalid Contact: Must be 10 digits starting with 6, 7, 8, or 9.", extra_tags='del_reg')
            return render(request, 'registration.html', {'vendors': vendors, 'areas': areas})

        # 5. Duplicate Contact Check
        if DeliveryBoy.objects.filter(contact=contact).exists():
            messages.error(request, "This mobile number is already registered.", extra_tags='del_reg')
            return render(request, 'registration.html', {'vendors': vendors, 'areas': areas})

        # 6. Password Validation
        if not re.match(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*_])[A-Za-z\d!@#$%^&*_]{8,16}$', password):
            messages.error(request, "Password must be 8-16 characters with uppercase, lowercase, number, and a special character (!@#$%^&*_).", extra_tags='del_reg')
            return render(request, 'registration.html', {'vendors': vendors, 'areas': areas})

        # 7. Vendor Selection
        if not v_id:
            messages.error(request, "Please select your linked store.", extra_tags='del_reg')
            return render(request, 'registration.html', {'vendors': vendors, 'areas': areas})

        # 8. Area Selection
        if not a_id:
            messages.error(request, "Please select your area.", extra_tags='del_reg')
            return render(request, 'registration.html', {'vendors': vendors, 'areas': areas})

        # 9. Profile Photo Validation
        if profile_img:
            allowed_ext = ['jpg', 'jpeg', 'png']
            ext = profile_img.name.split('.')[-1].lower()
            if ext not in allowed_ext:
                messages.error(request, "Profile photo must be JPG or PNG.", extra_tags='del_reg')
                return render(request, 'registration.html', {'vendors': vendors, 'areas': areas})
            if profile_img.size > 2 * 1024 * 1024:
                messages.error(request, "Profile photo must be under 2MB.", extra_tags='del_reg')
                return render(request, 'registration.html', {'vendors': vendors, 'areas': areas})

        try:
            vendor_obj = Vendor.objects.get(vendor_id=v_id)
            area_obj   = Area.objects.get(area_id=a_id)

            DeliveryBoy.objects.create(
                vendor_id=vendor_obj,
                area_id=area_obj,
                deliveryboy_name=name,
                email=email,
                contact=contact,
                password=make_password(password),
                deliveryboy_profile=profile_img,
                status=0
            )
            messages.success(request, "Registration successful! Please wait for Vendor approval before login.", extra_tags='delivery_login')
            return redirect('delivery_login')

        except Exception as e:
            messages.error(request, f"Registration failed: {str(e)}", extra_tags='del_reg')
            return render(request, 'registration.html', {'vendors': vendors, 'areas': areas})

    return render(request, 'registration.html', {'vendors': vendors, 'areas': areas})

# --- 2. LOGIN ---
def delivery_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            agent = DeliveryBoy.objects.get(email=email)
            if check_password(password, agent.password):
                # Status checks
                if agent.status == 0:
                    messages.error(request, "Your account is pending approval. Please wait for your vendor to approve your account.", extra_tags='delivery_login')
                    return render(request, 'dlogin.html')
                elif agent.status == 2:
                    messages.error(request, "Your account request has been rejected. Please contact your vendor for more details.", extra_tags='delivery_login')
                    return render(request, 'dlogin.html')
                elif agent.status == 3:
                    messages.error(request, "Your account has been restricted. Please contact your vendor for further assistance.", extra_tags='delivery_login')
                    return render(request, 'dlogin.html')

                # Login Success
                request.session['delivery_id'] = agent.deliveryboy_id
                messages.success(request, f"Welcome back, {agent.deliveryboy_name}!", extra_tags='delivery_login')
                return redirect('delivery_dashboard')
            else:
                messages.error(request, "Invalid Password!", extra_tags='delivery_login')
        except DeliveryBoy.DoesNotExist:
            messages.error(request, "Account not found!", extra_tags='delivery_login')
    return render(request, 'dlogin.html')

# --- 3. DASHBOARD ---
def delivery_dashboard(request):
    if 'delivery_id' not in request.session:
        return redirect('delivery_login')

    delivery_id = request.session['delivery_id']
    agent = get_object_or_404(DeliveryBoy, pk=delivery_id)

    # Status check
    if agent.status != 1:
        del request.session['delivery_id']
        if 'delivery_name' in request.session:
            del request.session['delivery_name']
        messages.error(request, "Access Denied: Your account is no longer active. 🚫", extra_tags='danger')
        return redirect('delivery_login')

    # --- POST: Edit Profile ---
    if request.method == 'POST' and 'edit_profile' in request.POST:
        import re
        name = request.POST.get('deliveryboy_name', '').strip()
        contact = request.POST.get('contact', '').strip()

        if not name or not contact:
            messages.error(request, "All fields are required!")
        elif not re.match(r'^[a-zA-Z\s]+$', name):
            messages.error(request, "Name can only contain letters and spaces.")
        elif re.match(r'^(.)\1+$', name.replace(' ', '')):
            messages.error(request, "Please enter a valid name.")
        elif not re.match(r'^[6-9]\d{9}$', contact):
            messages.error(request, "Contact must be 10 digits and start with 6-9.")
        elif DeliveryBoy.objects.filter(contact=contact).exclude(deliveryboy_id=agent.deliveryboy_id).exists():
            messages.error(request, "This contact number is already registered with another account.")
        else:
            agent.deliveryboy_name = name
            agent.contact = contact

            if 'profile_photo' in request.FILES:
                from django.core.files.uploadedfile import InMemoryUploadedFile
                photo = request.FILES['profile_photo']
                allowed = ['image/jpeg', 'image/jpg', 'image/png']
                if photo.content_type in allowed and photo.size <= 2 * 1024 * 1024:
                    agent.deliveryboy_profile = photo
                else:
                    messages.error(request, "Only JPG/PNG allowed, max 2MB.")
                    return redirect('delivery_dashboard')

            agent.save()
            request.session['delivery_name'] = agent.deliveryboy_name
            messages.success(request, "Profile updated successfully! 🐾")

        return redirect('delivery_dashboard')

    from test2.models import OrderDetail

    # Sirf is delivery boy ke assigned orders ke OrderDetails fetch karo
    # detail_status=1 (Assigned) ya 2 (Out for Delivery) wale active tasks hain
    active_details = OrderDetail.objects.filter(
        order_id__deliveryboy_id=agent,   # Is delivery boy ke assigned orders
        vendor_id=agent.vendor_id,        # Sirf apne vendor ke products
        detail_status__in=[1, 2]
    ).select_related(
        'order_id',
        'prod_id',
        'order_id__cust_id',
        'order_id__cust_id__area_id'
    ).order_by('order_id__order_id')

    # Order-wise group karo (ek order ke saare products ek saath)
    from collections import OrderedDict
    order_groups = OrderedDict()
    for detail in active_details:
        oid = detail.order_id.order_id
        if oid not in order_groups:
            order_groups[oid] = {
                'order': detail.order_id,
                'products': [],
                'detail_status': detail.detail_status  # Pehle product ka status
            }
        order_groups[oid]['products'].append({
            'detail': detail,
            'subtotal': detail.price * detail.quantity
        })

    # Completed orders fetch karo (detail_status=3)
    completed_details = OrderDetail.objects.filter(
        order_id__deliveryboy_id=agent,
        vendor_id=agent.vendor_id,        # Sirf apne vendor ke products
        detail_status=3
    ).select_related(
        'order_id',
        'prod_id',
        'order_id__cust_id',
        'order_id__cust_id__area_id',
        'vendor_id'
    ).order_by('-order_id__order_id')

    # Completed orders bhi group karo
    completed_groups = OrderedDict()
    for detail in completed_details:
        oid = detail.order_id.order_id
        if oid not in completed_groups:
            completed_groups[oid] = {
                'order': detail.order_id,
                'products': [],
                'detail_status': detail.detail_status
            }
        completed_groups[oid]['products'].append({
            'detail': detail,
            'subtotal': detail.price * detail.quantity
        })

    completed_count = len(completed_groups)

    context = {
        'agent': agent,
        'order_groups': list(order_groups.values()),        # Active orders
        'completed_groups': list(completed_groups.values()), # Completed orders
        'completed_count': completed_count,
    }
    return render(request, 'delivery_dashboard.html', context)

# --- 4. TOGGLE STATUS & ORDER UPDATES ---
def toggle_status(request):
    if 'delivery_id' not in request.session:
        return redirect('delivery_login')

    from test2.models import OrderDetail
    agent = DeliveryBoy.objects.get(pk=request.session['delivery_id'])

    # Sirf Online → Offline pe check karo
    if agent.is_available == 1:
        # Check: Koi Out for Delivery (detail_status=2) pending hai?
        pending_ofd = OrderDetail.objects.filter(
            order_id__deliveryboy_id=agent,
            vendor_id=agent.vendor_id,
            detail_status=2
        ).count()

        if pending_ofd > 0:
            # Block karo — pending deliveries hain
            messages.error(request, f"⚠️ {pending_ofd} deliver{'y' if pending_ofd == 1 else 'ies'} still Out for Delivery — please complete all deliveries before going offline!")
            return redirect('delivery_dashboard')

    # Safe to toggle
    agent.is_available = 0 if agent.is_available == 1 else 1
    agent.save()
    messages.success(request, f"Status set to {'Online' if agent.is_available == 1 else 'Offline'}.")
    return redirect('delivery_dashboard')

# --- 5. LOGOUT ---
def delivery_logout(request):
    if 'delivery_id' in request.session:
        del request.session['delivery_id']
    if 'delivery_name' in request.session:
        del request.session['delivery_name']
    messages.info(request, "Logged out successfully.")
    return redirect('delivery_login')

def update_delivery_status(request, order_id, new_status):
    if 'delivery_id' not in request.session:
        return redirect('delivery_login')

    from test2.models import OrderDetail
    
    agent = get_object_or_404(DeliveryBoy, pk=request.session['delivery_id'])
    order = get_object_or_404(Order, pk=order_id, deliveryboy_id=agent)

    # Logical check: Status sirf aage badh sakta hai
    # 1 (Assigned) → 2 (Out for Delivery) → 3 (Delivered)
    # Sirf is delivery boy ke vendor ke products update karo
    current_details = OrderDetail.objects.filter(
        order_id=order,
        order_id__deliveryboy_id=agent,
        vendor_id=agent.vendor_id         # Sirf apne vendor ke products
    )

    current_status = current_details.first().detail_status if current_details.exists() else 0

    if new_status == 2 and current_status != 1:
        messages.error(request, "Pehle order pick-up karna zaroori hai!")
        return redirect('delivery_dashboard')

    if new_status == 3 and current_status != 2:
        messages.error(request, "Pehle Out for Delivery karna zaroori hai!")
        return redirect('delivery_dashboard')

    # STEP 1: Is delivery boy ke is order ke saare OrderDetails update karo
    current_details.update(detail_status=new_status)

    # STEP 2: Order.order_status auto-calculate karo
    all_details = OrderDetail.objects.filter(order_id=order)
    all_statuses = list(all_details.values_list('detail_status', flat=True))

    if all(s == 3 for s in all_statuses):
        order.order_status = 3
    elif all(s >= 2 for s in all_statuses):
        order.order_status = 2
    elif all(s >= 1 for s in all_statuses):
        order.order_status = 1
    else:
        order.order_status = 0

    order.save()
    messages.success(request, "Status Updated! 🐾")
    return redirect('delivery_dashboard')

def delivery_change_password(request):
    if 'delivery_id' not in request.session:
        return redirect('delivery_login')

    from django.contrib.auth.hashers import check_password, make_password
    agent = get_object_or_404(DeliveryBoy, pk=request.session['delivery_id'])

    if request.method == 'POST':
        old_pass = request.POST.get('old_password', '')
        new_pass = request.POST.get('new_password', '')
        confirm_pass = request.POST.get('confirm_password', '')

        if not check_password(old_pass, agent.password):
            messages.error(request, "Current password is incorrect.")
        elif new_pass != confirm_pass:
            messages.error(request, "New passwords do not match.")
        elif len(new_pass) < 6 or len(new_pass) > 12:
            messages.error(request, "Password must be between 6 and 12 characters.")
        else:
            agent.password = make_password(new_pass)
            agent.save()
            messages.success(request, "Password updated successfully! 🔒")

    return redirect('delivery_dashboard')

def delivery_contact(request):
    return render(request,'delivery_contact.html')

# - Delivery Boy Password Reset
import random
import re
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password
from test2.models import DeliveryBoy

def delivery_forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        agent = DeliveryBoy.objects.filter(email=email).first()
        if agent:
            otp = str(random.randint(100000, 999999))
            request.session['reset_delivery_email'] = email # Unique session key
            agent.otp = otp
            agent.otp_used = 0
            agent.save()
            
            send_mail(
                subject='PetCareHub - Delivery Boy Reset OTP',
                message=f'Hello {agent.deliveryboy_name},\n\nYour OTP for password reset is: {otp}\n\n- Team PetCareHub 🐾',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )
            messages.success(request, 'OTP sent to your registered email!', extra_tags='delivery_login')
            return redirect('delivery_reset_password_url')
        messages.error(request, 'No DeliveryBoy account found with this email.')
    return render(request, 'delivery_forgot_password.html')

def delivery_reset_password(request):

    # Agar session mein email nahi hai toh forgot page pe bhej do
    e = request.session.get('reset_delivery_email')
    if not e:
        messages.error(request, 'Session expired. Please start again.')
        return redirect('delivery_forgot_password_url')

    if request.method == 'POST':
        otp_entered  = request.POST.get('otp', '').strip()
        new_pass     = request.POST.get('new_password', '').strip()
        confirm_pass = request.POST.get('confirm_password', '').strip()

        # ── Server-side Validations ──────────────────────────────

        # 1. OTP format check
        if not otp_entered.isdigit() or len(otp_entered) != 6:
            messages.error(request, 'OTP must be exactly 6 digits.')
            return render(request, 'delivery_reset_password.html')

        # 2. Password validation
        password_pattern = r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*_])[A-Za-z\d!@#$%^&*_]{8,16}$'
        if not re.match(password_pattern, new_pass):
            messages.error(request, 'Password must be 8-16 characters with uppercase, lowercase, number, and a special character (!@#$%^&*_).')
            return render(request, 'delivery_reset_password.html')

        # 3. Passwords match
        if new_pass != confirm_pass:
            messages.error(request, 'Passwords do not match. Please try again.')
            return render(request, 'delivery_reset_password.html')

        # ── Database Checks ──────────────────────────────────────

        try:
            agent = DeliveryBoy.objects.get(email=e)
        except DeliveryBoy.DoesNotExist:
            messages.error(request, 'Invalid session. Please start again.')
            return redirect('delivery_forgot_password_url')

        # 4. OTP already used check
        if agent.otp_used == 1:
            messages.error(request, 'This OTP has already been used. Please request a new one.')
            return redirect('delivery_forgot_password_url')

        # 5. OTP match check
        if agent.otp != otp_entered:
            messages.error(request, 'Invalid OTP. Please enter the correct OTP.')
            return render(request, 'delivery_reset_password.html')

        # ── All Good: Password Reset ─────────────────────────────

        agent.password = make_password(new_pass)  # Hashed password save karo
        agent.otp_used = 1                         # OTP use ho gaya, block karo
        agent.otp = None                           # OTP clear karo
        agent.save()

        # Session reset email clear karo
        del request.session['reset_delivery_email']

        messages.success(request, 'Password reset successful! Please login with your new password.', extra_tags='delivery_login')
        return redirect('delivery_login')

    return render(request, 'delivery_reset_password.html')