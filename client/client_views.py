from django.shortcuts import render, redirect, get_object_or_404
from django.db import models as db_models
from test2.models import Area,Customer,Product,ProductCategory,Gallery,Feedback,Vet, Appointment, Cart, Wishlist, VetSchedule
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from django.db.models import Avg, Count, Sum, Q
from django.http import JsonResponse
from datetime import datetime, timedelta, date
import re

# Create your views here.
from django.db.models import Avg, Count # Ye do cheezein import karna mat bhoolna

def show(request):
    # Annotate se har doctor ke liye average rating aur total reviews calculate honge
    vets = Vet.objects.filter(status=1).annotate(
        avg_rating=Avg('feedback__rating'),
        review_count=Count('feedback')
    ).order_by('-avg_rating')[:4]  # Top rated 4 vets
    
    total_vets = Vet.objects.filter(status=1).count()
    total_products = Product.objects.count()
    
    context = {
        'vets': vets,
        'total_vets': total_vets,
        'total_products': total_products,
    }
    return render(request, 'index.html', context)

def register(request):
    # Fetching all areas to populate the dropdown for GET requests
    areas = Area.objects.all()
    
    if request.method == "POST":
        # Extracting user data from the registration form
        name = request.POST.get('cust_name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password')
        contact = request.POST.get('contact', '').strip()
        address = request.POST.get('address', '').strip()
        area_id = request.POST.get('area_id')

        # --- SERVER-SIDE VALIDATION START ---
        
        email_pattern = r'^[a-zA-Z][a-zA-Z0-9._%+-]*@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            messages.error(request, "Invalid Email: Must start with a letter and follow standard format (e.g., petcarehub@gmail.com).")
            return render(request, 'register.html', {'areas': areas}) # redirect ki jagah render taaki user wahi rahe
        
        # 1. Name Validation: Check if it contains only letters and spaces
        if not (re.match(r'^[A-Za-z\s]+$', name) and len(name) > 1):
            messages.error(request, "Invalid Name: Please use alphabets and spaces only.")
            return render(request, 'register.html', {'areas': areas})

        # 2. Duplicate Email Check: Prevent multiple accounts with the same email address
        if Customer.objects.filter(email=email).exists():
            messages.error(request, "This email is already registered. Please login.")
            return render(request, 'register.html', {'areas': areas})
        
        # 3. Duplicate Contact Check (NEW)
        if Customer.objects.filter(contact=contact).exists():
            messages.error(request, "This mobile number is already registered. Please use a different one.")
            return render(request, 'register.html', {'areas': areas})
        
      # 3. Contact Validation: Exactly 10 digits and starts with 6-9
        if not re.match(r'^[6-9]\d{9}$', contact):
            messages.error(request, "Invalid Contact: Must be 10 digits starting with 6, 7, 8, or 9.")
            return render(request, 'register.html', {'areas': areas})
        
        # --- PASSWORD VALIDATION (New) ---
        password_pattern = r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*_])[A-Za-z\d!@#$%^&*_]{8,16}$'
        if not re.match(password_pattern, password):
            messages.error(request, "Password must be 8-16 characters with uppercase, lowercase, number, and a special character (!@#$%^&*_).")
            return render(request, 'register.html', {'areas': areas})
        
        # Address Validation
        if len(address) < 10:
            messages.error(request, "Address must be at least 10 characters.")
            return render(request, 'register.html', {'areas': areas})

        # Area Validation
        if not area_id:
            messages.error(request, "Please select your area.")
            return render(request, 'register.html', {'areas': areas})
        
        # --- DATABASE INSERTION ---
        try:
            area_obj = Area.objects.get(area_id=area_id)
            hashed_p = make_password(password)

            Customer.objects.create(
                cust_name=name,
                email=email,
                password=hashed_p, 
                contact=contact,
                address=address,
                area_id=area_obj,
                is_admin=0 
            )
            messages.success(request, "Registration successful! You can now log in to your account. 🐾")
            return redirect('login1')

        except Exception as e:
            messages.error(request, f"Registration failed: {str(e)}")
            return render(request, 'register.html', {'areas': areas})
    
    return render(request, 'register.html', {'areas': areas})

# client_views.py
def login(request):
    if request.method == "POST":
        email_val = request.POST.get('email', '').strip()
        password_val = request.POST.get('password')

        try:
            customer = Customer.objects.get(email=email_val)
            
            if check_password(password_val, customer.password):
                
                if customer.is_admin == 2:
                    messages.error(request,'Your account has been restricted. Please contact support')
                    return redirect('login1')
                # Basic session data
                request.session['cust_id'] = customer.cust_id
                request.session['cust_name'] = customer.cust_name
                request.session['is_admin'] = customer.is_admin
                
                # PROFILE PHOTO RESTORE: Permanent path database se uthana
                if customer.user_profile:
                    # Database se asli URL (e.g., /media/customer_profiles/abc.jpg)
                    request.session['cust_profile'] = customer.user_profile.url
                else:
                    # Default photo agar upload nahi ki hai
                    request.session['cust_profile'] = "/static/assets/img/users/default.png"
                
                messages.success(request, f"Welcome back, {customer.cust_name}! 🐾", extra_tags='login_home')
                return redirect('home') 
            else:
                messages.error(request, "Invalid Password. Please try again.")
                return redirect('login1')
                
        except Customer.DoesNotExist:
            messages.error(request, "This email is not registered. Please sign up first.")
            return redirect('login1')

    return render(request, 'login1.html')

def product(request):
    categories = ProductCategory.objects.all()
    cat_id = request.GET.get('category')
    sort_by = request.GET.get('sort') 
    page_number = request.GET.get('page')
    
    user_wishlist_ids = []
    if 'cust_id' in request.session:
        user_wishlist_ids = Wishlist.objects.filter(
            cust_id=request.session['cust_id']
        ).values_list('prod_id', flat=True)
    
    if cat_id:
        product_list = Product.objects.filter(category_id=cat_id)
    else:
        product_list = Product.objects.all()

    if sort_by == 'name_asc':
        product_list = product_list.order_by('prod_name')
    elif sort_by == 'name_desc':
        product_list = product_list.order_by('-prod_name')
    elif sort_by == 'price_asc':
        product_list = product_list.order_by('price')
    elif sort_by == 'price_desc':
        product_list = product_list.order_by('-price')
    else:
        product_list = product_list.order_by('prod_id')
        
    paginator = Paginator(product_list, 15)
    products = paginator.get_page(page_number)
        
    return render(request, 'product.html', {
        'products': products, 
        'categories': categories,
        'selected_cat': cat_id,
        'selected_sort': sort_by,
        'user_wishlist_ids': user_wishlist_ids 
    })
            
def product_details(request, pk):
    product = get_object_or_404(Product, prod_id=pk)
    gallery = Gallery.objects.filter(prod_id=product)
    related_products = Product.objects.filter(category_id=product.category_id).exclude(prod_id=pk).annotate(
        avg_rating=Avg('feedback__rating'), # Feedback table se average rating nikalna
        review_count=Count('feedback')      # Total reviews count karna
    )[:10]
    
    reviews = Feedback.objects.filter(prod_id=product).select_related('cust_id').order_by('-feedback_date')
    
    user_wishlist_ids = []
    if 'cust_id' in request.session:
        user_wishlist_ids = Wishlist.objects.filter(
            cust_id=request.session['cust_id']
        ).values_list('prod_id', flat=True) #
    
    avg_rating_data = reviews.aggregate(avg_rating=Avg('rating'))
    avg_rating = avg_rating_data['avg_rating'] or 0
    display_rating = round(avg_rating, 1)
    
    full_stars = range(int(avg_rating))
    empty_stars = range(5 - int(avg_rating))
    
    current_user = None
    cust_id = request.session.get('cust_id')
    if cust_id:
        try:
            current_user = Customer.objects.get(cust_id=cust_id)
        except Customer.DoesNotExist:
            current_user = None

    from datetime import date, timedelta
    expected_delivery = date.today() + timedelta(days=3)

    context = {
        'product': product,
        'gallery': gallery,
        'related_products': related_products,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'display_rating': display_rating,
        'full_stars': full_stars,
        'empty_stars': empty_stars,
        'current_user': current_user,
        'user_wishlist_ids': user_wishlist_ids,
        'expected_delivery': expected_delivery,
    }
    
    return render(request, 'product-details.html', context)

def submit_review(request, prod_id):
    if request.method == "POST":
        cust_id = request.session.get('cust_id')
        if not cust_id:
            messages.warning(request, "Please login to write a review! 🐾")
            return redirect('login1')

        product = get_object_or_404(Product, prod_id=prod_id)
        customer = get_object_or_404(Customer, cust_id=cust_id)
        
        rating = request.POST.get('rating')
        comments = request.POST.get('comments')

        Feedback.objects.create(
            cust_id=customer,
            prod_id=product,
            rating=rating,
            comments=comments
        )
        
        messages.success(request, "Thank you for your review! ❤️")
        return redirect('product_details', pk=prod_id)
    
def add_to_cart(request, prod_id):
    cust_id = request.session.get('cust_id')
    
    if not cust_id:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'login_required'}, status=401)
        messages.warning(request, "Please login first!")
        return redirect('login1')

    if request.method == "POST":
        product = get_object_or_404(Product, prod_id=prod_id)
        customer = get_object_or_404(Customer, cust_id=cust_id)
        qty = int(request.POST.get('quantity', 1))

        # Out of stock check
        if product.qty <= 0:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': 'This product is out of stock!'}, status=400)
            messages.error(request, "This product is out of stock!")
            return redirect(request.META.get('HTTP_REFERER', 'product'))

        # Cart mein already kitna hai check karo
        existing_cart = Cart.objects.filter(cust_id=customer, prod_id=product, status=1).first()
        already_in_cart = existing_cart.quantity if existing_cart else 0

        # Total requested qty stock se zyada nahi honi chahiye
        if already_in_cart + qty > product.qty:
            available = product.qty - already_in_cart
            if available <= 0:
                msg = f"You already have all available stock ({product.qty}) in your cart!"
            else:
                msg = f"Only {available} more unit(s) available. You already have {already_in_cart} in your cart."
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': msg}, status=400)
            messages.error(request, msg)
            return redirect(request.META.get('HTTP_REFERER', 'product'))

        cart_item, created = Cart.objects.get_or_create(
            cust_id=customer, prod_id=product, status=1,
            defaults={'quantity': qty, 'price': product.price, 'total_price': product.price * qty}
        )
        if not created:
            cart_item.quantity += qty
            cart_item.total_price = cart_item.quantity * product.price
            cart_item.save()

        Wishlist.objects.filter(cust_id=customer, prod_id=product).delete()

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': f'{product.prod_name} added to cart! 🛒'})

        messages.success(request, f"{product.prod_name} added to cart! 🛒")
        return redirect(request.META.get('HTTP_REFERER', 'product'))
    
