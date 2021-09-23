from rest_framework.test import APIRequestFactory
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse
from api.serializers import UserSerializer
from django.shortcuts import get_object_or_404
import json


class ViewTestCase(TestCase):
	def setUp(self):
		# self.factory = APIRequestFactory()
		self.client = Client()
		self.user = User.objects.create(username='ネジ')
		self.user.set_password('somePass53')
		self.user.save()


	def test_users(self):
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

	def test_posts(self):
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

	def test_patch(self):
		# without pk/id
		url = reverse('all-users-api')
		data = json.dumps({
			"email": "some@mail.com",
			})

		response = self.client.patch(url, data,
			content_type='application/json')
		self.assertEquals(response.status_code, 406)

		# pk/bad pk/bad changes
		url = reverse('all-users-api')
		data = json.dumps({
			"pk": 1,
			"email": "random@mail.com",
			
		})
		response = self.client.patch(url, data,
			content_type='application/json')

		self.assertEquals(response.status_code, 200)



