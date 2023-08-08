import html

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
# from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.
from django.shortcuts import render, redirect
from .models import Room, Booking
from .form import BookingForm
from bs4 import BeautifulSoup


def log_in(request):
    if request.method == "POST":
        username = request.POST.get("email")
        pass1 = request.POST.get("pass1")
        user = authenticate(username=username, password=pass1)

        print(username)
        print(pass1)
        if user:
            login(request, user)
            print("login success")
            return redirect("/")
        else:
            messages.error(request, 'Please Enter Valid Credentials!')
            return render(request, "main/login.html")
    else:
        return render(request, 'main/login.html')


def register(request):
    if request.method == "POST":

        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        if len(username) > 15:
            messages.error(request, "*Your user name must be under 10 characters")
            return render(request, 'main/register.html')

        if not username.isalnum():
            messages.error(request, "*User name should only contain letters and numbers")
            return render(request, 'main/register.html')
        SpecialSym = ['$', '@', '#', '%']

        if len(pass1) < 6:
            messages.error(request, '''*Password's length should be at least 6''')

            return render(request, 'main/register.html')

        if len(pass1) > 20:
            messages.error(request, '''*Password's length should be not be greater than 20''')

            return render(request, 'main/register.html')

        if not any(char.isdigit() for char in pass1):
            messages.error(request, '*Password should have at least one numeric / digit')

            return render(request, 'main/register.html')

        if not any(char.isupper() for char in pass1):
            messages.error('*Password should have at least one uppercase letter')

            return render(request, 'main/register.html')

        if not any(char.islower() for char in pass1):
            messages.error(request, '*Password should have at least one lowercase letter')

            return render(request, 'main/register.html')

        user_obj = User.objects.create(username=username, email=email)
        user_obj.set_password(pass1)
        user_obj.save()
        return render(request, "main/login.html")

    return render(request, 'main/register.html')


class MyView(TemplateView):
    template_name = 'louyats/base.html'


class Facilities(TemplateView):
    template_name = 'main/facilities.html'


def room_view(request):
    rooms = Room.objects.filter()
    return render(request, 'main/room_list.html', {'rooms': rooms})


def book_room(request, room_id):
    if request.method == 'POST':
        room = Room.objects.get(id=room_id)
        guest_name = request.POST['guest_name']
        check_in_date = request.POST['check_in_date']
        check_out_date = request.POST['check_out_date']
        booking = Booking.objects.create(room=room, guest_name=guest_name, check_in_date=check_in_date,
                                         check_out_date=check_out_date)
        # Perform any additional logic or operations
        return redirect('booking_success')
    else:
        room = Room.objects.get(id=room_id)
        return render(request, 'main/book_room.html', {'room': room})


def booking_detail(request, ):
    booking = Booking.objects.get()
    return render(request, 'main/booking_detail.html', {'booking': booking})


def booking_success(request):
    return render(request, 'main/booking_success.html')


def booking_view(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            room_number = form.cleaned_data['room_number']
            check_in_date = form.cleaned_data['check_in_date']
            check_out_date = form.cleaned_data['check_out_date']
            guest_name = form.cleaned_data['guest_name']

            room = Room.objects.get(room_number=room_number)
            if room.availability:
                booking = Booking.objects.create(room=room, check_in_date=check_in_date, check_out_date=check_out_date,
                                                 guest_name=guest_name)
                room.availability = False
                room.save()
                return redirect('booking_success')
            else:
                return redirect('booking_failed')
    else:
        form = BookingForm()

    return render(request, 'main/book_room.html', {'form': form})