def cart_view(request):
    cust_id = request.session.get('cust_id')
    if not cust_id:
        return redirect('login1')
    
    cart_items = Cart.objects.filter(cust_id=cust_id, status=1).select_related('prod_id')
    grand_total = sum(item.total_price for item in cart_items)

    # Koi bhi item out of stock hai?
    has_out_of_stock = any(item.prod_id.qty == 0 for item in cart_items)

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'grand_total': grand_total,
        'has_out_of_stock': has_out_of_stock,
    })
    
def update_cart(request, cart_id, action):
    item = get_object_or_404(Cart, cart_id=cart_id)

    if action == 'plus':
        # Stock check: cart qty already max stock pe hai?
        if item.quantity >= item.prod_id.qty:
            messages.error(request, f"Only {item.prod_id.qty} unit(s) available in stock! You already have max qty in cart.")
            return redirect('cart')
        item.quantity += 1
    elif action == 'minus':
        if item.quantity > 1:
            item.quantity -= 1
        else:
            item.delete()
            return redirect('cart')

    item.total_price = item.quantity * item.price
    item.save()
    return redirect('cart')

def remove_cart(request, cart_id):
    item = get_object_or_404(Cart, cart_id=cart_id)
    item.delete()
    return redirect('cart')

def move_to_wishlist(request, cart_id):
    cust_id = request.session.get('cust_id')
    if not cust_id:
        return redirect('login1')

    cart_item = get_object_or_404(Cart, cart_id=cart_id)
    product = cart_item.prod_id
    customer = get_object_or_404(Customer, cust_id=cust_id)

    # Wishlist mein already nahi hai toh add karo
    if not Wishlist.objects.filter(cust_id=customer, prod_id=product).exists():
        Wishlist.objects.create(cust_id=customer, prod_id=product)

    # Cart se hata do
    cart_item.delete()

    messages.success(request, f"'{product.prod_name}' moved to Wishlist! ❤️")
    return redirect('cart')

