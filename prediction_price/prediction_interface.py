from abc import ABC, abstractmethod
import pickle
from .prediction_model import Regression


class MainInterface:
	'''
	move `result = []` away from init
	as otherwise values will be stored
	there
	'''
	def __init__(self, *args):
		self.args = args

	def __call__(self, data):
		result = []
		for arg in self.args:
			result.append(arg.make_prediction(data))

		return result


class AbstractModels(ABC):
	'''
	As these two interfaces (below) have concern 
	regarding particular model, they can
	also tweak data as it lies within their
	scope
	'''
	@abstractmethod
	def make_prediction(self, data):
		raise NotImplementedError("Method isn't realized")

	@abstractmethod
	def _change_json(self, json_data):
		raise NotImplementedError("Method isn't realized")


class RegressionInterface(AbstractModels):
	def __init__(self):
		self.dv = self._get_dv()
		self.model = self._get_model()
		self.regression = Regression()
		self.columns = {
			'time_to_station': 'timetoneareststation',
			'building_year': 'buildingyear',
			'coverage_ratio': 'coverageratio',
			'floor_ratio': 'floorarearatio',
			'property_type': 'type',
			'municipality': 'municipality',
			'district': 'districtname',
			'nearest_station': 'neareststation',
			'structure': 'structure',
			'use': 'use',
			'city_planning': 'cityplanning',
			'municipality_code': 'municipalitycode',
			'age': 'age',
			'price': 'tradeprice'
		}

	def _get_dv(self):
		with open('ML_models/regression_model.bin', 'rb') as md:
			dv = pickle.load(md)[0]
		return dv

	def _get_model(self):
		with open('ML_models/regression_model.bin', 'rb') as md:
			model = pickle.load(md)[1]
		return model

	def make_prediction(self, data):
		final_data = self._change_json(data)
		return self.regression.predict_result(self.dv, self.model, final_data)

	def _change_json(self, json_data):
		final_data = {}
		for key, value in json_data[0].items():
			correct_column = self.columns[key]
			final_data[correct_column] = value

		return [final_data]


class DecisionTreeInterface(AbstractModels):
	def __init__(self):
		self.dv = self._get_dv()
		self.model = self._get_model()
		self.regression = Regression()
		self.columns = {
			'time_to_station': 'timetoneareststation',
			'building_year': 'buildingyear',
			'coverage_ratio': 'coverageratio',
			'floor_ratio': 'floorarearatio',
			'property_type': 'type',
			'municipality': 'municipality',
			'district': 'districtname',
			'nearest_station': 'neareststation',
			'structure': 'structure',
			'use': 'use',
			'city_planning': 'cityplanning',
			'municipality_code': 'municipalitycode',
			'age': 'age',
			'price': 'tradeprice'
		}

	def _get_dv(self):
		with open('ML_models/decision_tree_model.bin', 'rb') as md:
			dv = pickle.load(md)[0]
		return dv

	def _get_model(self):
		with open('ML_models/decision_tree_model.bin', 'rb') as md:
			model = pickle.load(md)[1]
		return model
	
	def make_prediction(self, data):
		final_data = self._change_json(data)
		return self.regression.predict_result(self.dv, self.model, final_data)

	def _change_json(self, json_data):
		final_data = {}
		for key, value in json_data[0].items():
			correct_column = self.columns[key]
			final_data[correct_column] = value

		return [final_data]
