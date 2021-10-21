from sklearn.linear_models import Ridge
from sklearn.feature_extraction import DictVectorizer
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from pickle import load, dump
from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
import os
import zipfile
from pathlib import Path


class TrainInterface(ABC):
	@abstractmethod
	def train_model(self):
		raise NotImplementedError("You don't reaize the method")


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
		with zipfile.ZipFile(self.processed_file, 'r') as zip_f:
			with zip_f.open(self.csv_file, 'r') as file:
				return pd.read_csv(file, index_col='No')

	def prepare_data(self):
		df_train, df_test, y_tr, y_ts = self._split_df()
		df_train_dict, df_test_dict = self._convert_dict(df_train, df_test)

		X_train, X_test = self._convert_X(df_train_dict, df_test_dict)

		return X_train, X_test, y_tr, y_ts

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


class RidgeClass(TrainInterface, MainPreprocess):
	def __init__(self):
		self.model = Ridge()
		

	def __call__(self):
		pass


	def _serialize_model(self):
		with open('regression_model_2.bin', 'wb') as reg_model:
			dump((dv, model), reg_model)


class dtRegressorClass(TrainInterface, MainPreprocess):
	def __init__(self):
		self.model = DecisionTreeRegressor(max_depth=20, min_samples_leaf=20,
                            max_features=None, random_state=5)

	def _serialize_model(self):
		with open('dt_model_2', 'wb') as dt_model:
			dump((dv, model, dt_model))



if __name__ == '__main__':
	pass
	