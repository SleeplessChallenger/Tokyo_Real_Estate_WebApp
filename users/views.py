from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import (GiveRights, UserRegistration, UserChange,
	ProfileChange, UserDelete)
from .decorators import special_user, login_required_message
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def register(request):
	if request.method == 'POST':
		form = UserRegistration(request.POST)
		if form.is_valid():
			form.save()
			new_user = form.cleaned_data.get('username')
			messages.success(request, f"{new_user}のアカウントがされた！")
			return redirect('login')

	else:
		form = UserRegistration()

	context = {
		'form': form,
		'title': 'アカウントの作成'
	}

	return render(request, 'users/register.html', context)


'''
Customized login is required
to give messages
'''
@special_user
@login_required
def display_users(request):
	pass
	# User = get_user_model()
	# users = User.objects.filter(is_staff=False).filter(is_superuser=False).all()

	# if request.method == 'POST':
	# 	b_form = GiveRights(request.POST, instance=request.user.profile)
	# 	print(b_form)
	# 	if b_form.is_valid():
	# 		print(b_form.cleaned_data)
	# 		# the one who makes request isn't the user who we change the value of		
	# 		b_form.save()
			

	# 		return redirect('start-page')

	# else:
	# 	b_form = GiveRights(instance=request.user.profile)

	# context = {
	# 	'b_form': b_form,
	# 	'users': users,
	# 	'title': '全部のユーザー'
	# }

	# return render(request, 'users/all_users.html', context)


@login_required_message
@login_required
def tweak_profile(request):
	if request.method == 'POST':
		u_from = UserChange(request.POST, instance=request.user)
		p_form = ProfileChange(request.POST, request.FILES,
										instance=request.user.profile)

		if u_from.is_valid() and p_form.is_valid():
			u_from.save()
			p_form.save()
			messages.success(request, f"Info for {request.user} was updated!")
			return redirect('profile')

	else:
		u_from = UserChange(instance=request.user)
		p_form = ProfileChange(instance=request.user.profile)

	context = {
		'u_form': u_from,
		'p_form': p_form,
		'title': 'アカウントの変化'
	}

	return render(request, 'users/profile_page.html', context)


@login_required_message
@login_required
def delete_user(request):
	if request.method == 'POST':
		d_form = UserDelete(request.POST, instance=request.user)
		if d_form.is_valid():
			user = request.user
			user.delete()
			messages.success(request, f"{user.username}のアカウントが削減された！")
			return redirect('start-page')

	else:
		d_form = UserDelete(instance=request.user)

	context = {
		'd_form': d_form,
		'title': 'アカウントの削減'
	}

	return render(request, 'users/delete_account.html', context)
