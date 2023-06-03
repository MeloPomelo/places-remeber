from django.urls import path
from . import views


urlpatterns = [
    path('login', views.user_login, name='user_login'),
    path('login/vk/', views.vk_login, name='vk_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('', views.home, name='home'),
    path('map/', views.map, name='map'),
    path('add_note/', views.add_note, name='add_note'),
    path('delete/<int:place_id>/', views.delete_place, name='delete_place'),
]