from django.test import TestCase
from users.forms import (UserRegistration, UserChange,
	ProfileChange, UserDelete)
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client


class FormsTestCase(TestCase):
	def setUp(self):
		pass

	def test_register(self):
		form_data = {
			'username': 'ツナデ',
			'email': 'tm@mail.com',
			'password1': 'Secure614',
			'password2': 'Secure614',
		}

		form = UserRegistration(data=form_data)
		self.assertTrue(form.is_valid())

	def test_user(self):
		form_data = {
			'username': 'ミナト',
			'email': 'm@jap.com'
		}

		form = UserChange(data=form_data)
		self.assertTrue(form.is_valid())

	def test_profile(self):
		form_data = {
			'first_name': 'サルトビ',
			'last_name': 'ヒルゼン',
			'country': 'Japan',
			'image': 'hokage.jpg',
		}

		form = ProfileChange(data=form_data)
		self.assertTrue(form.is_valid())

	def test_delete(self):
		form_data = {}
		form = UserDelete(data=form_data)
		self.assertTrue(form.is_valid())
