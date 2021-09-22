from django.test import TestCase
from general.models import PropertyClass
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse


class LoaderViewTestCase(TestCase):
	def setUp(self):
		self.client = Client()

	def test_get(self):
		url = reverse('make_injection')
		response = self.client.get(url)
		self.assertEquals(response.status_code, 200)

	def _register_user(self, super_user=False):
		if super_user:
			user = User.objects.create_superuser(username='ナガト')
			user.set_password('SixPaths39')
			user.save()
		else:
			user = User.objects.create(username='サソリ')
			user.set_password('RedSand53')
			user.save()


	def test_post(self):
		url = reverse('make_injection')

		# not logged in
		response = self.client.post(url, follow=True)
		response_code = response.redirect_chain[0][1]
		response_url = response.redirect_chain[0][0]
		self.assertEquals(response_code, 302)
		self.assertEquals(response_url, '/all_properties')

		# ordinary user
		self._register_user()
		self.client.login(username='サソリ', password='RedSand53')
		response = self.client.post(url, follow=True)

		message = list(response.context.get('messages'))

		response_code = response.redirect_chain[0][1]
		response_url = response.redirect_chain[0][0]
		self.assertEquals(response_code, 302)
		self.assertEquals(response_url, '/all_properties')
		self.assertEquals(str(message[0]), "You don't have rights to make this action")

		# super_user
		self._register_user(super_user=True)
		self.client.login(username='ナガト', password='SixPaths39')
		response = self.client.post(url, follow=True)

		message = list(response.context.get('messages'))

		response_code = response.redirect_chain[0][1]
		response_url = response.redirect_chain[0][0]
		self.assertEquals(response_code, 302)
		self.assertEquals(response_url, '/all_properties')
		self.assertEquals(str(message[0]), "Data has been injected")
