from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegistration(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']


class FlipAccess(forms.ModelForm):
	can_add_posts = forms.BooleanField(required=False, initial=False)


	class Meta:
		model = Profile
		fields = ['can_add_posts', 'country']


class UserChange(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email']


class ProfileChange(forms.ModelForm):

	class Meta:
		model = Profile
		fields = ['first_name', 'last_name', 'country', 'image']


class UserDelete(forms.ModelForm):
	class Meta:
		model = User
		fields = []
