import json

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from .forms import PlaceForm
from .models import Place


def user_login(request):
    return render(request, 'registration/login.html')


def vk_login(request):
    if request.user.is_authenticated:
        return redirect('home')  
    
    return redirect('social:begin', backend='vk-oauth2')


@login_required
def user_logout(request):
    logout(request)
    return redirect('user_login')


@login_required
def home(request):
    user = request.user  

    first_name = user.first_name
    last_name = user.last_name

    places = Place.objects.filter(user=request.user)
    places_json = json.dumps([place.to_json() for place in places])


    context = {
        'first_name': first_name,
        'last_name': last_name,
        # 'avatar': avatar,
        'places': places,
        'places_json': places_json,
    }

    return render(request, 'home.html', context)


def map(request):
    places = Place.objects.filter(user=request.user)
    places_json = json.dumps([place.to_json() for place in places])

    user = request.user  
    first_name = user.first_name
    last_name = user.last_name

    context = {
        'places': places,
        'places_json': places_json,
        'first_name': first_name,
        'last_name': last_name,
    }
    return render(request, 'map.html', context)


@login_required
def add_note(request):
    if request.method == 'POST':
        form = PlaceForm(request.POST)
        if form.is_valid():
            place = form.save(commit=False)
            place.user = request.user
            place.save()
            return redirect('home')
    else:
        form = PlaceForm()

    places = Place.objects.filter(user=request.user)
    places_json = json.dumps([place.to_json() for place in places])

    user = request.user  

    first_name = user.first_name
    last_name = user.last_name

    context = {
        'form': form,
        'places': places,
        'places_json': places_json,
        'first_name': first_name,
        'last_name': last_name,
    }
    return render(request, 'add_note.html', context)


@login_required
def delete_place(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    if place.user == request.user:
        place.delete()
    return redirect('home')
