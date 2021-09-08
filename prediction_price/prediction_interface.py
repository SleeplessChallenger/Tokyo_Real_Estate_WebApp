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
	@abstractmethod
	def make_prediction(self, data):
		raise NotImplementedError("Method isn't realized")


class RegressionInterface(AbstractModels):
	def __init__(self):
		self.dv = self._get_dv()
		self.model = self._get_model()
		self.regression = Regression()

	def _get_dv(self):
		with open('ML_models/regression_model.bin', 'rb') as md:
			dv = pickle.load(md)[0]
		return dv

	def _get_model(self):
		with open('ML_models/regression_model.bin', 'rb') as md:
			model = pickle.load(md)[1]
		return model

	def make_prediction(self, data):
		print('models', data)
		return self.regression.predict_result(self.dv, self.model, data)


class DecisionTreeInterface(AbstractModels):
	def __init__(self):
		self.dv = self._get_dv()
		self.model = self._get_model()
		self.regression = Regression()

	def _get_dv(self):
		with open('ML_models/decision_tree_model.bin', 'rb') as md:
			dv = pickle.load(md)[0]
		return dv

	def _get_model(self):
		with open('ML_models/decision_tree_model.bin', 'rb') as md:
			model = pickle.load(md)[1]
		return model
	
	def make_prediction(self, data):
		print('models', data)
		return self.regression.predict_result(self.dv, self.model, data)
