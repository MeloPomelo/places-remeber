import json

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from .forms import PlaceForm
from .models import Place


def get_user_data(request):
    user = request.user  
    first_name = user.first_name
    last_name = user.last_name
    places = Place.objects.filter(user=request.user)  
    places_json = json.dumps([place.to_json() for place in places])

    context = {
        'places': places,
        'places_json': places_json,
        'first_name': first_name,
        'last_name': last_name,
    }

    return context


def user_login(request):
    return render(request, 'registration/login.html')


def vk_auth(request):
    if request.user.is_authenticated:
        return redirect('index')  
    
    return redirect('social:begin', backend='vk-oauth2')


@login_required
def user_logout(request):
    logout(request)
    return redirect('user_login')


@login_required
def index(request):
    return render(request, 'index.html', get_user_data(request=request))


@login_required
def map(request):
    return render(request, 'map.html', get_user_data(request=request))


def add_note(request):
    if request.method == 'POST':
        form = PlaceForm(request.POST)
        if form.is_valid():
            place = form.save(commit=False)
            place.user = request.user
            place.save()
            return redirect('index')
    else:
        form = PlaceForm()

    context= get_user_data(request=request)
    context['form'] = form

    return render(request, 'add_note.html', context)


def delete_note(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    if place.user == request.user:
        place.delete()
    return redirect('index')