def cart_count(request):
    cust_id = request.session.get('cust_id')
    if cust_id:
        count = Cart.objects.filter(cust_id=cust_id, status=1).count()
        return {'cart_item_count': count}
    return {'cart_item_count': 0}

def logout_view(request):
    logout(request) 
    request.session.flush() 
    messages.success(request, "Logged out successfully! Come back soon. 🐾", extra_tags='login_home')
    return redirect('home')

from django.db import transaction
from datetime import date, timedelta
from test2.models import Order, OrderDetail, OrderPayment

def checkout(request, prod_id=None):
    # --- LOGIN CHECK ---
    cust_id = request.session.get('cust_id')
    if not cust_id:
        messages.warning(request, "Please login to proceed to checkout.")
        return redirect('login1')

    customer = get_object_or_404(Customer, cust_id=cust_id)
    checkout_items = []
    grand_total = 0

    # --- PATH B: BUY IT NOW (Single Product) ---
    if prod_id:
        product = get_object_or_404(Product, prod_id=prod_id)
        qty = int(request.GET.get('qty', 1))
        total = product.price * qty
        checkout_items.append({
            'product': product,       # Product object
            'quantity': qty,          # Kitne quantity
            'total_price': total,     # qty * price
            'vendor': product.vendor_id  # Vendor kaun hai (OrderDetail ke liye)
        })
        grand_total = total

    # --- PATH A: CART CHECKOUT (Multiple Products) ---
    else:
        items = Cart.objects.filter(cust_id=customer, status=1).select_related('prod_id')
        
        # Agar cart khali hai toh product page pe bhejo
        if not items:
            messages.info(request, "Your cart is empty!")
            return redirect('product')

        # Out of stock check — checkout se pehle
        out_of_stock_items = [item for item in items if item.prod_id.qty == 0]
        if out_of_stock_items:
            names = ", ".join([i.prod_id.prod_name for i in out_of_stock_items])
            messages.error(request, f"'{names}' is currently out of stock. Please remove it from cart before checkout.")
            return redirect('cart')

        for item in items:
            checkout_items.append({
                'product': item.prod_id,
                'quantity': item.quantity,
                'total_price': item.total_price,
                'vendor': item.prod_id.vendor_id
            })
        grand_total = sum(i['total_price'] for i in checkout_items)

    # --- POST: RAZORPAY SUCCESS KE BAAD YAHAN AAYEGA ---
    if request.method == "POST":
        address = request.POST.get('address', customer.address)
        razorpay_payment_id = request.POST.get('razorpay_payment_id', '')
        auto_delivery_date = date.today() + timedelta(days=3)

        # POST mein prod_id aur qty uthao (Buy It Now ke liye)
        post_prod_id = prod_id  # Function parameter se directly lo

        post_qty = request.POST.get('qty', 1)

        # POST ke time checkout_items rebuild karo
        post_checkout_items = []
        post_grand_total = 0

        if post_prod_id:
            # --- PATH B: BUY IT NOW ---
            product = get_object_or_404(Product, prod_id=post_prod_id)
            qty = int(post_qty or 1)
            total = product.price * qty
            post_checkout_items.append({
                'product': product,
                'quantity': qty,
                'total_price': total,
                'vendor': product.vendor_id
            })
            post_grand_total = total
        else:
            # --- PATH A: CART ---
            items = Cart.objects.filter(cust_id=customer, status=1)
            for item in items:
                post_checkout_items.append({
                    'product': item.prod_id,
                    'quantity': item.quantity,
                    'total_price': item.total_price,
                    'vendor': item.prod_id.vendor_id
                })
            post_grand_total = sum(i['total_price'] for i in post_checkout_items)

        try:
            with transaction.atomic():

                # STEP 1: Main Order entry banao
                new_order = Order.objects.create(
                    cust_id=customer,
                    area_id=customer.area_id,
                    total_amount=post_grand_total,
                    address=address,
                    delivery_date=auto_delivery_date
                )

                # STEP 2: Har product ke liye alag OrderDetail entry banao + qty deduct
                for item in post_checkout_items:
                    product_obj = item['product']
                    ordered_qty = item['quantity']

                    # Stock recheck inside transaction (race condition se bachne ke liye)
                    product_obj.refresh_from_db()
                    if product_obj.qty < ordered_qty:
                        raise Exception(f"Sorry, '{product_obj.prod_name}' is out of stock or has insufficient quantity.")

                    OrderDetail.objects.create(
                        order_id=new_order,
                        vendor_id=item['vendor'],
                        prod_id=product_obj,
                        quantity=ordered_qty,
                        price=product_obj.price
                    )

                    # Qty deduct karo
                    Product.objects.filter(prod_id=product_obj.prod_id).update(
                        qty=db_models.F('qty') - ordered_qty
                    )

                # STEP 3: Payment record save karo
                OrderPayment.objects.create(
                    order_id=new_order,
                    payment_mode='Online',
                    amount=post_grand_total,
                    payment_status=1,
                    payment_token=razorpay_payment_id if razorpay_payment_id else "BYPASS"
                )

                # STEP 4: Cart clear karo (sirf cart wale order mein)
                if not post_prod_id:
                    Cart.objects.filter(cust_id=customer, status=1).delete()

                messages.success(request, "Order placed successfully! 🎉")
                return redirect('order_success')

        except Exception as e:
            print(f"--- ORDER ERROR: {e} ---")
            messages.error(request, f"Something went wrong: {str(e)}")
            return redirect('cart')

    # --- GET: Checkout page render karo ---
    return render(request, 'checkout.html', {
        'checkout_items': checkout_items,
        'grand_total': grand_total,
        'customer': customer,
        'prod_id': prod_id,  # Template ko pata chale ki Buy It Now hai ya Cart

    })

