from django import forms
from general.models import PropertyClass


class PricePredictionForm(forms.ModelForm):
	class Meta:
		model = PropertyClass
		fields = ['time_to_station', 'building_year', 'coverage_ratio',
			'floor_ratio', 'property_type', 'municipality', 'district',
			'nearest_station', 'structure', 'use', 'city_planning', 
			'municipality_code', 'price', 'age']
