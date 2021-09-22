from django.test import TestCase
from general.models import PropertyClass
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
import json


class PropertyTestCase(TestCase):
	def setUp(self):
		self.client = Client()
		self.user = User.objects.create(username='ナルト')
		self.user.set_password('SomePass')
		self.user.save()
		
		PropertyClass.objects.get_or_create(
			id=32,
			title='Random Title',
			author=self.user,
			age=5,
			municipality_code=342,
			city_planning='house',
			use='shop',
			structure='rc',
			nearest_station='Tokyo',
			district='minamiyukigaya',
			municipality='ota_ward',
			property_type='residential_land',
			floor_ratio=150,
			coverage_ratio=80,
			building_year=2016,
			time_to_station=7,
			price=23434353
		)

	def test_home_page(self):
		url = reverse('start-page')
		response = self.client.get(url)
		self.assertEquals(response.status_code, 200)

	def test_all_posts(self):
		url = reverse('all_info')
		response = self.client.get(url)
		self.assertEquals(response.status_code, 200)

	def test_add_post(self):
		url = reverse('user-create-post')
		new_post = {
			'id': 500,
			'title': 'Random Title',
			'author': self.user,
			'age': 5,
			'municipality_code': 342,
			'city_planning': 'house',
			'use': 'shop',
			'structure': 'rc',
			'nearest_station': 'Tokyo',
			'district': 'minamiyukigaya',
			'municipality': 'ota_ward',
			'property_type': 'residential_land',
			'floor_ratio': 150,
			'coverage_ratio': 80,
			'building_year': 2016,
			'time_to_station': 7,
			'price': 23434353
		}

		response = self.client.post(url, new_post, follow=True)
		response_url = response.redirect_chain[0][0]
		response_code = response.redirect_chain[0][1]
		self.assertEquals(response_url, '/login/?next=/post/new/')
		self.assertEquals(response_code, 302)

		self.client.login(username='ナルト', password='SomePass')
		response = self.client.post(url, new_post, follow=True)
		response_url = response.redirect_chain[0][0]
		redirect_code = response.redirect_chain[0][1]

		self.assertEquals(redirect_code, 302)
		self.assertEquals(response_url, '/all_properties')

		# test db being affected
		posts = PropertyClass.objects.all()
		self.assertEquals(posts.count(), 2)

	def test_single_post(self):
		# non-existing
		url = reverse('post-info', kwargs={'pk': 35})
		response = self.client.get(url)
		self.assertEquals(response.status_code, 404)

		# observe
		url = reverse('post-info', kwargs={'pk': 32})
		response = self.client.get(url)
		self.assertEquals(response.status_code, 200)

		# trying update/delete being non-logged in
		url = reverse('post-update', kwargs={'pk': 32})
		response = self.client.get(url)
		self.assertEquals(response.status_code, 302)

		url = reverse('post-delete', kwargs={'pk': 32})
		response = self.client.get(url)
		self.assertEquals(response.status_code, 302)

		# trying update/delete being logged in
		url = reverse('post-update', kwargs={'pk': 32})
		self.client.login(username='ナルト', password='SomePass')
		response = self.client.get(url)
		self.assertEquals(response.status_code, 200)

		url = reverse('post-delete', kwargs={'pk': 32})
		response = self.client.get(url)
		self.assertEquals(response.status_code, 200)

	def test_login(self):
		response = self.client.post('/login/',
			{'username': 'ナルト', 'password': 'RandomPass54'})

		self.assertEquals(response.status_code, 200)

	def test_register(self):
		response = self.client.post('/register/', data={
			'username': 'サスケ',
			'email': 'd@mail.com',
			'password1': 'newPassword435',
			'password2': 'newPassword435',
			})
		
		self.assertEquals(response.status_code, 302)
		self.assertEquals(response.url, '/login/')

	def test_logged_in(self):
		url = reverse('user-create-post')

		# before login
		response = self.client.get(url, follow=True)
		redirect_url = response.redirect_chain[0][0]
		redirect_code = response.redirect_chain[0][1]

		self.assertEquals(redirect_code, 302)
		self.assertEquals(redirect_url, '/login/?next=/post/new/')

		# after
		self.client.login(username='ナルト', password='SomePass')
		response = self.client.get(url, follow=True)
		# as user is logged, no redirect
		self.assertEquals(response.redirect_chain, [])
		self.assertEquals(response.status_code, 200)

	def _create_user(self):
		user = User.objects.create(username='キバ')
		user.set_password('newUserpass46')
		user.save()
		return user

	def test_delete(self):
		# single & many pages
		url = reverse('post-delete', kwargs={'pk': 32})
		self._create_user()

		# another user
		self.client.login(username='キバ', password='newUserpass46')
		response = self.client.get(url)
		self.assertEquals(response.status_code, 403)

		url = reverse('erase-all-posts', kwargs={'username': 'ナルト'})
		response = self.client.get(url)
		self.assertEquals(response.status_code, 200)

		response = self.client.post(url, follow=True)
		response_url = response.redirect_chain[0][0]
		response_code = response.redirect_chain[0][1]
		self.assertEquals(response_code, 302)
		self.assertEquals(response_url, '/')