def add_to_wishlist(request, prod_id):
    cust_id = request.session.get('cust_id')
    if not cust_id:
        messages.warning(request, "Please login to manage your wishlist! 🐾")
        return redirect('login1')

    product = get_object_or_404(Product, prod_id=prod_id)
    customer = get_object_or_404(Customer, cust_id=cust_id)
    
    wish_item = Wishlist.objects.filter(cust_id=customer, prod_id=product).first()
    
    if wish_item:
        wish_item.delete()
        messages.success(request, f"'{product.prod_name}' has been removed from wishlist.")
    else:
        Wishlist.objects.create(cust_id=customer, prod_id=product)
        messages.success(request, f"Item is wishlisted! ❤️") 

    return redirect(request.META.get('HTTP_REFERER', 'product'))

def wishlist_view(request):
    cust_id = request.session.get('cust_id')
    if not cust_id:
        return redirect('login1')
    
    items = Wishlist.objects.filter(cust_id=cust_id).select_related('prod_id')
    return render(request, 'wishlist.html', {'items': items})    

def team(request):
    vets = Vet.objects.filter(status=1).select_related('area_id').annotate(
        avg_rating=Avg('feedback__rating'),
        review_count=Count('feedback')    
    )
    return render(request, 'team.html', {'vets': vets})

import re  # Top par regex import karna mat bhulna
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib import messages
from test2.models import Vet, VetSchedule, Appointment, Customer, Feedback

def vet_details(request, pk):
    # 1. Basic Setup & Data Fetching
    vet = get_object_or_404(Vet, vet_id=pk)
    cust_id = request.session.get('cust_id')
    current_customer = Customer.objects.filter(pk=cust_id).first() if cust_id else None

    # FEEDBACK FETCHING
    feedbacks = Feedback.objects.filter(vet_id=vet).select_related('cust_id').order_by('-feedback_date')

    now_aware = timezone.now()
    today_obj = now_aware.date()
    is_vet_vacation = (vet.availability_status == 0)

    # 2. Helper function to get available slots
    def get_slots_for_date(target_date):
        if is_vet_vacation: 
            return []
            
        day_index = target_date.weekday()
        schedule = VetSchedule.objects.filter(vet_id=vet, day_of_week=day_index).first()
        slots_list = []
        
        if schedule:
            d_start = timezone.make_aware(datetime.combine(target_date, datetime.min.time()))
            d_end = timezone.make_aware(datetime.combine(target_date, datetime.max.time()))

            # Is vet ke booked slots
            booked_appointments = Appointment.objects.filter(
                vet_id=vet,
                appointment_date__range=(d_start, d_end),
                appointment_status__in=[0, 1, 3, 6] 
            ).values_list('appointment_date', flat=True)
            
            booked_times = set([timezone.localtime(dt).strftime("%I:%M %p") for dt in booked_appointments])

            # Customer ke kisi bhi aur vet ke saath same din ke booked slots
            if current_customer:
                customer_other_appointments = Appointment.objects.filter(
                    cust_id=current_customer,
                    appointment_date__range=(d_start, d_end),
                    appointment_status__in=[0, 1, 3, 6]
                ).exclude(vet_id=vet).values_list('appointment_date', flat=True)
                
                customer_booked_times = set([timezone.localtime(dt).strftime("%I:%M %p") for dt in customer_other_appointments])
                booked_times = booked_times.union(customer_booked_times)

            current_slot = timezone.make_aware(datetime.combine(target_date, schedule.open_time))
            end_time = timezone.make_aware(datetime.combine(target_date, schedule.close_time))
            
            if target_date == today_obj:
                check_limit = now_aware + timedelta(minutes=45)
            else:
                check_limit = current_slot
            
            while current_slot < end_time:
                slot_str = current_slot.strftime("%I:%M %p")
                if current_slot >= check_limit: 
                    if slot_str not in booked_times:
                        slots_list.append(slot_str)
                current_slot += timedelta(hours=1)
        return slots_list

    # 3. POST Method: Booking Logic
    if request.method == "POST" and 'book_appointment' in request.POST:
        if not current_customer: 
            messages.error(request, "Please login to book an appointment.")
            return redirect('login1')
        
        if is_vet_vacation:
            messages.error(request, "Sorry, this Vet is currently on vacation.")
            return redirect('vet_details', pk=pk)

        # --- DESCRIPTION VALIDATION START ---
        raw_description = request.POST.get('description', '').strip()
        
        # Validation: Khali nahi hona chahiye, sirf spaces nahi, sirf dots nahi.
        # Kam se kam ek letter ya number hona chahiye.
        if not raw_description or not re.search(r'[a-zA-Z0-9]', raw_description):
            messages.error(request, "Description cannot be empty or contain only symbols/dots. Please explain the issue.")
            return redirect('vet_details', pk=pk)
        # --- DESCRIPTION VALIDATION END ---
            
        app_date = request.POST.get('app_date')
        app_slot = request.POST.get('app_slot')
        
        if not app_slot or "No slots" in app_slot:
            messages.error(request, "Please select a valid time slot.")
            return redirect('vet_details', pk=pk)

        try:
            naive_dt = datetime.strptime(f"{app_date} {app_slot}", "%Y-%m-%d %I:%M %p")
            check_datetime = timezone.make_aware(naive_dt)
            c_date = check_datetime.date()
            c_start = timezone.make_aware(datetime.combine(c_date, datetime.min.time()))
            c_end = timezone.make_aware(datetime.combine(c_date, datetime.max.time()))
        except ValueError:
            messages.error(request, "Invalid date/time format.")
            return redirect('vet_details', pk=pk)
        
        exists = Appointment.objects.filter(
            vet_id=vet, 
            appointment_date=check_datetime, 
            appointment_status__in=[0, 1, 3, 6]
        ).exists()
        
        if exists:
            messages.error(request, "Sorry, this slot was just booked. Please pick another.")
            return redirect('vet_details', pk=pk)

        already_booked_today = Appointment.objects.filter(
            cust_id=current_customer,
            vet_id=vet,
            appointment_date__range=(c_start, c_end),
            appointment_status__in=[0, 1, 3, 6]
        ).exists()

        if already_booked_today:
            messages.error(request, f"You already have an appointment on this date.")
            return redirect('vet_details', pk=pk)

        Appointment.objects.create(
            cust_id=current_customer,
            vet_id=vet,
            app_for=request.POST.get('app_for'),
            description=raw_description, # Cleaned description
            appointment_date=check_datetime,
            charges=vet.charges,
            appointment_status=0
        )
        
        # Photo wala message hatane ke liye is line ko comment kar diya hai:
        # messages.success(request, "Appointment request sent successfully! 🚀")
        
        return redirect('my_appointments')

    # 4. GET Method: Display Logic
    available_days = VetSchedule.objects.filter(vet_id=vet).values_list('day_of_week', flat=True)
    booking_range = []
    all_slots_dict = {}
    
    for i in range(3):
        temp_date = today_obj + timedelta(days=i)
        if temp_date.weekday() in available_days:
            date_str = temp_date.strftime('%Y-%m-%d')
            
            if is_vet_vacation:
                all_slots_dict[date_str] = ["VET_ON_VACATION"]
                booking_range.append(temp_date)
                continue

            t_start = timezone.make_aware(datetime.combine(temp_date, datetime.min.time()))
            t_end = timezone.make_aware(datetime.combine(temp_date, datetime.max.time()))

            has_appt = Appointment.objects.filter(
                cust_id=current_customer,
                vet_id=vet,
                appointment_date__range=(t_start, t_end),
                appointment_status__in=[0, 1, 3, 6]
            ).exists() if current_customer else False

            if has_appt:
                all_slots_dict[date_str] = ["ALREADY_BOOKED"]
                booking_range.append(temp_date)
            else:
                day_slots = get_slots_for_date(temp_date)
                if day_slots:
                    booking_range.append(temp_date)
                    all_slots_dict[date_str] = day_slots

    context = {
        'vet': vet,
        'customer': current_customer,
        'feedbacks': feedbacks,
        'booking_range': booking_range,
        'today': today_obj.strftime('%Y-%m-%d'),
        'all_slots_data': all_slots_dict,
        'is_on_vacation': is_vet_vacation,
    }
    return render(request, 'vet_details.html', context)

