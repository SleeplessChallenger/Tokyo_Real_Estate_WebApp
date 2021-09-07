from django.shortcuts import render
from django.contrib import messages
from .prediction_interface import RegressionInterface, DecisionTreeInterface
from .forms import PricePredictionForm
from django.shortcuts import render, redirect, get_object_or_404
from general.models import PropertyClass


first_model = RegressionInterface()
second_model = DecisionTreeInterface()


def calculate_price(request, pk=''):
	'''
	if url has additional param -> prefill form
	else don't prefill
	'''
	if request.method == 'POST':
		p_form = PricePredictionForm(request.POST)
		print(p_form)
		if p_form.is_valid():
			json_data = [p_form.cleaned_data]

			prediction_one = first_model.make_prediction(json_data)
			prediction_two = second_model.make_prediction(json_data)
			# print(prediction_one)
			# print(prediction_two)
			best_result = prediction_one if prediction_one > prediction_two\
				else prediction_two

			request.session['prediction'] = best_result
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

def present_result(request):
	retrieved_data = request.session.get('prediction', None)
	if retrieved_data:
		context = {
			'price': retrieved_data,
			'title': '予測の結果'
		}

		messages.success(request, 'Price has been predicted successfully!')
		# request.session.flush()
		return render(request, 'prediction_price/prediction_result.html', context)

	messages.warning(request, f"No prediction is found. Try again")
	return redirect('price-prediction')
