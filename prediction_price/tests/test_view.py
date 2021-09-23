from django.test import TestCase
from general.models import PropertyClass
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from unittest.mock import patch
from prediction_price.forms import PricePredictionForm


class PricePredictionView(TestCase):
	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_superuser(username='コナン')
		self.user.set_password('PaperMaster')
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


	def test_price(self):
		url = reverse('price-prediction')
		response = self.client.get(url)
		self.assertEquals(response.status_code, 200)

		# with patch('prediction_price.forms.PricePredictionForm') as mock:
		# 	mock.return_value.is_valid = True
		# 	mock.return_value.cleaned_data = {}

		# 	response = self.client.post(url, mock)
		# 	self.assertEquals(response.status_code, 302)


		url = reverse('price-prediction', kwargs={'pk': 32})
		response = self.client.get(url)
		self.assertEquals(response.status_code, 200)