def my_appointments(request):
    # 1. Session & Customer Validation
    cust_id = request.session.get('cust_id')
    if not cust_id: 
        return redirect('login1')
    
    customer = get_object_or_404(Customer, cust_id=cust_id)
    
    # --- AUTO-CANCEL EXPIRED SLOTS ---
    # GADBAD FIX: payment_timer_start__isnull=False add kiya hai 
    # taaki NULL values comparison mein crash na karein.
    expiry_limit = timezone.now() - timedelta(minutes=30)
    Appointment.objects.filter(
        cust_id=customer,
        appointment_status=1,
        payment_timer_start__isnull=False, 
        payment_timer_start__lt=expiry_limit
    ).update(appointment_status=2)

     # ✅ AUTO-REJECT: Vet ne 30 min pehle tak pending request ka jawab nahi diya
    auto_reject_cutoff = timezone.now() + timedelta(minutes=30)
    Appointment.objects.filter(
        cust_id=customer,
        appointment_status=0,
        appointment_date__lte=auto_reject_cutoff
    ).update(
        appointment_status=2,
        cancel_reason="Auto-rejected: Vet did not respond in time."
    )

    # ✅ OFFLINE AUTO-CANCEL: Vet offline hai aur appointment 3 hrs mein hai
    offline_cutoff = timezone.now() + timedelta(hours=3)
    offline_apps = Appointment.objects.filter(
        cust_id=customer,
        appointment_status__in=[0, 1, 3, 6],
        appointment_date__lte=offline_cutoff,
        vet_id__availability_status=0  # Vet offline hai
    )
    if offline_apps.exists():
        offline_apps.update(
            appointment_status=7,
            cancel_reason="Vet is currently offline."
        )

    # --- 2. POST Logic (Handling Actions) ---
    if request.method == "POST":
        
        # CASE A: Payment Confirmation (Status 1 -> 3)
        if 'confirm_payment' in request.POST:
            app_id = request.POST.get('app_id')
            mode = int(request.POST.get('payment_mode')) 
            appointment = get_object_or_404(Appointment, appointment_id=app_id, cust_id=customer)
            
            # GADBAD FIX: Server-side re-check for timer expiry before saving
            is_expired = False
            if appointment.payment_timer_start:
                if appointment.payment_timer_start < expiry_limit:
                    is_expired = True

            if appointment.appointment_status == 1 and not is_expired:
                if mode == 2 and customer.is_cash_blocked:
                    messages.error(request, "Cash payment is blocked due to previous no-shows.")
                else:
                    appointment.payment_mode = mode
                    appointment.appointment_status = 3 # Confirmed
                    appointment.save()
                    messages.success(request, "Appointment confirmed! See you at the clinic. 🐾")
            else:
                # Agar timer khatam ho gaya toh status update kar do manually
                appointment.appointment_status = 2
                appointment.save()
                messages.error(request, "Sorry, this payment window has expired.")

        # CASE B: Handle Reschedule (Status 6 -> 1 or 2)
        elif 'handle_reschedule' in request.POST:
            app_id = request.POST.get('app_id')
            action = request.POST.get('action') # 'accept' or 'reject'
            appointment = get_object_or_404(Appointment, appointment_id=app_id, cust_id=customer)

            if action == 'accept':
                appointment.appointment_status = 1  # Move to Payment Stage
                appointment.payment_timer_start = timezone.now() # Start NEW 30-min window
                appointment.save()
                messages.success(request, "Reschedule accepted! Please complete payment within 30 minutes.")
            else:
                appointment.appointment_status = 2  # Cancelled
                appointment.save()
                messages.warning(request, "Reschedule rejected. Appointment cancelled.")

        return redirect('my_appointments')

    # --- 3. GET Logic (Fetching Data) ---
    appointments = Appointment.objects.filter(cust_id=cust_id).order_by('-appointment_date')
    rated_app_ids = Feedback.objects.filter(cust_id=cust_id).values_list('appointment_id', flat=True)

    context = {
        'appointments': appointments,
        'customer': customer,
        'rated_app_ids': rated_app_ids,
        'now': timezone.now(), 
    }

    return render(request, 'my_appointments.html', context)
    
