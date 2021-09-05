from django.shortcuts import render, redirect, get_object_or_404
from .models import PropertyClass
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.views.generic import (CreateView, ListView,
	DetailView, DeleteView, UpdateView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from users import decorators as dec
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import ImageUpload, PricePredictionForm
from .abstraction_model import RegressionInterface, DecisionTreeInterface


first_model = RegressionInterface()
second_model = DecisionTreeInterface()

'''
create & update will redirect to 'all_info'
as I've specified it in the models.py
'''
def home(request):
	return render(request, 'general/start_page.html')


def calculate_price(request, pk=''):
	'''
	if url has additional param -> prefill form
	else don't prefill
	'''
	if request.method == 'POST':
		p_form = PricePredictionForm(request.POST)
		if p_form.is_valid():
			json_data = [p_form.cleaned_data]

			prediction_one = first_model.make_prediction(json_data)
			prediction_two = second_model.make_prediction(json_data)
			best_result = prediction_one if prediction_one > prediction_two\
				else prediction_two

			request.session['prediction'] = best_result
			return redirect('prediction-result')
	else:
		if pk:
			post = get_object_or_404(PropertyClass, pk=pk)
			p_form = PricePredictionForm(instance=post)

			context = {
				'p_form': p_form 
			}

			return render(request, 'general/price_prediction.html', context)

		else:
			p_form = PricePredictionForm()

			context = {
				'p_form': p_form 
			}

			return render(request, 'general/price_prediction.html', context)

def present_result(request):
	retrieved_data = request.session.get('prediction', None)
	if retrieved_data:
		context = {
			'price': retrieved_data
		}

		messages.success(request, 'Price has been predicted successfully!')
		request.session.flush()
		return render(request, 'general/prediction_result.html', context)

	messages.warning(request, f"No prediction is found. Try again")
	return redirect('price-prediction')


class PostCreateView(LoginRequiredMixin, CreateView):
	model = PropertyClass
	template_name = 'general/create_post.html'
	fields = ['title', 'time_to_station', 'building_year', 'coverage_ratio',
		'floor_ratio', 'property_type', 'municipality', 'district',
		'nearest_station', 'structure', 'use', 'city_planning', 
		'municipality_code', 'price', 'image']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)


class PostDetailView(DetailView):
	model = PropertyClass
	template_name = 'general/single_post.html'
	context_object_name = 'post'


class PostListView(ListView):
	model = PropertyClass
	template_name = 'general/all_properties.html'
	context_object_name = 'posts'
	ordering = ['-date_created']
	paginate_by = 4


class PostUserView(ListView):
	model = PropertyClass
	template_name = 'general/user_posts.html'
	context_object_name = 'posts'
	paginate_by = 4

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return PropertyClass.objects.filter(author=user).order_by('-date_created')


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = PropertyClass
	form_class = ImageUpload
	template_name = 'general/update_post.html'
	context_object_name = 'post'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = PropertyClass
	success_url = '/all_properties'
	template_name = 'general/delete_post.html'
	# to redirect after post is deleted

	def test_func(self):
		'''
		to prevent malicious delete
		'''
		post = self.get_object()
		if post.author == self.request.user:
			return True
		return False
