from django.shortcuts import render
from django.contrib import messages
from .prediction_interface import RegressionInterface, DecisionTreeInterface, MainInterface
from .forms import PricePredictionForm
from django.shortcuts import render, redirect, get_object_or_404
from general.models import PropertyClass


model1 = RegressionInterface()
model2 = DecisionTreeInterface()
main_interface = MainInterface(model1, model2)
'''
1.Abstraction class for model1 and model2 ensures that 
required methods are realized, if not -> error.

2. Interface is written here as we can easily add/remove
new models (in `MainInterface` there is *args => can add
new objects easily)
'''


def calculate_price(request, pk=''):
	'''
	if url has additional param -> prefill form
	else don't prefill
	'''
	if request.method == 'POST':
		p_form = PricePredictionForm(request.POST)
		if p_form.is_valid():
			json_data = [p_form.cleaned_data]

			predicted_data = make_prediction(json_data)

			request.session['predicted_data'] = predicted_data
			return redirect('prediction-result')
	else:
		if pk:
			post = get_object_or_404(PropertyClass, pk=pk)
			p_form = PricePredictionForm(instance=post)

			context = {
				'p_form': p_form,
				'title': '価格の予測'
			}

			return render(request, 'prediction_price/price_prediction.html', context)

		else:
			p_form = PricePredictionForm()

			context = {
				'p_form': p_form,
				'title': '価格の予測'
			}

			return render(request, 'prediction_price/price_prediction.html', context)

def make_prediction(data):
	return main_interface(data)

def present_result(request):
	retrieved_data = request.session.get('predicted_data', None)
	price_one, price_two = retrieved_data
	if retrieved_data:
		context = {
			'price1': price_one,
			'price2': price_two,
			'title': '予測の結果'
		}

		messages.success(request, 'Price has been predicted successfully!')
		# request.session.flush()
		return render(request, 'prediction_price/prediction_result.html', context)

	messages.warning(request, f"No prediction is found. Try again")
	return redirect('price-prediction')
