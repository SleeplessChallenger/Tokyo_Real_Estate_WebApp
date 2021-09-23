from django.test import TestCase
from prediction_price.forms import PricePredictionForm


class FormTestCase(TestCase):
	def test_form(self):
		form_data = {
			'time_to_station': 54,
			'building_year': 1965,
			'coverage_ratio': 20,
			'floor_ratio': 145,
			'property_type': 'house',
			'municipality': 'Tokyo',
			'district': 'Minato-ku',
			'nearest_station': 'Shinagawa',
			'structure': 'rc',
			'use': 'house',
			'city_planning': 'house', 
			'municipality_code': 424222,
			'price': 4425222,
			'age': 43
			}

		form = PricePredictionForm(data=form_data)
		self.assertTrue(form.is_valid())

		form = PricePredictionForm(data={})
		self.assertFalse(form.is_valid())
