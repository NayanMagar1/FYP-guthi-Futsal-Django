
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
            password=password
        )
        user.save()
        messages.success(request, "Registration successful. Please login.")
        return redirect("login")

    return render(request, "register.html")


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

def futsal_detail(request, id):
    futsal_obj = futsal.objects.get(id=id)

    today = date.today()
    week_dates = [today + timedelta(days=i) for i in range(7)]

    # Create time slots (6 AM - 10 PM)
    time_slots = []
    for hour in range(6, 22):
        start_time = time(hour, 0)
        end_time = time(hour + 1, 0)
        time_slots.append((start_time, end_time))

    bookings = Booking.objects.filter(futsal=futsal_obj)

    # ✅ HANDLE FORM SUBMIT
    if request.method == "POST":
        selected_date = request.POST.get("date")
        selected_time = request.POST.get("time")

        # convert to proper format
        booking_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
        booking_time = datetime.strptime(selected_time, "%H:%M").time()

        # ✅ CHECK IF ALREADY BOOKED
        if Booking.objects.filter(
            futsal=futsal_obj,
            date=booking_date,
            time=booking_time
        ).exists():
            return HttpResponse("This slot is already booked ❌")

        # store in session
        request.session['booking_data'] = {
            'futsal_id': futsal_obj.id,
            'date': selected_date,
            'time': selected_time,
        }

        return redirect('khalti_payment')

    context = {
        'futsal': futsal_obj,
        'week_dates': week_dates,
        'time_slots': time_slots,
        'bookings': bookings,
    }

    return render(request, 'futsal_detail.html', context)


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
        booking_data = request.session.get('booking_data')

        booking_date = datetime.strptime(booking_data['date'], "%Y-%m-%d").date()
        booking_time = datetime.strptime(booking_data['time'], "%H:%M").time()

        Booking.objects.create(
            futsal_id=booking_data['futsal_id'],
            user=request.user if request.user.is_authenticated else None,
            date=booking_date,
            time=booking_time,
            is_paid=True,
            transaction_id=pidx
        )

        return HttpResponse("Payment Successful ✅ Booking Confirmed")

    return HttpResponse("Payment Failed ❌")

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
