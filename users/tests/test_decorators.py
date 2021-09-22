from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from users.decorators import login_required_message
from django.http import HttpResponse


class DecoratorTestCase(TestCase):
	def setUp(self):
		self.client = Client()

	def test_decorator(self):
		user = User.objects.create(
			username='キサメ', password='SomeQpAss54')
		factory = RequestFactory()

		@login_required_message
		def wrapper(request):
			return HttpResponse()

		url = reverse('profile')
		request = factory.get(url)
		request.user = user
		response = wrapper(request)
		self.assertEquals(response.status_code, 200)

	def test_message(self):
		url = reverse('profile')
		response = self.client.get(url)
		self.assertRedirects(response, '/login/?next=/profile-info/')
