from django.shortcuts import render, redirect, get_object_or_404, reverse
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
from .forms import ImageUpload
from django.contrib.messages.views import SuccessMessageMixin


'''
create & update will redirect to 'all_info'
as I've specified it in the models.py
'''
def home(request):
	return render(request, 'general/start_page.html')


class TitleMixin:
	'''
	this Mixin will enable title
	addition to other CBV
	'''
	title = '東京の不動産'

	def get_title(self):
		return self.title

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = self.get_title()
		return context


class PostCreateView(LoginRequiredMixin, TitleMixin, CreateView):
	model = PropertyClass
	template_name = 'general/create_post.html'
	fields = ['title', 'time_to_station', 'building_year', 'coverage_ratio',
		'floor_ratio', 'property_type', 'municipality', 'district',
		'nearest_station', 'structure', 'use', 'city_planning', 
		'municipality_code', 'price', 'age', 'image']

	title = '新たな物'

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)


class PostDetailView(TitleMixin, DetailView):
	model = PropertyClass
	template_name = 'general/single_post.html'
	context_object_name = 'post'
	title = 'ポストの情報'


class PostListView(TitleMixin, ListView):
	model = PropertyClass
	template_name = 'general/all_properties.html'
	context_object_name = 'posts'
	ordering = ['-date_created']
	paginate_by = 4
	title = '全部のポスト'


class PostUserView(TitleMixin, ListView):
	model = PropertyClass
	template_name = 'general/user_posts.html'
	context_object_name = 'posts'
	paginate_by = 4
	title = 'ユーザーの全部のポスト'

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return PropertyClass.objects.filter(author=user).order_by('-date_created')


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, TitleMixin, UpdateView):
	model = PropertyClass
	form_class = ImageUpload
	template_name = 'general/update_post.html'
	context_object_name = 'post'
	title = 'ポストの変化'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def get_success_message(self, cleaned_data):
		return 'Post was updated'


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, TitleMixin, DeleteView):
	model = PropertyClass
	# to redirect after post is deleted
	success_url = '/all_properties'
	template_name = 'general/delete_post.html'
	title = 'ポストの削減'


	def test_func(self):
		'''
		to prevent malicious delete
		'''
		post = self.get_object()
		if post.author == self.request.user:
			return True
		return False


class PostDeleteAll(LoginRequiredMixin, SuccessMessageMixin, TitleMixin, ListView):
	'''
	if not the owner of the post or
	superuser/staff => won't allow to delete
	'''
	model = PropertyClass
	template_name = 'general/delete_all_posts.html'
	title = '全部のポストの削減'
	context_object_name = 'posts'
	paginate_by = 8
	success_url = '/all_properties'


	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return PropertyClass.objects.filter(author=user).order_by('-date_created')

	def post(self, request, *args, **kwargs):
		if 'checkedbox' not in dict(request.POST):
			messages.warning(request, "You didn't tick anything")
			return redirect(reverse('start-page'))

		data = dict(request.POST)['checkedbox']
		result = list(map(int, data))
		for i in result:
			post = self.model.objects.get(pk=i)
			if post.author != request.user or not request.user.is_staff or not request.user.is_superuser:
				messages.warning(request, '''You cannot delete other posts unless
you are superuser/staff''')
				return redirect('/profile-info')
			else:
				post.delete()

		messages.success(request, f"{', '.join([str(x) for x in result])} removed")
		return redirect(self.success_url)
