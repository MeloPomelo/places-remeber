import json
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Place
from .forms import PlaceForm


class YourAppTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
    

    def test_index(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)


    def test_get_user_data(self):
        place = Place.objects.create(user=self.user, name='test_name', comment='test_comment', latitude=55.978489, longitude=55.978489)
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertEqual(response.context['first_name'], self.user.first_name)
        self.assertEqual(response.context['last_name'], self.user.last_name)
        self.assertEqual(list(response.context['places']), [place])
        self.assertEqual(response.context['places_json'], json.dumps([place.to_json()]))


    def test_user_login(self):
        response = self.client.get(reverse('user_login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')


    def test_vk_auth_authenticated(self):
        response = self.client.get(reverse('vk_auth'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))


    def test_user_logout(self):
        response = self.client.get(reverse('user_logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user_login'))
        self.assertFalse('_auth_user_id' in self.client.session)


    def test_index(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


    def test_map(self):
        response = self.client.get(reverse('map'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'map.html')


    def test_add_note_get(self):
        response = self.client.get(reverse('add_note'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_note.html')
        self.assertIsInstance(response.context['form'], PlaceForm)


    def test_add_note_post_valid(self):
        form_data = {
            'name': 'New Place',
            'comment': 'Some description',
            'latitude': 55.978489,
            'longitude': 37.646866,
        }
        response = self.client.post(reverse('add_note'), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
        self.assertEqual(Place.objects.count(), 1)
        place = Place.objects.first()
        self.assertEqual(place.name, 'New Place')
        self.assertEqual(place.user, self.user)


    def test_delete_note(self):
        place = Place.objects.create(user=self.user, name='test_name', comment='test_comment', latitude=55.978489, longitude=55.978489)
        response = self.client.post(reverse('delete_note', kwargs={'place_id': place.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
        self.assertEqual(Place.objects.count(), 0)
