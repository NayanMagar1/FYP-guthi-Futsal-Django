
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import HomeSlider, futsal, Booking, Contact, Profile
from datetime import date, timedelta, time
import requests
from django.conf import settings
from django.http import HttpResponse
import uuid



def home(request):
    sliders = HomeSlider.objects.all()
    profile = None

    if request.user.is_authenticated:
        # Automatically create Profile if not exist
        profile, created = Profile.objects.get_or_create(user=request.user)
    
    return render(request, "home.html", {'sliders': sliders, 'profile': profile})


# def register_view(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         email = request.POST.get("email")
#         password = request.POST.get("password")
#         confirm_password = request.POST.get("confirm_password")

#         if password != confirm_password:
#             messages.error(request, "Passwords do not match")
#             return redirect("register")

#         if User.objects.filter(username=username).exists():
#             messages.error(request, "Username already exists")
#             return redirect("register")

#         user = User.objects.create_user(
#             username=username,
#             email=email,
#             password=password
#         )
#         user.save()
#         messages.success(request, "Registration successful. Please login.")
#         return redirect("login")

#     return render(request, "register.html")

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_active=False  # ❗ IMPORTANT
        )

        # 🔐 Generate token
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        verify_link = f"http://127.0.0.1:8000/activate/{uid}/{token}/"

        # 📧 Send email
        send_mail(
            subject="Activate your account",
            message=f"Click link to verify:\n{verify_link}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
        )

        messages.success(request, "Check your email to verify account")
        return redirect("login")

    return render(request, "register.html")

from django.utils.http import urlsafe_base64_decode
def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Account activated! You can login now.")
        return redirect("login")
    else:
        return HttpResponse("Activation link invalid")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")  
        else:
            messages.error(request, "Invalid username or password")
            return redirect("login")

    return render(request, "login.html")


def futsal_list(request):
    futsals = futsal.objects.all()
    return render(request, 'futsal_list.html', {'futsals': futsals})
# @login_required
# def futsal_detail(request, id):
#     futsal_obj = futsal.objects.get(id=id)

#     today = date.today()
#     week_dates = [today + timedelta(days=i) for i in range(7)]

#     # Create time slots (6 AM - 10 PM)
#     time_slots = []
#     for hour in range(6, 22):
#         start_time = time(hour, 0)
#         end_time = time(hour + 1, 0)
#         time_slots.append((start_time, end_time))

#     bookings = Booking.objects.filter(futsal=futsal_obj)

#     # ✅ HANDLE FORM SUBMIT
#     if request.method == "POST":
#         selected_date = request.POST.get("date")
#         selected_time = request.POST.get("time")

#         # convert to proper format
#         booking_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
#         booking_time = datetime.strptime(selected_time, "%H:%M").time()

#         # ✅ CHECK IF ALREADY BOOKED
#         if Booking.objects.filter(
#             futsal=futsal_obj,
#             date=booking_date,
#             time=booking_time
#         ).exists():
#             return HttpResponse("This slot is already booked ❌")

#         # store in session
#         request.session['booking_data'] = {
#             'futsal_id': futsal_obj.id,
#             'date': selected_date,
#             'time': selected_time,
#         }

#         return redirect('khalti_payment')

#     context = {
#         'futsal': futsal_obj,
#         'week_dates': week_dates,
#         'time_slots': time_slots,
#         'bookings': bookings,
#     }

#     return render(request, 'futsal_detail.html', context)

