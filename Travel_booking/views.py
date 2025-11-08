from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')


def mybookings(request):
    from bookings.models import Booking
    if not request.user.is_authenticated:
        return redirect('login')
    latest_id = request.GET.get('latest')
    if latest_id:
        bookings = Booking.objects.filter(user=request.user, id=latest_id)
        show_only_latest = True
    else:
        bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
        show_only_latest = False
    return render(request, 'mybookings.html', {'bookings': bookings, 'show_only_latest': show_only_latest})

def users(request):
    return render(request, 'users.html')

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'users.html', {'form': form, 'action': 'login'})

def user_logout(request):
    logout(request)
    return redirect('home')

def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def dashboard(request):
    # You can add user-specific context here later
    return render(request, 'dashboard.html')
