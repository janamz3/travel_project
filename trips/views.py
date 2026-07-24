from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Trip, Destination
from .forms import TripForm, SearchForm


# عرض الرحلات مع البحث والتصفية
def trip_list(request):
    trips = Trip.objects.all()
    form = SearchForm(request.GET or None)

    if request.GET.get('search'):
        trips = trips.filter(Q(title__icontains=request.GET.get('search')) |
                             Q(destination__name__icontains=request.GET.get('search')))

    if request.GET.get('trip_type'):
        trips = trips.filter(destination__trip_type=request.GET.get('trip_type'))

    if request.GET.get('max_budget'):
        try:
            trips = trips.filter(budget__lte=int(request.GET.get('max_budget')))
        except:
            pass

    return render(request, 'trips/trip_list.html', {'trips': trips, 'form': form})


# تفاصيل الرحلة
def trip_detail(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    similar = Trip.objects.filter(destination=trip.destination).exclude(pk=pk)[:3]
    return render(request, 'trips/trip_detail.html', {'trip': trip, 'similar': similar})


# إضافة رحلة
@login_required(login_url='admin:login')
def add_trip(request):
    if request.method == 'POST':
        form = TripForm(request.POST, request.FILES)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.user = request.user
            trip.save()
            return redirect('trip_detail', pk=trip.pk)
    else:
        form = TripForm()
    return render(request, 'trips/trip_form.html', {'form': form, 'title': 'إضافة رحلة'})


# تعديل رحلة
@login_required(login_url='admin:login')
def edit_trip(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    if trip.user != request.user:
        return redirect('trip_list')

    if request.method == 'POST':
        form = TripForm(request.POST, request.FILES, instance=trip)
        if form.is_valid():
            form.save()
            return redirect('trip_detail', pk=trip.pk)
    else:
        form = TripForm(instance=trip)
    return render(request, 'trips/trip_form.html', {'form': form, 'title': 'تعديل الرحلة'})


# حذف رحلة
@login_required(login_url='admin:login')
def delete_trip(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    if trip.user != request.user:
        return redirect('trip_list')

    if request.method == 'POST':
        trip.delete()
        return redirect('trip_list')
    return render(request, 'trips/delete.html', {'trip': trip})


# رحلاتي
@login_required(login_url='admin:login')
def my_trips(request):
    trips = request.user.trips.all()
    return render(request, 'trips/my_trips.html', {'trips': trips})


# التوصيات (حسب نوع السفر والميزانية والمدة)
def recommendations(request):
    trips = Trip.objects.all()
    destinations = Destination.objects.all()

    if request.method == 'POST':
        trip_type = request.POST.get('trip_type')
        budget = request.POST.get('budget')
        duration = request.POST.get('duration')

        if trip_type:
            destinations = destinations.filter(trip_type=trip_type)
            trips = trips.filter(destination__trip_type=trip_type)

        if budget:
            try:
                trips = trips.filter(budget__lte=int(budget))
            except:
                pass

        if duration:
            try:
                trips = trips.filter(duration__lte=int(duration))
            except:
                pass

    return render(request, 'trips/recommendations.html', {
        'trips': trips[:6],
        'destinations': destinations[:6]
    })


from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if password != password_confirm:
            return render(request, 'trips/signup.html', {'error': 'كلمات المرور غير متطابقة'})

        if User.objects.filter(username=username).exists():
            return render(request, 'trips/signup.html', {'error': 'المستخدم موجود بالفعل'})

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('trip_list')

    return render(request, 'trips/signup.html')
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('trip_list')


from django.contrib.auth import authenticate, login as auth_login


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('trip_list')
        else:
            return render(request, 'trips/login.html', {'error': 'بيانات الدخول خاطئة'})

    return render(request, 'trips/login.html')