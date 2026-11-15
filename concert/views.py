from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
import requests
from .forms import LoginForm, SignUpForm
from .models import Concert, ConcertAttending

def index(request):
    return render(request, 'index.html')

def signup(request):
    form = SignUpForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = User.objects.create_user(**form.cleaned_data)
        login(request, user)
        return redirect('index')
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('index')
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

def remote_page(request, url, template, key):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        records = response.json()
    except (requests.RequestException, ValueError):
        return HttpResponse('The requested service is temporarily unavailable.', status=503)
    return render(request, template, {key: records if isinstance(records, list) else [records]})

def songs(request):
    return remote_page(request, settings.SONGS_API_URL + '/song', 'songs.html', 'songs')

def photos(request):
    return remote_page(request, settings.PICTURES_API_URL + '/picture/1', 'photos.html', 'photos')

@login_required(login_url='login')
def concerts(request):
    statuses = dict(ConcertAttending.objects.filter(user=request.user).values_list('concert_id', 'attending'))
    records = [{'concert': concert, 'status': statuses.get(concert.id, '-')} for concert in Concert.objects.order_by('date')]
    return render(request, 'concerts.html', {'concerts': records})

@login_required(login_url='login')
def concert_detail(request, id):
    concert = get_object_or_404(Concert, pk=id)
    attendance = concert.attendee.filter(user=request.user).first()
    return render(request, 'concert_detail.html', {'concert_details': concert, 'status': attendance.attending if attendance else '-', 'attending_choices': ConcertAttending.AttendingChoices.choices})

@login_required(login_url='login')
@require_POST
def concert_attendee(request):
    concert = get_object_or_404(Concert, pk=request.POST.get('concert_id'))
    status = request.POST.get('attendee_choice')
    if status not in ConcertAttending.AttendingChoices.values:
        return HttpResponse('Invalid attendance choice.', status=400)
    ConcertAttending.objects.update_or_create(concert=concert, user=request.user, defaults={'attending': status})
    return redirect('concerts')
