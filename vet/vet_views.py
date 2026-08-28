from urllib import request

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from test2.models import Feedback, Vet, Area, Appointment, VetSchedule
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone as django_timezone
import re 
import random
from django.conf import settings
from django.core.mail import send_mail

def vet_register(request):
    areas = Area.objects.all()
    if request.method == "POST":
        # Capture text data
        v_name = request.POST.get('v_name', '').strip()
        v_email = request.POST.get('v_email', '').strip()
        v_pass = request.POST.get('v_pass')
        v_contact = request.POST.get('v_contact', '').strip()
        v_special = request.POST.get('v_specialization')
        v_charges = request.POST.get('v_charges', '0')
        v_area_id = request.POST.get('area_id')
        v_address = request.POST.get('v_address', '').strip()

        # Capture File data
        v_profile = request.FILES.get('vet_profile')
        v_docs = request.FILES.get('documents')

        # --- VALIDATIONS ---
        if not re.match(r'^[a-zA-Z\s]+$', v_name):
            messages.error(request, "Invalid Name: Please use alphabets and spaces only.", extra_tags='vet_danger')
            return render(request, 'register_vet.html', {'areas': areas})

        if not re.match(r'^[a-zA-Z][a-zA-Z0-9._%+-]*@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v_email):
            messages.error(request, "Invalid Email: Must start with a letter.", extra_tags='vet_danger')
            return render(request, 'register_vet.html', {'areas': areas})

        if not re.match(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*_])[A-Za-z\d!@#$%^&*_]{8,16}$', v_pass):
            messages.error(request, "Password must be 8-16 characters with uppercase, lowercase, number, and a special character (!@#$%^&*_).", extra_tags='vet_danger')
            return render(request, 'register_vet.html', {'areas': areas})

        if not re.match(r'^[6-9]\d{9}$', v_contact):
            messages.error(request, "Invalid Contact: Must be 10 digits starting with 6-9.", extra_tags='vet_danger')
            return render(request, 'register_vet.html', {'areas': areas})

        if not v_charges.isdigit() or int(v_charges) < 100 or int(v_charges) > 5000:
            messages.error(request, "Charges must be between ₹100 and ₹5000.", extra_tags='vet_danger')
            return render(request, 'register_vet.html', {'areas': areas})

        if v_profile and v_profile.size > 2 * 1024 * 1024:
            messages.error(request, "Profile photo size should be less than 2MB.", extra_tags='vet_danger')
            return render(request, 'register_vet.html', {'areas': areas})
        
        if v_docs and v_docs.size > 5 * 1024 * 1024:
            messages.error(request, "Documents size should be less than 5MB.", extra_tags='vet_danger')
            return render(request, 'register_vet.html', {'areas': areas})

        if Vet.objects.filter(email=v_email).exists():
            messages.error(request, "This email is already registered.", extra_tags='vet_danger')
            return render(request, 'register_vet.html', {'areas': areas})

        if Vet.objects.filter(contact=v_contact).exists():
            messages.error(request, "This mobile number is already registered.", extra_tags='vet_danger')
            return render(request, 'register_vet.html', {'areas': areas})

        try:
            area_obj = Area.objects.get(area_id=v_area_id)
            Vet.objects.create(
                vet_name=v_name,
                email=v_email,
                password=make_password(v_pass),
                contact=v_contact,
                specialization=v_special,
                charges=v_charges,
                address=v_address,
                area_id=area_obj,
                vet_profile=v_profile,
                documents=v_docs,
                status=0,
                availability_status=0
            )
            messages.success(request, "Registration successful! Please wait for the Admin to verify your account.", extra_tags='vet_success')
            return redirect('vet_login')
        except Exception as e:
            messages.error(request, f"Registration failed: {str(e)}", extra_tags='vet_danger')
            return render(request, 'register_vet.html', {'areas': areas})
            
    return render(request, 'register_vet.html', {'areas': areas})

def vet_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            vet = Vet.objects.get(email=email)
            if check_password(password, vet.password):
                if vet.status == 1:
                    request.session['vet_id'] = vet.vet_id
                    messages.success(request, f"Welcome back, Dr. {vet.vet_name}!", extra_tags='login_home')
                    return redirect('vet_dashboard')
                elif vet.status == 0:
                    messages.error(request,"Your account is pending for Admin approval.")
                elif vet.status == 2:
                    messages.error(request, "Your approval request was rejected.")
                elif vet.status == 3:
                    messages.error(request, "Your account has been restricted by Admin.")
                elif vet.status == 4:
                    messages.error(request, "Your account removal is under process by Admin.")
                    
                return redirect('vet_login')
            else:
                messages.error(request, "Invalid Password.")
                return redirect('vet_login')
        except Vet.DoesNotExist:
            messages.error(request, "No account found with this email.")
            return redirect('vet_login')
    return render(request, 'login_vet.html')

from datetime import datetime
import re
import os
from django.utils import timezone as django_timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from test2.models import Feedback, Vet, Appointment, VetSchedule
from django.db.models import Sum
from datetime import datetime, timedelta


def vet_dashboard(request):
    # 1. Session check
    vet_id = request.session.get('vet_id')
    if not vet_id:
        return redirect('vet_login')
    
    vet = get_object_or_404(Vet, vet_id=vet_id)
    days_list = [(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')]

    # Saari appointments ek baar mein uthao optimize karne ke liye
    base_query = Appointment.objects.filter(vet_id=vet)

    # ✅ AUTO-REJECT: 30 min pehle tak vet ne respond nahi kiya to auto-reject
    auto_reject_cutoff = django_timezone.now() + timedelta(minutes=30)
    Appointment.objects.filter(
        vet_id=vet,
        appointment_status=0,
        appointment_date__lte=auto_reject_cutoff
    ).update(
        appointment_status=2,
        cancel_reason="Auto-rejected: Vet did not respond in time."
    )

    # ✅ OFFLINE AUTO-CANCEL: Vet offline hai aur appointment 3 hrs mein hai
    if vet.availability_status == 0:
        offline_cutoff = django_timezone.now() + timedelta(hours=3)
        offline_conflicts = Appointment.objects.filter(
            vet_id=vet,
            appointment_status__in=[0, 1, 3, 6],
            appointment_date__lte=offline_cutoff
        )
        offline_count = offline_conflicts.count()
        if offline_count > 0:
            offline_conflicts.update(
                appointment_status=7,
                cancel_reason="Vet is currently offline. Sorry for the inconvenience."
            )
            vet.cancel_count = (vet.cancel_count or 0) + offline_count
            vet.save()
    
    # 4: Done, 2: Rejected by Vet, 7: Cancelled (Offline/Bulk), 5: Absent
    total_received = base_query.count()
    
    # 1. Sirf Completed appointments uthao (Status 4)
    completed_apps = Appointment.objects.filter(vet_id=vet, appointment_status=4)
    
    # 2. Count nikaalo
    completed_count = completed_apps.count()
    
    total_rejected = base_query.filter(appointment_status=2).count()
    total_cancelled = base_query.filter(appointment_status=7).count() # Jo bulk cancel hue offline mode se
    total_absent = base_query.filter(appointment_status=5).count()
    
    # 3. Dynamic Sum: Har appointment ke time jo charges the, uska total
    # Hum 'charges' field ka sum kar rahe hain jo Appointment model mein store hui thi
    earnings_query = completed_apps.aggregate(total=Sum('charges'))
    total_earnings = earnings_query['total'] if earnings_query['total'] else 0

    if request.method == "POST":
        # --- A. PROFILE UPDATE LOGIC (Updated for Spaces & Symbols) ---
        if 'update_profile' in request.POST:
            try:
                # .strip() aage-piche ki faltu spaces uda dega, beech ki rakhega
                new_name = request.POST.get('new_name', '').strip()
                new_contact = request.POST.get('new_contact', '').strip()
                new_address = request.POST.get('new_address', '').strip()
                new_specialization = request.POST.get('new_specialization')
                new_charges = request.POST.get('new_charges', '0')

                # 1. Name Validation (Letters & Single Spaces between words, 3-50 chars)
                if not re.match(r"^[A-Za-z]+([\s\.][A-Za-z]+)*$", new_name) or not (3 <= len(new_name) <= 50):
                    messages.error(request, "Name should be 3-50 characters, starting with letters, single spaces allowed between words.")
                    return redirect('vet_dashboard')

                # 2. Contact Validation
                if not re.match(r"^[6-9]\d{9}$", new_contact):
                    messages.error(request, "Invalid 10-digit contact number starting with 6-9.")
                    return redirect('vet_dashboard')

                # 2b. Duplicate contact check
                if Vet.objects.filter(contact=new_contact).exclude(vet_id=vet.vet_id).exists():
                    messages.error(request, "This mobile number is already registered with another account.")
                    return redirect('vet_dashboard')

                # 3. Address Validation (Letters, Numbers, Spaces, and symbols like - , / .)
                if not re.match(r"^[A-Za-z0-9]+([\s\-\,\/\.][A-Za-z0-9]+)*$", new_address):
                    messages.error(request, "Address must be valid. Use letters, numbers, and basic symbols (-,/.). No leading/trailing spaces.")
                    return redirect('vet_dashboard')

                # 4. Charges Validation
                try:
                    charges_val = int(new_charges)
                    if charges_val < 99 or charges_val > 5000:
                        messages.error(request, "Fees must be between ₹99 and ₹5000.")
                        return redirect('vet_dashboard')
                except ValueError:
                    messages.error(request, "Invalid fees value.")
                    return redirect('vet_dashboard')

                # 5. Image Upload Logic
                if 'new_profile' in request.FILES:
                    profile_pic = request.FILES['new_profile']
                    
                    # Size Check (2MB)
                    if profile_pic.size > 2 * 1024 * 1024:
                        messages.error(request, "Image must be under 2MB.")
                        return redirect('vet_dashboard')
                    
                    # Extension Check
                    ext = os.path.splitext(profile_pic.name)[1].lower()
                    if ext in ['.jpg', '.jpeg', '.png', '.webp']:
                        vet.vet_profile = profile_pic 
                    else:
                        messages.error(request, "Invalid image format. Use JPG, PNG or WEBP.")
                        return redirect('vet_dashboard')

                # Final Save
                vet.vet_name = new_name
                vet.contact = new_contact
                vet.address = new_address
                vet.charges = charges_val
                vet.save()
                
                messages.success(request, "Profile updated successfully! 🐾")

            except Exception as e:
                messages.error(request, f"Profile Update Error: {str(e)}")
            return redirect('vet_dashboard')

        # --- B. AVAILABILITY & BULK CANCEL ---
        elif 'update_availability' in request.POST:
            new_status = request.POST.get('availability_status')
            
            if new_status == "0":  # Offline Mode
                start_date_str = request.POST.get('start_date')
                end_date_str = request.POST.get('end_date')
                reason = request.POST.get('offline_reason', 'Vet is unavailable')

                if start_date_str and end_date_str:
                    try:
                        s_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                        e_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
                        
                        conflicts = Appointment.objects.filter(
                            vet_id=vet,
                            appointment_date__range=[
                                django_timezone.make_aware(datetime.combine(s_date, datetime.min.time())),
                                django_timezone.make_aware(datetime.combine(e_date, datetime.max.time()))
                            ],
                            appointment_status__in=[0, 1, 3, 6]
                        )

                        count = conflicts.count()
                        for appt in conflicts:
                            appt.appointment_status = 7  # Cancelled
                            if hasattr(appt, 'cancel_reason'):
                                appt.cancel_reason = reason
                            appt.save()
                        
                        vet.cancel_count = (vet.cancel_count or 0) + count
                        messages.success(request, f"Offline mode active. {count} appointments cancelled.")
                    except (ValueError, Exception) as e:
                        messages.error(request, f"Error: {str(e)}")
                
                vet.availability_status = 0
                vet.save()
                return redirect('vet_dashboard')

            elif new_status == "1":
                # Check karo ki database mein schedule exist karta hai ya nahi
                has_schedule = VetSchedule.objects.filter(vet_id=vet).exists()
                
                if has_schedule:
                    # Agar schedule hai, toh hi online karo
                    vet.availability_status = 1
                    vet.save()
                    messages.success(request, "You are now Online. 🐾")
                else:
                    # Agar schedule nahi hai, toh error do aur status mat badlo
                    messages.error(request, "First, set the schedule; only then can you go online.")
                
                return redirect('vet_dashboard')

        # --- C. SINGLE APPOINTMENT MANAGEMENT ---
        elif 'manage_appointment' in request.POST:
            app_id = request.POST.get('app_id')
            try:
                action = int(request.POST.get('action', 0))
                appointment = get_object_or_404(Appointment, appointment_id=app_id, vet_id=vet)
                
                if action == 1: # Accept
                    appointment.appointment_status = 1 
                    appointment.payment_timer_start = django_timezone.now()
                    messages.success(request, "Appointment Accepted.")
                
                elif action == 2: # Reject
                    appointment.appointment_status = 2 
                    reason = request.POST.get('cancel_reason', "Rejected by Vet.")
                    if hasattr(appointment, 'cancel_reason'):
                        appointment.cancel_reason = reason
                    messages.success(request, "Appointment Rejected.")
                
                elif action == 4: # Complete
                    if 'medical_report' in request.FILES:
                        appointment.medical_report = request.FILES['medical_report']
                        appointment.appointment_status = 4

                        # Cash payment entry — sirf tab jab mode cash ho aur entry pehle se na ho
                        if appointment.payment_mode == 2:
                            from test2.models import AppointmentPayment
                            already_exists = AppointmentPayment.objects.filter(
                                appointment_id=appointment
                            ).exists()
                            if not already_exists:
                                AppointmentPayment.objects.create(
                                    appointment_id=appointment,
                                    payment_mode='Cash',
                                    amount=appointment.charges,
                                    payment_status=1,  # Paid
                                    payment_token='CASH'
                                )

                        messages.success(request, "Report uploaded.")
                
                elif action == 5: # Absent
                    appointment.appointment_status = 5
                    client = appointment.cust_id
                    # Strike sirf cash payment wale ko — online ne pay kar diya tha
                    if client and appointment.payment_mode != 1:
                        client.strike_count = (client.strike_count or 0) + 1
                        if client.strike_count >= 3:
                            client.is_cash_blocked = True
                        client.save()
                    messages.success(request, "Client marked absent.")

                appointment.save()
            except Exception as e:
                messages.error(request, f"Update Error: {str(e)}")
            
            return redirect('vet_dashboard')

    # Per-day lock status calculate karo (12 hrs per day)
    now = django_timezone.now()
    current_schedule_objs = VetSchedule.objects.filter(vet_id=vet)

    per_day_locks = {}
    for s in current_schedule_objs:
        if s.locked_until and now < s.locked_until:
            per_day_locks[s.day_of_week] = True
        else:
            per_day_locks[s.day_of_week] = False

    # is_locked sirf tab True jab SAARE scheduled days locked hain
    is_locked = bool(per_day_locks) and all(per_day_locks.values())
    
    time_slots = []
    # Subah 6:00 (6) se lekar Raat 12:00 AM (24) tak
    for hour in range(6, 25): 
        if hour == 24:
            display_text = "12:00 AM (Midnight)"
            val_time = "23:59:59" # Database compatibility ke liye
            is_midnight = True
        else:
            period = 'AM' if hour < 12 else 'PM'
            display_hour = hour if hour <= 12 else hour - 12
            if display_hour == 0: display_hour = 12
            
            # Ab sirf ":00" format chalega
            display_text = f"{display_hour}:00 {period}"
            val_time = f"{hour:02d}:00:00"
            is_midnight = False
        
        time_slots.append({
            'display': display_text,
            'value': val_time,
            'index': len(time_slots),
            'is_midnight': is_midnight
        })
    
    # Database se current schedule uthao
    current_schedule_objs = VetSchedule.objects.filter(vet_id=vet)
    schedules_lookup = {s.day_of_week: s for s in current_schedule_objs}

    prefilled_days = []
    for i, day_name in days_list:
        existing = schedules_lookup.get(i)
        is_day_locked = per_day_locks.get(i, False)
        prefilled_days.append({
            'index': i,
            'name': day_name,
            'open_val': existing.open_time.strftime('%H:%M:%S') if existing and existing.open_time else "",
            'close_val': existing.close_time.strftime('%H:%M:%S') if existing and existing.close_time else "",
            'is_locked': is_day_locked
        })
    
    # --- GET DATA FETCHING ---
    context = {
        'vet': vet,
        'appointments': Appointment.objects.filter(vet_id=vet).order_by('-appointment_date'),
        'days_list': days_list,
        'time_slots': time_slots,
        'prefilled_days': prefilled_days,
        'current_schedule': VetSchedule.objects.filter(vet_id=vet).order_by('day_of_week'),
        'reviews': Feedback.objects.filter(vet_id=vet, prod_id__isnull=True).order_by('-feedback_date'),
        'today': django_timezone.now().date(),
        'now': django_timezone.now(),
        'is_locked': is_locked,
        'per_day_locks': per_day_locks,
        'completed_count': completed_count,
        'total_earnings': total_earnings, 
        'total_received': total_received,
        'total_rejected': total_rejected,
        'total_cancelled': total_cancelled,
        'total_absent': total_absent,
    }
    return render(request, 'vet-dashboard.html', context)

def update_vet_schedule(request):
    if 'vet_id' not in request.session: return redirect('vet_login')
    vet = get_object_or_404(Vet, vet_id=request.session['vet_id'])

    if request.method == "POST":
        from datetime import timedelta
        now = django_timezone.now()
        updated_any = False

        for i in range(7):
            open_t = request.POST.get(f'open_{i}')
            close_t = request.POST.get(f'close_{i}')
            existing = VetSchedule.objects.filter(vet_id=vet, day_of_week=i).first()

            if open_t and close_t:
                # Per-day lock check: 12 hrs
                if existing and existing.locked_until and now < existing.locked_until:
                    continue  # Yeh din locked hai — skip

                locked_until = now + timedelta(hours=12)  # Ab se 12 hrs lock

                if existing:
                    existing.open_time = open_t
                    existing.close_time = close_t
                    existing.locked_until = locked_until
                    existing.save()
                else:
                    VetSchedule.objects.create(
                        vet_id=vet,
                        day_of_week=i,
                        open_time=open_t,
                        close_time=close_t,
                        locked_until=locked_until
                    )
                updated_any = True

            else:
                # Blank — agar unlocked hai toh delete karo
                if existing:
                    if existing.locked_until and now < existing.locked_until:
                        continue  # Locked hai — skip
                    existing.delete()

        vet.is_first_login = False
        vet.save()

        force_online = request.POST.get('force_online')
        if force_online == "1":
            vet.availability_status = 1
            vet.save()
            messages.success(request, "Schedule Updated & You are now Online! 🐾")
        elif updated_any:
            messages.success(request, "Schedule Updated! Each day is locked for 12 hours. 🔒")
        else:
            messages.warning(request, "No changes — selected days are locked for 12 hours.")

    return redirect('vet_dashboard')

def request_removal(request):
    if 'vet_id' in request.session:
        vet = get_object_or_404(Vet, vet_id=request.session['vet_id'])
        if request.method == "POST":
            v_pass = request.POST.get('confirm_password')
            # Hash password check
            if check_password(v_pass, vet.password):
                vet.status = 4 # 4 = Removal Requested
                vet.availability_status = 0 
                vet.save()
                del request.session['vet_id']
                messages.success(request, "Account removal request sent to Admin.")
                return redirect('vet_login')
            else:
                messages.error(request, "Invalid password! Removal request failed.")
    return redirect('vet_dashboard')

def check_vet_status(request):
    if 'vet_id' in request.session:
        try:
            vet = Vet.objects.get(vet_id=request.session['vet_id'])
            # Dashboard status polling
            return JsonResponse({'status': vet.status}) 
        except Vet.DoesNotExist:
            return JsonResponse({'status': 'not_found'})
            
    return JsonResponse({'status': 'no_session'})

def vet_logout(request):
    if 'vet_id' in request.session: del request.session['vet_id']
    return redirect('vet_login')

# - Corrected Vet Password Reset Logic

def vet_forgot_password(request):
    if request.method == 'POST':
        v_email = request.POST.get('email', '').strip()
        vet = Vet.objects.filter(email=v_email).first()
        if vet:
            otp_val = str(random.randint(100000, 999999))
            request.session['reset_vet_email'] = v_email 
            vet.otp = otp_val
            vet.otp_used = 0 
            vet.save()
            
            send_mail(
                subject='PetCareHub - Vet Password Reset OTP',
                message=(
                    f'Hello Dr. {vet.vet_name},\n\n'
                    f'Your OTP for Vet Dashboard password reset is: {otp_val}\n\n'
                    f'This OTP is valid for one-time use only.\n\n'
                    f'If you did not request this, please ignore this email.\n\n'
                    f'- Team PetCareHub 🐾'
                ),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[v_email],
                fail_silently=False,
            )
            messages.success(request, "OTP sent successfully! Please check your email.")
            return redirect('vet_reset_password_url')
        else:
            messages.error(request, "No vet account found with this email.")
    return render(request, 'vet_forgot_password.html')

def vet_reset_password(request):
    reset_email = request.session.get('reset_vet_email')
    if not reset_email:
        messages.error(request, 'Session expired. Please start again.')
        return redirect('vet_forgot_password_url')

    if request.method == 'POST':
        otp_entered  = request.POST.get('otp', '').strip()
        new_pass     = request.POST.get('new_password', '').strip()
        confirm_pass = request.POST.get('confirm_password', '').strip()

        # 1. OTP format check
        if not otp_entered.isdigit() or len(otp_entered) != 6:
            messages.error(request, 'OTP must be exactly 6 digits.')
            return render(request, 'vet_reset_password.html')

        # 2. Password validation
        password_pattern = r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*_])[A-Za-z\d!@#$%^&*_]{8,16}$'
        if not re.match(password_pattern, new_pass):
            messages.error(request, 'Password must be 8-16 characters with uppercase, lowercase, number, and a special character (!@#$%^&*_).')
            return render(request, 'vet_reset_password.html')

        # 3. Passwords match
        if new_pass != confirm_pass:
            messages.error(request, 'Passwords do not match. Please try again.')
            return render(request, 'vet_reset_password.html')

        # Database Checks
        try:
            user = Vet.objects.get(email=reset_email)
        except Vet.DoesNotExist:
            messages.error(request, 'Invalid session. Please start again.')
            return redirect('vet_forgot_password_url')

        # 4. OTP already used check
        if user.otp_used == 1:
            messages.error(request, 'This OTP has already been used. Please request a new one.')
            return redirect('vet_forgot_password_url')

        # 5. OTP match check
        if user.otp != otp_entered:
            messages.error(request, 'Invalid OTP. Please enter the correct OTP.')
            return render(request, 'vet_reset_password.html')

        # All Good: Password Reset
        user.password = make_password(new_pass)
        user.otp_used = 1
        user.otp = None
        user.save()

        del request.session['reset_vet_email']

        messages.success(request, 'Password reset successful! Please login with your new password.')
        return redirect('vet_login')

    return render(request, 'vet_reset_password.html')

def vet_change_password(request):
    if 'vet_id' not in request.session:
        return redirect('vet_login')

    vet = get_object_or_404(Vet, vet_id=request.session['vet_id'])

    if request.method == 'POST':
        old_pass = request.POST.get('old_password', '')
        new_pass = request.POST.get('new_password', '')
        confirm_pass = request.POST.get('confirm_password', '')

        if not check_password(old_pass, vet.password):
            messages.error(request, "Current password is incorrect.", extra_tags='vet_security')
        elif new_pass != confirm_pass:
            messages.error(request, "New passwords do not match.", extra_tags='vet_security')
        elif len(new_pass) < 6 or len(new_pass) > 12:
            messages.error(request, "Password must be between 6 and 12 characters.", extra_tags='vet_security')
        else:
            vet.password = make_password(new_pass)
            vet.save()
            messages.success(request, "Password updated successfully! 🔒", extra_tags='vet_security')

    return redirect('vet_dashboard')

def vet_contact(request):
    if 'vet_id' not in request.session:
        return redirect('vet_login')
    
    return render(request,'vet_contact.html')