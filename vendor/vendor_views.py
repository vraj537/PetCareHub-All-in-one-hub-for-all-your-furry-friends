from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from test2.models import Vendor, Area  #

def vendor_register(request):
    areas = Area.objects.all()

    if request.method == "POST":
        v_name    = request.POST.get('vendor_name', '').strip()
        v_email   = request.POST.get('email', '').strip()
        v_pass    = request.POST.get('password', '')
        v_contact = request.POST.get('contact', '').strip()
        v_address = request.POST.get('address', '').strip()
        v_area    = request.POST.get('area_id')
        v_profile = request.FILES.get('vendor_profile')

        # --- SERVER-SIDE VALIDATION START ---

        # 1. Name Validation
        if not (re.match(r'^[A-Za-z\s]+$', v_name) and len(v_name) > 1):
            messages.error(request, "Invalid Name: Please use alphabets and spaces only.", extra_tags='vendor_reg')
            return render(request, 'vendor_register.html', {'areas': areas})

        # 2. Email Format Validation
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9._%+-]*@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v_email):
            messages.error(request, "Invalid Email: Must start with a letter and follow standard format(e.g., petcarehub@gmail.com).", extra_tags='vendor_reg')
            return render(request, 'vendor_register.html', {'areas': areas})

        # 3. Duplicate Email Check
        if Vendor.objects.filter(email=v_email).exists():
            messages.error(request, "This email is already registered. Please login.", extra_tags='vendor_reg')
            return render(request, 'vendor_register.html', {'areas': areas})

        # 4. Contact Validation
        if not re.match(r'^[6-9]\d{9}$', v_contact):
            messages.error(request, "Invalid Contact: Must be 10 digits starting with 6, 7, 8, or 9.", extra_tags='vendor_reg')
            return render(request, 'vendor_register.html', {'areas': areas})

        # 5. Duplicate Contact Check
        if Vendor.objects.filter(contact=v_contact).exists():
            messages.error(request, "This mobile number is already registered. Please use a different one.", extra_tags='vendor_reg')
            return render(request, 'vendor_register.html', {'areas': areas})

        # 6. Password Validation
        if not re.match(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*_])[A-Za-z\d!@#$%^&*_]{8,16}$', v_pass):
            messages.error(request, "Password must be 8-16 characters with uppercase, lowercase, number, and a special character (!@#$%^&*_).", extra_tags='vendor_reg')
            return render(request, 'vendor_register.html', {'areas': areas})

        # 7. Address Validation
        if len(v_address) < 10:
            messages.error(request, "Address must be at least 10 characters.", extra_tags='vendor_reg')
            return render(request, 'vendor_register.html', {'areas': areas})

        # 8. Area Validation
        if not v_area:
            messages.error(request, "Please select your area.", extra_tags='vendor_reg')
            return render(request, 'vendor_register.html', {'areas': areas})

        # 9. Profile Photo Validation
        if v_profile:
            allowed_ext = ['jpg', 'jpeg', 'png']
            ext = v_profile.name.split('.')[-1].lower()
            if ext not in allowed_ext:
                messages.error(request, "Profile photo must be JPG or PNG.", extra_tags='vendor_reg')
                return render(request, 'vendor_register.html', {'areas': areas})
            if v_profile.size > 2 * 1024 * 1024:
                messages.error(request, "Profile photo must be under 2MB.", extra_tags='vendor_reg')
                return render(request, 'vendor_register.html', {'areas': areas})

        try:
            area_obj = Area.objects.get(area_id=v_area)

            Vendor.objects.create(
                vendor_name=v_name,
                email=v_email,
                password=make_password(v_pass),
                contact=v_contact,
                address=v_address,
                area_id=area_obj,
                vendor_profile=v_profile,
                status=0
            )
            messages.success(request, "Registration successful! Please wait for Admin approval.", extra_tags='vendor_login')
            return redirect('vendor_login')

        except Exception as e:            
            messages.error(request, f"Registration failed: {str(e)}", extra_tags='vendor_reg')
            return render(request, 'vendor_register.html', {'areas': areas})

    return render(request, 'vendor_register.html', {'areas': areas})

from django.contrib.auth.hashers import check_password
def vendor_login(request):
    if request.method == "POST":
        v_email = request.POST.get('email')
        v_pass = request.POST.get('password')

        try:
            # Email se vendor ko dhundho
            vendor = Vendor.objects.get(email=v_email)

            # 1. Password check karo
            if check_password(v_pass, vendor.password):
                
                # 2. Status check karo (Sirf Approved vendor hi login kar sakega)
                if vendor.status == 1:
                    request.session['vendor_id'] = vendor.vendor_id
                    request.session['vendor_name'] = vendor.vendor_name
                    messages.success(request, f"Welcome back, {vendor.vendor_name}!", extra_tags='vendor_login')
                    return redirect('vendor_dashboard') # Apne dashboard ka naam check kar lena
                
                # - vendor_login function ke andar ye update karein
                elif vendor.status == 0:
                    messages.error(request, "Your account is pending for Admin approval.", extra_tags='vendor_login')
                elif vendor.status == 2:
                    messages.error(request, "Your approval request was rejected.", extra_tags='vendor_login')
                elif vendor.status == 3:
                    messages.error(request, "Your account has been restricted by Admin.", extra_tags='vendor_login')
                elif vendor.status == 4:
                    messages.error(request, "Your account removal is under process by Admin.", extra_tags='vendor_login')
                
            else:
                messages.error(request, "Invalid Password!", extra_tags='vendor_login')
        
        except Vendor.DoesNotExist:
            messages.error(request, "No account found with this email!", extra_tags='vendor_login')

    return render(request, 'vendor_login.html')

from django.shortcuts import render, redirect, get_object_or_404
from test2.models import Vendor, Product, ProductCategory, Gallery,DeliveryBoy,Order,OrderDetail #
from django.db.models import Count, Q, Sum, F

def vendor_dashboard(request):
    if 'vendor_id' not in request.session:
        messages.error(request, "Please login first!", extra_tags='vendor_login')
        return redirect('vendor_login')

    vendor = get_object_or_404(Vendor, vendor_id=request.session['vendor_id'])
    
    all_boys = DeliveryBoy.objects.filter(vendor_id=vendor)

    # Database se categories uthao dropdown ke liye
    categories = ProductCategory.objects.all()
    # Vendor ke purane products list karne ke liye
    my_products = Product.objects.filter(vendor_id=vendor).order_by('-prod_id')

    if request.method == "POST":
        # --- A. PRODUCT UPLOAD LOGIC ---
        if 'add_product' in request.POST:
            p_name = request.POST.get('p_name')
            p_cat_id = request.POST.get('p_category')
            p_price = request.POST.get('p_price')
            p_qty = request.POST.get('p_qty')
            p_desc = request.POST.get('p_desc')
            p_cover = request.FILES.get('p_cover') # Main Image
            p_gallery = request.FILES.getlist('p_gallery') # Multiple Gallery Images

            # Price validation
            try:
                p_price_int = int(p_price)
                if p_price_int < 1 or p_price_int > 99999:
                    messages.error(request, "Price must be between ₹1 and ₹99,999.", extra_tags='vendor_login')
                    return redirect('vendor_dashboard')
            except (ValueError, TypeError):
                messages.error(request, "Invalid price entered.", extra_tags='vendor_login')
                return redirect('vendor_dashboard')

            # Qty validation
            try:
                p_qty_int = int(p_qty)
                if p_qty_int < 0 or p_qty_int > 999:
                    messages.error(request, "Stock quantity must be between 0 and 999.", extra_tags='vendor_login')
                    return redirect('vendor_dashboard')
            except (ValueError, TypeError):
                messages.error(request, "Invalid quantity entered.", extra_tags='vendor_login')
                return redirect('vendor_dashboard')

            try:
                # Category object fetch karo
                cat_obj = ProductCategory.objects.get(category_id=p_cat_id)
                
                # 1. Product save karo
                new_prod = Product.objects.create(
                    vendor_id=vendor,
                    category_id=cat_obj,
                    prod_name=p_name,
                    price=p_price,
                    qty=p_qty,
                    description=p_desc,
                    cover_img_path=p_cover
                )

                # 2. Gallery images save karo
                for img in p_gallery:
                    Gallery.objects.create(prod_id=new_prod, image_path=img)

                messages.success(request, "Product listed successfully!", extra_tags='vendor_login')
                return redirect('vendor_dashboard')
            except Exception as e:
                messages.error(request, f"Upload failed: {e}")

        # --- B. PROFILE UPDATE LOGIC ---
        elif 'vendor_name' in request.POST:
            import re
            v_name = request.POST.get('vendor_name', '').strip()
            v_contact = request.POST.get('contact', '').strip()
            v_address = request.POST.get('address', '').strip()

            # Name validation: only letters/spaces, no repeated single char (e.g. ddddd)
            if not re.match(r'^[a-zA-Z\s]+$', v_name):
                messages.error(request, "Name can only contain letters and spaces.", extra_tags='vendor_login')
                return redirect('vendor_dashboard')
            if re.match(r'^(.)\1+$', v_name.replace(' ', '')):
                messages.error(request, "Please enter a valid name.", extra_tags='vendor_login')
                return redirect('vendor_dashboard')

            # Contact: 10 digits, starts with 6-9
            if not re.match(r'^[6-9]\d{9}$', v_contact):
                messages.error(request, "Contact must be 10 digits and start with 6-9.", extra_tags='vendor_login')
                return redirect('vendor_dashboard')

            # Contact duplicate check (exclude current vendor)
            if Vendor.objects.filter(contact=v_contact).exclude(vendor_id=vendor.vendor_id).exists():
                messages.error(request, "This contact number is already registered with another account.", extra_tags='vendor_login')
                return redirect('vendor_dashboard')

            if 'vendor_profile' in request.FILES:
                vendor.vendor_profile = request.FILES['vendor_profile']

            vendor.vendor_name = v_name
            vendor.contact = v_contact
            vendor.address = v_address
            vendor.save()
            request.session['vendor_name'] = vendor.vendor_name
            messages.success(request, "Profile updated successfully!", extra_tags='vendor_login')
            return redirect('vendor_dashboard')

    # OrderDetail se fetch karo aur order_id ke basis pe group karo
    raw_details = OrderDetail.objects.filter(
        vendor_id=vendor
    ).select_related(
        'order_id',
        'prod_id',
        'order_id__cust_id',
        'order_id__cust_id__area_id',
        'order_id__deliveryboy_id'
    ).order_by('-order_id__order_id')

    # Active orders (0,1,2), Delivered (3), Cancelled (4) alag karo
    active_grouped = {}
    delivered_grouped = {}
    cancelled_grouped = {}

    for detail in raw_details:
        oid = detail.order_id.order_id

        if detail.detail_status == 4:
            # Cancelled orders
            if oid not in cancelled_grouped:
                cancelled_grouped[oid] = {
                    'order': detail.order_id,
                    'products': [],
                    'detail_status': detail.detail_status
                }
            cancelled_grouped[oid]['products'].append({
                'detail': detail,
                'subtotal': detail.price * detail.quantity
            })
        elif detail.detail_status == 3:
            # Delivered orders
            if oid not in delivered_grouped:
                delivered_grouped[oid] = {
                    'order': detail.order_id,
                    'products': [],
                    'detail_status': detail.detail_status
                }
            delivered_grouped[oid]['products'].append({
                'detail': detail,
                'subtotal': detail.price * detail.quantity
            })
        else:
            # Active orders (0, 1, 2)
            if oid not in active_grouped:
                active_grouped[oid] = {
                    'order': detail.order_id,
                    'products': [],
                    'detail_status': detail.detail_status
                }
            active_grouped[oid]['products'].append({
                'detail': detail,
                'subtotal': detail.price * detail.quantity
            })

    # Lists mein convert karo
    order_groups = list(active_grouped.values())
    delivered_groups = list(delivered_grouped.values())
    cancelled_groups = list(cancelled_grouped.values())   # NEW
    delivered_count = len(delivered_groups)
    cancelled_count = len(cancelled_groups)               # NEW

    # Stats calculate karo
    # Total Sales: sirf delivered orders ke products ka sum
    from django.db.models import Sum
    total_sales = OrderDetail.objects.filter(
        vendor_id=vendor,
        detail_status=3
    ).aggregate(
        total=Sum(F('price') * F('quantity'))
    )['total'] or 0

    # Orders fulfilled = delivered orders count
    orders_fulfilled = delivered_count

    # Sirf approved delivery boys (status=1)
    # Har approved online boy ke liye active OrderDetail count karo
    # detail_status 1 (Assigned) ya 2 (Out for Delivery) wale count honge
    approved_boys = DeliveryBoy.objects.filter(
        vendor_id=vendor,
        status=1,
        is_available=1
    ).annotate(
        active_order_count=Count(
            'order',
            filter=Q(order__orderdetail__detail_status__in=[1, 2])
        )
    )

    # Reviews: is vendor ke har product ke liye feedback fetch karo
    from test2.models import Feedback
    vendor_products = Product.objects.filter(vendor_id=vendor)
    
    # Har product ke liye uski reviews group karke bhejo
    product_reviews = []
    for prod in vendor_products:
        reviews = Feedback.objects.filter(
            prod_id=prod,
            prod_id__isnull=False
        ).select_related('cust_id').order_by('-feedback_date')
        product_reviews.append({
            'product': prod,
            'reviews': reviews,
            'review_count': reviews.count(),
        })

    return render(request, 'vendor_dashboard.html', {
        'vendor': vendor,
        'categories': categories,
        'products': my_products,
        'all_boys': all_boys,
        'order_groups': order_groups,
        'delivered_groups': delivered_groups,
        'delivered_count': delivered_count,
        'cancelled_groups': cancelled_groups,
        'cancelled_count': cancelled_count,
        'approved_boys': approved_boys,
        'total_sales': total_sales,
        'orders_fulfilled': orders_fulfilled,
        'product_reviews': product_reviews,   # NEW
    })

def update_db_status(request, db_id, new_status):
    if 'vendor_id' not in request.session:
        return redirect('vendor_login')
    
    boy = get_object_or_404(DeliveryBoy, deliveryboy_id=db_id)

    # STRICT LOGIC: Rejected (2) case closed hai, koi badlav nahi hoga
    if boy.status == 2:
        messages.error(request, f"Access Denied: {boy.deliveryboy_name} is already Rejected.", extra_tags='vendor_login')
        return redirect('vendor_dashboard')

    # Status update karo
    boy.status = new_status
    boy.save()
    
    # Sirf wahi messages rakhe hain jo actually trigger honge
    status_msgs = {
        1: f"{boy.deliveryboy_name} is now Active! ✅",
        2: f"{boy.deliveryboy_name} Registration Rejected. ❌",
        3: f"{boy.deliveryboy_name} is now Restricted. 🚫"
    }
    
    # Reactivate ke liye special message
    if new_status == 1 and boy.status == 3:
        msg = f"{boy.deliveryboy_name} Reactivated successfully! 🔄"
    else:
        msg = status_msgs.get(new_status, "Status Updated!")

    messages.success(request, msg, extra_tags='vendor_login')
    return redirect('vendor_dashboard')

from test2.models import Order, OrderDetail, DeliveryBoy
from datetime import date

def assign_order(request):
    # --- LOGIN CHECK ---
    if 'vendor_id' not in request.session:
        return redirect('vendor_login')

    if request.method == "POST":
        order_id = request.POST.get('order_id')
        boy_id = request.POST.get('delivery_boy')
        delivery_date = request.POST.get('delivery_date')
        vendor_id = request.session['vendor_id']

        try:
            order = get_object_or_404(Order, order_id=order_id)
            boy = get_object_or_404(DeliveryBoy, deliveryboy_id=boy_id)
            vendor = get_object_or_404(Vendor, vendor_id=vendor_id)

            # STEP 1: Is vendor ke OrderDetails ka detail_status 1 karo
            OrderDetail.objects.filter(
                order_id=order,
                vendor_id=vendor
            ).update(detail_status=1)  # 1: Assigned

            # STEP 2: Delivery boy assign karo order pe
            order.deliveryboy_id = boy

            # STEP 3: Delivery date update karo
            if delivery_date:
                order.delivery_date = delivery_date

            order.save()

            messages.success(request, f"Order #{order_id} assigned to {boy.deliveryboy_name}! ✅", extra_tags='vendor_login')

        except Exception as e:
            print(f"--- ASSIGN ORDER ERROR: {e} ---")
            messages.error(request, f"Something went wrong: {str(e)}", extra_tags='vendor_login')

    return redirect('vendor_dashboard')

def update_product_qty(request, prod_id):
    if 'vendor_id' not in request.session:
        return redirect('vendor_login')

    vendor = get_object_or_404(Vendor, vendor_id=request.session['vendor_id'])
    product = get_object_or_404(Product, prod_id=prod_id, vendor_id=vendor)

    if request.method == 'POST':
        new_qty = request.POST.get('new_qty')
        try:
            new_qty = int(new_qty)
            if new_qty < 0 or new_qty > 999:
                raise ValueError
            product.qty = new_qty
            product.save()
            messages.success(request, f"Qty for '{product.prod_name}' updated to {new_qty}! ✅", extra_tags='vendor_login')
        except (ValueError, TypeError):
            messages.error(request, "Invalid quantity entered.", extra_tags='vendor_login')

    return redirect('vendor_dashboard')


def delete_product(request, prod_id):
    if 'vendor_id' not in request.session:
        return redirect('vendor_login')

    vendor = get_object_or_404(Vendor, vendor_id=request.session['vendor_id'])
    product = get_object_or_404(Product, prod_id=prod_id, vendor_id=vendor)

    if request.method == 'POST':
        prod_name = product.prod_name
        product.delete()
        messages.success(request, f"'{prod_name}' has been permanently deleted. 🗑️", extra_tags='vendor_login')

    return redirect('vendor_dashboard')


def vendor_change_password(request):
    if 'vendor_id' not in request.session:
        return redirect('vendor_login')

    from django.contrib.auth.hashers import check_password, make_password

    vendor = get_object_or_404(Vendor, vendor_id=request.session['vendor_id'])

    if request.method == 'POST':
        old_pass = request.POST.get('old_password', '')
        new_pass = request.POST.get('new_password', '')
        confirm_pass = request.POST.get('confirm_password', '')

        if not check_password(old_pass, vendor.password):
            messages.error(request, "Current password is incorrect.", extra_tags='vendor_security')
        elif new_pass != confirm_pass:
            messages.error(request, "New passwords do not match.", extra_tags='vendor_security')
        elif len(new_pass) < 6  or len(new_pass) > 12:
            messages.error(request, "Password must be between 6 and 12 characters.")
        else:
            vendor.password = make_password(new_pass)
            vendor.save()
            messages.success(request, "Password updated successfully! 🔒", extra_tags='vendor_security')

    return redirect('vendor_dashboard')

def vendor_logout(request):
    if 'vendor_id' in request.session:
        del request.session['vendor_id']
        del request.session['vendor_name']
    return redirect('vendor_login')

def vendor_contact(request):
    if 'vendor_id' not in request.session:
        return redirect('vendor_login')

    return render(request, 'vendor_contact.html')

# - Vendor Password Reset Logic
import random
import re
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password
from test2.models import Vendor

def vendor_forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        vendor = Vendor.objects.filter(email=email).first()
        if vendor:
            otp = str(random.randint(100000, 999999))
            request.session['reset_vendor_email'] = email # Vendor specific session
            vendor.otp = otp
            vendor.otp_used = 0
            vendor.save()
            
            send_mail(
                subject='PetCareHub - Vendor Reset OTP',
                message=f'Hello {vendor.vendor_name},\n\nYour OTP for password reset is: {otp}\n\n- Team PetCareHub 🐾',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )
            messages.success(request, 'OTP sent to your registered email!', extra_tags='vendor_login')
            return redirect('vendor_reset_password_url')
        messages.error(request, 'No vendor account found with this email.')
    return render(request, 'vendor_forgot_password.html')

def vendor_reset_password(request):

    # Agar session mein email nahi hai toh forgot page pe bhej do
    ve = request.session.get('reset_vendor_email')
    if not ve:
        messages.error(request, 'Session expired. Please start again.')
        return redirect('vendor_forgot_password_url')

    if request.method == 'POST':
        otp_entered   = request.POST.get('otp', '').strip()
        new_pass      = request.POST.get('new_password', '').strip()
        confirm_pass  = request.POST.get('confirm_password', '').strip()

        # ── Server-side Validations ──────────────────────────────

        # 1. OTP format check
        if not otp_entered.isdigit() or len(otp_entered) != 6:
            messages.error(request, 'OTP must be exactly 6 digits.')
            return render(request, 'vendor_reset_password.html')

        # 2. Password validation
        password_pattern = r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*_])[A-Za-z\d!@#$%^&*_]{8,16}$'
        if not re.match(password_pattern, new_pass):
            messages.error(request, 'Password must be 8-16 characters with uppercase, lowercase, number, and a special character (!@#$%^&*_).')
            return render(request, 'vendor_reset_password.html')

        # 3. Passwords match
        if new_pass != confirm_pass:
            messages.error(request, 'Passwords do not match. Please try again.')
            return render(request, 'vendor_reset_password.html')

        # ── Database Checks ──────────────────────────────────────

        try:
            vendor = Vendor.objects.get(email=ve)
        except Vendor.DoesNotExist:
            messages.error(request, 'Invalid session. Please start again.')
            return redirect('vendor_forgot_password_url')

        # 4. OTP already used check
        if vendor.otp_used == 1:
            messages.error(request, 'This OTP has already been used. Please request a new one.')
            return redirect('vendor_forgot_password_url')

        # 5. OTP match check
        if vendor.otp != otp_entered:
            messages.error(request, 'Invalid OTP. Please enter the correct OTP.')
            return render(request, 'vendor_reset_password.html')

        # ── All Good: Password Reset ─────────────────────────────

        vendor.password = make_password(new_pass)  # Hashed password save karo
        vendor.otp_used = 1                         # OTP use ho gaya, block karo
        vendor.otp = None                           # OTP clear karo
        vendor.save()

        # Session reset email clear karo
        del request.session['reset_vendor_email']

        messages.success(request, 'Password reset successful! Please login with your new password.', extra_tags='vendor_login')
        return redirect('vendor_login')

    return render(request, 'vendor_reset_password.html')

def vendor_request_removal(request):
    if 'vendor_id' in request.session:
        vendor = get_object_or_404(Vendor, vendor_id=request.session['vendor_id'])
        if request.method == "POST":
            v_pass = request.POST.get('confirm_password')
            if check_password(v_pass, vendor.password):
                vendor.status = 4  # 4 = Removal Requested
                vendor.save()
                del request.session['vendor_id']
                del request.session['vendor_name']
                messages.success(request, "Account removal request sent to Admin.",extra_tags='vendor_login')
                return redirect('vendor_login')
            else:
                messages.error(request, "Invalid password! Removal request failed.", extra_tags='vendor_removal_req')
    return redirect('vendor_dashboard')

from django.http import JsonResponse

def check_vendor_status(request):
    if 'vendor_id' in request.session:
        try:
            vendor = Vendor.objects.get(vendor_id=request.session['vendor_id'])
            return JsonResponse({'status': vendor.status})
        except Vendor.DoesNotExist:
            return JsonResponse({'status': 'not_found'})
    return JsonResponse({'status': 'no_session'})