@login_required
def futsal_detail(request, id):
    futsal_obj = futsal.objects.get(id=id)

    today = date.today()

    # ✅ next 7 days
    week_dates = [today + timedelta(days=i) for i in range(7)]

    # ✅ selected date from dropdown
    selected_date_str = request.GET.get('date')
    if selected_date_str:
        selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
    else:
        selected_date = today

    # ❌ prevent past date
    if selected_date < today:
        selected_date = today

    # ✅ time slots
    time_slots = []
    for hour in range(6, 22):
        time_slots.append(time(hour, 0))

    # ✅ bookings only for selected day
    bookings = Booking.objects.filter(
        futsal=futsal_obj,
        date=selected_date
    )

    booked_times = [b.time for b in bookings]

    # ✅ HANDLE BOOKING
    if request.method == "POST":
        selected_date = datetime.strptime(request.POST.get("date"), "%Y-%m-%d").date()
        selected_time = datetime.strptime(request.POST.get("time"), "%H:%M").time()

        if selected_date < today:
            return HttpResponse("Cannot book past date ❌")

        if Booking.objects.filter(
            futsal=futsal_obj,
            date=selected_date,
            time=selected_time
        ).exists():
            return HttpResponse("Already booked ❌")

        request.session['booking_data'] = {
            'futsal_id': futsal_obj.id,
            'date': str(selected_date),
            'time': selected_time.strftime("%H:%M"),
        }

        return redirect('khalti_payment')

    context = {
        'futsal': futsal_obj,
        'week_dates': week_dates,
        'time_slots': time_slots,
        'booked_times': booked_times,
        'selected_date': selected_date,
    }

    return render(request, 'futsal_detail.html', context)






@login_required
def khalti_payment(request):
    booking_data = request.session.get('booking_data')

    if not booking_data:
        return redirect('/')

    url = "https://a.khalti.com/api/v2/epayment/initiate/"

    headers = {
        "Authorization": f"Key {settings.KHALTI_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "return_url": "http://127.0.0.1:8000/khalti/verify/",
        "website_url": "http://127.0.0.1:8000/",
        "amount": 1000,  # Rs 10
        "purchase_order_id": str(uuid.uuid4()),
        "purchase_order_name": "Futsal Booking",
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()

    return redirect(data['payment_url'])





from datetime import datetime
from django.core.mail import send_mail

def khalti_verify(request):
    pidx = request.GET.get('pidx')

    url = "https://a.khalti.com/api/v2/epayment/lookup/"

    headers = {
        "Authorization": f"Key {settings.KHALTI_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "pidx": pidx
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()

    if data['status'] == 'Completed':

        # ✅ Prevent duplicate booking
        if Booking.objects.filter(transaction_id=pidx).exists():
            return redirect('payment_success')

        booking_data = request.session.get('booking_data')

        booking_date = datetime.strptime(booking_data['date'], "%Y-%m-%d").date()
        booking_time = datetime.strptime(booking_data['time'], "%H:%M").time()

        # ✅ Save booking
        booking = Booking.objects.create(
            futsal_id=booking_data['futsal_id'],
            user=request.user if request.user.is_authenticated else None,
            date=booking_date,
            time=booking_time,
            is_paid=True,
            transaction_id=pidx
        )

        # ✅ Send email ONLY once
        send_mail(
            subject='Futsal Booking Confirmed ✅',
            message=f"""
Hello {request.user.username},

Your booking is confirmed!

Futsal: {booking.futsal.name}
Date: {booking.date}
Time: {booking.time}
Transaction ID: {pidx}

Thank you!
""",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[request.user.email],
            fail_silently=False,
        )

        # Optional: clear session
        request.session.pop('booking_data', None)

        return redirect('payment_success')

    return redirect('payment_failed')

def logout_view(request):
    logout(request)
    return redirect("login")


def dashboard(request):
    return render(request, "dashboard.html")

def about_us(request):
    return render(request, "aboutus.html")

def contact_us(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Save to database
        Contact.objects.create(
            name=name,
            email=email,
            message=message
        )

        # Send success flag to template
        return render(request, "contactus.html", {"success": True})

    return render(request, "contactus.html")


# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile, Booking
from django.contrib.auth.models import User

@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    bookings = Booking.objects.filter(user=request.user).order_by('-date', '-time')

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        photo = request.FILES.get('photo')

        if full_name:
            profile.full_name = full_name
        if photo:
            profile.photo = photo

        profile.save()
        return redirect('profile')

    return render(request, 'profile.html', {'profile': profile, 'bookings': bookings})
@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-date', '-time')
    return render(request, 'my_bookings.html', {'bookings': bookings})



from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib import messages
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()  # This hashes the password properly
            update_session_auth_hash(request, user)  # Keep the user logged in after password change
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'change_password.html', {'form': form})

def payment_success(request):
    booking = Booking.objects.filter(user=request.user).order_by('-created_at').first()
    return render(request, 'payment_success.html', {'booking': booking})


def payment_failed(request):
    return HttpResponse("Payment Failed ❌ Try again")
