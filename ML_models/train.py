from sklearn.linear_model import Ridge
from sklearn.feature_extraction import DictVectorizer
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from pickle import load, dump
from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
import zipfile
from concurrent.futures.process import ProcessPoolExecutor as PoolExecutor
import multiprocessing


class TrainInterface(ABC):
	@abstractmethod
	def train_model(self):
		raise NotImplementedError("You don't reaize the method")


class MainInterface:
	def __init__(self, *args):
		self.models = args

	def train_models(self):
		results = []

		processor_count = multiprocessing.cpu_count()

		with PoolExecutor(max_workers=processor_count) as executor:

			for model in self.models:
				future = executor.submit(model.train_model)

				results.append(future)

		return results


class MainPreprocess:
	def __init__(self):
		self.zip_file = 'real_estate_processed.csv.zip'
		self.csv_file = 'real_estate_processed.csv'
		self.df = self._read_processed()
		self.dv = DictVectorizer(sparse=False)
		self.features = ['timetoneareststation', 'buildingyear', 'coverageratio',
			'floorarearatio', 'type', 'municipality', 'districtname', 'neareststation',
			'structure', 'use', 'cityplanning', 'municipalitycode']


	def _read_processed(self):
		with zipfile.ZipFile(self.zip_file, 'r') as zip_f:
			with zip_f.open(self.csv_file, 'r') as file:
				return pd.read_csv(file, index_col='No')

	def prepare_data(self):
		df_train, df_test, y_tr, y_ts = self._split_df()
		df_train_dict, df_test_dict = self._convert_dict(df_train, df_test)

		X_train, X_test = self._convert_X(df_train_dict, df_test_dict)

		return X_train, X_test, y_tr, y_ts, self.dv

	def _split_df(self):
		train, test = train_test_split(self.df, test_size=0.2, random_state=1)
		y_train = np.log1p(train.tradeprice.values)
		y_test = np.log1p(test.tradeprice.values)

		del train['tradeprice']
		del test['tradeprice']

		return train, test, y_train, y_test

	def _convert_dict(self, df1, df2):
		dict1 = df1[self.features].to_dict(orient='records')
		dict2 = df2[self.features].to_dict(orient='records')

		return dict1, dict2

	def _convert_X(self, df1, df2):
		X_train = self.dv.fit_transform(df1)
		X_valid = self.dv.transform(df2)
		return X_train, X_valid

	def _rmse(self, y_real, y_predict):
		error = y_predict - y_real
		mse = (error ** 2).mean()
		return np.sqrt(mse)


class RidgeClass(TrainInterface, MainPreprocess):
	def __init__(self):
		self.model_name = 'Ridge regression'
		self.model = Ridge()
		self.process = MainPreprocess()

	def __repr__(self):
		return f"Model: {self.model}"

	def train_model(self):
		X_train, X_test, y_tr, y_ts, dv = self.process.prepare_data()

		self.model.fit(X_train, y_tr)
		y_pred = self.model.predict(X_test)

		rmse = super()._rmse(y_ts, y_pred)

		self._serialize_model(dv)

		return f"{self.__repr__()}; rmse: {rmse}"

		
	def _serialize_model(self, dv):
		with open('regression_model_2.bin', 'wb') as reg_model:
			dump((dv, self.model), reg_model)


class dtRegressorClass(TrainInterface, MainPreprocess):
	def __init__(self):
		self.model_name = 'DecisionTree Regressor'
		self.model = DecisionTreeRegressor(max_depth=20, min_samples_leaf=20,
                            max_features=None, random_state=5)
		self.process = MainPreprocess()

	def __repr__(self):
		return f"Model: {self.model_name}"

	def train_model(self):
		X_train, X_test, y_tr, y_ts, dv = self.process.prepare_data()

		self.model.fit(X_train, y_tr)
		y_pred = self.model.predict(X_test)

		rmse = super()._rmse(y_ts, y_pred)

		self._serialize_model(dv)

		return f"{self.__repr__()}; rmse: {rmse}"

	def _serialize_model(self, dv):
		with open('dt_model_2.bin', 'wb') as dt_model:
			dump((dv, self.model), dt_model)


if __name__ == '__main__':
	# list all the models to be trained
	model1 = RidgeClass()
	model2 = dtRegressorClass()
	models = MainInterface(model1, model2)

	results = models.train_models()
	for r in results:
		print(r.result(), flush=True)
	