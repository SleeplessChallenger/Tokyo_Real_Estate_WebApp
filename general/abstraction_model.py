from abc import ABC, abstractmethod
import pickle
from .prediction_model import Regression


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
		with open('regression_model.bin', 'rb') as md:
			dv = pickle.load(md)[0]
		return dv

	def _get_model(self):
		with open('regression_model.bin', 'rb') as md:
			model = pickle.load(md)[1]
		return model

	def make_prediction(self, data):
		return self.regression.predict_result(self.dv, self.model, data)


class DecisionTreeInterface(AbstractModels):
	def __init__(self):
		self.dv = self._get_dv()
		self.model = self._get_model()
		self.regression = Regression()

	def _get_dv(self):
		with open('decision_tree_model.bin', 'rb') as md:
			dv = pickle.load(md)[0]
		return dv

	def _get_model(self):
		with open('decision_tree_model.bin', 'rb') as md:
			model = pickle.load(md)[1]
		return model
	
	def make_prediction(self, data):
		return self.regression.predict_result(self.dv, self.model, data)
