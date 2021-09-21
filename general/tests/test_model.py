from django.test import TestCase
from django.contrib.auth.models import User
from general.models import PropertyClass


class ModelTestCase(TestCase):
	def setUp(self):
		self.user = User.objects.create(username='ナルト')
		self.user.set_password('SomePass')
		self.user.save()
		self.post = PropertyClass.objects.create(
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


	def test_str(self):
		self.assertEquals(str(self.post), f"Random Title in minamiyukigaya")

	def test_absolute(self):
		url = self.post.get_absolute_url()
		self.assertEquals(url, '/all_properties')