def submit_vet_feedback(request):
    if request.method == "POST":
        # 1. Login Check
        cust_id = request.session.get('cust_id')
        if not cust_id:
            messages.error(request, "Please login to submit feedback.")
            return redirect('login1')

        # 2. Data Fetching from POST
        vet_id = request.POST.get('vet_id')
        app_id = request.POST.get('app_id')
        rating = request.POST.get('rating')
        comments = request.POST.get('comments', '').strip()

        try:
            # 3. Object Fetching (Database Safety)
            vet_obj = get_object_or_404(Vet, vet_id=vet_id)
            cust_obj = get_object_or_404(Customer, cust_id=cust_id)
            app_obj = get_object_or_404(Appointment, appointment_id=app_id)

            # 4. DUPLICATE CHECK: Ek appointment ka ek hi feedback hona chahiye
            existing_feedback = Feedback.objects.filter(appointment_id=app_obj).exists()
            if existing_feedback:
                messages.warning(request, "You have already submitted feedback for this appointment.")
                return redirect('my_appointments')

            # 5. CREATE FEEDBACK
            Feedback.objects.create(
                cust_id=cust_obj,
                vet_id=vet_obj,
                appointment_id=app_obj,
                rating=rating,
                comments=comments,
            )

            messages.success(request, f"Your review for Dr. {vet_obj.vet_name} has been submitted! ⭐")
        
        except Exception as e:
            # Troubleshooting ke liye terminal mein error print karega
            print(f"--- FEEDBACK SUBMISSION ERROR: {e} ---")
            messages.error(request, "Something went wrong while submitting feedback.")

        return redirect('my_appointments')

    # Agar koi direct URL hit kare bina POST ke
    return redirect('my_appointments')
 
# done by vraj
# client_views.py
# client_views.py
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.conf import settings 
from test2.models import Customer 

def edit_profile(request):
    cust_id = request.session.get('cust_id')
    if not cust_id: 
        return redirect('login1')
        
    customer = get_object_or_404(Customer, cust_id=cust_id)
    areas = Area.objects.all()  # Dropdown ke liye
    
    if request.method == "POST":
        new_name    = request.POST.get('name', '').strip()
        new_contact = request.POST.get('contact', '').strip()
        new_address = request.POST.get('address', '').strip()
        new_area_id = request.POST.get('area_id')

        # 1. Name validation: only letters and spaces
        if not re.match(r'^[a-zA-Z\s]+$', new_name):
            messages.error(request, "Invalid Name: Please use alphabets only.")
            return render(request, 'edit_profile.html', {'customer': customer})

        # 2. Contact validation: exactly 10 digits, starts with 6-9
        if not re.match(r'^[6-9]\d{9}$', new_contact):
            messages.error(request, "Invalid Contact: Must be 10 digits and start with 6, 7, 8, or 9.")
            return render(request, 'edit_profile.html', {'customer': customer})

        # 3. Duplicate contact check: koi aur customer toh nahi use kar raha?
        if Customer.objects.filter(contact=new_contact).exclude(cust_id=customer.cust_id).exists():
            messages.error(request, "This mobile number is already registered with another account.")
            return render(request, 'edit_profile.html', {'customer': customer})

        # 4. Address validation: empty nahi hona chahiye
        if not new_address:
            messages.error(request, "Address cannot be empty.")
            return render(request, 'edit_profile.html', {'customer': customer})
        
        # 5. Area validation
        if not new_area_id:
            messages.error(request, "Please select a valid area.")
            return render(request, 'edit_profile.html', {'customer': customer, 'areas': areas})

        # All validations passed — update karo
        customer.cust_name = new_name
        customer.contact   = new_contact
        customer.address   = new_address
        customer.area_id   = get_object_or_404(Area, area_id=new_area_id)

        # Photo Remove Logic
        if request.POST.get('remove_photo_flag') == "1":
            customer.user_profile = None 
        
        # Photo Upload
        elif 'profile_pic' in request.FILES:
            customer.user_profile = request.FILES['profile_pic']
            
        customer.save() 
        
        # Session Sync
        request.session['cust_name'] = customer.cust_name 
        if customer.user_profile:
            request.session['cust_profile'] = customer.user_profile.url
        else:
            request.session['cust_profile'] = f"{settings.STATIC_URL}assets/img/users/default.png"
            
        messages.success(request, "Profile updated successfully! 🐾")
        return redirect('edit_profile')

    return render(request, 'edit_profile.html', {'customer': customer, 'areas': areas})

def order_success(request):
    return render(request, 'order_success.html')

def appointment_success(request):
    return render(request, 'appointment_success.html')

# ✅ NEW VIEW
from test2.models import AppointmentPayment  # import at top preferred

