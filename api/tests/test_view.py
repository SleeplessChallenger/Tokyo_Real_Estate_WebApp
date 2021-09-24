from rest_framework.test import APIRequestFactory
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse
from api.serializers import UserSerializer, PropertySerializer
from django.shortcuts import get_object_or_404
from general.models import PropertyClass
import json


class ViewTestCase(TestCase):
	def setUp(self):
		# self.factory = APIRequestFactory()
		self.client = Client()
		self.user = User.objects.create(username='ネジ')
		self.user.set_password('somePass53')
		self.user.save()


	def test_get(self):
		url = reverse('all-users-api')
		response = self.client.get(url)
		users = User.objects.all()
		serializer = UserSerializer(users, many=True)
		self.assertEquals(response.data, serializer.data)
		self.assertEquals(response.status_code, 200)

		url = reverse('one-user-api', kwargs={'pk': 1})
		response = self.client.get(url)
		users = User.objects.filter(pk=1)
		serializer = UserSerializer(users, many=True)
		serializer_data = dict(serializer.data[0])
		self.assertEquals(response.data, serializer_data)
		self.assertEquals(response.status_code, 200)

		url = reverse('one-user-api', kwargs={'pk': 43})
		response = self.client.get(url)
		self.assertEquals(response.status_code, 204)

	def test_post(self):
		url = reverse('all-users-api')
		response = self.client.post(url, data={
			'username': 'オロチマル',
			'password': 'SomePass43',
			})

		self.assertEquals(response.status_code, 201)

		response = self.client.post(url, data={
			'username': 'ネジ',
			'password': 'somePass53'
			})
		self.assertEquals(response.status_code, 409)

		response = self.client.post(url, data={
			'username': 'アスマ',
			'password': '',
			})
		self.assertEquals(response.status_code, 409)

	def test_patch(self):
		# without pk/id
		url = reverse('all-users-api')
		data = json.dumps({
			"email": "some@mail.com",
			})

		response = self.client.patch(url, data,
			content_type='application/json')
		self.assertEquals(response.status_code, 406)

		# pk
		data = json.dumps({
			"pk": 1,
			"email": "random@mail.com",
			
		})
		response = self.client.patch(url, data,
			content_type='application/json')

		self.assertEquals(response.status_code, 200)

		#bad pk
		data = json.dumps({
			"pk": 4534,
			"email": "some@mail.com"
		})

		response = self.client.patch(url, data,
			content_type='application/json')

		self.assertEquals(response.status_code, 204)

		# bad changes
		data = json.dumps({
			"pk": 1,
			"email": "some.com"
		})

		response = self.client.patch(url, data,
			content_type='application/json')

		self.assertEquals(response.status_code, 400)

	def _create_user(self):
		user = User.objects.create(username='ツナデ')
		user.set_password('somePass534')
		user.save()

	def test_delete(self):
		# no pk
		url = reverse('all-users-api')
		response = self.client.delete(url)
		self.assertEquals(response.status_code, 400)

		# incorrect pk
		url = reverse('one-user-api', kwargs={'pk': 434})
		response = self.client.delete(url)
		self.assertEquals(response.status_code, 400)

		# correct pk
		self._create_user()
		url = reverse('one-user-api', kwargs={'pk': 2})
		response = self.client.delete(url)
		self.assertEquals(response.status_code, 200)


class PropertyTestCase(TestCase):
	def setUp(self):
		self.client = Client()
		self.user = User.objects.create(username='サクラ')
		self.user.set_password('Password324')
		self.user.save()

		PropertyClass.objects.get_or_create(
			id=1,
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

	def test_get(self):
		url = reverse('all-properties-api')
		response = self.client.get(url)
		self.assertEquals(response.status_code, 200)

		url = reverse('one-property-api', kwargs={'pk': 1})
		response = self.client.get(url)
		property_one = PropertyClass.objects.filter(pk=1)
		serializer = PropertySerializer(property_one, many=True)
		serializer_data = dict(serializer.data[0])
		self.assertEquals(response.data, serializer_data)
		self.assertEquals(response.status_code, 200)

		url = reverse('one-user-api', kwargs={'pk': 43})
		response = self.client.get(url)
		self.assertEquals(response.status_code, 204)

	def _get_property_data(self, bad_data=False):
		if not bad_data:
			data = {
			'id': 2,
			'title': 'Random Title',
			'author': self.user.pk,
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
		else:
			data = {
			'id': 3,
			'title': 'Random Title',
			'author': self.user.pk,
			'age': 5,
			'municipality_code': '',
			'city_planning': 'house',
			'use': 'shop',
			'structure': 'rc',
			'nearest_station': 'Tokyo',
			'district': 'minamiyukigaya',
			'municipality': 'ota_ward',
			'property_type': 'residential_land',
			'floor_ratio': '150',
			'coverage_ratio': 80,
			'building_year': 2016,
			'time_to_station': 7,
			'price': 23434353
			}

		return data	

	def _create_superuser(self):
		user = User.objects.create_superuser(username='ザブザ')
		user.set_password('Momochi43')
		user.save()
		return user

	def test_post(self):
		# not logged in
		url = reverse('all-properties-api')
		response = self.client.post(url, self._get_property_data())

		self.assertEquals(response.status_code, 400)

		# logged in, not passing checks
		self.client.login(
			username='サクラ', password='Password324')

		data = self._get_property_data()
		response = self.client.post(url, data)
		self.assertEquals(response.status_code, 409)

		# logged in, OK
		super_user = self._create_superuser()
		self.client.login(username='ザブザ', password='Momochi43')
		response = self.client.post(url, data)

		self.assertEquals(response.status_code, 200)

		post = PropertyClass.objects.filter(pk=2)
		serializer = PropertySerializer(post, many=True)
		serializer_data = dict(serializer.data[0])
		self.assertEquals(response.data, serializer_data)

		# logged in data with error
		data = self._get_property_data(bad_data=True)
		response = self.client.post(url, data)
		self.assertEquals(response.status_code, 400)

	def test_patch(self):
		# without id/pk of user
		url = reverse('all-properties-api')
		data = json.dumps({
			"title": "New random super title"
		})
		response = self.client.patch(url, data,
			content_type='application/json')

		self.assertEquals(response.status_code, 400)

		# checks with errors
		url = reverse('all-properties-api')
		data = json.dumps({
			"title": "Rewritten title",
			"pk": 1,
			})

		response = self.client.patch(url, data,
			content_type='application/json')

		self.assertEquals(response.status_code, 400)

		# superuser with wrong pk/id of post
		user = self._create_superuser()
		self.client.login(username='ザブザ', password='Momochi43')

		data = json.dumps({
			"title": "Here is title",
			"pk": 431,
			})

		response = self.client.patch(url, data,
			content_type='application/json')

		self.assertEquals(response.status_code, 400)

		# superuser without errors
		data = json.dumps({
			"pk": 1,
			"age": 20,
			})

		response = self.client.patch(url, data,
			content_type='application/json')
		
		self.assertEquals(response.status_code, 202)

		post = PropertyClass.objects.filter(pk=1)
		serializer = PropertySerializer(post, many=True)
		serializer_data = dict(serializer.data[0])
		self.assertEquals(serializer_data.get('age'), 20)

		# superuser with bad changes
		data = json.dumps({
			"pk": 1,
			"time_to_station": "",
			})

		response = self.client.patch(url, data,
			content_type='application/json')

		self.assertEquals(response.status_code, 400)

	def test_delete(self):
		pass









