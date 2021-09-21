from django.test import TestCase
from general.models import PropertyClass
from users.models import Profile
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model


class UserTestCase(TestCase):
	def setUp(self):
		self.client = Client()


	def test_register_login(self):
		# register at first
		url = reverse('register-newcomer')
		response = self.client.get(url)
		self.assertEquals(response.status_code, 200)

		response = self.client.post(url, data={
			'username': 'サスケ',
			'email': 'd@mail.com',
			'password1': 'newPassword435',
			'password2': 'newPassword435',
			})

		# test that db was affected
		self.assertEquals(response.status_code, 302)
		user = get_user_model().objects.all()
		self.assertEquals(user.count(), 1)

		# login
		url = reverse('login')
		response = self.client.get(url)
		self.assertEquals(response.status_code, 200)

		url = reverse('login')
		response = self.client.post(url, data={
			'username': 'サスケ',
			'password':  'newPassword435'
			})

		self.assertEquals(response.status_code, 302)
		self.assertEquals(int(self.client.session['_auth_user_id']), user[0].pk)

	def _regsiter_login(self):
		user = User.objects.create(username='イタチ')
		user.set_password('UchihaPassword')
		user.save()
		self.client.login(username='イタチ', password='UchihaPassword')

	def test_profile(self):
		self._regsiter_login()

		url = reverse('profile')
		response = self.client.get(url)
		self.assertEquals(response.status_code, 200)

		response = self.client.post(url, data={
			'username': 'イタチ_ウチハ',
			'email': 'i@gmail.com',
			'first_name': 'アノニマス',
			'last_name': 'アノニマス',
			'country': 'Japan',
			'image': 'イメージ.jpg',
			})
		print(response)

		response = self.client.post(url, data={
			'username': 'イタチ_ウチハ',
			'email': 'i@gmail.com',
			'first_name': 'アノニマス',
			'last_name': 'アノニマス',
			'country': 'Japan',
			'image': 'イメージ.jpg',
			}, follow=True)
		print(response)
		# self.assertEquals(response.status_code, 200)

		# user = get_user_model().objects.all()
		# user[0].refresh_from_db()
		# print(user)