def appointment_payment(request):
    if request.method != "POST":
        return redirect('my_appointments')

    cust_id = request.session.get('cust_id')
    if not cust_id:
        return redirect('login1')

    app_id             = request.POST.get('app_id')
    razorpay_payment_id = request.POST.get('razorpay_payment_id')

    customer    = get_object_or_404(Customer, cust_id=cust_id)
    appointment = get_object_or_404(Appointment, appointment_id=app_id, cust_id=customer)

    # Timer expiry server-side recheck
    expiry_limit = timezone.now() - timedelta(minutes=30)
    if appointment.payment_timer_start and appointment.payment_timer_start < expiry_limit:
        appointment.appointment_status = 2  # Cancelled
        appointment.save()
        messages.error(request, "Payment window expired. Appointment cancelled.")
        return redirect('my_appointments')

    # Appointment update: Online confirmed
    appointment.payment_mode       = 1  # Online
    appointment.appointment_status = 3  # Confirmed
    appointment.save()

    # AppointmentPayment table mein proper record save karo
    AppointmentPayment.objects.create(
        appointment_id=appointment,
        payment_mode='Online',
        amount=appointment.charges,
        payment_status=1,           # Paid
        payment_token=razorpay_payment_id
    )

    messages.success(request, "Appointment confirmed! See you at the clinic. 🐾")
    return redirect('appointment_success')

def my_orders(request):
    # --- LOGIN CHECK ---
    cust_id = request.session.get('cust_id')
    if not cust_id:
        return redirect('login1')

    # Orders fetch karo latest pehle
    user_orders = Order.objects.filter(
        cust_id=cust_id
    ).prefetch_related(
        'orderdetail_set__prod_id',
        'orderdetail_set__vendor_id'
    ).order_by('-order_id')

    # order_detail_id se exact check — same product alag order mein dobara rate ho sakta hai
    rated_order_detail_ids = set(
        Feedback.objects.filter(
            cust_id=cust_id,
            order_detail_id__isnull=False
        ).values_list('order_detail_id', flat=True)
    )

    # Har order ke andar vendor-wise group karo
    # grouped_orders = [ { 'order': order_obj, 'vendor_groups': [ { 'vendor': vendor_obj, 'products': [detail1, detail2] } ] } ]
    grouped_orders = []

    for order in user_orders:
        vendor_dict = {}

        for detail in order.orderdetail_set.all():
            vid = detail.vendor_id.vendor_id

            if vid not in vendor_dict:
                vendor_dict[vid] = {
                    'vendor': detail.vendor_id,
                    'products': [],
                    'detail_status': detail.detail_status,
                    # Ye vendor assigned hai ya nahi
                    'is_assigned': detail.detail_status >= 1,
                    'is_cancelled': detail.detail_status == 4,
                }
            vendor_dict[vid]['products'].append({
                'detail': detail,
                'subtotal': detail.price * detail.quantity,
                # Delivered hone ke baad rating check: kya is product pe review diya?
                'already_rated': detail.order_details_id in rated_order_detail_ids
            })
            
            # Status update: worst/highest status jo bhi ho
            vendor_dict[vid]['detail_status'] = detail.detail_status
            if detail.detail_status >= 1:
                vendor_dict[vid]['is_assigned'] = True
            if detail.detail_status == 4:
                vendor_dict[vid]['is_cancelled'] = True

        grouped_orders.append({
            'order': order,
            'vendor_groups': list(vendor_dict.values()),
        })

    return render(request, 'my_orders.html', {'grouped_orders': grouped_orders})

def cancel_order(request, order_id):
    cust_id = request.session.get('cust_id')
    if not cust_id:
        return redirect('login1')

    # vendor_id optional URL param se aayega
    vendor_id = request.GET.get('vendor_id')

    order = get_object_or_404(Order, order_id=order_id, cust_id=cust_id)

    if vendor_id:
        # --- VENDOR-WISE CANCEL ---
        details = order.orderdetail_set.filter(vendor_id=vendor_id)

        if not details.exists():
            messages.error(request, "Invalid vendor for this order.")
            return redirect('my_orders')

        # Check: kisi bhi detail ka status already assigned/beyond hai?
        if details.filter(detail_status__gte=1).exists():
            messages.error(request, "Cannot cancel — this vendor's items are already assigned. 🚫")
            return redirect('my_orders')

        # Sirf is vendor ke details cancel karo — pehle qty restock karo
        for d in details:
            Product.objects.filter(prod_id=d.prod_id_id).update(
                qty=db_models.F('qty') + d.quantity
            )
        details.update(detail_status=4)

        # Agar saare vendors ke details cancel ho gaye toh order bhi cancel mark karo
        all_cancelled = not order.orderdetail_set.exclude(detail_status=4).exists()
        if all_cancelled:
            order.is_cancelled = True
            order.cancelled_at = timezone.now()
            order.save()
            messages.success(request, "Entire order has been cancelled. 🐾")
        else:
            messages.success(request, "Selected vendor's items cancelled successfully. 🐾")

    else:
        # --- FULL ORDER CANCEL (fallback, pehle jaisa) ---
        if order.is_cancelled:
            messages.warning(request, "This order is already cancelled.")
            return redirect('my_orders')

        if order.orderdetail_set.filter(detail_status__gte=1).exists():
            messages.error(request, "Order cannot be cancelled — already assigned. 🚫")
            return redirect('my_orders')

        order.is_cancelled = True
        order.cancelled_at = timezone.now()
        # Qty restock karo — full cancel ke saare products ke liye
        for d in order.orderdetail_set.all():
            Product.objects.filter(prod_id=d.prod_id_id).update(
                qty=db_models.F('qty') + d.quantity
            )
        order.orderdetail_set.update(detail_status=4)
        order.save()
        messages.success(request, "Your order has been cancelled successfully. 🐾")

    return redirect('my_orders')

