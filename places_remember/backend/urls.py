from django.urls import path
from . import views


# notes = views.NotesViewSet.as_view({
#     'get': 'list',
#     'post': 'create',
# })

urlpatterns = [
    path('login', views.user_login, name='user_login'),
    path('login/vk/', views.vk_auth, name='vk_auth'),
    path('logout/', views.user_logout, name='user_logout'),

    path('', views.index, name='index'),

    path('map/', views.map, name='map'),
    path('add_note/', views.add_note, name='add_note'),
    path('delete/<int:place_id>/', views.delete_note, name='delete_note'),
]