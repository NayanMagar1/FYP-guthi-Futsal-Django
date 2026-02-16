from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import HomeSlider, futsal, Booking
from datetime import date, timedelta, time


def home(request):
    sliders = HomeSlider.objects.all()
    return render(request, "home.html", {'sliders': sliders})

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
            return redirect("dashboard")  # you can change later
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

    # Create time slots from 6 AM to 10 PM
    # time_slots = []
    # for hour in range(6, 22):   # 22 = 10PM
    #     time_slots.append(time(hour, 0))

    # bookings = Booking.objects.filter(futsal=futsal_obj)

    # context = {
    #     'futsal': futsal_obj,
    #     'week_dates': week_dates,
    #     'time_slots': time_slots,
    #     'bookings': bookings,
    # }


    # views.py
    time_slots = []
    for hour in range(6, 22):  # 6AM to 10PM
        start_time = time(hour, 0)
        end_time = time(hour+1, 0)
        time_slots.append((start_time, end_time))
    
    bookings = Booking.objects.filter(futsal=futsal_obj)

    # In context
    context = {
        'futsal': futsal_obj,
        'week_dates': week_dates,
        'time_slots': time_slots,   # now a list of tuples (start, end)
        'bookings': bookings,
    }


    return render(request, 'futsal_detail.html', context)


def logout_view(request):
    logout(request)
    return redirect("login")


def dashboard(request):
    return render(request, "dashboard.html")

def about_us(request):
    return render(request, "aboutus.html")

def contact_us(request):
    return render(request, "contactus.html")
