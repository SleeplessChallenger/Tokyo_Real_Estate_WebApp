from django.test import TestCase
from general.forms import ImageUpload
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client


class FormsTestCase(TestCase):
	def setUp(self):
		self.client = Client()
		self.user = User.objects.create(username='トモコ')
		self.user.set_password('RandomPassword')
		self.user.save()
		self.client.login(username='トモコ', password='RandomPassword')


	def test_form(self):
		form_data = {
			'time_to_station': 3,
			'building_year': 2015,
			'coverage_ratio': 105,
			'floor_ratio': 90,
			'property_type': 'house',
			'municipality': 'minamiyukigaya',
			'district': 'ota_ward',
			'nearest_station': 'Shinagawa',
			'structure': 'rc',
			'use': 'house',
			'city_planning': 'house', 
			'municipality_code': 3453,
			'price': 3001135,
			'age': 6,
			'image': 'some.jpg'
		}

		form = ImageUpload(data=form_data)
		self.assertTrue(form.is_valid())

	def test_error(self):
		form_data = {
			'time_to_station': 3,
			'building_year': 2015,
			'coverage_ratio': 105,
			'floor_ratio': 90,
			'property_type': 'house',
			'municipality': 'minamiyukigaya',
			'district': 'ota_ward',
			'nearest_station': 'Shinagawa',
			'structure': 'rc',
			'use': 'house',
			'city_planning': 'house', 
			'municipality_code': 3453,
			'price': 545,
			'age': '6',
			'image': 'some.jpg'
		}

		form = ImageUpload(data=form_data)
		# print(form.errors)
		# self.assertTrue(form.is_valid())
		#self.assertEquals(form.errors['age'], [''])
