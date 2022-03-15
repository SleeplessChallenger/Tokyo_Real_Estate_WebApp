import zipfile
import pandas as pd
import numpy as np
from datetime import datetime
from random import randint, choice


class DataInjection:
	'''
	I didn't make interface and specifically
	created class with tight coupling to
	action in views.py as dataset will be the same
	and columns are transformed in the same fashion.
	But I do allow to swap model if with another name, but with
	same features is pushed
	'''

	def __init__(self, curr_user, model):
		self.user = curr_user
		self.various_titles = ['Tokyo Harajuku apartment', 'Nagasaki coast house']
		self.model = model
		self.indicies = self._get_numbers()

		with zipfile.ZipFile('ML_models/real_estate_processed.csv.zip', 'r') as zip_file:
			with zip_file.open('real_estate_processed.csv', 'r') as file:
				self.df = pd.read_csv(file, index_col='No')

		self.mapped_columns = {
			'timetoneareststation': 'time_to_station',
			'buildingyear': 'building_year',
			'coverageratio': 'coverage_ratio',
			'floorarearatio': 'floor_ratio',

			'type': 'property_type',
			'municipality': 'municipality',
			'districtname': 'district',
			'neareststation': 'nearest_station',
			'structure': 'structure',
			'use': 'use',
			'cityplanning': 'city_planning',
			'municipalitycode': 'municipality_code',
			'age': 'age',

			'tradeprice': 'price'
		}

	@property
	def model(self):
		return self._model

	@model.setter
	def model(self, instance):
		self._model = instance

	def process_data(self):
		for idx in self.indicies:
			data = {}
			dict_data = self.df.iloc[idx, :].to_dict()
			for key, value in dict_data.items():
				if key == 'prefecture' or key == 'frontageisgreaterflag':
					continue
				
				correct_column = self.mapped_columns[key]
				'''
				transform from numpy type to python native
				'''
				if type(value) != str:
					value = value.item()

				data[correct_column] = value

			self.model.create(
				time_to_station=data['time_to_station'],
				building_year=data['building_year'],
				coverage_ratio=data['coverage_ratio'],
				floor_ratio=data['floor_ratio'],
				property_type=data['property_type'],
				municipality=data['municipality'],
				district=data['district'],
				nearest_station=data['nearest_station'],
				structure=data['structure'],
				use=data['use'],
				city_planning=data['city_planning'],
				municipality_code=data['municipality_code'],
				age=data['age'],
				price=data['price'],
				author=self.user,
				title=choice(self.various_titles)
			)

	def _get_numbers(self, lower=2, upper=400000, step=10000):
		all_numbers = []

		for i in range(lower, upper, step):
			number = randint(lower, upper)
			all_numbers.append(number)

		return all_numbers