def client_change_password(request):
    cust_id = request.session.get('cust_id')
    if not cust_id:
        return redirect('login1')

    customer = get_object_or_404(Customer, cust_id=cust_id)

    if request.method == 'POST':
        old_pass     = request.POST.get('old_password', '')
        new_pass     = request.POST.get('new_password', '')
        confirm_pass = request.POST.get('confirm_password', '')

        if not check_password(old_pass, customer.password):
            messages.error(request, "Current password is incorrect.")
        elif new_pass != confirm_pass:
            messages.error(request, "New passwords do not match.")
        elif len(new_pass) < 6  or len(new_pass) > 12:
            messages.error(request, "Password must be between 6 and 12 characters.")
        else:
            customer.password = make_password(new_pass)
            customer.save()
            messages.success(request, "Password updated successfully! 🔒")

    return redirect('edit_profile')

def contact(request):
    return render(request, 'contact.html')

import random
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password
from test2.models import Customer  # apna app name aur model adjust kar lena



def forgot_password(request):

    # Already logged in hai toh direct home pe bhej do
    if request.session.get('cust_id'):
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()

        # Email format basic check (HTML required bhi hai, ye extra layer hai)
        if not email:
            messages.error(request, 'Please enter your email address.')
            return render(request, 'forgot_password.html')

        try:
            customer = Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            # Security: exact error mat batao ki email registered hai ya nahi
            messages.error(request, 'No account found with this email address.')
            return render(request, 'forgot_password.html')

        # 6 digit OTP generate karo
        otp = str(random.randint(100000, 999999))

        # OTP database mein save karo aur used flag reset karo
        customer.otp = otp
        customer.otp_used = 0
        customer.save()

        # Session mein email save karo (reset page pe kaam aayega)
        request.session['reset_email'] = email

        # Email bhejo
        try:
            send_mail(
                subject='PetCareHub - Password Reset OTP',
                message=(
                    f'Hello {customer.cust_name},\n\n'
                    f'Your OTP for password reset is: {otp}\n\n'
                    f'This OTP is valid for one-time use only.\n\n'
                    f'If you did not request this, please ignore this email.\n\n'
                    f'- Team PetCareHub 🐾'
                ),
                from_email='vraj537github@gmail.com',
                recipient_list=[email],
                fail_silently=False,
            )
            messages.success(request, 'OTP sent successfully! Please check your email.')
            return redirect('reset_password')

        except Exception as e:
            messages.error(request, 'Failed to send OTP. Please try again later.')
            return render(request, 'forgot_password.html')

    return render(request, 'forgot_password.html')


def reset_password(request):

    # Agar session mein email nahi hai toh forgot page pe bhej do
    reset_email = request.session.get('reset_email')
    if not reset_email:
        messages.error(request, 'Session expired. Please start again.')
        return redirect('forgot_password')

    if request.method == 'POST':
        otp_entered    = request.POST.get('otp', '').strip()
        new_password   = request.POST.get('new_password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        # ── Server-side Validations ──────────────────────────────

        # 1. OTP format check
        if not otp_entered.isdigit() or len(otp_entered) != 6:
            messages.error(request, 'OTP must be exactly 6 digits.')
            return render(request, 'reset_password.html')

        # 2. Password validation
        password_pattern = r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*_])[A-Za-z\d!@#$%^&*_]{8,16}$'
        if not re.match(password_pattern, new_password):
            messages.error(request, 'Password must be 8-16 characters with uppercase, lowercase, number, and a special character (!@#$%^&*_).')
            return render(request, 'reset_password.html')

        # 3. Passwords match
        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match. Please try again.')
            return render(request, 'reset_password.html')

        # ── Database Checks ──────────────────────────────────────

        try:
            customer = Customer.objects.get(email=reset_email)
        except Customer.DoesNotExist:
            messages.error(request, 'Invalid session. Please start again.')
            return redirect('forgot_password')

        # 4. OTP already used check
        if customer.otp_used == 1:
            messages.error(request, 'This OTP has already been used. Please request a new one.')
            return redirect('forgot_password')

        # 5. OTP match check
        if customer.otp != otp_entered:
            messages.error(request, 'Invalid OTP. Please enter the correct OTP.')
            return render(request, 'reset_password.html')

        # ── All Good: Password Reset ─────────────────────────────

        customer.password = make_password(new_password)  # Hashed password save karo
        customer.otp_used = 1                             # OTP use ho gaya, block karo
        customer.otp = None                               # OTP clear karo (optional but cleaner)
        customer.save()

        # Session reset email clear karo
        del request.session['reset_email']

        messages.success(request, 'Password reset successful! Please login with your new password.')
        return redirect('login1')

    return render(request, 'reset_password.html')



def submit_order_review(request, prod_id):
    """My Orders page se product review submit karne ke liye"""
    if request.method == "POST":
        cust_id = request.session.get('cust_id')
        if not cust_id:
            messages.warning(request, "Please login to write a review! 🐾")
            return redirect('login1')

        # Pehle sab POST data fetch karo
        order_detail_id  = request.POST.get('order_detail_id')
        rating           = request.POST.get('rating')
        comments         = request.POST.get('comments', '').strip()

        product          = get_object_or_404(Product, prod_id=prod_id)
        customer         = get_object_or_404(Customer, cust_id=cust_id)
        order_detail_obj = get_object_or_404(OrderDetail, order_details_id=order_detail_id)

        # Duplicate check: sirf order_detail se — same order ka same product dobara rate nahi hoga
        if Feedback.objects.filter(order_detail_id=order_detail_obj).exists():
            messages.warning(request, "You have already reviewed this product.")
            return redirect('my_orders')

        Feedback.objects.create(
            cust_id=customer,
            prod_id=product,
            order_detail_id=order_detail_obj,
            rating=rating,
            comments=comments,
        )

        messages.success(request, f"Review submitted for {product.prod_name}! ⭐")
        return redirect('my_orders')

    return redirect('my_orders')

def adoption(request):
    return render(request,'adoption.html')

def developers(request):
    return render(request,'developers.html')

def future(request):
    return render(request,'future.html')
