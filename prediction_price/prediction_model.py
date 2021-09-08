import numpy as np


class Regression:
	def predict_result(self, dv, model, data):
		X_data = dv.transform(data)
		price = model.predict(X_data)[0]
		result = np.expm1(price)
		return result
