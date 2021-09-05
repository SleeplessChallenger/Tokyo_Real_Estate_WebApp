import numpy as np


class Regression:
	def predict_result(self, dv, model, data):
		X_data = dv.transform(data)
		result = np.expm1(model.predict(X_data)[0])
		return result
